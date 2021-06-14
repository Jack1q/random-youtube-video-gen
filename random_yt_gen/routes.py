from threading import Thread

from random_yt_gen import app
from random_video_generator import RandomVideoGenerator, RandomVideoCrawler
from flask import render_template, url_for, redirect

@app.route('/')
def main():
    video_id = RandomVideoGenerator().get_random_video().video_id
    return render_template(
        'videopage.html',
        video_id = video_id
    )

# setup a workflow to run this every few hours or so
@app.route('/crawl')
def background_crawl():
    run_crawler()
    return redirect(url_for('main'))

def run_crawler():
    thread = Thread(target=async_crawl_for_videos)
    thread.start()
    return thread

def async_crawl_for_videos():
    with app.app_context():
        crawler = RandomVideoCrawler()
        crawler.store_video_ids()