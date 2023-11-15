from flask import Flask, redirect, render_template, session, url_for#send_from_directory
import json
from os import environ as env
import sqlite3

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all_sharks():
    conn = get_db_connection()
    shark = conn.execute('SELECT * FROM sharks').fetchall()
    conn.close()
    return shark

def get_n_sharks(n):
    conn = get_db_connection()
    # idx 0: name, 1: image
    sharks = conn.execute('SELECT name, image FROM sharks LIMIT ?', (n,)).fetchall()
    conn.close()
    return sharks

def get_shark(shark_id):
    conn = get_db_connection()
    shark = conn.execute('SELECT * FROM sharks WHERE id = ?',
                        (shark_id,)).fetchone()
    conn.close()
    if shark is None:
        print('No Sharks Here.')
    return shark

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
# also add bios, put bios in db
# generate new bios for all 417 records, so how we optimize that? 
# home page that shows diff view for logged in vs not, kinda like 
#   fb when you haven't logged in
@app.route('/')
def index():
    sharks = get_n_sharks(3)
    return render_template('main_page.html', sharks=sharks, session=session)

# does this show all sharks or just one?
@app.route('/card')
def card():
    sharks = None
    with open('static/sharkdata.json', 'r') as f:
        sharks = json.load(f)
        sharks = sharks['features']
        print(sharks[0]['properties'])
    return render_template('card.html', sharks=sharks)

# what's even happening here?
'''@app.route('/dbtest/<string:shark_id>')
def post(shark_id):
    shark = get_all_sharks()    
    return render_template('rendertest.html', shark=shark)'''