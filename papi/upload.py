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

stage="Upload"

class Upload():
    def __init__(self,config):
        self.ok = False
        self.msg = []
        self.payload = {}
        self.allow=config.allow
        self.debug=config.debug

    def unique_id(self):
        return hex(uuid.uuid4().time)[2:-1]

    def checkmagic(self,filepath):
        m = magic.from_file(filepath, mime=True)
        type = m.split('/')[1]
        if type in self.allow:
            return type
        else:
            return False

    def sha1(self,filepath):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with open(filepath, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return(hasher.hexdigest())

    def allowed_file(self,filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.allow

    def preview_files():
        return send_from_directory(dapi.config['STAGING_FOLDER'],
            filename)

    def create_dir(dirname):
        try:
            os.makedirs(dirname)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

    # @staging.uploaded()
    def upload_files(self,req):
        if req.method == 'POST':
            files=[]
            filename = None
            # flask.request
            uploaded_files = req.files.getlist("file")
            print uploaded_files
            for file in uploaded_files:
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                else:
                    self.ok = False
                    if file.filename == "":
                        self.msg.append("No file submitted")
                    else:
                        self.msg.append("File '%s' not in allowed list" % (file.filename))
                    return self.ok

                # should save to a hashed dir with uuid and store that for retrieval later
                create_dir=api.config['STAGING_FOLDER']
                filepath="%s/%s" % (api.config['STAGING_FOLDER'], filename)
                file.save(filepath)
                # magic needs fixing, does not work now...
                filemagic=self.checkmagic(filepath)
                # if filemagic is False:
                #    print "skipping unlink of %s now" % (filepath)
                #    # os.unlink(filepath)
                # else:
                checksum=self.sha1(filepath)
                # check if we already have it
                origin=1
                d={ "name": filename, "type": filemagic, 'sha1': checksum }
                files.append(d)
            self.ok = True
            self.payload = files
            return self.ok
        if req.method == 'GET':
            self.ok = True
            return self.ok
        return self.ok

@api.route('/web/upload', methods=['GET', 'POST'])
def web_upload():
    form = UploadForm()
    loader = Upload(config)
    if request.method == 'GET':
        return render_template('upload.html',
            title='File upload',
            form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('File upload for="%s"' % (form.filename))
            return redirect('./')
        res = loader.upload_files(request)
        if res:
            return render_template('upload.html', 
                title='File upload',
                form=form,
                results=loader.payload)
            flash('File upload means we need a file...')
        else:
            for msg in loader.msg:
                flash(msg)
            return render_template('upload.html', 
                title='File upload',
                form=form)

@api.route('/api/upload', methods=['GET', 'POST'])
def api_upload():
    # print request.files.getlist("file")
    loader = Upload(config)
    res = loader.upload_files(request) 
    json_results=[]
    if res == False:
        return jsonify(error=loader.msg)
    else:
        # get the file locations and send them back
        return jsonify(items=res.payload)

if __name__ == '__main__':
  api.run(debug=True)
