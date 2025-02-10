# start with operating system for Red Hat Openshift
FROM registry.access.redhat.com/ubi8/python-312

COPY ./requirements.txt /opt/app-root/src
RUN cd /opt/app-root/src & \
    pip install -r requirements.txt

# this will invalidate the image layer - copy files
COPY . /opt/app-root/src

# Change this to UID that matches your username on the host
USER 1001

# Expose the application port
EXPOSE 8010

# Command to run the FastAPI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8010"]
