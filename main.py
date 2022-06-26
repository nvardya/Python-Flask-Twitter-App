from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from pullfromtwitter import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rds_user:rds_password@rds_endpoint:3306/mydb'
db = SQLAlchemy(app)

class TweetsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweetid = db.Column(db.Integer)
    authorid = db.Column(db.String(255))
    likecount = db.Column(db.Integer)
    tweet = db.Column(db.String(255))

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))

    def __repr__(self):
        return '<Tweets %r>' % self.id

@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == 'POST':
        user_input = request.form['newtweet']
        new_tweet=TweetsModel(tweet=user_input)
        db.session.add(new_tweet)
        db.session.commit()
        return render_template('mynewtweet.html', new_tweet=new_tweet)
    else:
     return render_template('base.html')

@app.route('/pulltweets')
def pulltweets():
    accesstwitter()
    mytweets = TweetsModel.query.order_by(TweetsModel.id.desc()).all()
    return render_template('pullfromtwitter.html', mytweets=mytweets)


if __name__ == "__main__":
    app.run(debug=True)
