#!/usr/bin/env python
# -*- coding:utf-8 -*-


class LandmarkMeta:

    def __init__(self):

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
                # noinspection PyUnresolvedReferences
                self.set_algorithm(meta.algorithm, meta.model, meta.name_list)
                # noinspection PyUnresolvedReferences
                self.set_annotation(meta.names, meta.scores, meta.ids)

            return True
        except Exception as e:
            print(f" @ Error in put method: {str(e)}")
            return False

    def get_simple(self, num_candidates=5):

        size = len(self.names) if num_candidates  > len(self.names) else num_candidates

        return {
            "names": self.names[:size],
            "scores": self.scores[:size]
        }
