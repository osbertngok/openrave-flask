FROM osbertngok/openrave:latest
ENV PROJECT_NAME openrave-flask
MAINTAINER osbertngok<osbertngok@gmail.com>

# Is this required?
# ENV PYTHONPATH=$PYTHONPATH:`openrave-config --python-dir`

RUN pip install flask pymongo
RUN mkdir -p /opt/openrave-flask/upload
RUN mkdir /python-restful-api
EXPOSE 5000

COPY python-restful-api /python-restful-api

ENTRYPOINT ["python", "/python-restful-api/app.py"]

