from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .logger import logger
import numpy as np
import os

from six.moves import range
from .proto.summary_pb2 import Summary
from .proto.summary_pb2 import HistogramProto
from .proto.summary_pb2 import SummaryMetadata
from .proto.tensor_pb2 import TensorProto
from .proto.tensor_shape_pb2 import TensorShapeProto
from .proto.plugin_pr_curve_pb2 import PrCurvePluginData
from .proto.plugin_text_pb2 import TextPluginData
from .proto.plugin_mesh_pb2 import MeshPluginData
from .proto import layout_pb2
from .x2num import make_np
from .utils import _prepare_video, convert_to_HWC


def _draw_single_box(image, xmin, ymin, xmax, ymax, display_str, color='black', color_text='black', thickness=2):
    from PIL import ImageDraw, ImageFont
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    (left, right, top, bottom) = (xmin, xmax, ymin, ymax)

    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)

    if display_str:
        text_bottom = bottom
        # Reverse list and print from bottom to top.
        text_width, text_height = font.getsize(display_str)

        draw.rectangle([(left, text_bottom), (left + text_width, text_bottom + text_height + 2)], fill=color)
        draw.text((left + 1, text_bottom + 1), display_str, fill=color_text, font=font)
    
    return image


def scalar(name, scalar_var, collections=None):
    """Outputs a `Summary` protocol buffer containing a single scalar value.
    The generated Summary has a Tensor.proto containing the input Tensor.

    :param name: A name for the generated node.
    :type name: string
    :param scalar_var: A single value.
    :type scalar_var: float
    :param collections: (Optional) list of graph collections keys. The new summary op
                        is added to these collections. Defaults to `[GraphKeys.SUMMARIES]`.

    :returns: A scalar `Tensor` of type `string`. Which contains a `Summary` protobuf.
    :raises: ValueError: If tensor has the wrong shape or type.
    """
    scalar_var = make_np(scalar_var)
    assert(scalar_var.squeeze().ndim == 0), 'scalar should be 0D'
    scalar_var = float(scalar_var)
    return Summary(value=[Summary.Value(tag=name, simple_value=scalar_var)])


def histogram_raw(name,
                  min,
                  max,
                  num,
                  sum,
                  sum_squares,
                  bucket_limits,
                  bucket_counts):
    """Outputs a `Summary` protocol buffer with a histogram.

    :param name: A name for the generated node.
    :param min: min value.
    :type min: float or int
    :param max: max value.
    :type max: float or int
    :param num: number of values.
    :type num: int
    :param sum: sum of all values.
    :type sum: float or int
    :param sum_squares: sum of squares for all values.
    :type sum_squares: float or int
    :param bucket_limits: A numeric `Tensor` with upper value per bucket.
    :param bucket_counts: A numeric `Tensor` with number of values per bucket.

    :return: A scalar `Tensor` of type `string`. The serialized `Summary` protocol buffer.
    """
    hist = HistogramProto(min=min,
                          max=max,
                          num=num,
                          sum=sum,
                          sum_squares=sum_squares,
                          bucket_limit=bucket_limits,
                          bucket=bucket_counts)
    return Summary(value=[Summary.Value(tag=name, histo=hist)])


def histogram(name, values, bins, max_bins=None):
    """Outputs a `Summary` protocol buffer with a histogram.

    :param name: A name for the generated node. Will also serve as a series name in TensorBoard.
    :type name: string
    :param values: Values to build the histogram.
    :type values: numpy.array
    :param bins: One of {'tensorflow','auto', 'fd', ...}.
                     This determines how the bins are made. You can find other options in:
                     https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html
    :type bins: string
    :return: A scalar `Tensor` of type `string`. The serialized `Summary` protocol buffer.
    """
    values = make_np(values)
    hist = make_histogram(values.astype(float), bins, max_bins)
    return Summary(value=[Summary.Value(tag=name, histo=hist)])


