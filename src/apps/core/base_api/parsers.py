import codecs

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser
from rest_framework.settings import api_settings
from rest_framework.utils import json


class PlainTextParser(BaseParser):
    """
    A parser that parses plain text requests and converts them to json.
    """

    media_type = "text/plain"
    strict = api_settings.STRICT_JSON

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as plain text and returns the resulting json data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get("encoding", settings.DEFAULT_CHARSET)

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            text_content = decoded_stream.read()

            parse_constant = json.strict_constant if self.strict else None
            return json.loads(text_content, parse_constant=parse_constant)

        except ValueError as exc:
            raise ParseError(_(f"Plain text parse error - {exc}"))
