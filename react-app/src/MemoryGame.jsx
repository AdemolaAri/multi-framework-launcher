import React, { useState, useEffect } from 'react';
import content from '../shared/content.json';

const symbols = ['🍕', '🚀', '🎧', '🐱', '🎲', '💡'];

export default function MemoryGame() {
  const [cards, setCards] = useState([]);
  const [first, setFirst] = useState(null);
  const [second, setSecond] = useState(null);
  const [moves, setMoves] = useState(0);
  const [gameComplete, setGameComplete] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [endTime, setEndTime] = useState(null);
  const [isFlipping, setIsFlipping] = useState(false);

  // Initialize game
  const initializeGame = () => {
    const deck = [...symbols, ...symbols].sort(() => Math.random() - 0.5);
    setCards(deck.map((s, i) => ({ id: i, symbol: s, flipped: false, matched: false })));
    setFirst(null);
    setSecond(null);
    setMoves(0);
    setGameComplete(false);
    setStartTime(Date.now());
    setEndTime(null);
    setIsFlipping(false);
  };

  // Initialize game on component mount
  useEffect(() => {
    initializeGame();
  }, []);

  // Handle card matching logic
  useEffect(() => {
    if (first && second) {
      setIsFlipping(true);
      setMoves(m => m + 1);
      
      if (first.symbol === second.symbol) {
        // Match found
        setCards(c => c.map(x => 
          x.symbol === first.symbol ? { ...x, matched: true } : x
        ));
        resetSelection();
        setIsFlipping(false);
      } else {
        // No match - flip back after delay
        setTimeout(() => {
          setCards(c => c.map(x => 
            x.id === first.id || x.id === second.id 
              ? { ...x, flipped: false } 
              : x
          ));
          resetSelection();
          setIsFlipping(false);
        }, 1000);
      }
    }
  }, [second]);

  // Check for game completion
  useEffect(() => {
    if (cards.length > 0 && cards.every(card => card.matched)) {
      setGameComplete(true);
      setEndTime(Date.now());
    }
  }, [cards]);

  const flip = (card) => {
    if (card.flipped || card.matched || isFlipping) return;
    
    setCards(c => c.map(x => 
      x.id === card.id ? { ...x, flipped: true } : x
    ));
    
    if (!first) {
      setFirst({ ...card, flipped: true });
    } else if (!second) {
      setSecond({ ...card, flipped: true });
    }
  };

  const resetSelection = () => {
    setFirst(null);
    setSecond(null);
  };

  const getGameTime = () => {
    if (!startTime) return 0;
    const end = endTime || Date.now();
    return Math.floor((end - startTime) / 1000);
  };

  const getPerformanceMessage = () => {
    const time = getGameTime();
    const efficiency = moves <= 8 ? 'excellent' : moves <= 12 ? 'good' : 'decent';
    
    return {
      title: "Outstanding Memory Skills! 🎯",
      message: `Completed in ${moves} moves and ${time} seconds with ${efficiency} efficiency.`,
      connection: content.games.react.skillConnection,
      insight: moves <= 8 
        ? "Your methodical approach mirrors the attention to detail I bring to code reviews and system architecture."
        : moves <= 12
        ? "Your systematic thinking reflects the problem-solving approach I use in debugging complex systems."
        : "Your persistence in solving challenges aligns with how I approach learning new technologies and frameworks."
    };
  };

  return (
    <div className="memory-game">
      <div className="game-header">
        <div className="game-stats">
          <span className="stat">Moves: {moves}</span>
          <span className="stat">Time: {getGameTime()}s</span>
        </div>
        <button 
          className="reset-button" 
          onClick={initializeGame}
          disabled={isFlipping}
        >
          New Game
        </button>
      </div>

      <div className="cards-grid">
        {cards.map(card => (
          <button
            key={card.id}
            className={`memory-card ${card.flipped ? 'flipped' : ''} ${card.matched ? 'matched' : ''}`}
            onClick={() => flip(card)}
            disabled={isFlipping}
          >
            <div className="card-inner">
              <div className="card-front">❓</div>
              <div className="card-back">{card.symbol}</div>
            </div>
          </button>
        ))}
      </div>

      {gameComplete && (
        <div className="completion-modal">
          <div className="completion-content">
            <h3>{getPerformanceMessage().title}</h3>
            <p className="completion-stats">{getPerformanceMessage().message}</p>
            <p className="skill-connection">{getPerformanceMessage().connection}</p>
            <p className="personal-insight">{getPerformanceMessage().insight}</p>
            <button className="play-again-button" onClick={initializeGame}>
              Play Again
            </button>
          </div>
        </div>
      )}
    </div>
  );
}