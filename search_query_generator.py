from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant, skilled in generating search queries that find the latest and hottest threads on reddit."},
    {"role": "user", "content": "generate 50 3-word reddit search queries that help me find the best threads for " + os.getenv("SEARCH_QUERY_SEED") + ". the output contains only the search queries, separated by commas, and nothing else."}
  ]
)

import json

queries = completion.choices[0].message.content.split(",")
with open('search_queries.json', 'w') as file:
    json.dump({"queries": queries}, file)

