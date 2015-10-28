#!/usr/bin/python
#
# Aim at a storage repo and create workers
#
import os, sys, tarfile, zipfile
import re
from flask import render_template
from papi import api, request, jsonify, landing

class Work():
    def __init__(self, conifg):
        self.ok = False
        self.msg = []
        self.payload = {}
        self.debug=config.debug
    
    # create workers
    def createWorker(self):
        id=""
        return id

    def createWorkers(self, count):
        return True
       
    def verifyStorage(self, location):
        return True

    def getArchive(self, location):
        return True

    def copyArchive(self, workers):
        return True

    def cleanUp(self, location):
        return True

    def unpackArchive(self, filename):
        source="%s/%s" % (dapi.config['STAGING_FOLDER'], filename)
        target="%s/%s" % (dapi.config['PROCESSING_FOLDER'], filename)
        # source=sour."".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        try:
             os.makedirs(target)
        except OSError, e:
             if e.errno != errno.EEXIST:
                 raisa
        if re.match('.tgz$', source):
            extractTgz(source, target)
        if re.match('.zip$', source):
            extractZip(source, target)

    def extractTgz(tar_url, extract_path='.'):
        print tar_url
        tar = tarfile.open(tar_url, 'r')
        for item in tar:
            tar.extract(item, extract_path)
            if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
                extract(item.name, "./" + item.name[:item.name.rfind('/')])

    def extractZip(zip_url, extract_path='.'):
        print zip_url
        zip_ref = zipfile.ZipFile(zip_url, 'r')
        zip_ref.extractall(extract_path)
        zip_ref.close()

# should not be here
@api.route('/api/process', methods=['GET'])
def api():
    archive=request.args.get('archive')
    workers=request.args.get('workers')
    unpackArchive(archive)

@api.route('/web/process', methods=['GET'])
def web():
    archive=request.args.get('archive')
    workers=request.args.get('workers')
    unpackArchive(archive)
    user = "Anonymous"
    return render_template('index.html',
                           title='Lander',
                           user=user)

if __name__ == '__main__':
  api.run(debug=True) 
