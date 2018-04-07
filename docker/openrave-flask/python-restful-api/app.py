from .scenemanagement import factory
import os

if __name__ == '__main__':
    config = {
        "UPLOAD_FOLDER": os.getenv('UPLOAD_FOLDER', "/opt/openrave-flask/upload")
    }
    app = factory.create_app(config)
    app.run()
