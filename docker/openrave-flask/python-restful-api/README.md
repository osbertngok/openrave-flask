# Python RESTful API for OpenRave Scene Management

## Requirements

* localhost:27017 mongo for storage (`docker pull mongo:latest && docker run -p 27017:27017 -t openrave_mongo mongo` would suffice
* require python3 / flask

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
curl -F "file=@/path/to/scene_file" http://localhost:5000/scene
```

### get meta data of a scene
```
curl http://localhost:5000/scene/<scene_file_name>
```

### delete a scene
```
curl -X DELETE http://localhost:5000/scene/<scene_file_name>
```

