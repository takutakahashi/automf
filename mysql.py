import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import os

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(String, primary_key=True)
    account_type = Column(String)
    name = Column(String)
    amount = Column(Integer)


def init():
  url = "mysql+pymysql://{}".format(os.environ["MYSQL_URL"])
  engine = sa.create_engine(url, echo=True)
  import pdb; pdb.set_trace()
  engine.execute("select * from mysql.user")
  Base.metadata.create_all(engine)

init()
