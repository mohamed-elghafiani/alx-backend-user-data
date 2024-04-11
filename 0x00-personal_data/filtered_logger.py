#!/usr/bin/env python3
"""Module for obfuscating log messages using regular expressions.

   This module provides a function called filter_datum that takes a log message
   and obfuscates specified fields using a regular expression substitution.

   Functions:
     filter_datum(fields, redaction, message, separator):
       Obfuscates specified fields in the log message with
       the specified redaction.

   Classes:
     RedactingFormatter(logging.Formatter):
       Redacting Formatter class
"""
import re
from typing import List
import logging


def filter_datum(
      fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscates specified fields in the log message"""
    for field in fields:
        message = re.sub(
            rf'{field}=[^{separator}]+', f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format log records according to FORMAT"""
        obfuscated_msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR
        )
        record.msg = obfuscated_msg
        return super().format(record)
