# Python-Flask-Twitter-App

This project is an enhancment of my oriingal Python/MySQL/Twitter project. This project was built using the Python Flask framework. This document will call out the important aspects of the Flask framework that were incorporated in creating this basic web app

# 1. SQLAlchemy
The `SQLAlchemy` extension for Flask was a major differenc in building this application. Connecting to my AWS hosted RDS could be executed with a single line of code:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rds_user:rds_password@rds_endpoint:3306/mydb'
```
Additionally, this project took adavantage of the `Model` concept within this Python framework. 2 Models were initially created via a Python shell. These models are used each time the program is executed:
```python
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
```

# 2. App Routing
Flask's `@app.route`functionality makes it very easy to build a simple web application. It essentially maps a specified URL to a function. Additionally, POST and GET methods can be defined within the routes if different lines of code need to be executed. Below is the homepage route used for this project:
```python
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
```
