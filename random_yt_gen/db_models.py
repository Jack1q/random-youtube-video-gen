from random_yt_gen import db

class YTVidID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vidID = db.Column(db.String, unique=True, nullable=False)
    
    def __init__(self, vid_id):
        self.vidID = vid_id