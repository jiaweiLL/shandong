import os
from .event_file_loader import EventFileLoader


def find_all_event_files(dir_path):
    """find all event files in directory `dir_path`.
    
    :param dir_path: directory path
    :type dir_path: str
    :return: list of file path. 
    """
    file_path_list = []
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            if "events" in file_name:
                file_path_list.append(os.path.join(root, file_name)) 

    return file_path_list


class SummaryReader(object):
    """Parse events protobuf into basic data and numpy.ndarray.
    """
    def __init__(self, parse_dir):
        """
        :param parse_dir: the directory of events file.
        :type parse_dir: str
        """
        self._parse_dir = parse_dir

    def get_scalar(self, tag):
        """
        :param tag: tag of scalar data.
        :type tag: str
        :return: a list of tuple, each element is (tag, step, scalar_value)
        """
        event_file_list = find_all_event_files(self._parse_dir)
       
        result = [] 
        for event_file in event_file_list:
            event_file_loader = EventFileLoader(event_file)
            
            for event_str in event_file_loader.Load():
                if event_str.summary.value:
                    for item in event_str.summary.value:
                        if item.tag == tag:
                            result.append((item.tag,
                                           event_str.step,
                                           item.simple_value))
        return result

