import content from './content.js';
import MemoryGame from './MemoryGame';
import './styles.css';

export default function App() {
  return (
    <div className="container">
      <header>
        <h1>{content.name} — {content.title}</h1>
        <nav>
          <a href={content.resume} target="_blank">View Resume</a>
        </nav>
      </header>
      
      <main>
        <section className="game-section">
          <h2>{content.games.react.title}</h2>
          <p className="game-description">{content.games.react.description}</p>
          <MemoryGame/>
          <div className="skill-connection">
            <strong>💡 Skill Connection:</strong> {content.games.react.skillConnection}
          </div>
        </section>

        <section className="projects-section">
          <h2>Featured Projects</h2>
          {content.projects.map((project, index) => (
            <div key={index} className="project">
              <h3>{project.title}</h3>
              <p>{project.desc}</p>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}