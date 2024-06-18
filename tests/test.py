import unittest
import json

import sys
sys.path.append('app/')

from run import app


class MainTest(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    # test home #
    def test_home(self):
        """ Test Home will ho to home page of the flask API and check if the home str equals
        the content of the home page """

        response = self.client.get("/cluster_status")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()