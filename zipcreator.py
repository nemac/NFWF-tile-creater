#!/usr/bin/env python

'''
A CLI utility for building the VRT raster that points to S3-hosted NFWF model datasets.

Relies on a config file in the root directory.
'''

import os
import os.path
import click
import yaml
import sys
import urllib2
from zipfile import ZipFile

baseurl = 'https://s3.amazonaws.com/nfwf-tool/'
basefolder = 'zips'

def get_config():
  with open('zipcreator.yml') as f:
    config = yaml.safe_load(f)
  return config

def get_all_config():
  with open('zip_all.yml') as f:
    config = yaml.safe_load(f)
  return config

def zipalls():
    config = get_all_config()
    file = config['zips']
    for zipindex in range(0, len(file)):
        zipname = file[zipindex]['name'] + '.zip'
        zipfiles = file[zipindex]['input_files']
        print(zipname)

        zipnamepath = os.path.join(basefolder, zipname)

        # get each file for the zip file
        for filetobeziped in zipfiles:
            print('  ' + filetobeziped)

        if(os.path.exists(zipnamepath)):
            os.remove(zipnamepath)

        # writing files to a zipfile
        with ZipFile(zipnamepath,'w') as zip:
            for filetobeziped in zipfiles:
                filetobezipedpath = os.path.join(basefolder, filetobeziped)
                print('  zipping ' + filetobezipedpath )
                zip.write(filetobezipedpath)

        print('')


def zipfile():
  config = get_config()
  if 'dataset_bucket' in config:
    dataset_bucket = config['dataset_bucket']
  else:
    dataset_bucket = None
  file = config['datasets']
  main_tree = None
  main_root = None
  for zipindex in range(0, len(file)):
      zipname = file[zipindex]['name'] + '.zip'
      zipnamepath = os.path.join(basefolder, zipname)
      zipfiles = file[zipindex]['input_files']

      s3folder = ''
      if 'folder' in file[zipindex]:
          s3folder = file[zipindex]['folder'] + '/'

      print(zipname)

      # get each file for the zip file
      for filetobeziped in zipfiles:
          print('  ' + filetobeziped)
          filetobezipedurl = baseurl + s3folder + filetobeziped
          print ('  downloading the file ' + filetobezipedurl + ' from s3.')

          response = urllib2.urlopen(filetobezipedurl)
          filetobezipedpath = os.path.join(basefolder, filetobeziped)
          if(os.path.exists(filetobezipedpath)):
              os.remove(filetobezipedpath)

          with open(filetobezipedpath,'wb') as output:
              output.write(response.read())

      print('  ')

      if(os.path.exists(zipnamepath)):
          os.remove(zipnamepath)

      print('  ')

      # writing files to a zipfile
      with ZipFile(zipnamepath,'w') as zip:
          for filetobeziped in zipfiles:
              filetobezipedpath = os.path.join(basefolder, filetobeziped)
              print('  zipping ' + filetobezipedpath )
              zip.write(filetobezipedpath)

      for filetobeziped in zipfiles:
          filetobezipedpath = os.path.join(basefolder, filetobeziped)
          if(os.path.exists(filetobezipedpath)):
              os.remove(filetobezipedpath)

      print('  ')

      # for zipfilesindex in file[zipindex]['input_files']
      #   print(file[zipindex]['input_files'][i])

if __name__ == '__main__':
  # zipfile()
  zipalls()
