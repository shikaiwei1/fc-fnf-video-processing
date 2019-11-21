# -*- coding: utf-8 -*-
import subprocess
import logging
import json
import os
import time

LOGGER = logging.getLogger()

NAS_ROOT = "/mnt/auto/"
FFMPEG_BIN = NAS_ROOT + "ffmpeg"

# a decorator for print the excute time of a function
def print_excute_time(func):
    def wrapper(*args, **kwargs):
        local_time = time.time()
        ret = func(*args, **kwargs)
        LOGGER.info('current Function [%s] excute time is %.2f' %
              (func.__name__, time.time() - local_time))
        return ret
    return wrapper

def get_fileNameExt(filename):
    (fileDir, tempfilename) = os.path.split(filename)
    (shortname, extension) = os.path.splitext(tempfilename)
    return fileDir, shortname, extension

@print_excute_time
def handler(event, context):
    evt = json.loads(event)
    # split video key, locate in nas
    input_path = evt['video_key'] 
    fileDir, shortname, extension = get_fileNameExt(input_path)

    target_type = evt['target_type']
    transcoded_filename = 'transcoded_%s%s' % (shortname, target_type)
    transcoded_filepath = os.path.join(fileDir, transcoded_filename)

    if os.path.exists(transcoded_filepath):
        os.remove(transcoded_filepath)

    subprocess.call([FFMPEG_BIN, '-y', '-i', input_path, transcoded_filepath])
    return {}
    