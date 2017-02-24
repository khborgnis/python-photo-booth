# import the necessary packages
import os
import threading
from TwitterAPI import TwitterAPI
import xml.etree.ElementTree

class TwitterPoster(threading.Thread):
    def __init__(self, config_xml_file, photo_file, msg_text):
        threading.Thread.__init__(self)

        self.photo_file = photo_file
        self.msg_text = msg_text

        root = xml.etree.ElementTree.parse(config_xml_file).getroot()
        for child in root:
            if child.tag == "twitter":
                for type in child:
                    if 'consumer_key' in type.attrib:
                        self.consumer_key = type.attrib['consumer_key'] 
                    elif 'consumer_secret' in type.attrib:
                        self.consumer_secret = type.attrib['consumer_secret'] 
                    elif 'access_token_key' in type.attrib:
                        self.access_token_key = type.attrib['access_token_key'] 
                    elif 'access_token_secret' in type.attrib:
                        self.access_token_secret = type.attrib['access_token_secret'] 

        self.api = TwitterAPI(self.consumer_key,
                              self.consumer_secret,
                              self.access_token_key,
                              self.access_token_secret,
                              auth_type='oAuth1')

    def run(self):
        file = open(self.photo_file, 'rb')
        data = file.read()
        r = self.api.request('statuses/update_with_media',
                        {'status': self.msg_text},
                        {'media': data})
        if r.status_code != 200:
            print(r.json())
        