def make_histogram(values, bins, max_bins=None):
    """Convert values into a histogram proto using logic from histogram.cc."""
    if values.size == 0:
        raise ValueError('The input has no element.')

    values = values.reshape(-1)
    counts, limits = np.histogram(values, bins=bins)
    num_bins = len(counts)

    if max_bins is not None and num_bins > max_bins:
        sub_sampling = num_bins // max_bins
        sub_sampling_remainder = num_bins % sub_sampling
        if sub_sampling_remainder != 0:
            counts = np.pad(counts, pad_width=[[0, sub_sampling - sub_sampling_remainder]],
                            mode="constant", constant_values=0)
        counts = counts.reshape(-1, sub_sampling).sum(axis=-1)
        new_limits = np.empty((counts.size + 1,), limits.dtype)
        new_limits[:-1] = limits[:-1:sub_sampling]
        new_limits[-1] = limits[-1]
        limits = new_limits

    # Find the first and the last bin defining the support of the histogram:
    cum_counts = np.cumsum(np.greater(counts, 0, dtype=np.int32))
    start, end = np.searchsorted(cum_counts, [0, cum_counts[-1] - 1], side="right")
    start = int(start)
    end = int(end) + 1
    del cum_counts

    # TensorBoard only includes the right bin limits.
    # To still have the leftmost limit included,
    # we include an empty bin left.
    # If start == 0, we need to add an empty one left,
    # otherwise we can just include the bin left to the first nonzero-count bin:
    counts = counts[start - 1:end] if start > 0 else np.concatenate([[0], counts[:end]])
    limits = limits[start:end + 1]

    if counts.size == 0 or limits.size == 0:
        raise ValueError('The histogram is empty, please file a bug report.')

    sum_sq = values.dot(values)
    return HistogramProto(min=values.min(),
                          max=values.max(),
                          num=len(values),
                          sum=values.sum(),
                          sum_squares=sum_sq,
                          bucket_limit=limits.tolist(),
                          bucket=counts.tolist())


def image(tag, tensor, rescale=1, dataformats='CHW'):
    """Outputs a `Summary` protocol buffer with images.
    The summary has up to `max_images` summary values containing images.
    The data shape of input must be `[height, width,channels]`,
    where `channels` can be:
        *  1: `tensor` is interpreted as Grayscale.
        *  3: `tensor` is interpreted as RGB.
        *  4: `tensor` is interpreted as RGBA.

    :param tag: A name for the generated node.
    :param tensor: image data with shape [height, width,channels].
                   'tensor' can either have values in:
                       * [0, 1]   (float32)
                       * [0, 255] (uint8)
    :type tensor: numpy.array,


    :returns: A scalar `Tensor` of type `string`. The serialized `Summary` protocol buffer.
    """
    tensor = make_np(tensor)
    tensor = convert_to_HWC(tensor, dataformats)

    if tensor.dtype != np.uint8:
        tensor = (tensor * 255.0).astype(np.uint8)

    image = make_image(tensor, rescale=rescale)
    return Summary(value=[Summary.Value(tag=tag, image=image)])


def image_boxes(tag, tensor_image, tensor_boxes, rescale=1, dataformats='CHW', 
                labels=None, box_color='red', text_color='black', box_thickness=1):
    """Outputs a `Summary` protocol buffer with images."""
    tensor_image = make_np(tensor_image)
    tensor_image = convert_to_HWC(tensor_image, dataformats)
    tensor_boxes = make_np(tensor_boxes)

    if tensor_image.dtype != np.uint8:
        tensor_image = (tensor_image * 255.0).astype(np.uint8)

    image = make_image(tensor_image, rescale=rescale, rois=tensor_boxes, labels=labels,
                       box_color=box_color, text_color=text_color, box_thickness=box_thickness)
    return Summary(value=[Summary.Value(tag=tag, image=image)])


def draw_boxes(display_image, boxes, labels=None, box_color='red', text_color='black', box_thickness=1):
    num_boxes = boxes.shape[0]
    list_gt = range(num_boxes)
    for i in list_gt:
        display_image = _draw_single_box(display_image,
                                         boxes[i, 0], boxes[i, 1], boxes[i, 2], boxes[i, 3],
                                         display_str=None if labels is None else labels[i],
                                         color=box_color, color_text=text_color, thickness=box_thickness)
    return display_image


def make_image(tensor, rescale=1, rois=None, labels=None, 
                box_color='red', text_color='black', box_thickness=1):
    """Convert an numpy representation image to Image protobuf"""
    from PIL import Image
    height, width, channel = tensor.shape
    scaled_height = int(height * rescale)
    scaled_width = int(width * rescale)
    image = Image.fromarray(tensor)

    if rois is not None:
        image = draw_boxes(image, rois, labels=labels, 
                           box_color=box_color, text_color=text_color, box_thickness=box_thickness)

    image = image.resize((scaled_width, scaled_height), Image.ANTIALIAS)

    import io
    output = io.BytesIO()
    image.save(output, format='PNG')
    image_string = output.getvalue()
    output.close()
    return Summary.Image(height=height,
                         width=width,
                         colorspace=channel,
                         encoded_image_string=image_string)


