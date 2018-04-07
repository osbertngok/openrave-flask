docker exec -t -e "UPLOAD_FOLDER=/opt/openrave-flask/test-upload" -e "MONGO_CONNECTION_STRING=mongodb://mongo:27017/" or_flask python /python-restful-api/tests/scenemanagement_tests.py
