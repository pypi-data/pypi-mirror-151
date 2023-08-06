#!/usr/bin/env python
# -*- coding:utf-8 -*-

__version__ = "2.0"
# 1. Add mask attribute.
# 2. Store top-n candidates.


class FaceMeta:

    def __init__(self):

        self.detect_algorithm = None
        self.recog_algorithm = None
        self.attr_algorithm = None
        self.mask_algorithm = None

        self.detect_model_path = None
        self.recog_model_path = None
        self.attr_model_path = None
        self.mask_model_path = None

        self.face_name_path = None
        self.race_name_path = None
        self.gender_name_path = None
        self.age_name_path = None
        self.mask_name_path = None

        self.bboxes = []
        self.bbox_scores = []
        self.vectors = []
        self.ids = []
        self.id_scores = []
        self.races = []
        self.race_scores = []
        self.genders = []
        self.gender_scores = []
        self.ages = []
        self.age_scores = []
        self.masks = []
        self.mask_scores = []

    def set_algorithm(self,
                      detect_algorithm=None,
                      recog_algorithm=None,
                      attr_algorithm=None,
                      mask_algorithm=None,
                      detect_model_path=None,
                      recog_model_path=None,
                      attr_model_path=None,
                      mask_model_path=None,
                      face_name_path=None,
                      race_name_path=None,
                      gender_name_path=None,
                      age_name_path=None,
                      mask_name_path=None):

        self.detect_algorithm = self.detect_algorithm if detect_algorithm is None else detect_algorithm
        self.recog_algorithm = self.recog_algorithm if recog_algorithm is None else recog_algorithm
        self.attr_algorithm = self.attr_algorithm if attr_algorithm is None else attr_algorithm
        self.mask_algorithm = self.mask_algorithm if mask_algorithm is None else mask_algorithm

        self.detect_model_path = self.detect_model_path if detect_model_path is None else detect_model_path
        self.recog_model_path = self.recog_model_path if recog_model_path is None else recog_model_path
        self.attr_model_path = self.attr_model_path if attr_model_path is None else attr_model_path
        self.mask_model_path = self.mask_model_path if mask_model_path is None else mask_model_path

        self.face_name_path = self.face_name_path if face_name_path is None else face_name_path
        self.race_name_path = self.race_name_path if race_name_path is None else race_name_path
        self.gender_name_path = self.gender_name_path if gender_name_path is None else gender_name_path
        self.age_name_path = self.age_name_path if age_name_path is None else age_name_path
        self.mask_name_path = self.mask_name_path if mask_name_path is None else mask_name_path

    def set_annotation(self,
                       bboxes, bbox_scores,
                       vectors=None, ids=None, id_scores=None,
                       races=None, race_scores=None,
                       genders=None, gender_scores=None,
                       ages=None, age_scores=None,
                       masks=None, mask_scores=None):

        self.bboxes = bboxes
        self.bbox_scores = bbox_scores
        self.vectors = vectors
        self.ids = ids
        self.id_scores = id_scores
        self.races = races
        self.race_scores = race_scores
        self.genders = genders
        self.gender_scores = gender_scores
        self.ages = ages
        self.age_scores = age_scores
        self.masks = masks
        self.mask_scores = mask_scores

    def get(self):

        return {'algorithm': self.get_algorithm(),
                'annotation': self.get_annotation()}

    def get_algorithm(self):
        return {"detect_algorithm": self.detect_algorithm,
                "recog_algorithm": self.recog_algorithm,
                "attr_algorithm": self.attr_algorithm,
                "mask_algorithm": self.mask_algorithm,
                "detect_model_path": self.detect_model_path,
                "recog_model_path": self.recog_model_path,
                "attr_model_path": self.attr_model_path,
                "mask_model_path": self.mask_model_path,
                "face_name_path": self.face_name_path,
                "race_name_path": self.race_name_path,
                "gender_name_path": self.gender_name_path,
                "age_name_path": self.age_name_path,
                "mask_name_path": self.mask_name_path}

    def get_annotation(self):
        return {"bboxes": self.bboxes,
                "bbox_scores": self.bbox_scores,
                "vectors": self.vectors,
                "ids": self.ids,
                "id_scores": self.id_scores,
                "races": self.races,
                "race_scores": self.race_scores,
                "genders": self.genders,
                "gender_scores": self.gender_scores,
                "ages": self.ages,
                "age_scores": self.age_scores,
                "masks": self.masks,
                "mask_scores": self.mask_scores}

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                algo = meta["algorithm"]
                tag = meta["annotation"]
            else:
                algo = meta.__dict__
                tag = meta.__dict__
            self.set_algorithm(detect_algorithm=algo.get("detect_algorithm"),
                               recog_algorithm=algo.get("recog_algorithm"),
                               attr_algorithm=algo.get("attr_algorithm"),
                               mask_algorithm=algo.get("mask_algorithm"),
                               detect_model_path=algo.get("detect_model_path"),
                               recog_model_path=algo.get("recog_model_path"),
                               attr_model_path=algo.get("attr_model_path"),
                               mask_model_path=algo.get("mask_model_path"),
                               face_name_path=algo.get("face_name_path"),
                               race_name_path=algo.get("race_name_path"),
                               gender_name_path=algo.get("gender_name_path"),
                               age_name_path=algo.get("age_name_path"),
                               mask_name_path=algo.get("mask_name_path"))
            self.set_annotation(bboxes=tag['bboxes'],
                                bbox_scores=tag['bbox_scores'],
                                vectors=tag['vectors'],
                                ids=tag['ids'],
                                id_scores=tag['id_scores'],
                                races=tag['races'],
                                race_scores=tag['race_scores'],
                                genders=tag['genders'],
                                gender_scores=tag['gender_scores'],
                                ages=tag['ages'],
                                age_scores=tag['age_scores'],
                                masks=tag['masks'],
                                mask_scores=tag['mask_scores'])
            return True

        except Exception as e:
            # noinspection PyArgumentList
            print(f" @ Error in put method: {str(e)}")
            return False

    def get_simple(self):

        return {
            "bboxes": self.bboxes,
            "ids": self.ids,
            "ages": self.ages,
            "genders": self.genders,
            "masks": self.masks
        }