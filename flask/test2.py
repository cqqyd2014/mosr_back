import os
import test
import unittest
import tempfile
from orm import create_session,SystemPar

class  FlaskTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        self.app=create_app('testing')
        self.app_context=self.app.app_context()
        self.app_context.push()

        self.client=self.app.test_client()

        print("setup")
         

    def tearDown(self):
        print("down")
    
    def test_empty_db(self):
        rv=self.client.get('/')
        assert 'No entries' in rv.data

if __name__=='__main__':
    unittest.main()
