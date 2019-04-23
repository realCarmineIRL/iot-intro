from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml

with open('config.yml', 'r') as c:
    conf = yaml.load(c)

db_url = conf['DB']

# basic sqlalchemy use.. this will create the db if not exists and will open connections to the db
engine = create_engine(db_url, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()
