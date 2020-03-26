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
"""Functionality for loading events from a record file."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect

from .record_reader import RecordReader
from .proto import event_pb2


class raise_exception_on_not_ok_status(object):
    """Context manager to check for C API status."""

    def __enter__(self):
        return "Status not OK"

    def __exit__(self, type_arg, value_arg, traceback_arg):
        return False  # False values do not suppress exceptions


class RawEventFileLoader(object):
    """An iterator that yields Event protos as serialized bytestrings."""
    def __init__(self, file_path):
        if file_path is None:
            raise ValueError('A file path is required')
           
        with raise_exception_on_not_ok_status() as status:
            self._reader = RecordReader(str(file_path), 0, None, status)
          
        self._file_path = file_path
        if not self._reader:
            raise IOError('Failed to open a record reader pointing to %s' % file_path)

    def Load(self):
        """Loads all new events from disk as raw serialized proto bytestrings.
         
        Calling Load multiple times in a row will not 'drop' events as long as the
        return value is not iterated over.
          
        Yields: All event proto bytestrings in the file that have not been yielded yet.
        """
        get_next_args = inspect.getargspec(self._reader.GetNext).args
        legacy_get_next = (len(get_next_args) > 1)
         
        while True:
            try:
                if legacy_get_next:
                    with raise_exception_on_not_ok_status() as status:
                        self._reader.GetNext(status)
                else:
                    self._reader.GetNext()
            except:
                break
          
            yield self._reader.record()
         

class EventFileLoader(RawEventFileLoader):
    """An iterator that yields parsed Event protos."""

    def Load(self):
        """Loads all new events from disk.

        Yields: All events in the file that have not been yielded yet.
        """
        for record in super(EventFileLoader, self).Load():
            yield event_pb2.Event.FromString(record)


class TimestampedEventFileLoader(EventFileLoader):
    """An iterator that yields (UNIX timestamp float, Event proto) pairs."""

    def Load(self):
        """Loads all new events and their wall time values from disk.

        Yields: Pairs of (UNIX timestamp float, Event proto) for all events
        in the file that have not been yielded yet.
        """
        for event in super(TimestampedEventFileLoader, self).Load():
            yield (event.wall_time, event)

