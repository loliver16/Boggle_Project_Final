/**
 * Mock REST API service for Boggle game
 * Simulates an API endpoint that returns Grid and Solutions based on Grid Size
 */

import { createRandomBoard } from '../utils/boardGenerator';
import BoggleSolver from '../boggleSolver';

// Common words dictionary - in a real app, this would come from an API or larger word list
const dictionary = [
  "art", "ego", "gent", "get", "net", "new", "newt", "prat", "pry",
  "qua", "quart", "quartz", "rat", "tar", "tarp", "ten", "went",
  "wet", "arty", "not", "quar", "hen", "pen", "rent", "wren", "ant",
  "tan", "pan", "pat", "hat", "that", "the", "then", "when", "where",
  "and", "are", "but", "for", "had", "has", "her", "him", "his", "how",
  "its", "let", "may", "old", "one", "our", "out", "say", "she", "the",
  "use", "was", "way", "who", "yes", "you", "act", "add", "age", "ago",
  "aid", "aim", "air", "all", "any", "arm", "ask", "ate", "bad", "bag",
  "bar", "bat", "bed", "bee", "beg", "big", "bit", "bow", "box", "boy",
  "bus", "but", "buy", "can", "cap", "car", "cat", "cut", "day", "did",
  "die", "dig", "dim", "din", "dip", "doe", "dog", "don", "dot", "dry",
  "due", "ear", "eat", "egg", "end", "era", "eve", "eye", "fan", "far",
  "fat", "few", "fig", "fin", "fir", "fit", "fix", "fly", "fog", "for",
  "fox", "fry", "fun", "fur", "gab", "gag", "gap", "gas", "get", "gun",
  "gut", "guy", "had", "ham", "has", "hat", "hay", "hen", "her", "hew",
  "hex", "hey", "hid", "him", "hip", "his", "hit", "hob", "hog", "hop",
  "hot", "how", "hub", "hue", "hug", "hum", "hut", "ice", "icy", "imp",
  "ink", "inn", "ion", "ire", "irk", "its", "ivy", "jab", "jam", "jar",
  "jaw", "jay", "jet", "jig", "job", "jog", "jot", "joy", "jug", "jut",
  "ken", "key", "kid", "kin", "kit", "lab", "lad", "lag", "lam", "lap",
  "law", "lax", "lay", "lea", "led", "leg", "let", "lew", "lid", "lie",
  "lip", "lit", "log", "lot", "low", "lug", "lye", "mad", "man", "map",
  "mar", "mat", "max", "may", "men", "met", "mid", "mix", "mob", "mod",
  "mom", "mop", "mot", "mow", "mud", "mug", "nab", "nag", "nap", "nay",
  "net", "new", "nib", "nil", "nim", "nip", "nit", "nob", "nod", "nog",
  "nor", "not", "now", "nub", "nun", "nut", "oaf", "oak", "oar", "oat",
  "odd", "ode", "off", "oft", "oil", "old", "one", "opt", "orb", "orc",
  "ore", "org", "our", "out", "ova", "owe", "owl", "own", "pad", "pal",
  "pam", "pan", "pap", "par", "pat", "paw", "pax", "pay", "pea", "peg",
  "pen", "pep", "per", "pet", "pew", "pie", "pig", "pin", "pip", "pit",
  "ply", "pod", "pol", "pom", "pop", "pot", "pow", "pox", "pro", "pry",
  "pub", "pug", "pun", "pup", "pur", "pus", "put", "qua", "rad", "rag",
  "ram", "ran", "rap", "rat", "raw", "rax", "ray", "reb", "red", "ref",
  "reg", "rei", "rem", "rep", "ret", "rev", "rex", "rho", "rib", "rid",
  "rig", "rim", "rin", "rip", "rob", "roc", "rod", "roe", "rom", "rot",
  "row", "rub", "rue", "rug", "rum", "run", "rut", "rye", "sab", "sac",
  "sad", "sag", "sal", "sam", "san", "sap", "sat", "saw", "sax", "say",
  "sea", "sec", "see", "seg", "sei", "sel", "sen", "ser", "set", "sew",
  "sex", "she", "shy", "sib", "sic", "sin", "sip", "sir", "sis", "sit",
  "six", "ska", "ski", "sky", "sly", "sob", "sod", "sol", "son", "sop",
  "sot", "sou", "sow", "sox", "soy", "spa", "spy", "sty", "sub", "sud",
  "sue", "sum", "sun", "sup", "tab", "tad", "tae", "tag", "taj", "tam",
  "tan", "tao", "tap", "tar", "tas", "tat", "tau", "tav", "taw", "tax",
  "tea", "ted", "tee", "teg", "tel", "ten", "tes", "tet", "tew", "the",
  "tho", "thy", "tic", "tie", "til", "tin", "tip", "tis", "tit", "tod",
  "toe", "tog", "tom", "ton", "too", "top", "tor", "tot", "tow", "toy",
  "try", "tsk", "tub", "tug", "tui", "tun", "tup", "tut", "tux", "twa",
  "two", "tye", "udo", "ugh", "uke", "ulu", "umm", "ump", "uns", "upo",
  "ups", "urb", "urd", "urn", "urp", "use", "uta", "ute", "uts", "vac",
  "van", "var", "vas", "vat", "vau", "vaw", "vee", "veg", "vet", "vex",
  "via", "vid", "vie", "vig", "vim", "vin", "vis", "voe", "vog", "vow",
  "vox", "vug", "vum", "wab", "wad", "wae", "wag", "wan", "wap", "war",
  "was", "wat", "waw", "wax", "way", "web", "wed", "wee", "wen", "wet",
  "wha", "who", "why", "wig", "win", "wis", "wit", "wiz", "woe", "wog",
  "wok", "won", "woo", "wop", "wot", "wow", "wry", "wud", "wye", "wyn",
  "xed", "xis", "yag", "yah", "yak", "yam", "yap", "yar", "yaw", "yay",
  "yea", "yeh", "yen", "yep", "yes", "yet", "yew", "yid", "yin", "yip",
  "yob", "yod", "yok", "yom", "yon", "you", "yow", "yox", "yuk", "yum",
  "yup", "zag", "zap", "zax", "zed", "zee", "zek", "zen", "zep", "zig",
  "zin", "zip", "zit", "zoa", "zoo", "zor", "zuz", "zzz"
];

/**
 * Mock REST API endpoint that returns Grid and Solutions based on Grid Size
 * @param {number} gridSize - The size of the board (N x N)
 * @returns {Promise<{grid: Array<Array<string>>, solutions: Array<string>}>}
 */
export const fetchBoggleGame = async (gridSize) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300));

  // Validate grid size
  if (!gridSize || gridSize < 2 || gridSize > 12) {
    throw new Error('Grid size must be between 2 and 12');
  }

  // Generate a random board of the specified size
  const grid = createRandomBoard(gridSize);

  // Solve the board to get all valid words
  const solver = new BoggleSolver(grid, dictionary);
  const solutions = solver.getSolution();

  // Return the response in the format a REST API would return
  return {
    grid,
    solutions
  };
};

