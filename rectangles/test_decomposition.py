import unittest

from parameterized import parameterized

from decomposition import Edge, make_rectangles, Rectangle


class DecompositionTest(unittest.TestCase):
    @parameterized.expand([
        ("",
         [Edge(0, 100, 0, 250),
          Edge(0, 100, 50, 100),
          Edge(50, 100, 50, 0),
          Edge(0, 250, 100, 250),
          Edge(100, 250, 100, 200),
          Edge(50, 0, 150, 0),
          Edge(100, 200, 150, 200),
          Edge(150, 200, 150, 0),
        ], [Rectangle(0, 50, 250, 100),
            Rectangle(50, 100, 250, 0),
            Rectangle(100, 150, 200, 0)]),
         ("", [Edge(0, 0, 0, 50),
          Edge(0, 50, 50, 50),
          Edge(50, 50, 50, 100),
          Edge(0, 100, 50, 100),
          Edge(0, 100, 0, 125),
          Edge(0, 125, 25, 125),
          Edge(25, 125, 25, 150),
          Edge(0, 150, 25, 150),
          Edge(0, 150, 0, 175),
          Edge(0, 175, 75, 175),
          Edge(75, 175, 75, 200),
          Edge(25, 200, 75, 200),
          Edge(25, 200, 25, 225),
          Edge(25, 225, 100, 225),
          Edge(100, 175, 100, 225),
          Edge(100, 175, 125, 175),
          Edge(125, 75, 125, 175),
          Edge(75, 75, 125, 75),
          Edge(75, 0, 75, 75),
          Edge(0, 0, 75, 0),
          ], [Rectangle(0, 25, 50, 0),
                Rectangle(0, 25, 125, 100),
                Rectangle(0, 25, 175, 150),
                Rectangle(25, 50, 50, 0),
                Rectangle(25, 50, 175, 100),
                Rectangle(25, 50, 225, 200),
                Rectangle(50, 75, 175, 0),
                Rectangle(50, 75, 225, 200),
                Rectangle(75, 100, 225, 75),
                Rectangle(100, 125, 175, 75)]),
         ("", [Edge(0, 0, 0, 150),
          Edge(0, 150, 150, 150),
          Edge(150, 100, 150, 150),
          Edge(50, 100, 150, 100),
          Edge(50, 50, 50, 100),
          Edge(50, 50, 150, 50),
          Edge(150, 0, 150, 50),
          Edge(0, 0, 150, 0),
          ], [Rectangle(0, 50, 150, 0),
                Rectangle(50, 150, 50, 0),
                Rectangle(50, 150, 150, 100)])
    ])
    def test_make_rectangles(self, name, edges, expected_rectangles):
        rectangles = make_rectangles(edges)

        self.assertItemsEqual(expected_rectangles, rectangles)