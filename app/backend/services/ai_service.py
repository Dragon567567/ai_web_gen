import json
import os

import requests

zhipu_token = '86d89750b1fb4c479c191674523286a4.dBmRMDvC85l0RUee'
zhipu_uri = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'

with open('./prompt_gen.txt', 'r', encoding='utf-8') as f:
    prompt_gen = f.read()

with open('./prompt_check.txt', 'r', encoding='utf-8') as f:
    prompt_check = f.read()

class AIService:
    def __init__(self, token, uri, is_check=False):
        self.token = token
        self.uri = uri
        self.headers = {
            "Authorization": token
        }
        self.is_check = is_check

    def gen_code(self, app_desc):
        app_prompt = prompt_gen.replace('{{req}}', app_desc)
        body = {
            'model': 'glm-4.7',
            'messages': [
                {
                    'role': 'user',
                    'content': app_prompt
                }
            ]
        }
        # 生成代码
        code_res = requests.post(self.uri, json=body, headers=self.headers)
        raw_code_json = self.normalize(code_res)
        if self.is_check:
            check_prompt = (prompt_check.replace('{{req}}', app_desc)
                            .replace("{{front_code}}", raw_code_json['front'])
                            .replace('{{end_code}}', raw_code_json['end']))
            body = {
                'model': 'glm-4.7',
                'messages': [
                    {
                        'role': 'user',
                        'content': check_prompt
                    }
                ]
            }
            # 检查代码并改正
            check_res = requests.post(self.uri, json=body, headers=self.headers)
            return self.normalize(check_res)
        else:
            return raw_code_json


    @staticmethod
    def normalize(resp):
        raw_text = resp.json()['choices'][0]['message']['content']
        return json.loads(raw_text[7: len(raw_text) - 3])

ai_service = AIService(zhipu_token, zhipu_uri)
