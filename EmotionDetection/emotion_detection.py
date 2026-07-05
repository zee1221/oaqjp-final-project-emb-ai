import json
import requests

def emotion_detector(text_to_analyze):
    # Base URL for the Skills Network Watson NLP proxy
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    myobj = { 
        "raw_document": { 
            "text": text_to_analyze 
        } 
    }
    
    # Send POST request
    response = requests.post(url, json=myobj, headers=headers)
    
    # Check if the response was successful
    if response.status_code == 200:
        # Convert the raw response text into a dictionary
        formatted_response = json.loads(response.text)
        
        # Extract the target emotion dictionary from the nested JSON structure
        # Watson NLP responses typically nest under 'emotionPredictions'[0]['emotion']
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        
        # Isolate the required individual emotion metrics
        anger_score = emotions.get('anger', 0)
        disgust_score = emotions.get('disgust', 0)
        fear_score = emotions.get('fear', 0)
        joy_score = emotions.get('joy', 0)
        sadness_score = emotions.get('sadness', 0)
        
        # Package scores into a simple temporary dictionary to easily locate the maximum
        target_emotions = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }
        
        # Determine the dominant emotion (key with the highest value)
        dominant_emotion = max(target_emotions, key=target_emotions.get)
        
        # Append the dominant_emotion field to match the exact requested output format
        target_emotions['dominant_emotion'] = dominant_emotion
        
        return target_emotions
    else:
        # Fallback return structure if the service fails
        return {
            'anger': None, 'disgust': None, 'fear': None, 'joy': None, 'sadness': None,
            'dominant_emotion': None
        }