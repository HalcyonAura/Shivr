from flask import Flask, redirect, render_template, session, url_for#send_from_directory
from os import environ as env
from database import Database
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from geopy.distance import great_circle

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

db = Database()

# could this be an init function?
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# could this be a file
@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# figure out what session is, where it's declared if at all
# randomize 3 sharks to pass into prevcards (why is it named this, 
#   change to preview cards)
# generate new bios for all 417 records, so how we optimize that? 
# home page that shows diff view for logged in vs not, kinda like 
#   fb when you haven't logged in
@app.route('/')
def index():
    sharks = db.get_n_sharks(3)
    return render_template('main_page.html', sharks=sharks, session=session)

# does this show all sharks or just one?
@app.route('/card')
def card():
    sharks = db.get_all_sharks()
    return render_template('card.html', sharks=sharks)

# what's even happening here?
'''@app.route('/dbtest/<string:shark_id>')
def post(shark_id):
    shark = db.get_all_sharks()    
    return render_template('rendertest.html', shark=shark)'''

def get_distance(id1, id2):
    shark1 = db.get_shark(id1)
    shark1_loc = (shark1[11], shark1[12])
    shark2 = db.get_shark(id2)
    shark2_loc = (shark2[11], shark2[12])
    distance = great_circle(shark1_loc, shark2_loc).miles
    return distance