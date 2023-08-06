#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Notice
# 1. make_subtitle_video doesn't work in moviepy==1.0.1.
#    If you have moviepy==1.0.1, downgrade it to 1.0.0.
#
import os
import sys
import datetime
import copy


_this_fname_ = os.path.basename(__file__)

try:
    import numpy as np
except Exception as e:
    print(f" @ Warning: numpy import error in {_this_fname_} - {str(e)}")
try:
    # noinspection PyUnresolvedReferences
    import srt
except Exception as e:
    print(f" @ Warning: srt import error in {_this_fname_} - {str(e)}")
try:
    # noinspection PyUnresolvedReferences
    import moviepy.editor as mpy
except Exception as e:
    print(f" @ Warning: moviepy import error in {_this_fname_} - {str(e)}")
try:
    import cv2
except Exception as e:
    print(f" @ Warning: cv2 import error in {_this_fname_} - {str(e)}")
try:
    # noinspection PyPep8
    from PIL import Image, ImageDraw, ImageFont
except Exception as e:
    print(f" @ Warning: Pillow import error in {_this_fname_} - {str(e)}")


_this_folder_ = os.path.dirname(os.path.abspath(__file__))
KOR_FONT = './Fonts/SourceHanSerifK-Regular.otf'


class LoggerWrapper:
    def info(self): pass
    def error(self): pass


def get_stdout_logger(logger=None):
    if logger is None:
        logger = LoggerWrapper()
        logger.info = print
        logger.error = print
    return logger


class VidProp:
    def __init__(self, width=None, height=None, fps=None, duration=None, frame_count=None):
        self.width = width
        self.height = height
        self.fps = fps
        self.frame_count = frame_count
        self.duration = duration

        if self.duration is None:
            if self.fps is not None and self.frame_count is not None:
                self.duration = self.frame_count / self.fps


VidInfo = VidProp


def extract_audio_from_video(vid_fname, aud_fname='', force_=True):
    """
    Extract audio from video and save it.

    :param vid_fname:
    :param aud_fname:
    :param force_:
    :return:
    """
    video_clip = mpy.VideoFileClip(vid_fname)
    audio_clip = video_clip.audio
    if not aud_fname:
        aud_fname = os.path.splitext(vid_fname)[0] + ".mp3"

    if force_:
        run_ = True
    else:
        if os.path.isfile(aud_fname):
            run_ = True if os.path.getsize(aud_fname) < 10000 else False
        else:
            run_ = True

    if run_:
        audio_clip.write_audiofile(aud_fname)

    return True


def convert_avi_to_mp4(out_vid_path, min_size=10000, logger=get_stdout_logger()):
    if out_vid_path:
        if os.path.getsize(out_vid_path) < min_size:
            # noinspection PyArgumentList
            logger.error(" @ Error: file size of {} < {:d}".format(out_vid_path, min_size))
            return False
        # noinspection PyShadowingNames
        try:
            out_vid_path_mp4 = os.path.splitext(out_vid_path)[0] + ".mp4"
            os.system("ffmpeg -i {} {} -y -loglevel panic".format(out_vid_path, out_vid_path_mp4))
            # noinspection PyShadowingNames
            try:
                if os.path.getsize(out_vid_path_mp4) > 0:
                    os.system("rm {}".format(out_vid_path))
            except Exception as e:
                # noinspection PyArgumentList
                logger.error(" @ Error in converting to mp4, {}".format(e))
        except Exception as e:
            # noinspection PyArgumentList
            logger.error(" @ Error in convert_avi_to_mp4 with {}: {}".format(out_vid_path, str(e)))
            # noinspection PyArgumentList
            logger.error(e)


def get_vid_info(vid_path, print_=True, logger=get_stdout_logger()):

    # noinspection PyUnresolvedReferences
    vid_cap = cv2.VideoCapture(vid_path)
    vid_info = VidInfo()
    if vid_cap.isOpened():
        # noinspection PyUnresolvedReferences
        vid_info.width = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # noinspection PyUnresolvedReferences
        vid_info.height = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # noinspection PyUnresolvedReferences
        vid_info.frame_count = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # noinspection PyUnresolvedReferences
        vid_info.fps = vid_cap.get(cv2.CAP_PROP_FPS)
        vid_info.duration = vid_info.frame_count / vid_info.fps
        if print_:
            # noinspection PyArgumentList
            logger.info(" # {} : ({:d} x {:d}), {:d} frames, {:.1f} fps, {:.1f} duration".
                        format(vid_path, vid_info.width, vid_info.height,
                               vid_info.frame_count, vid_info.fps, vid_info.duration))
    else:
        # noinspection PyArgumentList
        logger.error(" @ Error: vid_path is NOT opened via opencv.".format(vid_path))
    vid_cap.release()
    return vid_info


