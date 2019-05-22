#!/usr/bin/env python
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Upload current build to docker in google.')
parser.add_argument('tag', type=str, help='Tag for the docker image name')

args = parser.parse_args()

tag = args.tag

if tag == "":
    print("Tag can't be empty")

#
print("Backup settings")
subprocess.call(["cp","map/settings.py","map/settings_backup.py"])
print("Use correct settings")
subprocess.call(["cp","map/settings_gcloud.py","map/settings.py"])
print("Clear and generate static files")
subprocess.call(["./manage.py","collectstatic","--noinput","--clear"])
print("Upload static")
subprocess.call(["gsutil","-m","rsync","-R","static/","gs://tasador/static"])
print("Create docker")
subprocess.call(["docker","build","-t","gcr.io/proyectoinmobiliario-212003/tasador:{}".format(tag),"."])
print("Upload docker")
subprocess.call(["docker","push","gcr.io/proyectoinmobiliario-212003/tasador:{}".format(tag)])