import os.path
import unittest

import analysis

TEST_OUT = "test_outputs"
SB_FILE = os.path.join("test_data","sb_analysis_test.csv")

# class TestStringMethods(unittest.TestCase):
#     def test_draw_basic_stats_lineplot(self):
#         analysis.draw_basic_stats_lineplot(TEST_OUT, 'test1', SB_FILE, None)
#         file1 = os.path.join(TEST_OUT, "fig_lineplot_test1_None.png")
#         assert(os.path.isfile(file1))
#         analysis.draw_basic_stats_lineplot(TEST_OUT, 'test2', SB_FILE, 5)
#         file2 = os.path.join(TEST_OUT, "fig_lineplot_test2_5.png")
#         assert(os.path.isfile(file2))
#
#
# if __name__ == '__main__':
#     unittest.main()