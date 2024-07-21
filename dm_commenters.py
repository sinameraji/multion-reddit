from multion.client import MultiOn
import json
import os
from dotenv import load_dotenv 

load_dotenv()
def dm_profiles():
    client = MultiOn(api_key=os.getenv("MULTION_API_KEY"))


    with open('user_profiles.json', 'r') as file:
        data = json.load(file)
        user_profiles = data['profiles']

    for profile in user_profiles:
        username = profile['username']
        message_cmd = os.getenv("MESSAGE_TEMPLATE")
        message_cmd = message_cmd.replace("{username}", username)
        follow_response = client.browse(
            cmd=message_cmd,
            url=f"https://chat.reddit.com/user/{username}",
            local=True,
        )
        print(f"Message sent to {username}: {follow_response.message}")


