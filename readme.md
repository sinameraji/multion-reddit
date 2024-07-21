# Redditoor

using multion to find all the commenters under a given reddit post, and DMing a message to them.

## order of execution
1. login to reddit manually on the default browser
2. create a .env file with MULTION_API_KEY, MESSAGE_TEMPLATE, POST_URL and SEARCH_QUERY_SEED (search query seed for auto generating many search queries)
3. run search-query-generator.py to generate search queries
4. run discover.py to randomly select a search query and scrape the hottest latest reddit posts about it (or manually assign a reddit post to POST_URL)
5. run scrape.py to scrape reddit commenters under the post
6. run dm.py to send dms to scraped users

## next iterations
* use anon.com to programmatically log the user into reddit
* have agents that DM commentors and book calls or get them to sign up for a product
* slack notifications for me and my team when there's an opportunity to participate in a high signal thread

## open to collab
submit a PR, lets make this better!