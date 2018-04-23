import os

curr_dir_path = os.path.dirname(os.path.realpath(__file__))

VIDEO_DATA_DIR = os.path.join(curr_dir_path, "data/")


# audio related
SAMPLE_RATE = 16000
BYTE_WIDTH = 2