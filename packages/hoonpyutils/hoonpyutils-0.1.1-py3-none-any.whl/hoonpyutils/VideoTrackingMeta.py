#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

__version__ = "1.1"


class VideoTrackingMeta:

    def __init__(self):

        self.video_meta = None
        self.face_algorithm = None
        self.object_algorithm = None
        self.reid_algorithm = None

    def get(self):

        return {
            "image": self.image_meta.get(),
            "content": self.content_meta.get()
        }

    def put_image_meta_by_fname_url(self, fname):
        self.image_meta.set_by_url(fname)

    def put_image_meta(self, img_meta):
        self.image_meta.put(img_meta)

    def put_content_meta(self, face_meta, object_meta, brand_meta, scene_meta, landmark_meta):
        self.content_meta.face_meta.put(face_meta)
        self.content_meta.object_meta.put(object_meta)
        self.content_meta.brand_meta.put(brand_meta)
        self.content_meta.scene_meta.put(scene_meta)
        self.content_meta.landmark_meta.put(landmark_meta)


class DatasetMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.description = None
        self.version = None
        self.date_created = None

        self.augmented = None
        self.answer_refined = None

    def set(self, description=None, version=None, date_created=None, augmented=None, answer_refined=None):

        self.description = self.description if description is None else description
        self.version = self.version if version is None else version
        self.date_created = self.date_created if date_created is None else date_created

        self.augmented = self.augmented if augmented is None else augmented
        self.answer_refined = self.answer_refined if answer_refined is None else answer_refined

    def get(self):

        return {
            "description": self.description,
            "version": self.version,
            "date_created": self.date_created,

            "attributes": {
                "augmented": self.augmented,
                "answer_refined": self.answer_refined
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                attr = meta['attributes']
                self.set(meta['description'], meta['version'], meta['date_created'],
                         attr['augmented'], attr['answer_refined'])
            else:
                self.set(meta.description, meta.version, meta.date_created, meta.augmented, meta.answer_refined)

            return True
        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False


class ImageMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.file_name = None

        self.color = None
        self.width = None
        self.height = None
        self.url = None

    def set_by_url(self, url):

        self.file_name = os.path.basename(url)

        img_shape = cv2.imread(url).shape
        self.height, self.width, self.color = img_shape[0], img_shape[1], img_shape[2]
        self.url = os.path.abspath(url)

    def set(self, file_name=None, color=None, width=None, height=None, url=None):

        if file_name is None and url is not None:
            self.file_name = os.path.basename(url)
            img_shape = cv2.imread(url).shape
            self.height, self.width, self.color = img_shape[0], img_shape[1], img_shape[2]
            self.url = os.path.abspath(url)

        self.file_name = self.file_name if file_name is None else file_name
        self.color = self.color if color is None else color
        self.width = self.width if width is None else width
        self.height = self.height if height is None else height
        self.url = self.url if url is None else url

    def get(self):
        return {
            "file_name": self.file_name,
            "attributes": {
                "color": self.color,
                "width": self.width,
                "height": self.height,
                "url": self.url
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                attr = meta["attributes"]
                self.set(meta["file_name"], attr["color"], attr["width"], attr["height"], attr["url"])
            else:
                self.set(meta.file_name, meta.color, meta.width, meta.height, meta.url)
            return True
        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False


class ContentMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.face_meta = FaceMeta()
        self.object_meta = ObjectMeta()
        self.brand_meta = BrandMeta()
        self.scene_meta = SceneMeta()
        self.landmark_meta = LandmarkMeta()
        self.text_meta = TextMeta()

    def get(self):

        return {
            "face": self.face_meta.get(),
            "object": self.object_meta.get(),
            "brand": self.brand_meta.get(),
            "scene": self.scene_meta.get(),
            "landmark": self.landmark_meta.get(),
            "text": self.text_meta.get()
        }


class FaceMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.detect_algorithm = None
        self.recog_algorithm = None
        self.attr_algorithm = None
        self.detect_model = None
        self.recog_model = None
        self.attr_model = None
        self.name_list = None

        self.bboxes = None
        self.vectors = None
        self.ids = None
        self.names = None
        self.name_scores = None
        self.races = None
        self.race_scores = None
        self.genders = None
        self.gender_scores = None
        self.ages = None
        self.age_scores = None

    def set_algorithm(self,
                      detect_algorithm=None,
                      recog_algorithm=None,
                      attr_algorithm=None,
                      detect_model=None,
                      recog_model=None,
                      attr_model=None,
                      name_list=None):

        self.detect_algorithm = self.detect_algorithm if detect_algorithm is None else detect_algorithm
        self.recog_algorithm = self.recog_algorithm if recog_algorithm is None else recog_algorithm
        self.attr_algorithm = self.attr_algorithm if attr_algorithm is None else attr_algorithm
        self.detect_model = self.detect_model if detect_model is None else detect_model
        self.recog_model = self.recog_model if recog_model is None else recog_model
        self.attr_model = self.attr_model if attr_model is None else attr_model
        self.name_list = self.name_list if name_list is None else name_list

    def set_annotation(self, bboxes, vectors, ids, names, name_scores,
                       races=None, race_scores=None,
                       genders=None, gender_scores=None,
                       ages=None, age_scores=None):

        self.bboxes = bboxes
        self.vectors = vectors
        self.ids = ids
        self.names = names
        self.name_scores = name_scores
        self.races = races
        self.race_scores = race_scores
        self.genders = genders
        self.gender_scores = gender_scores
        self.ages = ages
        self.age_scores = age_scores

    def get(self):

        return {
            "algorithm": {
                "detect_algorithm": self.detect_algorithm,
                "recog_algorithm": self.recog_algorithm,
                "attr_algorithm": self.attr_algorithm,
                "detect_model": self.detect_model,
                "recog_model": self.recog_model,
                "attr_model": self.attr_model,
            },
            "annotation": {
                "bboxes": self.bboxes,
                "vectors": self.vectors,
                "ids": self.ids,
                "names": self.names,
                "scores": self.name_scores,
                "races": self.races,
                "race_scores": self.race_scores,
                "genders": self.genders,
                "gender_scores": self.gender_scores,
                "ages": self.ages,
                "age_scores": self.age_scores
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                algo = meta["algorithm"]
                tag = meta["annotation"]
                self.set_algorithm(algo.get("detect_algorithm"),
                                   algo.get("recog_algorithm"),
                                   algo.get("attr_algorithm"),
                                   algo.get("detect_model"),
                                   algo.get("recog_model"),
                                   algo.get("attr_model"),
                                   algo.get("name_list"))
                self.set_annotation(tag['bboxes'], tag['vectors'], tag['ids'], tag['names'], tag['scores'],
                                    tag['races'], tag['race_scores'],
                                    tag['genders'], tag['gender_scores'],
                                    tag['ages'], tag['age_scores'])
            else:
                self.set_algorithm(meta.detect_algorithm,
                                   meta.recog_algorithm,
                                   meta.attr_algorithm,
                                   meta.detect_model,
                                   meta.recog_model,
                                   meta.attr_model,
                                   meta.name_list)
                self.set_annotation(meta.bboxes, meta.vectors, meta.ids, meta.names, meta.name_scores,
                                    meta.races, meta.race_scores,
                                    meta.genders, meta.gender_scores,
                                    meta.ages, meta.age_scores)

            return True

        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False

    def get_simple(self):

        return {
            "bboxes": self.bboxes,
            "names": self.names,
            "ages": self.ages,
            "genders": self.genders
        }


class ObjectMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.algorithm = None
        self.model = None
        self.name_list = None

        self.bboxes = None
        self.ids = None
        self.names = None
        self.scores = None

    def set_algorithm(self, algorithm=None, model=None, name_list=None):

        self.algorithm = self.algorithm if algorithm is None else algorithm
        self.model = self.model if model is None else model
        self.name_list = self.name_list if name_list is None else name_list

    def set_annotation(self, bboxes, ids, names, scores):

        self.bboxes = bboxes
        self.ids = ids
        self.names = names
        self.scores = scores

    def get(self):

        return {
            "algorithm": {
                "algorithm": self.algorithm,
                "model": self.model,
                "name_list": self.name_list
            },
            "annotation": {
                "bboxes": self.bboxes,
                "ids": self.ids,
                "names": self.names,
                "scores": self.scores
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                algo = meta["algorithm"]
                obj = meta["annotation"]
                self.set_algorithm(algo.get("algorithm"), algo.get("model"), algo.get("name_list"))
                self.set_annotation(obj.get("bboxes"), obj.get("ids"), obj.get("names"), obj.get("scores"))
            else:
                self.set_algorithm(meta.algorithm, meta.model, meta.name_list)
                self.set_annotation(meta.bboxes, meta.ids, meta.names, meta.scores)

            return True
        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False

    def get_simple(self):

        return {
            "bboxes": self.bboxes,
            "names": self.names,
            "scores": self.scores
        }


class BrandMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.algorithm = None
        self.model = None
        self.name_list = None

        self.bboxes = None
        self.ids = None
        self.names = None
        self.scores = None

    def set_algorithm(self, algorithm=None, model=None, name_list=None):

        self.algorithm = self.algorithm if algorithm is None else algorithm
        self.model = self.model if model is None else model
        self.name_list = self.name_list if name_list is None else name_list

    def set_annotation(self, bboxes, ids, names, scores):

        self.bboxes = bboxes
        self.ids = ids
        self.names = names
        self.scores = scores

    def get(self):

        return {
            "algorithm": {
                "algorithm": self.algorithm,
                "model": self.model,
                "name_list": self.name_list
            },
            "annotation": {
                "bboxes": self.bboxes,
                "ids": self.ids,
                "names": self.names,
                "scores": self.scores
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                algo = meta["algorithm"]
                tag = meta["annotation"]
                self.set_algorithm(algo.get("algorithm"), algo.get("model"), algo.get("name_list"))
                self.set_annotation(tag.get("bboxes"), tag.get("ids"), tag.get("names"), tag.get("scores"))
            else:
                self.set_algorithm(meta.algorithm, meta.model, meta.name_list)
                self.set_annotation(meta.bboxes, meta.ids, meta.names, meta.scores)
            return True

        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False

    def get_simple(self):

        return {
            "bboxes": self.bboxes,
            "names": self.names,
            "scores": self.scores
        }


class SceneMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.algorithm = None
        self.model = None
        self.name_list = None

        self.ids = None
        self.names = None
        self.scores = None

    def set_algorithm(self, algorithm=None, model=None, name_list=None):

        self.algorithm = self.algorithm if algorithm is None else algorithm
        self.model = self.model if model is None else model
        self.name_list = self.name_list if name_list is None else name_list

    def set_annotation(self, ids, names, scores):

        self.ids = ids
        self.names = names
        self.scores = scores

    def get(self):

        return {
            "algorithm": {
                "algorithm": self.algorithm,
                "model": self.model,
                "name_list": self.name_list
            },
            "annotation": {
                "ids": self.ids,
                "names": self.names,
                "scores": self.scores
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                algo = meta["algorithm"]
                tag = meta["annotation"]
                self.set_algorithm(algo.get("algorithm"), algo.get("model"), algo.get("name_list"))
                self.set_annotation(tag.get("ids"), tag.get("names"), tag.get("scores"))
            else:
                self.set_algorithm(meta.algorithm, meta.model, meta.name_list)
                self.set_annotation(meta.ids, meta.names, meta.scores)
            return True

        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False

    def get_simple(self, num_candidates=5):

        return {
            "names": self.names[:num_candidates],
            "scores": self.scores[:num_candidates]
        }


class LandmarkMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.algorithm = None
        self.model = None
        self.name_list = None

        self.names = None
        self.scores = None
        self.ids = None

    def set_algorithm(self, algorithm=None, model=None, name_list=None):

        self.algorithm = self.algorithm if algorithm is None else algorithm
        self.model = self.model if model is None else model
        self.name_list = self.name_list if name_list is None else name_list

    def set_annotation(self, names, scores, ids):

        self.names = names
        self.scores = scores
        self.ids = ids

    def get(self):

        return {
            "algorithm": {
                "algorithm": self.algorithm,
                "model": self.model,
                "name_list": self.name_list
            },
            "annotation": {
                "names": self.names,
                "ids": self.ids,
                "scores": self.scores
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                algo = meta["algorithm"]
                tag = meta["annotation"]
                self.set_algorithm(algo.get("algorithm"), algo.get("model"), algo.get("name_list"))
                self.set_annotation(tag.get("names"), tag.get("scores"), tag.get("ids"))
            else:
                self.set_algorithm(meta.algorithm, meta.model, meta.name_list)
                self.set_annotation(meta.names, meta.scores, meta.ids)

            return True
        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False

    def get_simple(self, num_candidates=5):

        size = len(self.names) if num_candidates  > len(self.names) else num_candidates

        return {
            "names": self.names[:size],
            "scores": self.scores[:size]
        }


class TextMeta:

    def __init__(self, logger=get_stdout_logger()):

        self.logger = logger

        self.algorithm = None
        self.model = None

        self.classes = None
        self.languages = None
        self.bboxes = None
        self.texts = None
        self.legibilities = None
        self.scores = None

    def set_algorithm(self, algorithm=None, model=None):

        self.algorithm = self.algorithm if algorithm is None else algorithm
        self.model = self.model if model is None else model

    def set_annotation(self, classes, languages, bboxes, texts, legibilities, scores):

        self.classes = classes
        self.languages = languages
        self.bboxes = bboxes
        self.texts = texts
        self.legibilities = legibilities
        self.scores = scores

    def get(self):

        return {
            "algorithm": {
                "algorithm": self.algorithm,
                "model": self.model
            },
            "annotation": {
                "classes": self.classes,
                "languages": self.languages,
                "bboxes": self.bboxes,
                "texts": self.texts,
                "legibilities": self.legibilities,
                "scores": self.scores
            }
        }

    def put(self, meta):

        if meta is None or meta == []:
            return False

        try:
            if isinstance(meta, dict):
                algo = meta["algorithm"]
                tag = meta["annotation"]
                self.set_algorithm(algo.get("algorithm"), algo.get("model"))
                self.set_annotation(tag.get("classes"), tag.get("languages"),
                                    tag.get("bboxes"), tag.get("texts"), tag.get("legibilities"), tag.get("scores"))
            else:
                self.set_algorithm(meta.algorithm, meta.model)
                self.set_annotation(meta.classes, meta.languages,
                                    meta.bboxes, meta.texts, meta.legibilities, meta.scores)
            return True

        except Exception as e:
            # noinspection PyArgumentList
            self.logger.error(" @ Error in put method")
            # noinspection PyArgumentList
            self.logger.error(e)
            return False
