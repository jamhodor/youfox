#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import re

# grab the api key from a file
with open('notes.txt', 'r') as file:
    my_api_key = re.match(r"(api-key: )([\w|\-]+)\b", file.read()).group(2)


# api = "https://www.googleapis.com/youtube/v3/playlistItems?"
# part = "snippet"
# playlistId = "UUXIJgqnII2ZOINSWNOGFThA"
# maxResults = 50


storage = {}
counter = 1
# initial url, first call returns pageToken
url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet" + "&maxResults=50" + "&playlistId=UUXIJgqnII2ZOINSWNOGFThA" + "&key=" + my_api_key
data = json.loads(requests.get(url).text)
storage.update(data)

print(storage["items"][0]["snippet"]["title"])

page_token = data.get("nextPageToken")

# repeat calls with new pageToken as long there is one
while page_token:
        url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet" + "&maxResults=50" + "&pageToken=" + page_token + "&playlistId=UUXIJgqnII2ZOINSWNOGFThA" + "&key=" + my_api_key
        data = json.loads(requests.get(url).text)
        page_token = data.get("nextPageToken")
        counter += 1

        #print out title first title of api call and number of total items to check progress
        print(data["items"][0]["snippet"]["title"], len(storage["items"]))

        for item in data["items"]:
            storage["items"].append(item)

        # (optional) save current stored data from api calls every 50 calls in case of interruption
        if counter in range(50, 6000, 50):
            print(counter, "saving storage to file")
            with open('current.json', 'w') as file:
                json.dump(storage, file, ensure_ascii=False)


with open('alldata.json', 'w') as file:
    json.dump(storage, file, ensure_ascii=False)

