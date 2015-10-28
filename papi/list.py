#!/usr/bin/python
#
# Upload images to be processed
# TODO: multi-tenancy
#
import os, errno
import magic
import hashlib
import uuid
from papi import api, request, jsonify
from werkzeug import secure_filename
from flask import render_template, flash, redirect
from .forms import UploadForm
import config

stage="List"

class List():
    def __init__(self,config):
        self.ok = False
        self.msg = []
        self.payload = {}
        self.allow=config.allow
        self.debug=config.debug

    def list_files(self, path):
        tree = dict(name=path, children=[])
        return os.listdir(path)

@api.route('/web/list', methods=['GET', 'POST'])
def web_list():
    form = UploadForm()
    loader = List(config)
    res = loader.list_files(api.config['STAGING_FOLDER'])
    if res:
        return render_template('list.html', 
            title='File listing',
            form=form,
            results=res)
    else:
        for msg in loader.msg:
            flash(msg)
        return render_template('list.html', 
            title='File Listing',
            form=form)

@api.route('/api/list', methods=['GET', 'POST'])
def api_list():
    # print request.files.getlist("file")
    loader = List(config)
    res = loader.list_files(api.config['STAGING_FOLDER'])
    json_results=[]
    if res == False:
        return jsonify(error=loader.msg)
    else:
        # get the file locations and send them back
        return jsonify(items=res.payload)

if __name__ == '__main__':
  api.run(debug=True)
