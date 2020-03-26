# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Writes events to disk in a logdir."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import socket
import threading
import time

import six

from .proto import event_pb2
from .record_writer import RecordWriter, directory_check


class EventsWriter(object):
    """Writes `Event` protocol buffers to an event file."""

    def __init__(self, file_prefix, filename_suffix=''):
        """
        Events files have a name of the form:
            '/some/file/path/events.out.tfevents.[timestamp].[hostname]'
        """
        self._file_name = file_prefix + ".out.tfevents." + str(time.time())[:10] + "." +\
            socket.gethostname() + filename_suffix
        self._num_outstanding_events = 0
        self._py_recordio_writer = RecordWriter(self._file_name)
        self._event = event_pb2.Event()  # Initialize an event instance.
        self._event.wall_time = time.time()
        self._event.file_version = 'brain.Event:2'
        self._lock = threading.Lock()
        self.write_event(self._event)

    def write_event(self, event):
        """Append "event" to the file."""

        # Check if event is of type event_pb2.Event proto.
        if not isinstance(event, event_pb2.Event):
            raise TypeError("Expected an event_pb2.Event proto, but got %s" % type(event))
        return self._write_serialized_event(event.SerializeToString())

    def _write_serialized_event(self, event_str):
        with self._lock:
            self._num_outstanding_events += 1
            self._py_recordio_writer.write(event_str)

    def flush(self):
        """Flushes the event file to disk."""
        with self._lock:
            self._num_outstanding_events = 0
            self._py_recordio_writer.flush()
        return True

    def close(self):
        """Call self.flush()."""
        return_value = self.flush()
        with self._lock:
            self._py_recordio_writer.close()
        return return_value


class EventFileWriter(object):
    """Writes `Event` protocol buffers to an event file.

    The `EventFileWriter` class creates an event file in the specified directory,
    and asynchronously writes Event protocol buffers to the file. The Event file
    is encoded using the tfrecord format, which is similar to RecordIO.
    """

    def __init__(self, logdir, max_queue_size=1024, filename_suffix=''):
        """Creates a `EventFileWriter` and an event file to write to.

        On construction the summary writer creates a new event file in `logdir`.
        This event file will contain `Event` protocol buffers, which are written to
        disk via the add_event method.
        The other arguments to the constructor control the asynchronous writes to
        the event file:

        :param logdir: Directory where event file will be written.
        :type logdir: string
        :param max_queue_size: Size of the queue for pending events and summaries.
        :type max_queue_size: int
        """
        self._logdir = str(logdir)
        directory_check(self._logdir)
        self._event_queue = six.moves.queue.Queue(max_queue_size)
        self._ev_writer = EventsWriter(os.path.join(self._logdir, "events"), filename_suffix)
        self._sentinel_event = self._get_sentinel_event()
        self._closed = False
        self._worker = _EventLoggerThread(self._event_queue, self._ev_writer, self._sentinel_event)
        self._worker.start()

    def _get_sentinel_event(self):
        """Generate a sentinel event for terminating worker."""
        return event_pb2.Event()

    def get_logdir(self):
        """Returns the directory where event file will be written."""
        return self._logdir

    def reopen(self):
        """Reopens the EventFileWriter.
        Can be called after `close()` to add more events in the same directory.
        The events will go into a new events file and a new write/flush worker is created.
        Does nothing if the EventFileWriter was not closed.
        """
        if self._closed:
            self._worker = _EventLoggerThread(self._event_queue, self._ev_writer, self._sentinel_event)
            self._worker.start()
            self._closed = False

    def add_event(self, event):
        """Adds an event to the event file.

        :param event: An `Event` protocol buffer.
        """
        if not self._closed:
            self._event_queue.put(event)

    def flush(self):
        """Flushes the event file to disk.

        Call this method to make sure that all pending events have been written to disk.
        """
        if not self._closed:
            self._event_queue.join()
            self._ev_writer.flush()

    def close(self):
        """Flushes the event file to disk and close the file.

        Call this method when you do not need the summary writer anymore.
        """
        self.add_event(self._sentinel_event)
        self.flush()
        self._worker.join()
        self._ev_writer.close()
        self._closed = True


class _EventLoggerThread(threading.Thread):
    """Thread that logs events."""
    
    def __init__(self, queue, ev_writer, sentinel_event):
        """Creates an _EventLoggerThread.

        :param queue: A Queue from which to dequeue data.
        :param ev_writer: Used to log brain events for the visualizer.
        :type ev_writer: An instance of class EventWriter
        :param sentinel_event: Sentinel, Used to judge whether run or not.
        :type sentinel_event: An instance of class EventWriter.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self._queue = queue
        self._ev_writer = ev_writer
        self._sentinel_event = sentinel_event

    def run(self):
        while True:
            event = self._queue.get()
            if event is self._sentinel_event:
                self._queue.task_done()
                break
            try:
                self._ev_writer.write_event(event)
            finally:
                self._queue.task_done()
