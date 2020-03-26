import os.path
import struct

from .crc32c import *

REGISTERED_FACTORIES = {}


def directory_check(path):
    """Initialize the directory for log files."""
    try:
        prefix = path.split(':')[0]
        factory = REGISTERED_FACTORIES[prefix]
        return factory.directory_check(path)
    except KeyError:
        if not os.path.exists(path):
            os.makedirs(path)


class RecordWriter(object):
    def __init__(self, path):
        self._name_to_tf_name = {}
        self._tf_names = set()
        self.path = path
        self._writer = open(path, 'wb')

    def write(self, data):
        w = self._writer.write
        header = struct.pack('Q', len(data))
        w(header)
        w(struct.pack('I', masked_crc32c(header)))
        w(data)
        w(struct.pack('I', masked_crc32c(data)))

    def flush(self):
        self._writer.flush()

    def close(self):
        self._writer.close()