def convert_stt_to_srt(stt_string, srt_fname=None, logger=get_stdout_logger()):
    """
    Convert stt string to srt object and save it as a file.

    :param stt_string:
    :param srt_fname:
    :param logger:
    :return:
    """
    # noinspection PyArgumentList
    logger.info(" # Convert stt to srt, {}".format(srt_fname))

    srt_string = ''
    for i, stt_text in enumerate(stt_string):
        if stt_text['txt'] != '':
            srt_string += '{:d}\n'.format(i + 1)
            # print(stt_text)
            times = [
                datetime.datetime.utcfromtimestamp(float(stt_text['start'])),
                datetime.datetime.utcfromtimestamp(float(stt_text['end']))
            ]
            srt_string += "{:02d}:{:02d}:{:02d},{:03d}". \
                format(times[0].hour, times[0].minute, times[0].second, int(times[0].microsecond / 1000))
            srt_string += " --> "
            srt_string += "{:02d}:{:02d}:{:02d},{:03d}\n". \
                format(times[1].hour, times[1].minute, times[1].second, int(times[1].microsecond / 1000))
            srt_string += stt_text['txt'] + "\n\n"
    srt_string = srt.compose(list(srt.parse(srt_string)))

    if srt_fname is not None:
        with open(srt_fname, 'w') as f:
            f.write(srt_string)

    return srt_string


def make_subtitle_video(vid_fname, srt_vid_fname, srt_obj, font_fname=KOR_FONT):

    if not os.path.isfile(font_fname):
        print(f"Font file name found, {font_fname} for example, {KOR_FONT}.")
        sys.exit()

    vid_obj = mpy.VideoFileClip(vid_fname)
    blank_img = Image.fromarray(np.zeros((128, vid_obj.w, 3), dtype=np.uint8))
    pos_offset = (64, 64)
    clips = []
    ref_time = 0
    for idx in range(len(srt_obj)):
        # print(" {:f} - {:f} - {:f}".format(ref_time, srt_obj[idx].start.total_seconds(),
        #                                    srt_obj[idx].end.total_seconds()))
        # blank_duration = int(srt_obj[idx].start.total_seconds()) - ref_time
        # text_duration = int(srt_obj[idx].end.total_seconds()) - int(srt_obj[idx].start.total_seconds())
        blank_duration = srt_obj[idx].start.total_seconds() - ref_time
        text_duration = srt_obj[idx].end.total_seconds() - srt_obj[idx].start.total_seconds()
        clips.append(mpy.ImageClip(np.array(blank_img)).set_duration(blank_duration))
        sub_img = copy.deepcopy(blank_img)
        draw = ImageDraw.Draw(sub_img)
        draw.text(pos_offset, "SpeechRecognizer : " + srt_obj[idx].content.strip(),
                  font=ImageFont.truetype(font_fname, 24))
        clips.append(mpy.ImageClip(np.array(sub_img)).set_duration(text_duration))
        ref_time = srt_obj[idx].end.total_seconds()

    # blank_duration = int(vid_obj.duration) - int(srt_obj[-1].end.total_seconds())
    blank_duration = vid_obj.duration - srt_obj[-1].end.total_seconds()
    clips.append(mpy.ImageClip(np.array(blank_img)).set_duration(blank_duration))
    sub_obj = mpy.concatenate_videoclips(clips, method="compose")
    final_clip = mpy.clips_array([[vid_obj], [sub_obj]])
    final_clip.resize(width=1080).write_videofile(srt_vid_fname)

    return True


def merge_stt_strings(stt_arr, time_interval=0.1):

    if stt_arr is None or stt_arr == [] or len(stt_arr) == 1:
        return stt_arr

    stt_time = stt_arr[0]['start']
    stt_text = stt_arr[0]['txt']
    new_stt_arr = []
    for idx in range(len(stt_arr) - 1):
        if stt_arr[idx+1]['start'] - stt_arr[idx]['end'] < time_interval:
            stt_text += " " + stt_arr[idx+1]['txt']
        else:
            new_stt_arr.append({'start': stt_time,
                                'end': stt_arr[idx]['end'],
                                'txt': stt_text})
            stt_time = stt_arr[idx+1]['start']
            stt_text = stt_arr[idx+1]['txt']

    new_stt_arr.append({'start': stt_time,
                        'end': stt_arr[-1]['end'],
                        'txt': stt_text})

    return new_stt_arr


def extract_frames_from_video(vid_fname, interval=1, logger=get_stdout_logger()):

    vid_obj = mpy.VideoFileClip(vid_fname)
    vid_info = get_vid_info(vid_fname, logger=logger)

    frames = []
    for sec in np.arange(0, vid_info.duration, interval):
        frames.append(vid_obj.get_frame(sec))

    return frames


def get_cv2_vid_properties(cap):

    vid_prop = VidProp()

    if not cap.isOpened():
        print(" @ Error: cap is NOT  opened.")

    # noinspection PyUnresolvedReferences
    vid_prop.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # noinspection PyUnresolvedReferences
    vid_prop.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # noinspection PyUnresolvedReferences
    vid_prop.fps = cap.get(cv2.CAP_PROP_FPS)
    # noinspection PyUnresolvedReferences
    vid_prop.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_prop.duration = vid_prop.frame_count / vid_prop.fps

    return vid_prop


def get_snapshot_from_video(vid_path, time_msec):
    # noinspection PyUnresolvedReferences
    vid_inst = cv2.VideoCapture(vid_path)
    # noinspection PyUnresolvedReferences
    vid_inst.set(cv2.CAP_PROP_POS_MSEC, time_msec)
    ret, frame = vid_inst.read()
    vid_inst.release()
    if ret:
        return frame
    else:
        return None


"""
def split_audio_file(audio_fname, postfix="_", logger=get_stdout_logger()):
    
    if not utils.check_file_existence(audio_fname, logger=logger):
        logger.error(" @ Error: ")

        return
    sound = pydub.AudioSegment.from_file(audio_fname)
"""