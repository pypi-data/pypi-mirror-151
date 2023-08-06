#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

_this_fname_ = os.path.basename(__file__)


class ObjectMeta:

    def __init__(self):

        self.detect_algorithm = None
        self.detect_model_path = None
        self.obj_name_path = None

        self.track_algorithm = None
        self.track_model_path = None
        self.track_name_path = None

        self.reid_algorithm = None
        self.reid_model_path = None
        self.reid_name_path = None

        self.bboxes = None
        self.bbox_scores = None
        self.ids = None
        self.id_scores = None
        self.track_ids = None
        self.track_scores = None
        self.reid_ids = None
        self.reid_scores = None

        self.obj_name_dict = []
        self.track_name_dict = []
        self.reid_name_dict = []

    def set_algorithm(self,
                      detect_algorithm=None,
                      track_algorithm=None,
                      reid_algorithm=None,
                      detect_model_path=None,
                      track_model_path=None,
                      reid_model_path=None,
                      obj_name_path=None,
                      track_name_path=None,
                      reid_name_path=None):

        self.detect_algorithm  = detect_algorithm  if detect_algorithm  else self.detect_algorithm
        self.track_algorithm   = track_algorithm   if track_algorithm   else self.track_algorithm
        self.reid_algorithm    = reid_algorithm    if reid_algorithm    else self.reid_algorithm
        self.detect_model_path = detect_model_path if detect_model_path else self.detect_model_path
        self.track_model_path  = track_model_path  if track_model_path  else self.track_model_path
        self.reid_model_path   = reid_model_path   if reid_model_path   else self.reid_model_path
        self.obj_name_path     = obj_name_path     if obj_name_path     else self.obj_name_path
        self.track_name_path   = track_name_path   if track_name_path   else self.track_name_path
        self.reid_name_path    = reid_name_path    if reid_name_path    else self.reid_name_path

    def set_annotation(self, bboxes, bbox_scores, ids, id_scores,
                       track_ids=None, track_scores=None, reid_ids=None, reid_scores=None):
        self.bboxes = bboxes
        self.bbox_scores = bbox_scores
        self.ids = ids
        self.id_scores = id_scores
        self.track_ids = track_ids
        self.track_scores = track_scores
        self.reid_ids = reid_ids
        self.reid_scores = reid_scores

    def get(self):
        return { 'algorithm': self.get_algorithm(),
                 'annotation': self.get_annotation()
                 }

    def get_algorithm(self):
        return {  "detect_algorithm":  self.detect_algorithm,
                  "detect_model_path": self.detect_model_path,
                  "obj_name_path":     self.obj_name_path,
                  "track_algorithm":   self.track_algorithm,
                  "track_model_path":  self.track_model_path,
                  "track_name_path":   self.track_name_path,
                  "reid_algorithm":    self.reid_algorithm,
                  "reid_model_path":   self.reid_model_path,
                  "reid_name_path":    self.reid_name_path
                  }

    def get_annotation(self):
        return { "bboxes": self.bboxes,
                 "bbox_scores": self.bbox_scores,
                 "ids": self.ids,
                 "id_scores": self.id_scores,
                 "track_ids": self.track_ids,
                 "track_scores": self.track_scores,
                 "reid_ids": self.reid_ids,
                 "reid_scores": self.reid_scores
                 }

    def put(self, meta):

        try:
            algo = meta["algorithm"]  if isinstance(meta, dict) else meta.__dict__
            obj  = meta["annotation"] if isinstance(meta, dict) else meta.__dict__
            self.set_algorithm(algo.get("detect_algorithm"),
                               algo.get("detect_model_path"),
                               algo.get("obj_name_path"),
                               algo.get("track_algorithm"),
                               algo.get("track_model_path"),
                               algo.get("track_name_path"),
                               algo.get("reid_algorithm"),
                               algo.get("reid_model_path"),
                               algo.get("reid_name_path")
                               )
            self.set_annotation(obj.get("bboxes"),
                                obj.get("bbox_scores"),
                                obj.get("ids"),
                                obj.get("id_scores"),
                                obj.get("track_ids"),
                                obj.get("track_scores"),
                                obj.get("reid_ids"),
                                obj.get("reid_scores")
                                )
            return True
        except Exception as e:
            print(f" @ Error in {_this_fname_} put method: {str(e)}")
            return False

    def put_obj_name_dict(self, obj_name_dict):
        self.obj_name_dict = obj_name_dict

    def put_track_name_dict(self, track_name_dict):
        self.track_name_dict = track_name_dict

    def put_reid_name_dict(self, reid_name_dict):
        self.reid_name_dict = reid_name_dict

    def get_simple(self):
        return {
            "bboxes": self.bboxes,
            "ids": self.ids,
            "id_scores": self.id_scores
        }