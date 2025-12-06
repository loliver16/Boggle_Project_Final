import unittest
import sys
import os
from boggle_solver import Boggle

# Add current directory to path to find boggle_solver.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestSuite_Alg_Scalability_Cases(unittest.TestCase):
    """
    Tests 3x3 grid
    Expected Output: ["abc", "abdhj", "cfj", "dea"]
    """

    def test_Normal_case_3x3(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "J"]]
        dictionary = ["abc", "abdhj", "abi", "ef", "cfj", "dea"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]
        expected = ["abc", "abdhj", "cfj", "dea"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests 4x4 grid
  Expected Output: ["abc", "abcd", "efg", "dhlp", "cfknop"]
  """

    def test_Normal_case_4x4(self):
        grid = [
            ["A", "B", "C", "D"],
            ["E", "F", "G", "H"],
            ["R", "J", "K", "L"],
            ["M", "N", "O", "P"],
        ]
        dictionary = [
            "abc",
            "abcd",
            "abdh",
            "ab",
            "dhlp",
            "efg",
            "cfkm",
            "dea",
            "aek",
            "cfknop",
        ]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]
        expected = ["abc", "abcd", "efg", "dhlp", "cfknop"]
        expected = [x.upper() for x in expected]
        solution = sorted(solution)
        expected = sorted(expected)
        self.assertEqual(expected, solution)

    """
  Tests 5x5 grid
  Expected Output: ["ABC", "FGHZJ", "BHNT"]
  """

    def test_Normal_case_5x5(self):
        grid = [
            ["A", "B", "C", "D", "E"],
            ["F", "G", "H", "Z", "J"],
            ["K", "L", "M", "N", "O"],
            ["P", "Qu", "R", "St", "T"],
            ["U", "V", "W", "X", "Y"],
        ]
        dictionary = ["abc", "mnop", "fghzj", "bhnt", "klru", "cfzl", "xyz"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]
        expected = ["ABC", "FGHZJ", "BHNT"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests 6x6 grid with medium dictionary
  Expected Output: ["ABC", "GHIEJ", "YZAB", "VBH", "EZAVWR"]
  """

    def test_6x6_grid_mediumDictionary(self):
        grid = [
            ["A", "B", "C", "D", "E", "F"],
            ["G", "H", "Ie", "J", "K", "L"],
            ["M", "N", "O", "P", "Qu", "R"],
            ["St", "T", "U", "V", "W", "X"],
            ["Y", "Z", "A", "B", "C", "D"],
            ["E", "F", "G", "H", "Ie", "J"],
        ]
        dictionary = ["abc", "ghiej", "ago", "vbh", "stuv", "yzab", "ezavwr"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["ABC", "GHIEJ", "YZAB", "VBH", "EZAVWR"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    def test_Normal_case_10x10_with_Special_Tiles(self):
        grid = [
            ["A", "B", "C", "D", "E", "F", "G", "H", "Ie", "J"],
            ["K", "L", "M", "N", "O", "P", "Qu", "R", "St", "T"],
            ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D"],
            ["E", "F", "G", "H", "Ie", "J", "K", "L", "M", "N"],
            ["O", "P", "Qu", "R", "St", "T", "U", "V", "W", "X"],
            ["Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H"],
            ["Ie", "J", "K", "L", "M", "N", "O", "P", "Qu", "R"],
            ["St", "T", "U", "V", "W", "X", "Y", "Z", "A", "B"],
            ["C", "D", "E", "F", "G", "H", "Ie", "J", "K", "L"],
            ["M", "N", "O", "P", "Qu", "R", "St", "T", "U", "V"],
        ]

        # Dictionary includes words that require Qu, St, and Ie
        dictionary = [
            "ABCIe",
            "QuR",
            "StTUV",
            "NOPQu",
            "IeJK",
        ]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]
        expected = ["QUR", "StTUV", "NOPQu", "IeJK"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests 12x12 grid
  Expected Output: ["ABC", "STTUVWX", "YZAB", "KLMNOP", "XYZ", "ABCDEF"]
  """

    def test_Normal_case_12x12(self):
        grid = [
            ["A", "B", "C", "D", "E", "F", "G", "H", "Ie", "J", "K", "L"],
            ["M", "N", "O", "P", "Qu", "R", "St", "T", "U", "V", "W", "X"],
            ["Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H", "Ie", "J"],
            ["K", "L", "M", "N", "O", "P", "Qu", "R", "St", "T", "U", "V"],
            ["W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H"],
            ["Ie", "J", "K", "L", "M", "N", "O", "P", "Qu", "R", "St", "T"],
            ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F"],
            ["G", "H", "Ie", "J", "K", "L", "M", "N", "O", "P", "Qu", "R"],
            ["St", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D"],
            ["E", "F", "G", "H", "Ie", "J", "K", "L", "M", "N", "O", "P"],
            ["Qu", "R", "St", "T", "U", "V", "W", "X", "Y", "Z", "A", "B"],
            ["C", "D", "E", "F", "G", "H", "Ie", "J", "K", "L", "M", "N"],
        ]

        dictionary = [
            "abc",
            "sttuvwx",
            "yzab",
            "klmnop",
            "xyz",
            "abcdef",
            "notaword",
            "pqurs",
        ]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]
        expected = ["ABC", "STTUVWX", "YZAB", "KLMNOP", "XYZ", "ABCDEF"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests 13x13 normal grid with small dictionary with
  valid words of small length
  Expected Output: ["ABC", "NOP", "GHIEJK"]
  """

    def test_Normal_case_13x13(self):
        grid = [
            [
              "A", "B", "C", "D", "E", "F", "G",
              "H", "Ie", "J", "K", "L", "M"
            ],
            [
              "N", "O", "P", "Qu", "R", "St",
              "T", "U", "V", "W", "X", "Y", "Z"
            ],
            [
              "A", "B", "C", "D", "E", "F", "G",
              "H", "Ie", "J", "K", "L", "M"
            ],
            [
              "N", "O", "P", "Qu", "R", "St", "T",
              "U", "V", "W", "X", "Y", "Z"
            ],
            [
              "A", "B", "C", "D", "E", "F", "G",
              "H", "Ie", "J", "K", "L", "M"
            ],
            [
              "N", "O", "P", "Qu", "R", "St", "T",
              "U", "V", "W", "X", "Y", "Z"
            ],
            [
              "A", "B", "C", "D", "E", "F", "G",
              "H", "Ie", "J", "K", "L", "M"
            ],
            [
              "N", "O", "P", "Qu", "R", "St", "T",
              "U", "V", "W", "X", "Y", "Z"
            ],
            [
              "A", "B", "C", "D", "E", "F", "G", "H",
              "Ie", "J", "K", "L", "M"
            ],
            [
              "N", "O", "P", "Qu", "R", "St",
              "T", "U", "V", "W", "X", "Y", "Z"
            ],
            [
              "A", "B", "C", "D", "E", "F", "G",
              "H", "Ie", "J", "K", "L", "M"
            ],
            [
              "N", "O", "P", "Qu", "R", "St",
              "T", "U", "V", "W", "X", "Y", "Z"
            ],
            [
              "A", "B", "C", "D", "E", "F", "G",
              "H", "Ie", "J", "K", "L", "M"
            ],
        ]
        dictionary = ["ABC", "NOP", "APQU", "MNO", "XAT", "GHIEJK"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["ABC", "NOP", "GHIEJK"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))


class TestSuite_Simple_Edge_Cases(unittest.TestCase):
    """
    Tests 1x1 grid
    Expected Output: []
    """

    def test_SquareGrid_case_1x1(self):
        grid = [["A"]]
        dictionary = ["a", "b", "c"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests an empty grid with one row, and a dictionary with values
  Expected Output: []
  """

    def test_EmptyGrid_case_0x0(self):
        grid = [[]]
        dictionary = ["hello", "there", "general", "kenobi"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        solution = [x.upper() for x in solution]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests when grid is empty (no rows) but dictionary has values
  Expected Output: []
  """

    def test_EmptyGrid_nonEmptyDictionary(self):
        grid = []
        dictionary = ["WORD", "PYTHON", "GRID"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests 1x1 grid
  Expected Output: [] (because solution must have 3 letters)
  """

    def test_1x1_grid_noValidWords(self):
        grid = [["A"]]
        dictionary = ["A", "B", "C"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests a grid that isn't NxN
  Expected Output: []
  """

    def test_NonSquare_3x5_grid(self):
        grid = [
            ["A", "B", "C", "D", "E"],
            ["F", "G", "H", "Ie", "J"],
            ["K", "L", "M", "N", "O"],
        ]
        dictionary = ["ABC", "FGH", "KLM", "GHI", "EJO"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests dictionary with mixed case values
  Expected Output: ["DOG", "CAT", "RAT", "TOE"]
  """

    def test_MixedCaseDictionary(self):
        grid = [
            ["D", "O", "G", "P"],
            ["C", "A", "T", "L"],
            ["M", "O", "U", "M"],
            ["E", "R", "A", "T"],
        ]
        dictionary = ["Dog", "cat", "MOUSE", "rat", "TOE"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["DOG", "CAT", "RAT", "TOE"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

        """
    Tests for and doesn't inlcude words shorter than 3 letters
    Expected Output: ["ABC", "DEF", "GHI"]
    """

        def test_Words_Shorter_Than_Three_Not_Included(self):
            grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "Ie"]]
            dictionary = ["A", "AB", "ABC", "DEF", "HIe", "GHIe"]
            mygame = Boggle(grid, dictionary)
            solution = mygame.getSolution()
            solution = [x.upper() for x in solution]
            expected = ["ABC", "DEF", "GHIe"]
            expected = [x.upper() for x in expected]
            self.assertEqual(sorted(solution), sorted(expected))

        """
    Tests for valid words only when letter are adjacent (no skipping tiles)
    Expected Output: ["ADG", "CEG"]
    """

        def test_NonAdjacent_Letters_Not_Valid(self):
            grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "Ie"]]
            dictionary = ["AFIe", "CEG", "BGH", "ADG"]
            mygame = Boggle(grid, dictionary)
            solution = mygame.getSolution()
            solution = [x.upper() for x in solution]
            expected = ["ADG", "CEG"]
            expected = [x.upper() for x in expected]
            self.assertEqual(sorted(solution), sorted(expected))


class TestSuite_Complete_Coverage(unittest.TestCase):
    """
    Tests grid with Qu and Ie that create words with diagonal connections
    Expected Output: ["QUAB", "IEBC", "ABCD"]
    """

    def test_Mixed_Special_Tiles_Diagonal(self):
        grid = [
            ["Qu", "B", "St", "O"],
            ["Ie", "A", "C", "D"],
            ["E", "F", "G", "H"],
            ["J", "K", "L", "Ie"],
        ]
        dictionary = ["QUAB", "IEBC", "ABCD", "EFODH"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["QUAB", "IEBC", "ABCD"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests grid when dictionary requires words formed through
  complex movements (diagonal, backwards, upwards).
  Expected Output: ["AEIE", "CEG", "BFHD"]
  """

    def test_Zigzag_Moves(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "Ie"]]
        dictionary = ["AEIE", "CEG", "ACD", "BFHD", "IAE"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["AEIE", "CEG", "BFHD"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests when dictionary has word that requires a tile to be reused.
  Expected Output: []
  """

    def test_Reusing_Same_Tile_Disallowed(self):
        grid = [["A", "A"], ["B", "C"]]
        dictionary = ["AAA"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertNotIn("AAA", solution)


class TestSuite_Qu_and_St(unittest.TestCase):
    """
    Tests grid with qu tile
    Expected Output: ["QUAT", "QUAD", "BAT"]
    """

    def test_Grid_with_Qu(self):
        grid = [
            ["Qu", "A", "T", "E"],
            ["B", "C", "D", "E"],
            ["F", "G", "H", "Ie"],
            ["J", "K", "L", "M"],
        ]
        dictionary = ["QUAT", "QUAD", "BAT", "FAT", "LATE"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["QUAT", "QUAD", "BAT"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests grid with St tile
  Expected Output: ["START", "STAB", "STAR", "BAD"]
  """

    def test_Grid_with_St(self):
        grid = [
            ["St", "A", "R", "T"],
            ["B", "C", "D", "E"],
            ["F", "G", "H", "Ie"],
            ["J", "K", "L", "M"],
        ]
        dictionary = ["START", "STAB", "MID", "STAR", "BAD", "TEA"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["START", "STAB", "STAR", "BAD"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests grid with Qu and St
  Expected Output: ["QUAST", "QUAD", "STAB", "LIE"]
  """

    def test_Grid_with_Qu_and_St(self):
        grid = [
            ["Qu", "A", "St", "F"],
            ["B", "C", "D", "E"],
            ["F", "G", "H", "Ie"],
            ["J", "K", "L", "M"],
        ]
        dictionary = ["QUAST", "QUAD", "STAB", "STAR", "BAT", "LIB", "LIE"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["QUAST", "QUAD", "STAB", "LIE"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests grid with raw q tile
  Expected Output: []
  """

    def test_Grid_with_Raw_Q(self):
        grid = [
            ["Q", "A", "B", "C"],
            ["D", "E", "F", "G"],
            ["H", "I", "J", "K"],
            ["L", "M", "N", "O"],
        ]
        dictionary = ["QAB", "QEF", "HIJ"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests grid with raw S tile
  Expected Output: []
  """

    def test_Grid_with_Raw_S(self):
        grid = [
            ["S", "A", "R", "T"],
            ["B", "C", "D", "E"],
            ["F", "G", "H", "Ie"],
            ["J", "K", "L", "M"],
        ]
        dictionary = ["SAR", "CHIE", "BCDE"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))


class TestSuite_Ie(unittest.TestCase):
    """
    Tests grid with Ie tile
    Expected Output: ["IEAD", "IEFG"]
    """

    def test_Grid_with_Ie_tile(self):
        # Valid case: "Ie" counts as 2 letters
        grid = [
            ["Ie", "A", "B", "C"],
            ["D", "E", "F", "G"],
            ["H", "Ie", "J", "K"],
            ["L", "M", "N", "O"],
        ]
        dictionary = ["IEAD", "IEFG", "HIJ", "MID"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = ["IEAD", "IEFG"]
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))

    """
  Tests grid with raw I tile
  Expected Output: []
  """

    def test_Grid_with_Raw_I(self):
        grid = [
            ["I", "A", "B", "C"],
            ["D", "E", "F", "G"],
            ["H", "Ie", "J", "K"],
            ["L", "M", "N", "O"],
        ]
        dictionary = ["IAD", "IEFG", "HIJ"]
        mygame = Boggle(grid, dictionary)
        solution = [x.upper() for x in mygame.getSolution()]
        expected = []
        expected = [x.upper() for x in expected]
        self.assertEqual(sorted(expected), sorted(solution))


if __name__ == "__main__":
    unittest.main()


# Used ChatGPT to generate test cases based on
# the test frames, constraints, and function descriptions.
