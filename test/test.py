import sys
sys.path.append("../")

import unittest
from core import Parser, Process

test1_region_result = [[1, 1200, 1300],
                       [1, 1500, 1550],
                       [1, 8000, 8200],
                       [2, 8100, 8300],
                       [3, 8100, 8300],
                       [4, 8150, 8350],]

test1_segments_result = [[1, 1200, 1299], 
                         [1, 1500, 1549], 
                         [1, 8000, 8099], 
                         [3, 8100, 8149], 
                         [4, 8150, 8199], 
                         [3, 8200, 8299], 
                         [1, 8300, 8349],]

test2_region_result = [[1, 20500, 20700],
                       [2, 20400, 20900],
                       [1, 21200, 21500],
                       [2, 21300, 21700],
                       [3, 21300, 21700],
                       [1, 22000, 22100],
                       [1, 22100, 22200],
                       [1, 22200, 22300],
                       [2, 22299, 22400],
                       [1, 22399, 22450],
                       [4, 20000, 23000],]

test2_segments_result = [[1, 20000, 20399],
                         [2, 20400, 20499],
                         [3, 20500, 20699],
                         [2, 20700, 20899],
                         [1, 20900, 21199],
                         [2, 21200, 21299],
                         [4, 21300, 21499],
                         [3, 21500, 21699],
                         [1, 21700, 21999],
                         [2, 22000, 22099],
                         [2, 22100, 22199],
                         [2, 22200, 22298],
                         [3, 22299, 22299],
                         [2, 22300, 22398],
                         [3, 22399, 22399],
                         [2, 22400, 22449],
                         [1, 22450, 22999],]

class TestMetadata(unittest.TestCase):
    """Test data format and quality inputs as application required to work properly"""

    @classmethod
    def setUpClass(self):
        """Create regions and segments for later use in the tests"""

        self.parser_large = Parser("../Regions_Large.txt")
        self.parser_small = Parser("../Regions_Small.txt")

        self.test1 = Parser("test1.txt")
        self.test1_process = Process(self.test1.regions, self.test1.segments)
        self.test1_process.part1_task()
        self.test1_process.part2_task()

        self.test2 = Parser("test2.txt")
        self.test2_process = Process(self.test2.regions, self.test2.segments)
        self.test2_process.part1_task()
        self.test2_process.part2_task()

    def test_one_direction(self):
        """Test if stop is always greater than start coordinate"""
        for region in self.parser_large.regions:
            self.assertGreaterEqual(region.stop, region.start)
        for region in self.parser_small.regions:
            self.assertGreaterEqual(region.stop, region.start)
    
    def test_levels(self):
        """Test region Y-axis level assignation"""
        self.assertEqual(self.test1_process.to_list(self.test1_process.regions), test1_region_result)
        self.assertEqual(self.test2_process.to_list(self.test2_process.regions), test2_region_result) 

    def test_segments_count(self):
        """Test non-overlapping segments count"""
        self.assertEqual(self.test1_process.to_list(self.test1_process.segments), test1_segments_result)
        self.assertEqual(self.test2_process.to_list(self.test2_process.segments), test2_segments_result)


if __name__ == "__main__":
    unittest.main()
