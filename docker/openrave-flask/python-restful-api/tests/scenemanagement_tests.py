import sys, os, io
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from os.path import join
import json

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
        rv = self.client.delete('/scenes')
        assert 200 == rv.status_code
        assert b'{"success": true}' in rv.data

    def test_non_existent_path(self):
        rv = self.client.get('/')
        assert 404 == rv.status_code

    def test_upload(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        hanoi_file_path = join(dir_path, 'test_files/hanoi.env.xml')
        in_file = open(hanoi_file_path, "rb")  # opening for [r]eading as [b]inary
        bin_data = in_file.read()
        data = dict(
          file=(io.BytesIO(bin_data), "hanoi.env.xml"),
        )

        rv = self.client.post('/scenes', content_type='multipart/form-data', data=data)
        assert 200 == rv.status_code
        assert b'{"success": true, "filename": "hanoi.env.xml"}' in rv.data

        rv = self.client.get('/scenes/hanoi.env.xml')
        assert 200 == rv.status_code
        ret = rv.data.decode("utf-8")
        dic = json.loads(ret)
        assert len(dic['bodies']) == 9

    def test_duplicate_upload(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        hanoi_file_path = join(dir_path, 'test_files/hanoi.env.xml')
        in_file = open(hanoi_file_path, "rb")  # opening for [r]eading as [b]inary
        bin_data = in_file.read()
        data = dict(
          file=(io.BytesIO(bin_data), "hanoi.env.xml"),
        )

        rv = self.client.post('/scenes', content_type='multipart/form-data', data=data)
        assert 200 == rv.status_code
        assert b'{"success": true, "filename": "hanoi.env.xml"}' in rv.data

        data = dict(
            file=(io.BytesIO(bin_data), "hanoi.env.xml"),
        )

        rv = self.client.post('/scenes', content_type='multipart/form-data', data=data)
        assert 400 == rv.status_code
        assert b'{"success": false, "error": "file already exists"}' in rv.data

    def test_get_data(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        hanoi_file_path = join(dir_path, 'test_files/hanoi.env.xml')
        in_file = open(hanoi_file_path, "rb")  # opening for [r]eading as [b]inary
        bin_data = in_file.read()
        data = dict(
            file=(io.BytesIO(bin_data), "hanoi.env.xml"),
        )

        rv = self.client.post('/scenes', content_type='multipart/form-data', data=data)

        rv = self.client.get('/scenes/hanoi.env.xml')
        assert 200 == rv.status_code
        ret = rv.data.decode("utf-8")
        dic = json.loads(ret)
        assert len(dic['bodies']) == 9
        print(dic['createdDateTime'])
        assert dic['filename'] == 'hanoi.env.xml'
        assert dic['bodies'][0]['is_robot'] is True
        assert dic['bodies'][0]['name'] == 'Puma'

    def test_delete_data(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        hanoi_file_path = join(dir_path, 'test_files/hanoi.env.xml')
        in_file = open(hanoi_file_path, "rb")  # opening for [r]eading as [b]inary
        bin_data = in_file.read()
        data = dict(
            file=(io.BytesIO(bin_data), "hanoi.env.xml"),
        )

        self.client.post('/scenes', content_type='multipart/form-data', data=data)

        rv = self.client.get('/scenes/hanoi.env.xml')
        assert 200 == rv.status_code
        assert 'null' != rv.data.decode('utf-8')
        rv = self.client.delete('/scenes/hanoi.env.xml')
        assert 200 == rv.status_code
        rv = self.client.get('/scenes/hanoi.env.xml')
        assert 200 == rv.status_code
        assert 'null' == rv.data.decode('utf-8')

    def test_empty_collection(self):
        rv = self.client.get('/scenes')
        assert 200 == rv.status_code
        assert b'[]' in rv.data


if __name__ == '__main__':
    unittest.main()

