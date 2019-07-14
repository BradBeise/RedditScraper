import praw
import time
import smtplib
import ssl
import Config


reddit = praw.Reddit(client_id=Config.client_id,
                     client_secret=Config.client_secret,
                     user_agent=Config.user_agent,
                     username=Config.username,
                     password=Config.password)

subreddit = reddit.subreddit('buildapcsales')

id_list = []

loop = True
while loop:
    hours = 0
    message = ""
    for submission in subreddit.new(limit=10):
        if '[SSD]' in submission.title:
            if submission.id not in id_list:
                message += submission.title + '\n'
                message += submission.url + '\n\n'
                id_list.append(submission.id)

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(Config.email_address, Config.password)
        server.sendmail(Config.email_address, Config.email_address, message)

    hours += 0.5
    if hours == 24:
        id_list = []
    time.sleep(1800)




