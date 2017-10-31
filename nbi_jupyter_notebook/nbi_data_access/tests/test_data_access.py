import unittest, sys, _io
sys.path.append("..")
from nbi.DataStore import ErdaShare, IDMCShare


class ErdaShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        # Open connection to a sharelink
        self.share = ErdaShare('jg6pkLQJse')

    def tearDown(self):
        pass

    def test_share(self):
        # ERDA Sharelink example
        print("ERDA")
        # List files/dirs in share
        self.assertIn('tmp', self.share.list())
        # Read file directly as string
        self.assertEqual(self.share.read('tmp'), 'sddsfsf')
        # Read file directly as binary
        self.assertEqual(self.share.read_binary('tmp'), b'sddsfsf')

        # Get a _io.TextIOWrapper object with automatic close
        with self.share.open('tmp', 'r') as tmp:
            self.assertEqual(tmp.read(), 'sddsfsf')

        # Get a default _io.TextIOWrapper object with manual lifetime
        file = self.share.open('tmp', 'r')
        self.assertIsInstance(file, _io.TextIOWrapper)
        self.assertEqual(file.read(), 'sddsfsf')
        file.close()


class IdmcShareTest(unittest.TestCase):
    share = None

    def setUp(self):
        # Open connection to a sharelink
        self.share = IDMCShare('KGDlunrM3w')

    def tearDown(self):
        pass

    def test_share(self):
        # ERDA Sharelink example
        print("IDMC")
        # List files/dirs in share
        self.assertIn('fisk', self.share.list())
        # Read file directly as string
        self.assertEqual(self.share.read('fisk'), 'Torsk')
        # Read file directly as binary
        self.assertEqual(self.share.read_binary('fisk'), b'Torsk')

        # Get a _io.TextIOWrapper object with automatic close
        with self.share.open('fisk', 'r') as tmp:
            self.assertEqual(tmp.read(), 'Torsk')

        # Get a default _io.TextIOWrapper object with manual lifetime
        file = self.share.open('fisk', 'r')
        self.assertIsInstance(file, _io.TextIOWrapper)
        self.assertEqual(file.read(), 'Torsk')
        file.close()


