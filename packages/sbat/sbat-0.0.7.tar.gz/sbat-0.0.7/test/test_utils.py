import datetime
import unittest

import sbat.utils as utils


class TestUtils(unittest.TestCase):
    def test_get_filename(self):
        file = "/path/to/my/ngs_file.fasta"
        expected = "ngs_file"
        result = utils.get_filename(file)
        self.assertEqual(result, expected)

        file = "/path/to/my/ngs_file.fasta"
        result = utils.get_filename(file)
        self.assertEqual(result, expected)

        file = "ngs_file"
        result = utils.get_filename(file)
        self.assertEqual(result, expected)

    def test_unique_path(self):
        path = "../data/nonextisting_file.fasta"
        result = utils.unique_path(path)
        self.assertEqual(result, path)

        path = "../data/test_data_nanopore.fasta"
        expected = "../data/test_data_nanopore_1.fasta"
        result = utils.unique_path(path)
        self.assertEqual(result, expected)

    def test_hours_aligned(self):
        bins = utils.hours_aligned(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(2))
        self.assertTrue(len(bins) > 48 and len(bins) <= 50)

        bins = utils.hours_aligned(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(2), interval=10)
        self.assertTrue(len(bins) == 5)

    def test_get_ratio(self):
        n1 = 10000
        n2 = 5000
        expected = 0.5
        result = utils.get_ratio(n1, n2)
        result_rev = utils.get_ratio(n2, n1)

        self.assertEqual(result, expected)
        self.assertEqual(result_rev, expected)

    def test_strand_bias_percentage(self):
        n1 = 10000
        n2 = 8000
        expected = 80
        expected_rev = 80
        result = utils.get_strand_bias_percentage(utils.get_ratio(n1, n2))
        self.assertEqual(result, expected)

    def test_parse_iso_size(self):
        input = "500G"
        expected = 500000000000
        result = utils.parse_iso_size(input)
        self.assertEqual(result, expected)

        input = "500"
        expected = 500
        result = utils.parse_iso_size(input)
        self.assertEqual(result, expected)

        with self.assertRaises(SystemExit):
            utils.parse_iso_size("nonumberhere")

        with self.assertRaises(SystemExit):
            utils.parse_iso_size("")

        with self.assertRaises(SystemExit):
            utils.parse_iso_size("G")

    def test_gc_percentage(self):
        string1 = "CGGGGCCCGC"
        exp1 = 100
        string2 = "ATTATACGTT"
        exp2 = 20

        result1 = utils.gc_percentage(string1)
        result2 = utils.gc_percentage(string2)

        self.assertEqual(result1, exp1)
        self.assertEqual(result2, exp2)

