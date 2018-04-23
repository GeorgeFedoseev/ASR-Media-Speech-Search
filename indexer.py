# =* coding: utf-8 *=
import os
import subprocess
import wave
import shutil

import const
from utils.yt_utils import download_yt_audio
from utils.slicing_utils import slice_audio_by_silence
from utils import audio_utils
from utils.deepspeech_utils import run_deepspeech_for_wav

YT_VIDEOS_TO_INDEX = [
    "SAQFzYnRTts"
]


def check_dependencies():
    try:
        subprocess.check_output(['soxi'], stderr=subprocess.STDOUT)        
        subprocess.check_output(['ffmpeg', '--help'], stderr=subprocess.STDOUT)
        subprocess.check_output(['deepspeech', '-h'], stderr=subprocess.STDOUT)
    except Exception as ex:
        print 'ERROR: some of dependencies are not installed: ffmpeg or sox: '+str(ex)
        return False

    return True

def process_video(yt_video_id):
    curr_dir_path = os.getcwd()

    video_data_path = os.path.join(const.VIDEO_DATA_DIR, yt_video_id)

    # download video
    original_audio_path = download_yt_audio(yt_video_id)

    # convert audio and apply filters
    wav_audio_path = os.path.join(video_data_path, "audio.wav")
    if not os.path.exists(wav_audio_path):
        audio_utils.convert_to_wav(original_audio_path, wav_audio_path)

    wav_vol_corr_path = os.path.join(video_data_path, "audio_vol_corr.wav")
    print("correct_volume")
    if not os.path.exists(wav_vol_corr_path):  
        audio_utils.correct_volume(wav_audio_path, wav_vol_corr_path, db=-12)

    wav_filtered_path = os.path.join(video_data_path, "audio_filtered.wav")
    if not os.path.exists(wav_filtered_path):    
        print("apply_bandpass_filter")
        audio_utils.apply_bandpass_filter(wav_vol_corr_path, wav_filtered_path, low=2500)

    wave_o = wave.open(wav_filtered_path, "r")

    print("slice audio")
    pieces, avg_len_sec = slice_audio_by_silence(wave_o)
    print("total pieces: %i, avg_len_sec: %f" % (len(pieces), avg_len_sec))

    # first remove prev pieces
    pieces_folder_path = os.path.join(curr_dir_path, "data/pieces")

    if os.path.exists(pieces_folder_path):
        shutil.rmtree(pieces_folder_path)

    os.makedirs(pieces_folder_path)


    print("start transcribing...")
    for i, piece in enumerate(pieces):
        piece_path = os.path.join(pieces_folder_path, "piece_%i.wav" % i)
        audio_utils.save_wave_samples_to_file(piece["samples"], n_channels=1, byte_width=2, sample_rate=16000, file_path=piece_path)

        # run inference
        text = run_deepspeech_for_wav(piece_path, use_lm=False)
        print(text)        

if __name__ == "__main__":
    if check_dependencies():
        process_video(YT_VIDEOS_TO_INDEX[0])