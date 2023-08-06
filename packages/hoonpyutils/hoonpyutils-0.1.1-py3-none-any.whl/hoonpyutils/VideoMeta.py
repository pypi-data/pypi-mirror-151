#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import cv2
import sys


class VideoMeta:

    def __init__(self):

        self.url = None
        self.width = None
        self.height = None
        self.fps = None
        self.duration = None

    def set(self, url, width=None, height=None, fps=None, duration=None, vid_prop=None):

        self.url = url

        if vid_prop:
            self.width = vid_prop.width
            self.height = vid_prop.width
            self.fps = vid_prop.width
            self.duration = vid_prop.width

        if width and height and fps and duration:
            self.width = width
            self.height = height
            self.fps = fps
            self.duration = duration
        else:
            # noinspection PyUnresolvedReferences
            vid_inst =  cv2.VideoCapture(self.url)
            if not vid_inst.isOpened():
                # noinspection PyArgumentList
                print(" @ ERROR: opening video stream.")
                sys.exit(1)
            # noinspection PyUnresolvedReferences
            self.width = int(vid_inst.get(cv2.CAP_PROP_FRAME_WIDTH))
            # noinspection PyUnresolvedReferences
            self.height = int(vid_inst.get(cv2.CAP_PROP_FRAME_HEIGHT))
            # noinspection PyUnresolvedReferences
            self.fps = vid_inst.get(cv2.CAP_PROP_FPS)
            # noinspection PyUnresolvedReferences
            frame_count = int(vid_inst.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration = frame_count / vid_prop.fps


    def get(self):
        return {
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "fps": self.fps,
            "duration": self.duration
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        # noinspection PyShadowingNames
        try:
            if isinstance(meta, dict):
                self.set(meta["url"], meta["width"], meta["height"], meta["fps"], meta["duration"])
            else:
                # noinspection PyUnresolvedReferences
                self.set(meta.url, meta.width, meta.height, meta.fps, meta.duration)
            return True
        except Exception as e:
            # noinspection PyArgumentList
            print(" @ Error in put method: {}".format(str(e)))
            # noinspection PyArgumentList
            print(e)
            return False
