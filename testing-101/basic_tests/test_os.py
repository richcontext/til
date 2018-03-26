import mock
import unittest
from .file_funcs import rm

class RmTestCase(unittest.TestCase):
    """Code under test:

    import os
    import os.path

    def rm(filename):
        if os.path.isfile(filename):
            os.remove(filename)
    """

    @mock.patch('basic_tests.file_funcs.os.path')
    @mock.patch('basic_tests.file_funcs.os')
    def test_rm(self, mock_os, mock_path):
        # set up the mock
        mock_path.isfile.return_value = False

        rm("any path")

        # test that the remove call was NOT called.
        self.assertFalse(mock_os.remove.called, "Failed to not remove the file if not present.")

        # make the file 'exist'
        mock_path.isfile.return_value = True

        rm("any path")

        mock_os.remove.assert_called_with("any path")
