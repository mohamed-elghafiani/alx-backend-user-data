#!/usr/bin/env python3
"""Module for obfuscating log messages using regular expressions.

   This module provides a function called filter_datum that takes a log message
   and obfuscates specified fields using a regular expression substitution.

   Functions:
     filter_datum(fields, redaction, message, separator):
       Obfuscates specified fields in the log message with
       the specified redaction.

     get_logger():
       returns a logging.Logger object

     get_db():
       returns a connector to the database

   Classes:
     RedactingFormatter(logging.Formatter):
       Redacting Formatter class
"""
import re
from typing import List
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
      fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Obfuscates specified fields in the log message"""
    for field in fields:
        message = re.sub(
            rf'{field}=[^{separator}]+', f'{field}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return connection


def main():
    """Read and filter data
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        msg = "".join(["{}={};".format(f, v) for (f, v) in zip(fields, row)])
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
