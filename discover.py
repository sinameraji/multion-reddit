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

# search reddit for posts that match the selected query
create_response = client.sessions.create(
    url="https://reddit.com",
    local=True
)

session_id = create_response.session_id


status = "CONTINUE"

while status == "CONTINUE":
    step_response = client.sessions.step(
        session_id=session_id,
        cmd=f"Search for {selected_query}"
    )
    status = step_response.status


scraped_posts = []
has_more = True
page = 1

while has_more:
    retrieve_response = client.retrieve(
        session_id=session_id,
        cmd="get the threads that have the most upvotes and are less than 1 week old",
        fields=["thread_title", "thread_url"],
        scroll_to_bottom=True,
        render_js=True
    )
    scraped_posts.extend(retrieve_response.data)
    print(f"Scraped page {page} with {len(retrieve_response.data)} posts")
    page += 1
    step_response = client.sessions.step(
        session_id=session_id,
        cmd="Click the 'Next' button to go to the next page."
    )
    has_more = "last page" not in step_response.message

print(f"Scraped {len(scraped_posts)} posts:\n{scraped_posts}")


# check if the post is relevant to our startup

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant, skilled in deciding whether a reddit thread is relevant to our startup or not. our startup description: " + os.getenv("STARTUP_DESCRIPTION")},
    {"role": "user", "content": "is this thread title sound relevant to our startup? should we jump in to comment and potentially shill our startup to the commentors? post title: " + scraped_posts[0]["thread_title"] + "reply True if it is relevant, False if it is not."}
  ]
)

# if relevant, then scrape the profiles of the commentors under the post and trigger the next steps. else, exit. in the next iterations this can be turned into a recursion with the exit condition being either a finite number of attempts or a success event.

if completion.choices[0].message.content == "True":
    scrape_profiles(scraped_posts[0]["thread_url"])
else:
    print("NO")