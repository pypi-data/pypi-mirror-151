#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import cv2


class ImageMeta:

    def __init__(self):
        self.url = None
        self.color = None
        self.width = None
        self.height = None

    def set(self, url, width=None, height=None, color=None):

        self.url = url
        if width and height and color:
            self.width = width
            self.height = height
            self.color = color
        else:
            # noinspection PyUnresolvedReferences
            img_shape = cv2.imread(url).shape
            self.height, self.width, self.color = img_shape[0], img_shape[1], img_shape[2]

    def get(self):
        return {
            "url": self.url,
            "width": self.width,
            "height": self.height,
            "color": self.color
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                self.set(meta["url"], meta["width"], meta["height"], meta["color"])
            else:
                # noinspection PyUnresolvedReferences
                self.set(meta.url, meta.width, meta.height, meta.color)
            return True
        except Exception as _e:
            print(f" @ Error in put method of ImageMeta: {_e}")
            return False
