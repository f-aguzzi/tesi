'''This module contains the test cases for the LLDF module.'''
import unittest
from src.lldf import LLDFSettings, LLDF

class TestLLDF(unittest.TestCase):
    '''Test suite for the LLDF module.'''

    def test_file_loading(self):
        '''Test case against file loading errors.'''
        # load a non-existent file on purpose
        settings = LLDFSettings(
            qepas_path='tests/notfound.xlsx',
            qepas_sheet='Sheet1',
            rt_path='tests/rt.xlsx',
            rt_sheet='Sheet1',
            preprocessing='savgol'
        )
        lldf = LLDF(settings)
        self.assertRaises(FileNotFoundError, lldf.lldf)

    def test_preprocessing_techniques(self):
        '''Test case against wrong preprocessing user input.'''
        settings = LLDFSettings(
            qepas_path='src/tests/qepas.xlsx',
            qepas_sheet='Sheet1',
            rt_path='src/tests/rt.xlsx',
            rt_sheet='Sheet1',
            preprocessing='qpl' # test with non-existant preprocessing technique
        )
        lldf = LLDF(settings)
        self.assertRaises(SyntaxError, lldf.lldf)

        # now check if it works with the three real processing techniques:
        lldf.settings.preprocessing='snv'
        lldf.lldf()
        lldf.settings.preprocessing='savgol'
        lldf.lldf()
        lldf.settings.preprocessing='savgol+snv'
        lldf.lldf()

if __name__ == '__main__':
    unittest.main()
