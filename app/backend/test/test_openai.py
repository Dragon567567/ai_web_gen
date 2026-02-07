from openai import OpenAI
import os

api_key = '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'

client = OpenAI(api_key=api_key)

completion = client.completions.create(model='gpt-3.5-turbo', prompt="1+1=？")
print(completion.choices[0].text)
print(dict(completion).get('usage'))
print(completion.model_dump_json(indent=2))
