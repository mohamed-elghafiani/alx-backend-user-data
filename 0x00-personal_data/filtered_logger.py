#!/usr/bin/env python3
"""Module for obfuscating log messages using regular expressions.

   This module provides a function called filter_datum that takes a log message
   and obfuscates specified fields using a regular expression substitution.

   Functions:
     filter_datum(fields, redaction, message, separator):
       Obfuscates specified fields in the log message with
       the specified redaction.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message:str, separator:str) -> str:
    """Obfuscates specified fields in the log message"""
    for field in fields:
        message = re.sub(
            rf'{field}=[^{separator}]+', f'{field}={redaction}', message)
    return message
