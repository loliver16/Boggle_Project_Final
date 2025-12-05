import React, { useState, useEffect, useRef } from 'react';
import BoggleSolver from './boggleSolver';
import { fetchBoggleGame } from './services/boggleApi';
import './BoggleGame.css';
import Notification from './components/Notification';
import Timer from './components/Timer';
import Score from './components/Score';
import WelcomeScreen from './components/WelcomeScreen';
import GameBoard from './components/GameBoard';
import FoundWordsList from './components/FoundWordsList';
import RemainingWordsList from './components/RemainingWordsList';
import GameControls from './components/GameControls';

const BoggleGame = () => {
  const [gameStarted, setGameStarted] = useState(false);
  const [gameStopped, setGameStopped] = useState(false);
  const [timeLeft, setTimeLeft] = useState(180); // 3 minutes default
  const [foundWords, setFoundWords] = useState([]);
  const [inputWord, setInputWord] = useState('');
  const [notification, setNotification] = useState('');
  const [remainingWords, setRemainingWords] = useState([]);
  const [selectedPath, setSelectedPath] = useState([]);
  const [isSelecting, setIsSelecting] = useState(false);
  const [grid, setGrid] = useState([]);

  const solverRef = useRef(null);
  const timerRef = useRef(null);
  const notificationTimeoutRef = useRef(null);

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

  // Initialize solver when grid changes
  useEffect(() => {
    if (grid.length > 0) {
      solverRef.current = new BoggleSolver(grid, dictionary);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [grid]);

  useEffect(() => {
    if (gameStarted && !gameStopped) {
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [gameStarted, gameStopped]);

  // Handle timer expiration
  useEffect(() => {
    if (timeLeft === 0 && gameStarted && !gameStopped) {
      setGameStopped(true);
      // Calculate remaining words when timer ends
      const allSolutions = solverRef.current.getSolution();
      const foundWordsUpper = foundWords.map(w => w.toUpperCase());
      const remaining = allSolutions.filter(word => !foundWordsUpper.includes(word));
      setRemainingWords(remaining);
    }
  }, [timeLeft, gameStarted, gameStopped, foundWords]);

  const handleStartGame = async (boardSize) => {
    try {
      // Call mock REST API to get grid and solutions
      showNotification('Loading game...', 'info');
      const response = await fetchBoggleGame(boardSize);
      
      setGrid(response.grid);
      setGameStarted(true);
      setGameStopped(false);
      setTimeLeft(180); // Reset to 3 minutes
      setFoundWords([]);
      setRemainingWords([]);
      setInputWord('');
      setNotification('');
      setSelectedPath([]);
      setIsSelecting(false);
    } catch (error) {
      showNotification(`Error loading game: ${error.message}`, 'error');
    }
  };

  const handleStopGame = () => {
    if (gameStarted && !gameStopped) {
      setGameStopped(true);
      // Calculate remaining words
      const allSolutions = solverRef.current.getSolution();
      const foundWordsUpper = foundWords.map(w => w.toUpperCase());
      const remaining = allSolutions.filter(word => !foundWordsUpper.includes(word));
      setRemainingWords(remaining);
    }
  };

  const handleResetGame = () => {
    setGameStarted(false);
    setGameStopped(false);
    setTimeLeft(180);
    setFoundWords([]);
    setRemainingWords([]);
    setInputWord('');
    setNotification('');
    setSelectedPath([]);
    setIsSelecting(false);
  };

  const handleWordSubmit = (e) => {
    e.preventDefault();
    if (!gameStarted || gameStopped) return;

    const word = inputWord.trim().toUpperCase();
    if (!word || word.length < 3) {
      showNotification('Words must be at least 3 letters long!', 'error');
      setInputWord('');
      return;
    }

    // Check if already found
    if (foundWords.map(w => w.toUpperCase()).includes(word)) {
      showNotification('You already found this word!', 'error');
      setInputWord('');
      return;
    }

    // Check if word is valid
    const allSolutions = solverRef.current.getSolution();
    if (allSolutions.includes(word)) {
      setFoundWords(prev => [...prev, word]);
      showNotification(`Great! Found "${word}"`, 'success');
    } else {
      showNotification(`"${word}" is not a valid word on this board!`, 'error');
    }

    setInputWord('');
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    if (notificationTimeoutRef.current) {
      clearTimeout(notificationTimeoutRef.current);
    }
    notificationTimeoutRef.current = setTimeout(() => {
      setNotification('');
    }, 3000);
  };

  const handleCellClick = (row, col) => {
    if (!gameStarted || gameStopped || !isSelecting) return;
    
    const lastCell = selectedPath[selectedPath.length - 1];
    if (lastCell) {
      const [lastRow, lastCol] = lastCell;
      const rowDiff = Math.abs(row - lastRow);
      const colDiff = Math.abs(col - lastCol);
      
      // Check if adjacent (including diagonal)
      if (rowDiff <= 1 && colDiff <= 1 && !(rowDiff === 0 && colDiff === 0)) {
        // Check if not already in path
        if (!selectedPath.find(([r, c]) => r === row && c === col)) {
          setSelectedPath([...selectedPath, [row, col]]);
        }
      }
    } else {
      setSelectedPath([[row, col]]);
    }
  };

  const getWordFromPath = () => {
    if (grid.length === 0) return '';
    return selectedPath.map(([r, c]) => grid[r][c]).join('').toUpperCase();
  };

  const handlePathSubmit = () => {
    if (!gameStarted || gameStopped) return;

    const word = getWordFromPath();
    if (!word || word.length < 3) {
      showNotification('Words must be at least 3 letters long!', 'error');
      setSelectedPath([]);
      setIsSelecting(false);
      return;
    }

    // Check if already found
    if (foundWords.map(w => w.toUpperCase()).includes(word)) {
      showNotification('You already found this word!', 'error');
      setSelectedPath([]);
      setIsSelecting(false);
      return;
    }

    // Check if word is valid
    const allSolutions = solverRef.current.getSolution();
    if (allSolutions.includes(word)) {
      setFoundWords(prev => [...prev, word]);
      showNotification(`Great! Found "${word}"`, 'success');
    } else {
      showNotification(`"${word}" is not a valid word on this board!`, 'error');
    }

    setSelectedPath([]);
    setIsSelecting(false);
  };

  const handleToggleSelecting = () => {
    setIsSelecting(!isSelecting);
    setSelectedPath([]);
  };

  const handleInputChange = (e) => {
    setInputWord(e.target.value.toUpperCase());
  };

  return (
    <div className="boggle-container">
      <div className="boggle-header">
        <h1>🎲 Boggle Game</h1>
        {gameStarted && (
          <GameControls
            gameStopped={gameStopped}
            onStopGame={handleStopGame}
            onResetGame={handleResetGame}
          />
        )}
      </div>

      {gameStarted && (
        <div className="game-info">
          <Timer timeLeft={timeLeft} />
          <Score foundWords={foundWords} />
        </div>
      )}

      <Notification notification={notification} />

      <div className="game-content">
        {gameStarted ? (
          <>
            {grid.length > 0 && (
              <GameBoard
                grid={grid}
                selectedPath={selectedPath}
                isSelecting={isSelecting}
                onCellClick={handleCellClick}
                onToggleSelecting={handleToggleSelecting}
                onPathSubmit={handlePathSubmit}
                onWordSubmit={handleWordSubmit}
                inputWord={inputWord}
                onInputChange={handleInputChange}
                gameStopped={gameStopped}
                getWordFromPath={getWordFromPath}
              />
            )}

            <div className="words-section">
              <FoundWordsList foundWords={foundWords} />
              {gameStopped && (
                <RemainingWordsList remainingWords={remainingWords} />
              )}
            </div>
          </>
        ) : (
          <WelcomeScreen onStartGame={handleStartGame} />
        )}
      </div>
    </div>
  );
};

export default BoggleGame;
