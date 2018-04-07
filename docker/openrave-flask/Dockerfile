FROM osbertngok/openrave:latest
ENV PROJECT_NAME openrave-flask
MAINTAINER osbertngok<osbertngok@gmail.com>

# Is this required?
# ENV PYTHONPATH=$PYTHONPATH:`openrave-config --python-dir`

COPY python-restful-api /

RUN pip install flask

EXPOSE 5000

ENTRYPOINT ["python", "/python-restful-api/app.py"]
