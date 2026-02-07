# import requests
#
# headers = {
#     "Authorization": "86d89750b1fb4c479c191674523286a4.dBmRMDvC85l0RUee",
# }
#
# body = {
#     'model': 'glm-4.7',
#     'messages': [
#         {
#             'role': 'user',
#             'content': '使用html实现加法计算器，回答只包含代码，不要包含别的内容！！！'
#         }
#     ]
# }
#
# uri = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
#
# response = requests.post(uri, headers=headers, json=body)
# print(response.json()['choices'][0]['content'])
from app.backend.services.ai_service import ai_service

# print('ssss55'.replace('5', '4'))

print(ai_service.gen_code('实现计数器'))
