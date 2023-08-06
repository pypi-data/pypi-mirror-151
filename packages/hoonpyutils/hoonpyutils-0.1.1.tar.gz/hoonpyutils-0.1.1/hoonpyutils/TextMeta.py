#!/usr/bin/env python
# -*- coding:utf-8 -*-


class TextMeta:

    def __init__(self):

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
                # noinspection PyUnresolvedReferences
                self.set_algorithm(meta.algorithm, meta.model)
                # noinspection PyUnresolvedReferences
                self.set_annotation(meta.classes, meta.languages,
                                    meta.bboxes, meta.texts, meta.legibilities, meta.scores)
            return True

        except Exception as e:
            print(f" @ Error in put method: {str(e)}")
            return False
