#!/usr/bin/env python
# -*- coding:utf-8 -*-


class DatasetMeta:

    def __init__(self):

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
                # noinspection PyUnresolvedReferences
                self.set(meta.description, meta.version, meta.date_created, meta.augmented, meta.answer_refined)

            return True
        except Exception as e:
            # noinspection PyArgumentList
            print(f" @ Error in put method: {str(e)}")
            return False
