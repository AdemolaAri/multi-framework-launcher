from django.db import models
import json
import random

class WordAssociationGame:
    """
    Word Association Game logic - presents tech terms and collects related concept responses
    """
    
    TECH_TERMS = [
        {
            'term': 'API',
            'expected_associations': ['REST', 'GraphQL', 'endpoint', 'interface', 'HTTP', 'JSON', 'microservices'],
            'category': 'Backend'
        },
        {
            'term': 'React',
            'expected_associations': ['component', 'JSX', 'hooks', 'state', 'props', 'virtual DOM', 'frontend'],
            'category': 'Frontend'
        },
        {
            'term': 'Database',
            'expected_associations': ['SQL', 'NoSQL', 'MongoDB', 'PostgreSQL', 'schema', 'query', 'CRUD'],
            'category': 'Data'
        },
        {
            'term': 'Docker',
            'expected_associations': ['container', 'image', 'deployment', 'microservices', 'orchestration', 'Kubernetes'],
            'category': 'DevOps'
        },
        {
            'term': 'Git',
            'expected_associations': ['version control', 'branch', 'merge', 'commit', 'repository', 'GitHub', 'collaboration'],
            'category': 'Tools'
        },
        {
            'term': 'Python',
            'expected_associations': ['Django', 'Flask', 'backend', 'scripting', 'data science', 'machine learning'],
            'category': 'Language'
        },
        {
            'term': 'Microservices',
            'expected_associations': ['architecture', 'distributed', 'API', 'scalability', 'Docker', 'communication'],
            'category': 'Architecture'
        },
        {
            'term': 'Testing',
            'expected_associations': ['unit test', 'integration', 'TDD', 'quality', 'automation', 'debugging'],
            'category': 'Quality'
        }
    ]
    
    @classmethod
    def get_random_terms(cls, count=5):
        """Get random terms for the game"""
        return random.sample(cls.TECH_TERMS, min(count, len(cls.TECH_TERMS)))
    
    @classmethod
    def calculate_score(cls, term_data, user_response):
        """Calculate score based on how well the response matches expected associations"""
        if not user_response or not user_response.strip():
            return 0
        
        user_words = [word.lower().strip() for word in user_response.split()]
        expected = [assoc.lower() for assoc in term_data['expected_associations']]
        
        # Score based on matching words and concepts
        matches = 0
        for user_word in user_words:
            for expected_word in expected:
                if user_word in expected_word or expected_word in user_word:
                    matches += 1
                    break
        
        # Base score on matches, with bonus for multiple relevant words
        base_score = min(matches * 20, 100)
        length_bonus = min(len(user_words) * 2, 10) if matches > 0 else 0
        
        return min(base_score + length_bonus, 100)
    
    @classmethod
    def get_feedback(cls, term_data, user_response, score):
        """Generate feedback based on the response and score"""
        if score >= 80:
            return f"Excellent! Your association with '{term_data['term']}' shows deep technical understanding."
        elif score >= 60:
            return f"Good connection! You understand key concepts related to '{term_data['term']}'."
        elif score >= 40:
            return f"Nice try! '{term_data['term']}' relates to: {', '.join(term_data['expected_associations'][:3])}."
        else:
            return f"'{term_data['term']}' is commonly associated with: {', '.join(term_data['expected_associations'][:2])}. Keep exploring!"