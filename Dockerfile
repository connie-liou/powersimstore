FROM aetd-dockerlab.gsfc.nasa.gov/docker/nasa-docker-containers/python3/nasa-ubuntu18-python3:latest
LABEL Code 563 EPS Design Tool Version 0.2.0

RUN mkdir /app

WORKDIR /app

COPY . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8050

ENV NAME World

CMD ["python3", "server.py"]