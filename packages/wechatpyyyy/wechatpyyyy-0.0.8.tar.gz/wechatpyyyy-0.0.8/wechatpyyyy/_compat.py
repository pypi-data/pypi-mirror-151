# -*- coding: utf-8 -*-
"""
    wechatpyyyy._compat
    ~~~~~~~~~~~~~~~~~

    This module makes it easy for wechatpy to run on both Python 2 and 3.

    :copyright: (c) 2014 by messense.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import sys  # NOQA
import six  # NOQA
import warnings

warnings.warn("Module `wechatpyyyy._compat` is deprecated, will be removed in 2.0"
              "use `wechatpyyyy.utils` instead",
              DeprecationWarning, stacklevel=2)

from wechatpyyyy.utils import get_querystring  # NOQA
from wechatpyyyy.utils import json  # NOQA
