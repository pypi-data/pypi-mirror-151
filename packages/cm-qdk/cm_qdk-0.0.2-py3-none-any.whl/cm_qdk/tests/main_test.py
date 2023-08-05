import unittest
from cm_qdk.main import CMQDK


class TestCase(unittest.TestCase):
    cm_qdk = CMQDK('localhost', 50505)
    cm_qdk.make_connection()

    def test_zoom(self):
        self.cm_qdk.zoom_app()
        response = self.cm_qdk.get_data()
        return response


if __name__ == '__main__':
    unittest.main()
