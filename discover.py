from multion.client import MultiOn
import os
from dotenv import load_dotenv
from openai import OpenAI
from scrape_profiles import scrape_profiles 
import json
import random

load_dotenv()


# Load search queries from the list of recommended search queries
with open('search_queries.json', 'r') as file:
    data = json.load(file)
    search_queries = data['queries']

# Randomly select 1 search query
selected_query = random.choice(search_queries).strip()

client = MultiOn(
    api_key=os.getenv("MULTION_API_KEY")
)


retrieve_response = client.retrieve(
    cmd=f"Search for {selected_query} on reddit and pick the first item that shows up. ",
    url="https://reddit.com/",
    fields=["thread_title", "thread_url"],
    max_items=1,
    local=True
)


scraped_post = retrieve_response.data

    

print(f"Scraped post:\n{scraped_post}")


# check if the post is relevant to our startup

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant, skilled in deciding whether a reddit thread is relevant to our startup or not. our startup description: " + os.getenv("STARTUP_DESCRIPTION")},
    {"role": "user", "content": "is this thread title sound relevant to our startup? should we jump in to comment and potentially shill our startup to the commentors? post title: " + scraped_post["thread_title"] + "reply True if it is relevant, False if it is not."}
  ]
)


# if relevant, then scrape the profiles of the commentors under the post and trigger the next steps. else, exit. in the next iterations this can be turned into a recursion with the exit condition being either a finite number of attempts or a success event.

if completion.choices[0].message.content == "True":
    scrape_profiles(scraped_post["thread_url"])
    print(scraped_post["thread_url"])
else:
    print("this search query didn't lead help us find the best thread. try another search query by re-reunning discover.py")