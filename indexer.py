# =* coding: utf-8 *=
import subprocess

YT_VIDEOS_TO_INDEX = [
    "ZIi5rTJ0JJQ"
]


def check_dependencies():
     try:
        subprocess.check_output(['soxi'], stderr=subprocess.STDOUT)        
        subprocess.check_output(['ffmpeg', '--help'], stderr=subprocess.STDOUT)
    except Exception as ex:
        print 'ERROR: some of dependencies are not installed: ffmpeg or sox: '+str(ex)
        return False

    return True

def process_video(yt_video_id):
    pass