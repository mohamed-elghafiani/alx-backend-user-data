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


def filter_datum(fields, redaction, message, separator):
    """Obfuscates specified fields in the log message with
       the specified redaction.
    """
    obfuscated = message
    for field in fields:
        obfuscated = re.sub(
            rf'{field}=[^{separator}]+', f'{field}={redaction}', obfuscated)

    return obfuscated
