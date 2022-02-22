import os
import flask 
from flask_sqlalchemy import SQLAlchemy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URL"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class TvShow(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    new_tvshow = db.Column(db.String(100), nullable = False)
    alreadyListed = db.Column(db.Boolean)

db.create_all()
no_tv = TvShow(new_tvshow = None, alreadyListed = True)
db.session.add(no_tv)
db.session.commit()

@app.route("/", methods=["GET", "POST"])
def index():
        if flask.request.method == "POST":
            data = flask.request.form
            print(data)
            new_tvshow = TvShow(
                tv_show = data["tv_show"], 
                alreadyListed = ("alreadyListed" in data),
            )
            db.session.add(new_tvshow)
            db.session.commit()

        tv = TvShow.query.all()
        num_tvshows = len(tv)
        return flask.render_template (
             "index.html",
            num_tvshows = num_tvshows,
            tv = tv,
        )
        
app.run(debug=True)
