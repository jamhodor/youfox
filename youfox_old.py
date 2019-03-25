#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import json
import xml.etree.ElementTree as ET
import datetime
import re

def start_xml():
    root            = ET.Element("root")
    source          = ET.SubElement(root, "source") # xml[0]
    source_id       = ET.SubElement(source, "id")
    source_name     = ET.SubElement(source, "name")
    video_channel   = ET.SubElement(root, "channelid") # xml[1]
    video_list      = ET.SubElement(video_channel, "videos") # xml[1][0]
    tree            = ET.ElementTree(root)
    return tree

def add_video(element):
    video = ET.SubElement(element, "video")
    title = ET.SubElement(video, "title")
    title.text = parsed_json['items'][i]['snippet']['title']
    description = ET.SubElement(video, "description")
    description.text = re.match(r".*", parsed_json['items'][i]['snippet']['description']).group()
    timestamp = ET.SubElement(video, "timestamp")
    timestamp.attrib = {"timezone":"UTC"}
    timestamp.text = parsed_json['items'][i]['snippet']['publishedAt']
    id = ET.SubElement(video, "id")
    id.text = parsed_json['items'][i]['snippet']['resourceId']['videoId']
    return

def get_xml():
    if os.path.isfile('foxml.xml') is True:
        tree = ET.parse('foxml.xml')
        return tree
    else:
        tree = start_xml()
        return tree


if __name__ == '__main__':

    tree = get_xml()
    root = tree.getroot()
    counter = 0
    id_list = set([vid.text for vid in root.iter('id')])

    #gets api-key from a file which is kept out of git
    with open('notes.txt', 'r') as file:
        my_api_key = re.match(r"(api-key: )(\w+)\b", file.read()).group(2)

    max_results = 5
    pages = 5


    for i in range(0, pages):

        if  i == 0:
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={max_results}&playlistId=UUXIJgqnII2ZOINSWNOGFThA&key={my_api_key}"
            data = requests.get(url).text
            parsed_json = json.loads(data)

            for i in range(0, max_results):
                if parsed_json['items'][i]['snippet']['resourceId']['videoId'] in id_list:
                    print("duplicate found, abort")
                    break
                add_video(root[1][0])
                counter += 1


            page_token = "&pageToken=" + str(parsed_json['nextPageToken'])

        else:
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults={max_results}" + page_token + f"&playlistId=UUXIJgqnII2ZOINSWNOGFThA&key={my_api_key}"
            data = requests.get(url).text
            parsed_json = json.loads(data)
            page_token = "&pageToken=" + str(parsed_json['nextPageToken'])

            for i in range(0, max_results):
                if parsed_json['items'][i]['snippet']['resourceId']['videoId'] in id_list:
                    print("duplicate found, abort")
                    break
                add_video(root[1][0])
                counter += 1

    print(str(counter))

    root[1][0][:] = sorted(root[1][0], key=lambda video: datetime.datetime.strptime(video[2].text, '%Y-%m-%dT%H:%M:%S.000Z'), reverse=True)

    tree.write('foxml.xml')
