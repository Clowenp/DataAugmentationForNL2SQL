import json
import requests
import os
import re

from dotenv import load_dotenv


class Voiceflow:
    
    def __init__(self, userID):
        load_dotenv('.env')
        self.API_KEY = os.getenv('API_KEY')
        self.url = "https://general-runtime.voiceflow.com/state/user/" + userID + "/interact?logs=off"

    def launch_workflow(self, variable_map):
        payload = {
            "action": { "type": "launch" },
            "config": {
                "tts": False,
                "stripSSML": True,
                "stopAll": True,
                "excludeTypes": ["block", "debug", "flow"]
            },
            "state": { "variables": variable_map }
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": self.API_KEY
        }

        return requests.post(self.url, json=payload, headers=headers)
        
    
    def send_intent(self, variable_map, query, intent):
        payload = {
            "action": {
                "type": "intent",
                "payload": {
                    "query": query,
                    "intent": { "name": intent },
                    "confidence": 0.5
                }
            },
            "config": {
                "tts": False,
                "stripSSML": True,
                "stopAll": True,
                "excludeTypes": ["block", "debug", "flow"]
            },
            "state": { "variables": variable_map }
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": self.API_KEY
        }

        return requests.post(self.url, json=payload, headers=headers)

    def send_text(self, variable_map, text):
        payload = {
            "action": {
                "type": "text",
                "payload": text
            },
            "config": {
                "tts": False,
                "stripSSML": True,
                "stopAll": True,
                "excludeTypes": ["block", "debug", "flow"]
            },
            "state": { "variables": variable_map }
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": self.API_KEY
        }

        return requests.post(self.url, json=payload, headers=headers)

    def close_flow(self):
        headers = {"Authorization": self.API_KEY}

        return requests.delete(self.url[:len(self.url) - 18], headers=headers)

class MockText:

    @staticmethod
    def mock(text):
        vf = Voiceflow("2")
        res = vf.launch_workflow({"mock": text}).json()[0]
        print("=== Res ===")
        print(res)
        print("=== End Res ===")
        children = res["payload"]["slate"]["content"]
        for child in children:
            for text in child["children"]:
                list_queries = json.loads(text["text"])["Queries"]
                return list_queries

def tokenize(string):
    return re.findall(r'\w+|[.,!?;]', string)
    


def main():
    # parse data
    augmented_json = []
    with open("augmentation_week2/test.json", "r") as input_file:
        data = json.load(input_file)
        with open("augmentation_week2/test_augment_2.json", "w") as output_file:
            try:
                for query in data:
                    augmented_json.append(query.copy())
                    result_list = MockText.mock(query["question"])
                    for result in result_list:
                        query["question"] = result
                        # query["question_toks"] = tokenize(result)
                        augmented_json.append(query.copy())
                json.dump(augmented_json, output_file, indent=4)
            except:
                json.dump(augmented_json, output_file, indent=4)


            

if __name__ == "__main__":
    main()
