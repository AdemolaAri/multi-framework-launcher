from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, pathlib
from .models import WordAssociationGame

def index(request):
    cur = pathlib.Path(__file__).resolve().parent.parent
    content = json.load(open(cur/'shared'/'content.json'))
    return render(request,'portfolio/index.html',{'content':content})

@csrf_exempt
def start_game(request):
    """Start a new word association game session"""
    if request.method == 'POST':
        # Get random terms for the game
        terms = WordAssociationGame.get_random_terms(5)
        
        # Store game data in session
        request.session['game_terms'] = terms
        request.session['current_term_index'] = 0
        request.session['game_score'] = 0
        request.session['game_responses'] = []
        
        return JsonResponse({
            'success': True,
            'current_term': terms[0],
            'term_number': 1,
            'total_terms': len(terms)
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def submit_response(request):
    """Submit a response for the current term"""
    if request.method == 'POST':
        data = json.loads(request.body)
        user_response = data.get('response', '').strip()
        
        # Get current game state
        terms = request.session.get('game_terms', [])
        current_index = request.session.get('current_term_index', 0)
        
        if not terms or current_index >= len(terms):
            return JsonResponse({'success': False, 'error': 'No active game'})
        
        current_term = terms[current_index]
        
        # Calculate score for this response
        score = WordAssociationGame.calculate_score(current_term, user_response)
        feedback = WordAssociationGame.get_feedback(current_term, user_response, score)
        
        # Update game state
        game_responses = request.session.get('game_responses', [])
        game_responses.append({
            'term': current_term['term'],
            'response': user_response,
            'score': score,
            'feedback': feedback
        })
        
        request.session['game_responses'] = game_responses
        request.session['game_score'] = request.session.get('game_score', 0) + score
        request.session['current_term_index'] = current_index + 1
        
        # Check if game is complete
        if current_index + 1 >= len(terms):
            total_score = request.session.get('game_score', 0)
            avg_score = total_score / len(terms)
            
            return JsonResponse({
                'success': True,
                'game_complete': True,
                'score': score,
                'feedback': feedback,
                'total_score': total_score,
                'average_score': round(avg_score, 1),
                'responses': game_responses
            })
        else:
            # Move to next term
            next_term = terms[current_index + 1]
            return JsonResponse({
                'success': True,
                'game_complete': False,
                'score': score,
                'feedback': feedback,
                'next_term': next_term,
                'term_number': current_index + 2,
                'total_terms': len(terms)
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
