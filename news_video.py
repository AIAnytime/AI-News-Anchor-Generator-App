import requests
import json

class VideoGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_video(self, input_text, source_url):
        url = "https://api.d-id.com/talks"

        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-US-JennyNeural"
                },
                "ssml": "false",
                "input": input_text
            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0"
            },
            "source_url": source_url
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(url, json=payload, headers=headers)
        _response = json.loads(response.text)
        print("Response: ",_response)
        while _response["status"] != "created":
            response = requests.post(url, json=payload, headers=headers)
            _response = json.loads(response.text)

        talk_id = json.loads(response.text)['id']

        talk_url = f"{url}/{talk_id}"

        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(talk_url, headers=headers)
        video_response = json.loads(response.text)

        while video_response["status"] != "done":
            response = requests.get(talk_url, headers=headers)
            video_response = json.loads(response.text)

        video_url = video_response["result_url"]
        return video_url
