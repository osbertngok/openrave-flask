from scenemanagement import factory
import os

if __name__ == '__main__':
    config = {
        "UPLOAD_FOLDER": os.getenv('UPLOAD_FOLDER', "/opt/openrave-flask/upload"),
        "MONGO_CONNECTION_STRING": os.getenv('MONGO_CONNECTION_STRING', "mongodb://localhost:27017/")
    }
    app = factory.create_app(config)
    app.run(host='0.0.0.0', port=5000)
