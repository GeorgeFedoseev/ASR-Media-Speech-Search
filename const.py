import os

curr_dir_path = os.path.dirname(os.path.realpath(__file__))


DATA_DIR = os.path.join(curr_dir_path, "data/")

VIDEO_DATA_DIR = os.path.join(DATA_DIR, "media_data/")

DEEP_SPEECH_MODEL_PATH = os.path.join(DATA_DIR, "deepspeech_model/")


# audio related
SAMPLE_RATE = 16000
BYTE_WIDTH = 2