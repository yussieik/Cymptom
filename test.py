"""
Created on Sat Feb  5 19:02:13 2022.

@author: Yossi Eikelman
"""

import unittest
from dataextractor import ConnectDB
from instance import Instance
import dataclasses


class TestConnectDB(unittest.TestCase):
    """
    Tester for ConnectDB class with fake/incorrect data on 
    Access_key and Secret_Access_key.
    """

    a_k: str = "23fef"
    s_k: str = "fdsfdsfdsfds"
    conn_db = ConnectDB(a_k, s_k)

    def test_no_regions(self):
        """Check if ConnectDB recognizes failure on connecting."""
        with self.assertRaises(Exception) as context:
            self.conn_db.upload_db()

        self.assertTrue('regions' in str(context.exception))

    def test_db_empty(self):
        """Check if ConnectDB is empty on uploaded database."""
        with self.assertRaises(Exception) as context:
            self.conn_db.get_db

        self.assertTrue('No data in Database' in str(context.exception))

    def test_getdf(self):
        """Check if ConnectDB return None on empty dataframe."""
        with self.assertRaises(Exception) as context:
            self.conn_db.get_df

        self.assertTrue(
            'No data in Processed data in DB' in str(context.exception))


class TestInstance(unittest.TestCase):
    """
    Tester for Instance class.
    """
    instance_test_0 = Instance('test_instance', {'Test Key': 'value'})

    def test_equal_instances(self):
        """Check if TestInstance comparison-trully equal."""
        instance_test_1 = Instance('test_instance', {'Test Key': 'value'})
        self.assertEqual(self.instance_test_0, instance_test_1)

    def test_unequal_instances(self):
        """Check if TestInstance comparison-falsly equal."""
        instance_test_1 = Instance(
            'test_instance', {'Test Key': 'different value'})
        self.assertNotEqual(self.instance_test_0, instance_test_1)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
