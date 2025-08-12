from flask import Flask, render_template, jsonify, request
import json
import random

app = Flask(__name__, template_folder='templates', static_folder='static')
CONTENT = json.load(open('shared/content.json'))

# Tech trivia questions with explanatory feedback
TRIVIA_QUESTIONS = [
    {
        "id": "q1",
        "question": "Which Python framework is known for its 'batteries included' philosophy?",
        "options": ["Flask", "Django", "FastAPI", "Tornado"],
        "correct": "Django",
        "explanation": "Django follows the 'batteries included' philosophy, providing many built-in features like ORM, admin interface, and authentication out of the box.",
        "category": "Backend Frameworks"
    },
    {
        "id": "q2", 
        "question": "What does the 'V' in MVC architecture stand for?",
        "options": ["Variable", "View", "Version", "Virtual"],
        "correct": "View",
        "explanation": "In MVC (Model-View-Controller), the View is responsible for presenting data to the user and handling the user interface.",
        "category": "Software Architecture"
    },
    {
        "id": "q3",
        "question": "Which database type is MongoDB?",
        "options": ["Relational", "Document", "Graph", "Key-Value"],
        "correct": "Document",
        "explanation": "MongoDB is a document database that stores data in flexible, JSON-like documents, making it ideal for applications with evolving schemas.",
        "category": "Databases"
    },
    {
        "id": "q4",
        "question": "What is the primary purpose of Docker containers?",
        "options": ["Version control", "Application packaging", "Database management", "Code compilation"],
        "correct": "Application packaging",
        "explanation": "Docker containers package applications with their dependencies, ensuring consistent deployment across different environments.",
        "category": "DevOps"
    },
    {
        "id": "q5",
        "question": "Which JavaScript framework uses a virtual DOM?",
        "options": ["Angular", "React", "Vue", "All of the above"],
        "correct": "All of the above",
        "explanation": "React pioneered the virtual DOM concept, and both Angular and Vue have adopted similar approaches for efficient DOM updates.",
        "category": "Frontend Frameworks"
    },
    {
        "id": "q6",
        "question": "What does API stand for?",
        "options": ["Application Programming Interface", "Advanced Programming Integration", "Automated Process Integration", "Application Process Interface"],
        "correct": "Application Programming Interface",
        "explanation": "APIs define how different software components communicate, enabling integration between systems and services.",
        "category": "Software Integration"
    },
    {
        "id": "q7",
        "question": "Which HTTP status code indicates a successful request?",
        "options": ["404", "500", "200", "301"],
        "correct": "200",
        "explanation": "HTTP 200 OK indicates that the request was successful and the server returned the requested data.",
        "category": "Web Protocols"
    },
    {
        "id": "q8",
        "question": "What is the main advantage of microservices architecture?",
        "options": ["Faster development", "Independent scaling", "Reduced complexity", "Lower costs"],
        "correct": "Independent scaling",
        "explanation": "Microservices allow individual services to be scaled independently based on demand, improving resource efficiency and system resilience.",
        "category": "System Architecture"
    }
]

@app.route('/')
def index():
    # Select 5 random questions for each game session
    selected_questions = random.sample(TRIVIA_QUESTIONS, 5)
    return render_template('index.html', content=CONTENT, questions=selected_questions)

@app.route('/trivia/submit', methods=['POST'])
def trivia_submit():
    data = request.json
    user_answers = data.get('answers', {})
    
    # Create a lookup for correct answers
    question_lookup = {q['id']: q for q in TRIVIA_QUESTIONS}
    
    results = []
    correct_count = 0
    
    for question_id, user_answer in user_answers.items():
        question = question_lookup.get(question_id)
        if question:
            is_correct = user_answer == question['correct']
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_id': question_id,
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': question['correct'],
                'is_correct': is_correct,
                'explanation': question['explanation'],
                'category': question['category']
            })
    
    total_questions = len(user_answers)
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Generate personalized feedback based on score
    if score_percentage >= 80:
        feedback = "Excellent! Your broad technical knowledge reflects the kind of continuous learning that drives innovation in software engineering."
    elif score_percentage >= 60:
        feedback = "Great job! Your solid understanding of core concepts shows the foundation needed for effective problem-solving."
    elif score_percentage >= 40:
        feedback = "Good effort! Building technical knowledge is a journey - each concept learned strengthens your engineering toolkit."
    else:
        feedback = "Keep learning! Every expert was once a beginner. The curiosity to understand these concepts is what leads to mastery."
    
    return jsonify({
        'score': correct_count,
        'total': total_questions,
        'percentage': round(score_percentage, 1),
        'feedback': feedback,
        'results': results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
