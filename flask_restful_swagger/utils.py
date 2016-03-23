# -*- coding: utf-8 -*-

import functools
import warnings
import re

__author__ = 'sobolevn'


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    :param func: function to decorated.
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn_explicit(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            filename=func.func_code.co_filename,
            lineno=func.func_code.co_firstlineno + 1,
        )
        return func(*args, **kwargs)

    return new_func


def convert_from_camel_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def prettify_class_name(name):
    """
        Split words in PascalCase string into separate words.
        :param name:
            String to split
    """
    return re.sub(r'(?<=.)([A-Z])', r' \1', name)