def video(tag, tensor, fps=4):
    tensor = make_np(tensor)
    tensor = _prepare_video(tensor)

    if tensor.dtype != np.uint8:
        tensor = (tensor * 255.0).astype(np.uint8)

    video = make_video(tensor, fps)
    return Summary(value=[Summary.Value(tag=tag, image=video)])


def make_video(tensor, fps):
    try:
        import moviepy
    except ImportError:
        print('add_video needs package moviepy')
        return
    try:
        from moviepy import editor as mpy
    except ImportError:
        print("moviepy is installed, but can't import moviepy.editor.",
              "Some packages could be missing [imageio, requests]")
        return
    import tempfile

    t, h, w, c = tensor.shape

    # encode sequence of images into gif string
    clip = mpy.ImageSequenceClip(list(tensor), fps=fps)

    filename = tempfile.NamedTemporaryFile(suffix='.gif', delete=False).name
    try:  # older version of moviepy does not support progress_bar argument.
        clip.write_gif(filename, verbose=False, progress_bar=False)
    except TypeError:
        clip.write_gif(filename, verbose=False)

    with open(filename, 'rb') as f:
        tensor_string = f.read()

    try:
        os.remove(filename)
    except OSError:
        logger.error('The temporary file used by moviepy cannot be deleted.')

    return Summary.Image(height=h, width=w, colorspace=c, encoded_image_string=tensor_string)


def audio(tag, tensor, sample_rate=44100):
    tensor = make_np(tensor)
    tensor = tensor.squeeze()
    if abs(tensor).max() > 1:
        print('warning: audio amplitude out of range, auto clipped.')
        tensor = tensor.clip(-1, 1)
    assert(tensor.ndim == 1), 'input tensor should be 1 dimensional.'

    tensor_list = [int(32767.0 * x) for x in tensor]
    import io
    import wave
    import struct
    fio = io.BytesIO()
    Wave_write = wave.open(fio, 'wb')
    Wave_write.setnchannels(1)
    Wave_write.setsampwidth(2)
    Wave_write.setframerate(sample_rate)
    tensor_enc = b''
    tensor_enc += struct.pack("<" + "h" * len(tensor_list), *tensor_list)

    Wave_write.writeframes(tensor_enc)
    Wave_write.close()
    audio_string = fio.getvalue()
    fio.close()
    audio = Summary.Audio(sample_rate=sample_rate,
                          num_channels=1,
                          length_frames=len(tensor_list),
                          encoded_audio_string=audio_string,
                          content_type='audio/wav')
    return Summary(value=[Summary.Value(tag=tag, audio=audio)])


def custom_scalars(layout):
    categories = []
    for k, v in layout.items():
        charts = []
        for chart_name, chart_meatadata in v.items():
            tags = chart_meatadata[1]
            if chart_meatadata[0] == 'Margin':
                assert len(tags) == 3

                mgcc = layout_pb2.MarginChartContent(series=[
                    layout_pb2.MarginChartContent.Series(value=tags[0],
                                                         lower=tags[1],
                                                         upper=tags[2])])

                chart = layout_pb2.Chart(title=chart_name, margin=mgcc)
            else:
                mlcc = layout_pb2.MultilineChartContent(tag=tags)
                chart = layout_pb2.Chart(title=chart_name, multiline=mlcc)
            charts.append(chart)
        categories.append(layout_pb2.Category(title=k, chart=charts))

    layout = layout_pb2.Layout(category=categories)
    PluginData = SummaryMetadata.PluginData(plugin_name='custom_scalars')
    smd = SummaryMetadata(plugin_data=PluginData)

    tensor = TensorProto(dtype='DT_STRING',
                         string_val=[layout.SerializeToString()],
                         tensor_shape=TensorShapeProto())

    return Summary(value=[Summary.Value(tag='custom_scalars__config__', tensor=tensor, metadata=smd)])


def text(tag, text_data):
    PluginData = SummaryMetadata.PluginData(
        plugin_name='text', content=TextPluginData(version=0).SerializeToString())

    smd = SummaryMetadata(plugin_data=PluginData)

    tensor = TensorProto(dtype='DT_STRING',
                         string_val=[text_data.encode(encoding='utf_8')],
                         tensor_shape=TensorShapeProto(dim=[TensorShapeProto.Dim(size=1)]))

    return Summary(value=[Summary.Value(tag=tag, metadata=smd, tensor=tensor)])


