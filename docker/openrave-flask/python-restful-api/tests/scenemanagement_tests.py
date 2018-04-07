import sys, os, io
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from os import listdir
from os.path import isfile, join

from scenemanagement import factory
import unittest


class OpenRaveTestCase(unittest.TestCase):

    def setUp(self):
        config = {
          "DATABASE": 'openrave_test',
          "TESTING": True,
          "UPLOAD_FOLDER": os.getenv('UPLOAD_FOLDER', "/opt/openrave-flask/test-upload"),
          "MONGO_CONNECTION_STRING": os.getenv('MONGO_CONNECTION_STRING', "mongodb://localhost:27017/")
        }
        app = factory.create_app(config)
        self.app = app
        self.client= app.test_client()

    def tearDown(self):
        UPLOAD_FOLDER = self.app.config['UPLOAD_FOLDER']
        for f in listdir(UPLOAD_FOLDER):
            if isfile(join(UPLOAD_FOLDER, f)):
                os.remove(join(UPLOAD_FOLDER, f))
        rv = self.client.delete('/scenes')
        assert 200 == rv.status_code
        assert b'{"success": true}' in rv.data

    def test_non_existent_path(self):
        rv = self.client.get('/')
        assert 404 == rv.status_code

    def test_upload(self):
        data = dict(
          file=(io.BytesIO(b'{"a": "b"}'), "test_file_1"),
        )

        rv = self.client.post('/scenes', content_type='multipart/form-data', data=data)
        assert 200 == rv.status_code
        assert b'{"success": true, "filename": "test_file_1"}' in rv.data

    def test_empty_collection(self):
        rv = self.client.get('/scenes')
        assert 200 == rv.status_code
        assert b'[]' in rv.data


if __name__ == '__main__':
    unittest.main()

