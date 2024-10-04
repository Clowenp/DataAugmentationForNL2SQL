import requests


class Voiceflow:

    def __init__(self, userID):
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
            "Authorization": "VF.DM.66e4e1a6ec948227a6f65180.7f5cMxkTGWfY0Za1"
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
            "Authorization": "VF.DM.66e4e1a6ec948227a6f65180.7f5cMxkTGWfY0Za1"
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
            "Authorization": "VF.DM.66e4e1a6ec948227a6f65180.7f5cMxkTGWfY0Za1"
        }

        return requests.post(self.url, json=payload, headers=headers)

    def close_flow(self):
        headers = {"Authorization": "VF.DM.66e4e1a6ec948227a6f65180.7f5cMxkTGWfY0Za1"}

        return requests.delete(self.url[:len(self.url) - 18], headers=headers)

def main():
    vf = Voiceflow("1")
    print(vf.launch_workflow( {"myVar": 'a'} ).text)
    print(vf.send_text( {}, "I'd like to be connected to the head of the sales department for a strategic partnership discussion.").text)
    # print(vf.send_intent( {}, "I'd like to be connected to the head of the sales department for a strategic partnership discussion.", "" ).text)
    print(vf.close_flow())

if __name__ == "__main__":
    main()
