"""Script to keep me posted on new anime episodes."""
import os
import os
import yaml
import hashlib
import smtplib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from optparse import OptionParser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from email.message import EmailMessage
from flask import Flask, json, render_template

app = Flask(__name__)
app.secret_key = hashlib.sha1(os.urandom(128)).hexdigest()

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
f = open(os.path.join(THIS_DIR, 'config.yaml'))
config = yaml.safe_load(f)
f.close()

db = create_engine(
    f"postgresql+psycopg2://{config['db_username']}:{config['db_password']}@{config['db_host']}:{config['db_port']}/{config['db_name']}"
)

Base = declarative_base()
Base.metadata.reflect(db)
Session = sessionmaker(bind=db)
session = Session()


class Anime(Base):
    """Class for translation table."""

    __table__ = Base.metadata.tables[config['table_name']]


@app.route("/crawler", methods=['GET'])
def crawler():
    """Function to crawl and update anime schedule."""
    updated = {}
    for anime in session.query(Anime).all():
        if anime.active:
            _url = f'{anime.base_url}/{anime.anime_url}-episode-{anime.episode + 1}'
            r = requests.get(_url)
            if r.status_code == 200:
                data = r.text
                soup = BeautifulSoup(data)
                anime.last_refreshed_at = datetime.now().isoformat()
                if soup.find_all('div', {'class': 'anime_video_body_watch'}):
                    anime.episode = anime.episode + 1
                    anime.updated_at = datetime.now().isoformat()
                    updated[anime.name] = _url

    message = ''

    if updated:
        for anime in updated.keys():
            message += f'New episode of {anime} is published:\n {updated[anime]}\n\n'

        msg = EmailMessage()
        msg['Subject'] = 'New anime episodes'
        msg['From'] = config['fromaddr']
        msg['To'] = config['toaddr']
        msg.add_header('Content-Type', 'text')
        msg.set_payload(message)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config['fromaddr'], config['password'])
        text = msg.as_string()
        server.sendmail(config['fromaddr'], config['toaddr'], text)

    session.commit()
    return "Anime watch updated successfully...!"


@app.route("/", methods=['GET'])
def index():
    """Root funciton."""
    _list = []
    for anime in session.query(Anime).all():
        _dict = anime.__dict__
        _dict.pop('_sa_instance_state')
        _dict['url'] = f'{anime.base_url}/{anime.anime_url}-episode-{anime.episode}'
        _list.append(_dict)
    return render_template('index.html', data=json.dumps(_list))

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "-p",
        "--port",
        dest="port",
        help="Port on which the app will run",
        default=5000)
    (options, args) = parser.parse_args()
    app.run(host='0.0.0.0', debug=True, port=int(options.port))
