'''This module contains the test cases for the LR module.'''
import unittest

import numpy as np
import pandas as pd

from chemfusekit.lldf import LLDFSettings, LLDF, Table
from chemfusekit.pca import PCASettings, PCA
from chemfusekit.lr import LRSettings, LR, GraphMode

class TestLR(unittest.TestCase):
    '''Test suite for the LR module.'''

    def test_lr_settings(self):
        '''Test case against settings input errors.'''
        # Should raise an exception when the algorithm is not available
        with self.assertRaises(ValueError):
            LRSettings(
                algorithm='unknown',
                output=GraphMode.NONE,
                test_split=True
            )

        # Should raise an exception when any of the inputs is a null value
        with self.assertRaises(TypeError):
            LRSettings(
                algorithm=None,
                output=GraphMode.NONE,
                test_split=True
            )
        with self.assertRaises(TypeError):
            LRSettings(
                algorithm='liblinear',
                output=None,
                test_split=True
            ) 
        with self.assertRaises(TypeError):
            LRSettings(
                algorithm='liblinear',
                output=GraphMode.NONE,
                test_split=None
            )
        
        # Check if split tests with no output cause warnings:
        with self.assertRaises(Warning):
            LRSettings(output=GraphMode.NONE, test_split=True)

        # Should not raise any exception when the input is correct
        LRSettings(
            algorithm='liblinear',
            output=GraphMode.TEXT
        )

    def test_lr_constructor(self):
        '''Test case against constructor input errors.'''
        # Should raise an exception when the inputs are null
        with self.assertRaises(TypeError):
            LR(
                settings=None,
                array_scores=np.asarray([21.0, 3.44, 7.65]),
                y=np.asarray([7.854, 1.543, 93.55])
            )
        with self.assertRaises(TypeError):
            LR(
                settings=LRSettings(),
                array_scores=None,
                y=np.asarray([7.854, 1.543, 93.55])
            )
        with self.assertRaises(TypeError):
            LR(
                settings=LRSettings(),
                array_scores=np.asarray([21.0, 3.44, 7.65]),
                y=None
            )

        # Should not raise any exception when all inputs are valid
        LR(
            settings=LRSettings(),
            array_scores=np.asarray([21.0, 3.44, 7.65]),
            y=np.asarray([7.854, 1.543, 93.55])
        )

    def test_lr(self):
        '''Integration test case for LR training.'''
        # Perform preliminary data fusion
        lldf_settings = LLDFSettings(output=GraphMode.NONE)
        table1 = Table(
            file_path="tests/qepas.xlsx",
            sheet_name="Sheet1",
            preprocessing="snv"
        )
        table2 = Table(
            file_path="tests/rt.xlsx",
            sheet_name="Sheet1",
            preprocessing="none"
        )
        lldf = LLDF([table1, table2], lldf_settings)
        lldf.lldf()

        pca_settings = PCASettings()
        pca = PCA(lldf.fused_data, pca_settings)
        pca.pca()
        pca.pca_stats()

        # With no output
        lr_settings = LRSettings()
        lr = LR(lr_settings, pca.array_scores, lldf.fused_data.y)
        lr.lr()

        # With text output
        lr_settings = LRSettings(output=GraphMode.TEXT)
        lr = LR(lr_settings, pca.array_scores, lldf.fused_data.y)
        lr.lr()

        # With graph output
        # With text output
        lr_settings = LRSettings(output=GraphMode.GRAPHIC)
        lr = LR(lr_settings, pca.array_scores, lldf.fused_data.y)
        lr.lr()

        # With text output and split tests
        lr_settings = LRSettings(output=GraphMode.TEXT, test_split=True)
        lr = LR(lr_settings, pca.array_scores, lldf.fused_data.y)
        lr.lr()

        # With graph output and split tests
        lr_settings = LRSettings(output=GraphMode.GRAPHIC, test_split=True)
        lr = LR(lr_settings, pca.array_scores, lldf.fused_data.y)
        lr.lr()

    def test_lr_predict(self):
        '''Test case against prediction input errors.'''
        # Set up the model
        lr_settings = LRSettings()
        lr = LR(lr_settings, np.asarray([7.02, 8.11]), np.asarray([43.1, 0.06]))

        # Shold raise an exception when started with no data
        with self.assertRaises(TypeError):
            lr.predict(None)

        # Should raise an exception when started with no training
        with self.assertRaises(RuntimeError):
            lr.predict(pd.DataFrame([4.03, 3.14]))
