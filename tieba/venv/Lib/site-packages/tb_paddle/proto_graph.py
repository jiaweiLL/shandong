# coding=utf-8
from .proto.node_def_pb2 import NodeDef
from .proto.attr_value_pb2 import AttrValue
from .proto.tensor_shape_pb2 import TensorShapeProto


def attr_value_proto(value):
    """ return AttrValue proto according to the value of op attributes.
    
    :param value: The attribute value of the op.
    :return: AttrValue proto
    """
    value_type = str(type(value))
    op_attr_str = str(value)
    value_attr = AttrValue(s=op_attr_str.encode(encoding='utf_8'))

    if value_type == "<class 'int'>" or value_type == "<type 'int'>":
        value_attr = AttrValue(i=value)
    elif value_type == "<class 'float'>" or value_type == "<type 'float'>":
        value_attr = AttrValue(f=value)
    elif value_type == "<class 'bool'>" or value_type == "<type 'bool'>":
        value_attr = AttrValue(b=value)
    elif value_type == "<class 'list'>" or value_type == "<type 'list'>":
        if len(value) > 0:
            value_list_dtype = str(type(value[0]))
            if value_list_dtype == "<class 'int'>" or value_list_dtype == "<type 'int'>":
                value_attr = AttrValue(list=AttrValue.ListValue(i=value))
            elif value_list_dtype == "<class 'float'>" or value_list_dtype == "<type 'float'>":
                value_attr = AttrValue(list=AttrValue.ListValue(f=value))
            elif value_list_dtype == "<class 'bool'>" or value_list_dtype == "<type 'bool'>":
                value_attr = AttrValue(list=AttrValue.ListValue(b=value))

    return value_attr


def tensor_shape_proto(output_size):
    """
    The shape of this tensor.
    """
    return TensorShapeProto(dim=[TensorShapeProto.Dim(size=d) for d in output_size])


def node_proto(name,
               op='UnSpecified',
               input_args=None,
               attributes={}
               ):
    """

    :param name: The name of this node.
    :type name: string
    :param op: The name of Operator.
    :type op: string
    :param input_args: The input arguments of this node.
    :type input_args: list of string.
    :param attributes: The attributes of this node.
    :type attributes: dict, each value is AttrValue protobuf.
    :return: NodeDef proto
    """
    if input_args is None:
        input_args = []
    if not isinstance(input_args, list):
        input_args = [input_args]
    return NodeDef(name=name.encode(encoding='utf_8'),
                   op=op,
                   input=input_args,
                   attr=attributes)
