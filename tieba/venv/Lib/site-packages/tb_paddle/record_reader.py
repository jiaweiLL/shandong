# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
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
# =============================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import struct

from .crc32c import *

TFE_DEVICE_PLACEMENT_WARN = 0
TFE_DEVICE_PLACEMENT_SILENT_FOR_INT32 = 0
TFE_DEVICE_PLACEMENT_SILENT = 0
TFE_DEVICE_PLACEMENT_EXPLICIT = 0


class RecordReader:
    def __init__(self, filename=None, start_offset=0, compression_type=None, status=None):
        if filename is None:
            raise FileNotFoundError('No filename provided, cannot read Events')
        if not os.path.exists(filename):
            raise FileNotFoundError('File \'{}\' does not exist'.format(filename))
        if start_offset:
            raise NotImplementedError('start offset not supported by compat reader')
        if compression_type:
            # TODO: Handle gzip and zlib compressed files
            raise NotImplementedError('compression not supported by compat reader')
        self.filename = filename
        self.start_offset = start_offset
        self.compression_type = compression_type
        self.status = status
        self.curr_event = None
        self.file_handle = open(self.filename, 'rb')
          
    def GetNext(self):
        # Read the header
        self.curr_event = None
        header_str = self.file_handle.read(8)
        if len(header_str) != 8:
            raise StopIteration('No more events to read')
        header = struct.unpack('Q', header_str)
           
        # Read the crc32, which is 4 bytes, and check it against the crc32 of the header
        crc_header_str = self.file_handle.read(4)
        crc_header = struct.unpack('I', crc_header_str)
        header_crc_calc = masked_crc32c(header_str)
        if header_crc_calc != crc_header[0]:
            raise ValueError('{} failed header crc32 check'.format(self.filename))
         
        # The length of the header tells us how many bytes the Event string takes
        header_len = int(header[0])
        event_str = self.file_handle.read(header_len)
        event_crc_calc = masked_crc32c(event_str)
          
        # The next 4 bytes contain the crc32 of the Event string, which we check for integrity.
        # Sometimes, the last Event has no crc32, in which case we skip.
        crc_event_str = self.file_handle.read(4)
        if crc_event_str:
            crc_event = struct.unpack('I', crc_event_str)
            if event_crc_calc != crc_event[0]:
                raise ValueError('{} failed event crc32 check'.format(self.filename))
          
        # Set the current event to be read later by record() call
        self.curr_event = event_str
          
    def record(self):
        return self.curr_event
