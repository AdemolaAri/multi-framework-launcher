<template>
  <div class="container">
    <header>
      <h1>{{ content.name }} — {{ content.title }}</h1>
      <nav>
        <a href="/">← Back to Launcher</a>
        <a :href="content.resume" target="_blank">View Resume</a>
      </nav>
    </header>
    
    <main>
      <section class="profile-section">
        <img src="/shared/assets/avatar.jpg" width="120" alt="Profile Avatar"/>
        <p>{{ content.bio }}</p>
        <a :href="content.resume" target="_blank" class="resume-link">View Resume</a>
      </section>

      <section>
        <h2>{{ content.games.vue.title }}</h2>
        <p>{{ content.games.vue.description }}</p>
        
        <div class="puzzle-game">
          <div class="game-header">
            <div class="game-stats">
              <span class="stat">Moves: {{ moves }}</span>
              <span class="stat">Time: {{ gameTime }}s</span>
            </div>
            <button 
              class="reset-button" 
              @click="initializeGame"
              :disabled="isAnimating"
            >
              New Game
            </button>
          </div>

          <div class="puzzle-grid">
            <div
              v-for="(tile, index) in tiles"
              :key="index"
              :class="['puzzle-tile', { 'empty': tile === 0, 'animating': isAnimating }]"
              @click="moveTile(index)"
              :style="getTileStyle(tile)"
            >
              <span v-if="tile !== 0">{{ tile }}</span>
            </div>
          </div>

          <div v-if="gameComplete" class="completion-modal">
            <div class="completion-content">
              <h3>{{ getCompletionMessage().title }}</h3>
              <p class="completion-stats">{{ getCompletionMessage().message }}</p>
              <p class="skill-connection">{{ content.games.vue.skillConnection }}</p>
              <p class="personal-insight">{{ getCompletionMessage().insight }}</p>
              <button class="play-again-button" @click="initializeGame">
                Play Again
              </button>
            </div>
          </div>
        </div>
      </section>

      <section class="projects-section">
        <h2>Featured Projects</h2>
        <div v-for="(project, index) in content.projects" :key="index" class="project">
          <h3>{{ project.title }}</h3>
          <p>{{ project.desc }}</p>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import content from './content.js'

export default {
  name: 'App',
  setup() {
    const tiles = ref([])
    const moves = ref(0)
    const startTime = ref(null)
    const currentTime = ref(null)
    const gameComplete = ref(false)
    const isAnimating = ref(false)
    let timer = null

    const gameTime = computed(() => {
      if (!startTime.value) return 0
      const end = gameComplete.value ? currentTime.value : Date.now()
      return Math.floor((end - startTime.value) / 1000)
    })

    const initializeGame = () => {
      // Create solved puzzle: [1,2,3,4,5,6,7,8,0]
      const solvedPuzzle = [1, 2, 3, 4, 5, 6, 7, 8, 0]
      
      // Shuffle by making random valid moves
      let puzzle = [...solvedPuzzle]
      for (let i = 0; i < 1000; i++) {
        const emptyIndex = puzzle.indexOf(0)
        const validMoves = getValidMoves(emptyIndex)
        const randomMove = validMoves[Math.floor(Math.random() * validMoves.length)]
        [puzzle[emptyIndex], puzzle[randomMove]] = [puzzle[randomMove], puzzle[emptyIndex]]
      }
      
      tiles.value = puzzle
      moves.value = 0
      gameComplete.value = false
      startTime.value = Date.now()
      currentTime.value = null
      isAnimating.value = false
      
      // Start timer
      if (timer) clearInterval(timer)
      timer = setInterval(() => {
        if (!gameComplete.value) {
          currentTime.value = Date.now()
        }
      }, 1000)
    }

    const getValidMoves = (emptyIndex) => {
      const validMoves = []
      const row = Math.floor(emptyIndex / 3)
      const col = emptyIndex % 3
      
      // Up
      if (row > 0) validMoves.push(emptyIndex - 3)
      // Down
      if (row < 2) validMoves.push(emptyIndex + 3)
      // Left
      if (col > 0) validMoves.push(emptyIndex - 1)
      // Right
      if (col < 2) validMoves.push(emptyIndex + 1)
      
      return validMoves
    }

    const moveTile = (index) => {
      if (isAnimating.value || gameComplete.value) return
      
      const emptyIndex = tiles.value.indexOf(0)
      const validMoves = getValidMoves(emptyIndex)
      
      if (validMoves.includes(index)) {
        isAnimating.value = true
        
        // Swap tiles
        const newTiles = [...tiles.value]
        ;[newTiles[emptyIndex], newTiles[index]] = [newTiles[index], newTiles[emptyIndex]]
        tiles.value = newTiles
        moves.value++
        
        // Check for completion
        setTimeout(() => {
          isAnimating.value = false
          checkCompletion()
        }, 200)
      }
    }

    const checkCompletion = () => {
      const solved = [1, 2, 3, 4, 5, 6, 7, 8, 0]
      if (tiles.value.every((tile, index) => tile === solved[index])) {
        gameComplete.value = true
        currentTime.value = Date.now()
        if (timer) clearInterval(timer)
      }
    }

    const getTileStyle = (tile) => {
      if (tile === 0) return {}
      
      // Generate a gradient based on the tile number
      const hue = (tile * 40) % 360
      return {
        background: `linear-gradient(135deg, hsl(${hue}, 60%, 70%), hsl(${hue}, 60%, 60%))`,
        color: 'white',
        textShadow: '0 1px 2px rgba(0,0,0,0.3)'
      }
    }

    const getCompletionMessage = () => {
      const time = gameTime.value
      const efficiency = moves.value <= 50 ? 'excellent' : moves.value <= 100 ? 'good' : 'decent'
      
      return {
        title: "Puzzle Mastered! 🧩",
        message: `Solved in ${moves.value} moves and ${time} seconds with ${efficiency} efficiency.`,
        insight: moves.value <= 50 
          ? "Your systematic approach to breaking down complex problems mirrors how I architect scalable software solutions."
          : moves.value <= 100
          ? "Your methodical problem-solving reflects the analytical thinking I apply to debugging and optimization challenges."
          : "Your persistence in finding the solution demonstrates the same determination I bring to tackling complex technical challenges."
      }
    }

    onMounted(() => {
      initializeGame()
    })

    onUnmounted(() => {
      if (timer) clearInterval(timer)
    })

    return {
      content,
      tiles,
      moves,
      gameTime,
      gameComplete,
      isAnimating,
      initializeGame,
      moveTile,
      getTileStyle,
      getCompletionMessage
    }
  }
}
</script>

