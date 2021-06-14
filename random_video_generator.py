from youtube_api import YouTubeDataAPI
from random_yt_gen import db
from random_yt_gen.db_models import YTVidID

import os
import sqlite3
import random

# Word generation functions
#################################################################
class RandomWordGenerator():
    # Returns random line from a .txt file of words
    def random_line(self, file): 
        with open(file) as f:
            return random.choice(f.readlines()).strip()

    # Generates random words to feed YT Crawler
    def get_random_word(self):
        file = 'words/' + ['adjectives.txt','adverbs.txt','nouns.txt','verbs.txt'][random.randint(0,3)]    
        return self.random_line(file)

    # generates sequence of random length of random words to be input
    def get_random_sequence_of_words(self):
        number_of_words = random.randint(1,4) # set from 1-4, too long could produce odd results
        return ' '.join([self.get_random_word() for x in range(number_of_words)])
#################################################################

# Class to store individual video object data to be returned to front end web app
class YTVideo:
    def __init__(self, video_id):
        self.video_id = video_id

# The crawler loads the database with video ids that can be called upon
# by the randomizer. This is done to reduce the amount of API calls because
# the daily quotas are fairly limited for YouTube's Data API.
# Thinking of adding a function to run the crawler for 500 new videos
# every day at a specific time. 
class RandomVideoCrawler:

    def __init__(self):
        try:
            self.yt_api = YouTubeDataAPI(self.get_api_key())
        except:
            self.yt_api = None

    def get_api_key(self):
        return os.getenv('GOOGLE_API_KEY') 

    def collect_video_sample_data(self):
        while True:
            try:
                randomized_sequence = RandomWordGenerator().get_random_sequence_of_words()
                return self.yt_api.search(q=randomized_sequence, max_results=70) # higher max = longer wait, but greater randomization
            except:
                continue
        
    # Grabs sample of videos ids, stores them all into table
    def store_video_ids(self):
        video_sample = self.collect_video_sample_data()
        found = [YTVidID(video['video_id']) for video in video_sample]
        print(found)
        db.session.add_all(found)
        db.session.commit()
    
    # Returns all stored ids as a list of strings
    def read_ids(self):
        try:
            return [video.vidID for video in YTVidID.query.all()]
        except:
            print('Ids could not be read.')

class RandomVideoGenerator:
    # generates random video based on words
    def get_random_video(self):
        random_sample = RandomVideoCrawler().read_ids()
        print(random_sample)
        raw_choice_data = random.choice(random_sample)
        return YTVideo(video_id=raw_choice_data)

if __name__ == '__main__':
    c = RandomVideoCrawler()
    if input('Would you like to add videos to the database? Y/N ') == 'Y':
        c.store_video_ids()
    all_ids = c.read_ids()
    print(f'current list of {len(all_ids)} ids:')
    print(all_ids)
