"""This module contains the test cases for the KNN module."""
import unittest

import pandas as pd
import numpy as np

from chemfusekit.knn import KNNSettings, KNN
from chemfusekit.df import DFSettings, DF, DFDataModel, Table


class TestKNN(unittest.TestCase):
    """Test suite for the KNN module."""

    def test_knn_settings(self):
        """Test case against settings errors."""

        # n_neighbors parameter
        with self.assertRaises(ValueError):
            KNNSettings(n_neighbors=-3)  # Negative value
        with self.assertRaises(ValueError):
            KNNSettings(n_neighbors=0)  # Zero value
        KNNSettings(n_neighbors=7)  # Correct value (shouldn't raise anything)

        # metric parameter
        with self.assertRaises(ValueError):
            KNNSettings(metric='invalid attribute')  # Non-existent technique
        with self.assertRaises(TypeError):
            value = 3
            KNNSettings(metric=value)  # Non-callable

        for x in ['minkwoski', 'precomputed', 'euclidean']:
            KNNSettings(metric=x)  # Correct values (shouldn't raise anything)
        x = lambda a: a + 10
        KNNSettings(metric=x)  # Pass a callable (shouldn't raise anything)

        # weights parameter
        with self.assertRaises(ValueError):
            KNNSettings(weights='invalid attribute')  # Non-existent technique
        with self.assertRaises(TypeError):
            value = 3
            KNNSettings(weights=value)  # Non-callable

        for x in ['uniform', 'distance']:  # Correct values (shouldn't raise anything)
            KNNSettings(weights=x)
        x = lambda a: a + 10
        KNNSettings(weights=x)  # Pass a callable (shouldn't raise anything)

        # algorithm parameter
        with self.assertRaises(ValueError):
            KNNSettings(algorithm='invalid attribute')  # Non-existent technique
        for x in ['auto', 'ball_tree', 'kd_tree', 'brute']:
            KNNSettings(algorithm=x)  # Correct values (shouldn't raise anything)

        # output parameter
        with self.assertRaises(TypeError):
            KNNSettings(output=3)  # Wrong type (not a GraphMode enum)

        # test_split parameter
        with self.assertRaises(TypeError):
            KNNSettings(test_split=3)  # Wrong type (not a bool)

        # output and test_split incompatibilities
        with self.assertRaises(Warning):
            KNNSettings(output='none', test_split=True)

    def test_knn_constructor(self):
        """Test case against constructor errors."""
        # Perform preliminary data fusion
        df_settings = DFSettings(output='none')
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
        df = DF(df_settings, [table1, table2])
        df.fuse()

        # settings parameter
        wrong_settings = DFDataModel(pd.DataFrame([1]), pd.DataFrame([1]), np.asarray([1]), [])
        with self.assertRaises(TypeError):
            KNN(wrong_settings, df.fused_data)  # pass an object of the wrong class as settings

        # fused_data parameter
        knn_settings = KNNSettings()
        wrong_fused_data = df_settings
        with self.assertRaises(TypeError):
            KNN(knn_settings, wrong_fused_data)  # pass an object of the wrong class as fused_data

    def test_knn(self):
        """Integration test case for the training function."""
        # Perform preliminary data fusion
        df_settings = DFSettings(output='none')
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
        df = DF(df_settings, [table1, table2])
        df.fuse()

        # Set up and run KNN (no output)
        knn_settings = KNNSettings()
        knn = KNN(knn_settings, df.fused_data)
        knn.train()

        # With graph output
        knn_settings = KNNSettings(output='graphical')
        knn = KNN(knn_settings, df.fused_data)
        knn.train()

        # With text output
        knn_settings = KNNSettings(output='text')
        knn = KNN(knn_settings, df.fused_data)
        knn.train()

    def test_prediction(self):
        """Test case against prediction parameter issues."""
        # Perform preliminary data fusion
        df_settings = DFSettings(output='none')
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
        df = DF(df_settings, [table1, table2])
        df.fuse()

        # Set up KNN without training it
        knn_settings = KNNSettings()
        knn = KNN(knn_settings, df.fused_data)

        # Pick a random sample for prediction
        x_data_sample = df.fused_data.x_train.iloc[119]  # should be DMMP
        x_data_sample = x_data_sample.iloc[1:].to_frame().transpose()

        # Run prediction with untrained model (should throw exception)
        with self.assertRaises(RuntimeError):
            knn.predict(x_data_sample)

        # Run training
        knn.train()

        # Run prediction with empty data (should throw exception)
        with self.assertRaises(TypeError):
            knn.predict(None)

        # Run prediction with trained model and non-null data
        knn.predict(x_data_sample)
