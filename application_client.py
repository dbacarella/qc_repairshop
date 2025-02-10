import requests
import json

watsonx_response = ""

#resx = requests.post('https://ssgxlate-api.z929zicbgpt.us-south.codeengine.appdomain.cloud/translate', json={"message": "Delete a folder from the Home screen. 1. From Apps, touch and hold a folder to delete. 2. Tap Delete folder, and confirm when prompted.", "model": "google/flan-t5-xxl", "from_language": "English", "to_language": "Spanish"})
resx = requests.post('http://0.0.0.0:8010/translate', json={"message": "Hello, I am glad to be in Spain at this time of year.", "lang_source": "English", "lang_dest": "Polish"})
print(resx)

if resx.ok:
    watsonx_response = resx.content
    wxrsp = json.loads(watsonx_response.decode('utf-8'))
    print(wxrsp['translation'])
else:
    print("Error: Error posting request to summary function.")