def pr_curve_raw(tag, tp, fp, tn, fn, precision, recall, num_thresholds=127, weights=None):
    if num_thresholds > 127:  # weird, value > 127 breaks protobuf
        num_thresholds = 127
    data = np.stack((tp, fp, tn, fn, precision, recall))
    pr_curve_plugin_data = PrCurvePluginData(
        version=0, num_thresholds=num_thresholds).SerializeToString()
    PluginData = SummaryMetadata.PluginData(plugin_name='pr_curves', content=pr_curve_plugin_data)
    smd = SummaryMetadata(plugin_data=PluginData)
    tensor = TensorProto(dtype='DT_FLOAT',
                         float_val=data.reshape(-1).tolist(),
                         tensor_shape=TensorShapeProto(dim=[
                             TensorShapeProto.Dim(size=data.shape[0]),
                             TensorShapeProto.Dim(size=data.shape[1])]))
    return Summary(value=[Summary.Value(tag=tag, metadata=smd, tensor=tensor)])


def pr_curve(tag, labels, predictions, num_thresholds=127, weights=None):
    num_thresholds = min(num_thresholds, 127)

    data = compute_curve(labels, predictions,
                         num_thresholds=num_thresholds, weights=weights)

    pr_curve_plugin_data = PrCurvePluginData(
        version=0, num_thresholds=num_thresholds).SerializeToString()

    PluginData = SummaryMetadata.PluginData(
        plugin_name='pr_curves', content=pr_curve_plugin_data)

    smd = SummaryMetadata(plugin_data=PluginData)

    tensor = TensorProto(dtype='DT_FLOAT',
                         float_val=data.reshape(-1).tolist(),
                         tensor_shape=TensorShapeProto(
                             dim=[TensorShapeProto.Dim(
                                 size=data.shape[0]),
                                 TensorShapeProto.Dim(size=data.shape[1])]))

    return Summary(value=[Summary.Value(tag=tag, metadata=smd, tensor=tensor)])


def compute_curve(labels, predictions, num_thresholds=None, weights=None):
    _MINIMUM_COUNT = 1e-7

    if weights is None:
        weights = 1.0

    # Compute bins of true positives and false positives.
    bucket_indices = np.int32(np.floor(predictions * (num_thresholds - 1)))
    float_labels = labels.astype(np.float)
    histogram_range = (0, num_thresholds - 1)

    tp_buckets, _ = np.histogram(
        bucket_indices,
        bins=num_thresholds,
        range=histogram_range,
        weights=float_labels * weights)

    fp_buckets, _ = np.histogram(
        bucket_indices,
        bins=num_thresholds,
        range=histogram_range,
        weights=(1.0 - float_labels) * weights)

    # Obtain the reverse cumulative sum.
    tp = np.cumsum(tp_buckets[::-1])[::-1]
    fp = np.cumsum(fp_buckets[::-1])[::-1]
    tn = fp[0] - fp
    fn = tp[0] - tp
    precision = tp / np.maximum(_MINIMUM_COUNT, tp + fp)
    recall = tp / np.maximum(_MINIMUM_COUNT, tp + fn)
    return np.stack((tp, fp, tn, fn, precision, recall))


def _get_tensor_summary(tag, tensor, content_type, json_config):
    mesh_plugin_data = MeshPluginData(
        version=0,
        name=tag,
        content_type=content_type,
        json_config=json_config,
        shape=tensor.shape)

    content = mesh_plugin_data.SerializeToString()
    smd = SummaryMetadata(
        plugin_data=SummaryMetadata.PluginData(plugin_name='mesh',
                                               content=content))

    tensor = TensorProto(dtype='DT_FLOAT',
                         float_val=tensor.reshape(-1).tolist(),
                         tensor_shape=TensorShapeProto(dim=[
                             TensorShapeProto.Dim(size=tensor.shape[0]),
                             TensorShapeProto.Dim(size=tensor.shape[1]),
                             TensorShapeProto.Dim(size=tensor.shape[2])]))

    tensor_summary = Summary.Value(tag='{}_{}'.format(tag, content_type),
                                   tensor=tensor,
                                   metadata=smd)
    return tensor_summary


def mesh(tag, vertices, colors, faces, config_dict=None):

    import json
    summaries = []
    tensors = [(vertices, 1),
               (faces, 2),
               (colors, 3)]

    for tensor, content_type in tensors:
        if tensor is None:
            continue
        summaries.append(_get_tensor_summary(tag,
                                             make_np(tensor),
                                             content_type,
                                             json.dumps(config_dict, sort_keys=True)))

    return Summary(value=summaries)
