from __future__ import absolute_import, unicode_literals

import logging

from wechatpyyyy.client import WeChatClient  # NOQA
from wechatpyyyy.component import ComponentOAuth, WeChatComponent  # NOQA
from wechatpyyyy.exceptions import WeChatClientException, WeChatException, WeChatOAuthException, WeChatPayException  # NOQA
from wechatpyyyy.oauth import WeChatOAuth  # NOQA
from wechatpyyyy.parser import parse_message  # NOQA
from wechatpyyyy.pay import WeChatPay  # NOQA
from wechatpyyyy.replies import create_reply  # NOQA

__version__ = '1.8.18'
__author__ = 'messense'

# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
