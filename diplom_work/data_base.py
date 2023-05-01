import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from config import db_url_object

engine = sq.create_engine(db_url_object)

metadata = MetaData()
Base = declarative_base()


class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


class elect(Base):
    __tablename__ = 'elect'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    worksheet_id = sq.Column(sq.Integer, primary_key=True)


def add_id_users(profile_id, worksheet_id):
    engine = create_engine(db_url_object)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        to_bd = Viewed(profile_id=profile_id, worksheet_id=\
        worksheet_id)
        session.add(to_bd)
        session.commit()


def add_id_users_elect(profile_id, worksheet_id):
    engine = create_engine(db_url_object)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        to_bd = elect(profile_id=profile_id, worksheet_id=\
        worksheet_id)
        session.add(to_bd)
        session.commit()


def get_id_users(profile_id):
    engine = create_engine(db_url_object)
    list_id = []
    with Session(engine) as session:
        from_bd = session.query(Viewed).filter(Viewed.profile_id\
        ==profile_id).all()
        for item in from_bd:
            list_id.append(item.worksheet_id)
    return list_id


def get_id_users_elect(profile_id=None):
    engine = create_engine(db_url_object)
    list_id = []
    with Session(engine) as session:
        from_bd = session.query(elect).filter(elect.profile_id\
        ==profile_id).all()
        for item in from_bd:
            list_id.append(item.worksheet_id)
    return list_id


def create_tables(engine):
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables(engine)
    
    