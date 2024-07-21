# Redditoor

using multion to find all the commenters under a given reddit post, and DMing a message to them.

## order of execution
1. login to reddit manually on the default browser
2. create a .env file with MULTION_API_KEY, MESSAGE_TEMPLATE,and POST_URL
3. run scrape.py to scrape reddit commenters under the post
4. run dm.py to send dms to scraped users

## work in progress
1. search_query_generator.py (done): creating a search query generator that can generates many search queries given a seed phrase
2. discover.py (in progress): use the AI generated search queries to find the hottest posts


## next iterations
* use anon.com to programmatically log the user into reddit
* have agents that DM commentors and book calls or get them to sign up for a product
* slack notifications for me and my team when there's an opportunity to participate in a high signal thread

## open to collab
submit a PR, lets make this better!