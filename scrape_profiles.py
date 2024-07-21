from multion.client import MultiOn
import os
import json
from dm_commenters import dm_profiles
from dotenv import load_dotenv



def scrape_profiles(thread_url=None):
    if not thread_url:
        load_dotenv()
        thread_url = os.getenv("POST_URL")
    
    client = MultiOn(api_key=os.getenv("MULTION_API_KEY"))


    create_response = client.sessions.create(
        url=thread_url,
        local=True
    )

    session_id = create_response.session_id

    status = "CONTINUE"

    while status == "CONTINUE":
        step_response = client.sessions.step(
            session_id=session_id,
            cmd="go to this reddit post and see all the replies."
        )
        status = step_response.status

    scraped_profiles = []
    has_more = True
    page = 1

    while has_more:
        retrieve_response = client.retrieve(
            session_id=session_id,
            cmd="Get all commentors'profiles with their reddit username",
            fields=["username"],
            scroll_to_bottom=True,
            render_js=True
        )
        scraped_profiles.extend(retrieve_response.data)
        print(f"Scraped page {page} with {len(retrieve_response.data)} profiles")
        page += 1
        step_response = client.sessions.step(
            session_id=session_id,
            cmd="keep scrolling down to see more comments or click View All Comments."
        )
        if (len(scraped_profiles) > 5):
            has_more = False

    print(f"Scraped {len(scraped_profiles)} profiles:\n{scraped_profiles}")



    user_profiles = []
    seen_usernames = set()
    for profile in scraped_profiles:
        username = profile['username']
        if username not in seen_usernames:
            seen_usernames.add(username)
            user_url = f"https://www.reddit.com/user/{username}"
            user_profiles.append({'username': username, 'profile_url': user_url})
    with open('user_profiles.json', 'w') as json_file:
        json.dump({'profiles': user_profiles}, json_file, indent=4)

    print("User profiles JSON file has been created.")

    dm_profiles(user_profiles)

scrape_profiles()