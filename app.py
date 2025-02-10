import os
import json
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    message: str
    lang_source: str
    lang_dest: str


@app.get("/")
async def root():
    return {"Status: ": "On-line - Active"}

# Load environment variables for api key, url, and project id from the .env file
load_dotenv()
api_key = os.getenv("GENAI_KEY", None)
url = os.getenv("GENAI_API", None)
project_id = os.getenv("GENAI_PROJECT_ID", None)

def get_bearer_token(apikey):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": apikey
    }
    response = requests.post(url, headers=headers, data=data, )
    return "Bearer " + response.json()['access_token']

@app.post("/translate")
async def translate(message: Message):
    json_data = message.json()
    print("Message: ", json_data)
    data = json.loads(json_data)
    print(type(data))
    print(data["lang_source"])

    api_token = get_bearer_token(api_key)

    body = {
		"input": """Translate the following text from""" + data["lang_source"] + """ to """ + data["lang_dest"] + """:

	Text: Finally, I welcome paragraph 16 which calls for a review of the way we deal with human rights issues in Parliament.
	Translation: Enfin, je me réjouis du paragraphe 16 qui appelle à une révision de la manière dont nous abordons les questions relatives aux droits de l'\''homme au sein du Parlement.

	Text: I remember very well that we discussed it in a session in Luxembourg.
	Translation: Je me souviens très bien que nous en avions parlé lors d'\''une séance à Luxembourg.

	Text: """ + data["message"] + """
	Translation:""",
		"parameters": {
			"decoding_method": "sample",
			"max_new_tokens": 1024,
			"min_new_tokens": 1,
			"random_seed": 42,
			"stop_sequences": ["\n"],
			"temperature": 0.5,
			"top_k": 50,
			"top_p": 0.75,
			"repetition_penalty": 1
		},
		"model_id": "ibm/granite-3-8b-instruct",
		"project_id": "6a02dbed-7ff4-473e-9850-eb699b0402db"
	}

    headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": api_token
	}

    response = requests.post(
		url,
		headers=headers,
		json=body
	)

    if response.status_code != 200:
	    raise Exception("Non-200 response: " + str(response.text))

    translation = response.json()['results'][0]['generated_text']
    translation_obj = {}
    translation_obj['translation'] = translation
    print(translation_obj)
    return(translation_obj)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)