<style scoped>
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.container header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
}

.container header h1 {
  color: #2c3e50;
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.container header nav {
  display: flex;
  gap: 15px;
}

.container header nav a {
  background: #3498db;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  transition: background 0.3s ease;
}

.container header nav a:hover {
  background: #2980b9;
}

main {
  display: grid;
  gap: 30px;
}

section {
  background: white;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

section img {
  border-radius: 50%;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  margin-bottom: 15px;
}

section h2 {
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.5rem;
}

section p {
  line-height: 1.6;
  color: #555;
  font-size: 1.1rem;
}

/* Resume link */
.resume-link {
  display: inline-block;
  background: #28a745;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 500;
  margin-top: 15px;
  transition: background 0.3s ease;
}

.resume-link:hover {
  background: #218838;
}

/* Projects section */
.projects-section h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.project {
  background: #f8f9fa;
  padding: 15px;
  margin: 15px 0;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.project h3 {
  margin: 0 0 10px 0;
  color: #667eea;
}

.project p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

/* Puzzle Game Styles */
.puzzle-game {
  max-width: 400px;
  margin: 0 auto;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px solid #e9ecef;
}

.game-stats {
  display: flex;
  gap: 20px;
}

.stat {
  font-weight: 600;
  color: #495057;
  font-size: 1.1rem;
}

.reset-button {
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.reset-button:hover:not(:disabled) {
  background: #218838;
  transform: translateY(-2px);
}

.reset-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.puzzle-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  background: #495057;
  padding: 4px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
}

.puzzle-tile {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
  border: 2px solid transparent;
}

.puzzle-tile:not(.empty) {
  background: linear-gradient(135deg, #6c757d, #495057);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.puzzle-tile:not(.empty):hover {
  transform: scale(1.05);
  border-color: #007bff;
}

.puzzle-tile.empty {
  background: transparent;
  cursor: default;
}

.puzzle-tile.animating {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Completion Modal */
.completion-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.completion-content {
  background: white;
  padding: 40px;
  border-radius: 16px;
  text-align: center;
  max-width: 500px;
  margin: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(30px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

.completion-content h3 {
  color: #28a745;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.8rem;
}

.completion-stats {
  font-size: 1.2rem;
  font-weight: 600;
  color: #495057;
  margin-bottom: 20px;
}

.skill-connection {
  font-style: italic;
  color: #6c757d;
  margin-bottom: 15px;
  line-height: 1.5;
}

.personal-insight {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #28a745;
  margin-bottom: 25px;
  font-weight: 500;
  color: #495057;
  line-height: 1.5;
}

.play-again-button {
  background: #007bff;
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.play-again-button:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .container {
    padding: 15px;
    margin: 8px;
    border-radius: 8px;
  }
  
  .container header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .container header h1 {
    font-size: 1.5rem;
  }
  
  main {
    gap: 20px;
  }
  
  section {
    padding: 20px;
  }
  
  .puzzle-game {
    max-width: 300px;
  }
  
  .puzzle-tile {
    font-size: 1.5rem;
  }
  
  .game-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .game-stats {
    justify-content: center;
  }
  
  .completion-content {
    padding: 30px 20px;
    margin: 10px;
  }
  
  .completion-content h3 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .puzzle-game {
    max-width: 280px;
  }
  
  .puzzle-tile {
    font-size: 1.2rem;
  }
  
  .stat {
    font-size: 1rem;
  }
  
  .completion-content {
    padding: 25px 15px;
  }
}
</style>