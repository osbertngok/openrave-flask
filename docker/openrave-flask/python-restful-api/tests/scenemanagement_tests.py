import sys, os, io
testdir = os.path.dirname(__file__)
srcdir = '../'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from scenemanagement import factory
import unittest


class OpenRaveTestCase(unittest.TestCase):

    def setUp(self):
        config = {
          "DATABASE": 'openrave_test',
          "TESTING": True
        }
        app = factory.create_app(config)
        self.client= app.test_client()

    def tearDown(self):
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

        rv = self.client.post('/scene', content_type='multipart/form-data', data=data)
        assert 200 == rv.status_code
        print(rv.data)
        assert b'{"success": true, "filename": "test_file_1"}' in rv.data

    def test_empty_collection(self):
        rv = self.client.get('/scenes')
        assert 200 == rv.status_code
        assert b'[]' in rv.data


if __name__ == '__main__':
    unittest.main()

