import json
import os
from datetime import datetime
from http.client import HTTPResponse
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Feedback

def handler(event, context):
    """Serverless function to handle feedback operations"""
    
    if event['httpMethod'] == 'GET':
        # List all feedback
        feedbacks = list(Feedback.objects.all().values())
        return {
            'statusCode': 200,
            'body': json.dumps({
                'feedbacks': feedbacks,
                'count': len(feedbacks)
            })
        }
        
    elif event['httpMethod'] == 'POST':
        # Create new feedback
        try:
            body = json.loads(event['body'])
            feedback = Feedback.objects.create(
                name=body['name'],
                message=body['message']
            )
            return {
                'statusCode': 201,
                'body': json.dumps({
                    'id': feedback.id,
                    'name': feedback.name,
                    'message': feedback.message,
                    'created_at': feedback.created_at.isoformat()
                })
            }
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': str(e)})
            }
            
    return {
        'statusCode': 405,
        'body': json.dumps({'error': 'Method not allowed'})
    }
