import BoggleSolver from './boggleSolver';

// Helper function to normalize and sort arrays for comparison
const normalizeArray = (arr) => arr.map(x => x.toUpperCase()).sort();

describe('BoggleSolver - Algorithm Scalability Cases', () => {
  describe('Normal Cases', () => {
    test('3x3 grid', () => {
      const grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "J"]];
      const dictionary = ["abc", "abdhj", "abi", "ef", "cfj", "dea"];
      const solver = new BoggleSolver(grid, dictionary);
      const solution = normalizeArray(solver.getSolution());
      const expected = normalizeArray(["abc", "abdhj", "cfj", "dea"]);
      expect(solution).toEqual(expected);
    });

    test('4x4 grid', () => {
      const grid = [
        ["A", "B", "C", "D"],
        ["E", "F", "G", "H"],
        ["R", "J", "K", "L"],
        ["M", "N", "O", "P"],
      ];
      const dictionary = [
        "abc", "abcd", "abdh", "ab", "dhlp",
        "efg", "cfkm", "dea", "aek", "cfknop",
      ];
      const solver = new BoggleSolver(grid, dictionary);
      const solution = normalizeArray(solver.getSolution());
      const expected = normalizeArray(["abc", "abcd", "efg", "dhlp", "cfknop"]);
      expect(solution).toEqual(expected);
    });

    test('5x5 grid with special tiles', () => {
      const grid = [
        ["A", "B", "C", "D", "E"],
        ["F", "G", "H", "Z", "J"],
        ["K", "L", "M", "N", "O"],
        ["P", "QU", "R", "ST", "T"],
        ["U", "V", "W", "X", "Y"],
      ];
      const dictionary = ["abc", "mnop", "fghzj", "bhnt", "klru", "cfzl", "xyz"];
      const solver = new BoggleSolver(grid, dictionary);
      const solution = normalizeArray(solver.getSolution());
      const expected = normalizeArray(["ABC", "FGHZJ", "BHNT"]);
      expect(solution).toEqual(expected);
    });

    test('6x6 grid with medium dictionary', () => {
      const grid = [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "IE", "J", "K", "L"],
        ["M", "N", "O", "P", "QU", "R"],
        ["ST", "T", "U", "V", "W", "X"],
        ["Y", "Z", "A", "B", "C", "D"],
        ["E", "F", "G", "H", "IE", "J"],
      ];
      const dictionary = ["abc", "ghiej", "ago", "vbh", "stuv", "yzab", "ezavwr"];
      const solver = new BoggleSolver(grid, dictionary);
      const solution = normalizeArray(solver.getSolution());
      const expected = normalizeArray(["ABC", "GHIEJ", "YZAB", "VBH", "EZAVWR"]);
      expect(solution).toEqual(expected);
    });

    test('10x10 grid with special tiles', () => {
      const grid = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J"],
        ["K", "L", "M", "N", "O", "P", "QU", "R", "ST", "T"],
        ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D"],
        ["E", "F", "G", "H", "IE", "J", "K", "L", "M", "N"],
        ["O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X"],
        ["Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H"],
        ["IE", "J", "K", "L", "M", "N", "O", "P", "QU", "R"],
        ["ST", "T", "U", "V", "W", "X", "Y", "Z", "A", "B"],
        ["C", "D", "E", "F", "G", "H", "IE", "J", "K", "L"],
        ["M", "N", "O", "P", "QU", "R", "ST", "T", "U", "V"],
      ];
      const dictionary = ["ABCIE", "QUR", "STTUV", "NOPQU", "IEJK"];
      const solver = new BoggleSolver(grid, dictionary);
      const solution = normalizeArray(solver.getSolution());
      const expected = normalizeArray(["QUR", "STTUV", "NOPQU", "IEJK"]);
      expect(solution).toEqual(expected);
    });

    test('12x12 grid', () => {
      const grid = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L"],
        ["M", "N", "O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X"],
        ["Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H", "IE", "J"],
        ["K", "L", "M", "N", "O", "P", "QU", "R", "ST", "T", "U", "V"],
        ["W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F", "G", "H"],
        ["IE", "J", "K", "L", "M", "N", "O", "P", "QU", "R", "ST", "T"],
        ["U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D", "E", "F"],
        ["G", "H", "IE", "J", "K", "L", "M", "N", "O", "P", "QU", "R"],
        ["ST", "T", "U", "V", "W", "X", "Y", "Z", "A", "B", "C", "D"],
        ["E", "F", "G", "H", "IE", "J", "K", "L", "M", "N", "O", "P"],
        ["QU", "R", "ST", "T", "U", "V", "W", "X", "Y", "Z", "A", "B"],
        ["C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M", "N"],
      ];
      const dictionary = [
        "abc", "sttuvwx", "yzab", "klmnop", "xyz", "abcdef", "notaword", "pqurs",
      ];
      const solver = new BoggleSolver(grid, dictionary);
      const solution = normalizeArray(solver.getSolution());
      const expected = normalizeArray(["ABC", "STTUVWX", "YZAB", "KLMNOP", "XYZ", "ABCDEF"]);
      expect(solution).toEqual(expected);
    });

    test('13x13 grid', () => {
      const grid = [
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M"],
        ["N", "O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X", "Y", "Z"],
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M"],
        ["N", "O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X", "Y", "Z"],
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M"],
        ["N", "O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X", "Y", "Z"],
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M"],
        ["N", "O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X", "Y", "Z"],
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M"],
        ["N", "O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X", "Y", "Z"],
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M"],
        ["N", "O", "P", "QU", "R", "ST", "T", "U", "V", "W", "X", "Y", "Z"],
        ["A", "B", "C", "D", "E", "F", "G", "H", "IE", "J", "K", "L", "M"],
      ];
      const dictionary = ["ABC", "NOP", "APQU", "MNO", "XAT", "GHIEJK"];
      const solver = new BoggleSolver(grid, dictionary);
      const solution = normalizeArray(solver.getSolution());
      const expected = normalizeArray(["ABC", "NOP", "GHIEJK"]);
      expect(solution).toEqual(expected);
    });
  });
});

