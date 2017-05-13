import os

POST_DIR = os.path.abspath("../_posts")

for post in os.listdir(POST_DIR):
    full_path = os.path.join(POST_DIR, post)
    with open()