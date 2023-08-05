# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from copy import copy


class AbstractBase():

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(f"Attribute '{name}' does not exist on "
                                 f"'{type(self).__name__}' instance.")

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def to_dict(self):

        def format(value):
            if isinstance(value, AbstractBase):
                return value.to_dict()
            elif isinstance(value, list):
                return [format(item) for item in value]
            else:
                return value

        data = copy(self.__dict__)
        for key, value in data.items():
            data[key] = format(value)
        return data

    def to_json(self):
        return json.dumps(self.to_dict(),
                          sort_keys=True,
                          indent=2,
                          default=str)


class Person(AbstractBase):
    pass


class Student(AbstractBase):
    pass


class Employee(AbstractBase):
    pass


class Transcript(AbstractBase):
    pass


class Major(AbstractBase):
    pass


class Sport(AbstractBase):
    pass


class Adviser(AbstractBase):
    pass


class Term(AbstractBase):
    pass