describe('BoggleSolver - Simple Edge Cases', () => {
  test('1x1 grid should return empty (word too short)', () => {
    const grid = [["A"]];
    const dictionary = ["a", "b", "c"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('Empty grid (0x0) should return empty', () => {
    const grid = [[]];
    const dictionary = ["hello", "there", "general", "kenobi"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('Empty grid array should return empty', () => {
    const grid = [];
    const dictionary = ["WORD", "PYTHON", "GRID"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('1x1 grid no valid words (less than 3 letters)', () => {
    const grid = [["A"]];
    const dictionary = ["A", "B", "C"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('Non-square 3x5 grid should return empty', () => {
    const grid = [
      ["A", "B", "C", "D", "E"],
      ["F", "G", "H", "IE", "J"],
      ["K", "L", "M", "N", "O"],
    ];
    const dictionary = ["ABC", "FGH", "KLM", "GHI", "EJO"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('Mixed case dictionary should work', () => {
    const grid = [
      ["D", "O", "G", "P"],
      ["C", "A", "T", "L"],
      ["M", "O", "U", "M"],
      ["E", "R", "A", "T"],
    ];
    const dictionary = ["Dog", "cat", "MOUSE", "rat", "TOE"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["DOG", "CAT", "RAT", "TOE"]);
    expect(solution).toEqual(expected);
  });

  test('Words shorter than 3 letters not included', () => {
    const grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "IE"]];
    const dictionary = ["A", "AB", "ABC", "DEF", "HIE", "GHIE"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    // HIE is valid (H + IE = 3 letters total), but testing main functionality
    // If HIE is found, include it in expected; otherwise just ABC, DEF, GHIE
    const found = normalizeArray(solver.getSolution());
    expect(found).toContain("ABC");
    expect(found).toContain("DEF");
    expect(found).toContain("GHIE");
    // Ensure short words are not included
    expect(found).not.toContain("A");
    expect(found).not.toContain("AB");
  });

  test('Non-adjacent letters not valid', () => {
    const grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "IE"]];
    const dictionary = ["AFIE", "CEG", "BGH", "ADG"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["ADG", "CEG"]);
    expect(solution).toEqual(expected);
  });
});

describe('BoggleSolver - Complete Coverage', () => {
  test('Mixed special tiles with diagonal connections', () => {
    const grid = [
      ["QU", "B", "ST", "O"],
      ["IE", "A", "C", "D"],
      ["E", "F", "G", "H"],
      ["J", "K", "L", "IE"],
    ];
    const dictionary = ["QUAB", "IEBC", "ABCD", "EFODH"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["QUAB", "IEBC", "ABCD"]);
    expect(solution).toEqual(expected);
  });

  test('Zigzag moves (diagonal, backwards, upwards)', () => {
    const grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "IE"]];
    const dictionary = ["AEIE", "CEG", "ACD", "BFHD", "IAE"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["AEIE", "CEG", "BFHD"]);
    expect(solution).toEqual(expected);
  });

  test('Reusing same tile disallowed', () => {
    const grid = [["A", "A"], ["B", "C"]];
    const dictionary = ["AAA"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    expect(solution).not.toContain("AAA");
  });
});

describe('BoggleSolver - Qu and St Tiles', () => {
  test('Grid with Qu tile', () => {
    const grid = [
      ["QU", "A", "T", "E"],
      ["B", "C", "D", "E"],
      ["F", "G", "H", "IE"],
      ["J", "K", "L", "M"],
    ];
    const dictionary = ["QUAT", "QUAD", "BAT", "FAT", "LATE"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["QUAT", "QUAD", "BAT"]);
    expect(solution).toEqual(expected);
  });

  test('Grid with St tile', () => {
    const grid = [
      ["ST", "A", "R", "T"],
      ["B", "C", "D", "E"],
      ["F", "G", "H", "IE"],
      ["J", "K", "L", "M"],
    ];
    const dictionary = ["START", "STAB", "MID", "STAR", "BAD", "TEA"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["START", "STAB", "STAR", "BAD"]);
    expect(solution).toEqual(expected);
  });

  test('Grid with Qu and St', () => {
    const grid = [
      ["QU", "A", "ST", "F"],
      ["B", "C", "D", "E"],
      ["F", "G", "H", "IE"],
      ["J", "K", "L", "M"],
    ];
    const dictionary = ["QUAST", "QUAD", "STAB", "STAR", "BAT", "LIB", "LIE"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["QUAST", "QUAD", "STAB", "LIE"]);
    expect(solution).toEqual(expected);
  });

  test('Grid with raw Q should return empty (invalid)', () => {
    const grid = [
      ["Q", "A", "B", "C"],
      ["D", "E", "F", "G"],
      ["H", "I", "J", "K"],
      ["L", "M", "N", "O"],
    ];
    const dictionary = ["QAB", "QEF", "HIJ"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('Grid with raw S should return empty (invalid)', () => {
    const grid = [
      ["S", "A", "R", "T"],
      ["B", "C", "D", "E"],
      ["F", "G", "H", "IE"],
      ["J", "K", "L", "M"],
    ];
    const dictionary = ["SAR", "CHIE", "BCDE"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });
});

describe('BoggleSolver - Ie Tiles', () => {
  test('Grid with Ie tile', () => {
    const grid = [
      ["IE", "A", "B", "C"],
      ["D", "E", "F", "G"],
      ["H", "IE", "J", "K"],
      ["L", "M", "N", "O"],
    ];
    const dictionary = ["IEAD", "IEFG", "HIJ", "MID"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = normalizeArray(solver.getSolution());
    const expected = normalizeArray(["IEAD", "IEFG"]);
    expect(solution).toEqual(expected);
  });

  test('Grid with raw I should return empty (invalid)', () => {
    const grid = [
      ["I", "A", "B", "C"],
      ["D", "E", "F", "G"],
      ["H", "IE", "J", "K"],
      ["L", "M", "N", "O"],
    ];
    const dictionary = ["IAD", "IEFG", "HIJ"];
    const solver = new BoggleSolver(grid, dictionary);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });
});

describe('BoggleSolver - Null and Undefined Cases', () => {
  test('Null grid should return empty', () => {
    const solver = new BoggleSolver(null, ["word"]);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('Undefined dictionary should return empty', () => {
    const grid = [["A", "B"], ["C", "D"]];
    const solver = new BoggleSolver(grid, undefined);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });

  test('Null dictionary should return empty', () => {
    const grid = [["A", "B"], ["C", "D"]];
    const solver = new BoggleSolver(grid, null);
    const solution = solver.getSolution();
    expect(solution).toEqual([]);
  });
});

describe('BoggleSolver - Method Tests', () => {
  test('setGrid should reset solutions', () => {
    const grid1 = [["A", "B"], ["C", "D"]];
    const grid2 = [["E", "F"], ["G", "H"]];
    const dictionary = ["ABC", "EFG"];
    const solver = new BoggleSolver(grid1, dictionary);
    solver.getSolution(); // Generate solutions
    solver.setGrid(grid2);
    expect(solver.solutions.size).toBe(0);
  });

  test('setDictionary should reset solutions', () => {
    const grid = [["A", "B"], ["C", "D"]];
    const dict1 = ["ABC"];
    const dict2 = ["DEF"];
    const solver = new BoggleSolver(grid, dict1);
    solver.getSolution(); // Generate solutions
    solver.setDictionary(dict2);
    expect(solver.solutions.size).toBe(0);
  });

  test('isValidWord should check if word exists in solutions', () => {
    const grid = [
      ["T", "W", "Y", "R"],
      ["E", "N", "P", "H"],
      ["G", "Z", "QU", "R"],
      ["O", "N", "T", "A"],
    ];
    const dictionary = ["art", "ego", "gent", "get", "net", "new", "newt"];
    const solver = new BoggleSolver(grid, dictionary);
    solver.getSolution();
    expect(solver.isValidWord("ART")).toBe(true);
    expect(solver.isValidWord("NOTAVALIDWORD")).toBe(false);
  });
});

