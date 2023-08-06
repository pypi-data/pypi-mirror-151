#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import json

from . import DatasetMeta
from . import ImageMeta
from . import FaceMeta
from . import ObjectMeta
from . import BrandMeta
from . import SceneMeta
from . import LandmarkMeta
from . import TextMeta


__version__ = "1.1"


class ImageContentMeta:

    def __init__(self):

        self.dataset_meta = DatasetMeta.DatasetMeta()
        self.image_meta = ImageMeta.ImageMeta()
        self.content_meta = ContentMeta()

    def get(self):

        return {
            "dataset": self.dataset_meta.get(),
            "image": self.image_meta.get(),
            "content": self.content_meta.get()
        }

    def put_image_meta_by_fname_url(self, fname):
        self.image_meta.set(fname)

    def put_image_meta(self, img_meta):
        self.image_meta.put(img_meta)

    def put_content_meta(self, face_meta, object_meta, brand_meta, scene_meta, landmark_meta):
        self.content_meta.face_meta.put(face_meta)
        self.content_meta.object_meta.put(object_meta)
        self.content_meta.brand_meta.put(brand_meta)
        self.content_meta.scene_meta.put(scene_meta)
        self.content_meta.landmark_meta.put(landmark_meta)


class ContentMeta:

    def __init__(self):

        self.face_meta     = FaceMeta.FaceMeta()
        self.object_meta   = ObjectMeta.ObjectMeta()
        self.brand_meta    = BrandMeta.BrandMeta()
        self.scene_meta    = SceneMeta.SceneMeta()
        self.landmark_meta = LandmarkMeta.LandmarkMeta()
        self.text_meta     = TextMeta.TextMeta()

    def get(self):

        return {
            "face":     self.face_meta.get(),
            "object":   self.object_meta.get(),
            "brand":    self.brand_meta.get(),
            "scene":    self.scene_meta.get(),
            "landmark": self.landmark_meta.get(),
            "text":     self.text_meta.get()
        }


def get_bbox_info(img_filename, json_filename=None, json_folder=None, json_filename_list=None, cat='face'):

    output_dict = None
    json_fnames = []

    if json_filename:
        json_fnames = [json_filename]
    elif json_folder:
        json_fnames = [os.path.join(json_folder, x) for x in os.listdir(json_folder)]
    elif json_filename_list:
        json_fnames = json_filename_list
    else:
        pass

    img_corename = os.path.splitext(os.path.basename(img_filename))[0]

    for json_fname in json_fnames:
        # noinspection PyUnresolvedReferences
        if os.path.splitext(json_fname)[1].lower() == ".json":
            json_corename = os.path.splitext(os.path.basename(json_fname))[0]
            if img_corename in json_corename:
                with open(json_fname, 'r') as fid:
                    img_content_dict = json.load(fid)
                if cat == 'face':
                    output_dict = _get_face_bbox_info(img_content_dict)
                elif cat == 'object':
                    output_dict = _get_object_bbox_info(img_content_dict)
                else:
                    output_dict = {}
                break

    return output_dict


def _get_object_bbox_info(img_content_dict):

    _dict = img_content_dict
    width = _dict["image"]["width"]
    height = _dict["image"]["height"]
    ptr = _dict["content"]["object"]["annotation"]
    denorm_bboxes = denormalize_bboxes(ptr["bboxes"], width=width, height=height)

    ids       = [x[0] for x in ptr["ids"]]       if ptr["ids"]       else []
    track_ids = [x[0] for x in ptr["track_ids"]] if ptr["track_ids"] else []
    reid_ids  = [x[0] for x in ptr["reid_ids"]]  if ptr["reid_ids"]  else []

    return {
        'bboxes':    denorm_bboxes,
        'ids':       ids,
        'track_ids': track_ids,
        'reid_ids':  reid_ids
    }


def _get_face_bbox_info(img_content_dict):

    _dict = img_content_dict
    width = _dict["image"]["width"]
    height = _dict["image"]["height"]
    ptr = _dict["content"]["face"]["annotation"]
    denorm_bboxes = denormalize_bboxes(ptr["bboxes"], width=width, height=height)

    ids     = [x[0] for x in ptr["ids"]]     if ptr["ids"]     else []
    races   = [x    for x in ptr["races"]]   if ptr["races"]   else []
    genders = [x    for x in ptr["genders"]] if ptr["genders"] else []
    ages    = [x    for x in ptr["ages"]]    if ptr["ages"]    else []
    masks   = [x    for x in ptr["masks"]]   if ptr["masks"]   else []

    return {
        'bboxes':  denorm_bboxes,
        'ids':     ids,
        'races':   races,
        'genders': genders,
        'ages':    ages,
        'masks':   masks
    }


def denormalize_bboxes(bboxes, width=0, height=0):

    if not bboxes:
        return bboxes

    if bboxes[0][2] > 1 and bboxes[0][3] > 1:
        return bboxes

    denorm_bboxes = []
    for bbox in bboxes:
        t0 = int(bbox[0] * width)
        t1 = int(bbox[1] * height)
        t2 = int(bbox[2] * width)
        t3 = int(bbox[3] * height)
        denorm_bboxes.append([t0, t1, t2, t3])
    return denorm_bboxes


def test_get_bbox_info(cat):
    from pprint import pprint
    _this_folder_ = os.path.dirname(os.path.abspath(__file__))

    img_fname   = os.path.abspath(os.path.join(_this_folder_, "./camera_1/img/camera_1.000.000ms.jpg"))
    json_fname  = os.path.abspath(os.path.join(_this_folder_, "./camera_1/json/camera_1.000.000ms.json"))
    json_folder = os.path.abspath(os.path.join(_this_folder_, "./camera_1/json/"))
    json_file_list = [os.path.join(json_folder, x) for x in os.listdir(json_folder)]

    print(f"\n # {cat} test of get_bbox_info with json_filename.")
    pprint(get_bbox_info(img_fname, json_filename=json_fname, cat=cat))

    print(f"\n # {cat} test of get_bbox_info with json_folder.")
    pprint(get_bbox_info(img_fname, json_folder=json_folder, cat=cat))

    print(f"\n # {cat} test of get_bbox_info with json_file_list.")
    pprint(get_bbox_info(img_fname, json_filename_list=json_file_list, cat=cat))


if __name__ == "__main__":

    test_get_bbox_info('face')
