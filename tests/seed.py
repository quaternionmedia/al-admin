from json import loads

from sqlmodel import Session

from admin.app import init_database
from admin.db import engine
from admin.models import Edl

if __name__ == '__main__':
    init_database()
    with open('seed.json') as f:
        seed = loads(f.read())
    with Session(engine) as session:
        for edl in seed['edls']:
            session.add(Edl(**edl))
        session.commit()
