#!/usr/bin/env python3
""" Filtered logger module """

import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """ Formatter for filtered logging """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Returns filtered values from log records """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def get_db() -> mysql.connector.connection.MYSQLConnection:
    """ MySQL database connection """
    db_connect = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns regex obfuscated log messages """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object """
    logger_inst = logging.getLogger("user_data")
    logger_inst.setLevel(logging.INFO)
    logger_inst.propagate = False

    strream_handlers = logging.StreamHandler()
    strream_handler.setLevel(logging.INFO)

    formattewd = RedactingFormatter(list(PII_FIELDS))
    strream_handler.setFormatter(formattewd)

    logger_inst.addHandler(strream_handler)
    return logger_inst


def main() -> None:
    """ Retrieves all rows from the users table and logs them """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    logger_inst = get_logger()
    all_headers = [field[0] for field in cursor.description]

    for row in cursor:
        information = ''
        for f, p in zip(row, all_headers):
            information += f'{p}={(f)}; '
        logger_inst.info(information)

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

