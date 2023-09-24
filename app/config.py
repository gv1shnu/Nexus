
# Standard library
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY: bytes = os.urandom(24)
