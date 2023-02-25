import feedparser
import requests
import time
import shelve
# URL of the RSS feed
feed_url = # you can get it in your Upwork feed

# Slack webhook URL
slack_webhook_url = # you need to create an app in Slack first and then get the webhook's URL of the app

# Open the database to store the unique identifiers of already sent posts
db = shelve.open('sent_posts')
response = requests.get(feed_url)
print(response.status_code) # just to make sure connection was successfully done. Should print code 200

try:
    sent_posts = db['sent_posts']
except KeyError:
    sent_posts = set()

while True:
    # Fetch the RSS feed
    feed = feedparser.parse(feed_url)

    # Loop through the entries in the RSS feed
    for entry in feed.entries:
        # Check if the post has already been sent
        if entry.id not in sent_posts:
            # Send a notification to Slack
            payload = {
                'text': entry.title,
                'attachments': [{
                    'title': entry.title,
                    'title_link': entry.link,
                    'text': entry.summary
                }]
            }
            requests.post(slack_webhook_url, json=payload)
            # Add the post's unique identifier to the set of sent posts
            print(entry.id) # will print ids of jobs
            sent_posts.add(entry.id)

    # Wait for 30 seconds before fetching the RSS feed again
    time.sleep(5) # check Upwork documentation for max calls per minute. 
    # Save the set of sent posts to the database
    db['sent_posts'] = sent_posts
    # Close the database
    #db.close() # if you want to close the db. you can also just delete the db manually. it will be created in the same folder

