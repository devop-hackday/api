#!/usr/bin/python
import os

port=5001
debug=True
maxsize=16 * 1024 * 1024
# allow=tuple('jpg jpeg png gif npm pdf odf bmp tiff'.split())
allow=tuple('zip tar.gz tgz'.split())
basedir = os.path.abspath(os.path.dirname(__file__))

STAGING_FOLDER = "tmp/upload"
MAX_CONTENT_LENGTH = maxsize
PROCESSING_FOLDER = "tmp/processing"
DONE_FOLDER = "tmp/done"
ALLOW_FILES=allow
WTF_CSRF_ENABLED = True
SECRET_KEY = 'gtfo-man-gtfo'
subscription_id= ''
auth_token= "meh"
region='us'

