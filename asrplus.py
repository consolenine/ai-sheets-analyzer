import requests
import base64
import os
from flask import jsonify

from csv_analysis import analyse_sheet


# Keys
BHASHINI_API_KEY = os.getenv('BHASHINI_API_KEY')
BHASHINI_UID = os.getenv('BHASHINI_UID')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def process_lang(request):
    data = request.get_json()
    message = data.get('message')
    
    in_hindi = True
    try:
        # if in_hindi:
        #     message = translate(message, to_lang="en", from_lang="hi")
            
        response = analyse_sheet(message)
        
        if in_hindi:
            response = translate(response["output"])
        
        # Return the response to the client
        result = {
            "data": response
        }
        
        return result
    except Exception as e:
        return {
            "error": str(e)
        }

def translate(msg, to_lang="hi", from_lang="en"):
    config_payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
            }
        ],
        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    }
    config_endpint = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    
    headers = {'userID': BHASHINI_UID, 'ulcaApiKey': BHASHINI_API_KEY}
    response = requests.post(config_endpint, headers=headers, json=config_payload)
    
    # Process the response from the Bhashini API
    bhashini_response = response.json()
    
    
    service_id = ""
    for config in bhashini_response["pipelineResponseConfig"]:
        # Iterate through the config dictionaries
        for item in config["config"]:
            # Check if sourceLanguage is "en"
            if item["language"]["sourceLanguage"] == from_lang:
                # Print the serviceId
                service_id = item["serviceId"]
                
    compute_endpoint = bhashini_response["pipelineInferenceAPIEndPoint"]["callbackUrl"]
    headers = {bhashini_response["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]: bhashini_response["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]}
    
    compute_payload = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": from_lang,
                        "targetLanguage": to_lang
                    },
                    "serviceId": service_id,
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": msg
                }
            ]
        }
    }

    response = requests.post(compute_endpoint, headers=headers, json=compute_payload)
    response = response.json()
    
    return response["pipelineResponse"][0]["output"][0]["target"]