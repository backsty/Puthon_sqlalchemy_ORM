import json
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Shop, Stock, Sale


DSN = "postgresql://postgres:Pro23242pro@localhost:5432/ORM_db"
engine = sq.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/data_test_3.json', 'r', encoding='utf-8') as db:
    data = json.load(db)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()

publ_name = input('Ведите имя писателя или id для вывода: ')
if publ_name.isnumeric():
    for c in session.query(Publisher).filter(Publisher.id == int(publ_name)).all():
        print(c)
else:
    for c in session.query(Publisher).filter(Publisher.name.like(f'%{publ_name}%')).all():
        print(c)


def output_full_info():
    query = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale).join(Publisher).join(
        Stock).join(Shop).join(Sale)
    return query


session.commit()
