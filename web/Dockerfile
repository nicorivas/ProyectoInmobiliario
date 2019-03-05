# [START docker]
# https://github.com/GoogleCloudPlatform/python-docker
FROM gcr.io/google_appengine/python

# Install GDAL
RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  python-gdal

# Create a virtualenv for the application dependencies.
# If you want to use Python 3, add the -p python3.4 flag.
RUN virtualenv -p python3 /env

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate. This ensures the application is executed within
# the context of the virtualenv and will have access to its dependencies.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Install dependencies.
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install --upgrade pip && /env/bin/pip install -r /app/requirements.txt
ADD . /app

CMD export DJANGO_PASSWORD=$(cat /etc/secrets/djangouserpw);
CMD gunicorn -b :$PORT map.wsgi
# [END docker]