FROM registry.access.redhat.com/ubi8/python-39

# Add application sources with correct permissions for OpenShift
USER 0
# ADD app-src .
RUN chown -R 1001:0 ./
USER 1001

WORKDIR /

COPY ./requirements.txt .

RUN pip install -U "pip>=19.3.1"
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 8010

CMD ["fastapi", "run", "app.py", "--port", "8010"]

