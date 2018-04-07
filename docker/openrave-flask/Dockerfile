FROM osbertngok/openrave:latest
ENV PROJECT_NAME openrave-flask
MAINTAINER osbertngok<osbertngok@gmail.com>

# Is this required?
# ENV PYTHONPATH=$PYTHONPATH:`openrave-config --python-dir`

RUN mkdir -p /opt/openrave-flask/upload
RUN mkdir /python-restful-api
COPY python-restful-api /python-restful-api

RUN pip install flask

EXPOSE 5000

ENTRYPOINT ["python", "/python-restful-api/app.py"]

