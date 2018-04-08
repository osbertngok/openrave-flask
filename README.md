# OpenRave Docker

## Usage
```
docker pull osbertngok/openrave
docker run -it osbertngok/openrave openrave.py --example hanoi
```

To recreate the docker image, simply run
```
docker build -t openrave ./docker/openrave
```

# Python RESTful API for OpenRave Scene Management

## Usage and Requirements:

To recreate the docker image, simply run
```
docker build -t openrave-flask ./docker/openrave-flask
```

### Method 1: Local
* localhost:27017 mongo for storage (`docker pull mongo:latest && docker run -p 27017:27017 -t openrave_mongo mongo` would suffice
* require python2 / flask
* python ./docker/openrave-flask/python-restful-api/tests/scenemanagement_tests.py

### Method 2: Docker
* docker-compose up -d
* ./scripts/unittest.sh

## Examples:

### get a list of stored scenes:

```
curl http://localhost:5000/scenes
```

### remove all stored scenes (only available in test environment):
```
curl -X DELETE http://localhost:5000/scenes
```

### upload a scene:
```
curl -F "file=@/path/to/scene_file" http://localhost:5000/scenes
```

### get meta data of a scene
```
curl http://localhost:5000/scenes/<scene_file_name>
```

### delete a scene
```
curl -X DELETE http://localhost:5000/scenes/<scene_file_name>
```



