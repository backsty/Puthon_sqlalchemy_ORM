import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
from models import Publisher, Book, Shop, Stock, Sale


DSN = "postgresql://postgres:Pro23242pro@localhost:5432/testORM_db"
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def load_publisher_from_json():
    with open('fixtures/data_test_3.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    publishers = {}
    for entry in data:
        if entry['model'] == 'publisher':
            id = entry['pk']
            name = entry['fields']['name']
            if str(id) not in publishers:
                publishers[name.lower()] = id
                publishers[str(id)] = name
    return publishers


def info_sale():
    """1 вариант реализации выборки!"""
    publishers = load_publisher_from_json()
    print("Доступные id и имена издателей -> ")
    for id in range(1, 5):
        name = publishers.get(str(id))
        if name:
            print(f"{id}: {name}")

    input_name_or_id = input("Введите id или name одного из издателей: ")

    if input_name_or_id.isdigit():
        id = int(input_name_or_id)
        if id not in publishers.values():
            print("ID введён неверно!")
            return
    else:
        id = publishers.get(input_name_or_id.lower())
        if id is None:
            print("ID или name введены некорректно!")
            return
    print(f"Выбранный ID/name издателя: {id}")

    query = session.query(Book).join(Stock).join(Shop).join(Sale).join(Publisher).filter(Publisher.id == id).all()
    print(f"Number of records retrieved: {len(query)}")
    data = {}
    for q in query:
        book_title = q.title
        data.setdefault(book_title, [])
        for st in q.stock:
            shop_name = st.shop.name
            for c, pr in enumerate(st.sale):
                price = pr.price
                data[book_title].append({'shop_name': shop_name, 'price': price, 'date_sale': pr.date_sale})
    for book in data.keys():
        title = book
        for item in data[title]:
            shop_name = item['shop_name']
            price = item['price']
            date_sale = item['date_sale']
            print(title.ljust(20) + '|' + shop_name.ljust(15) + '|' + str(price).ljust(10) + '|' + (date_sale).strftime('%m/%d/%Y').ljust(30))


def get_shops(input_name_or_id):
    """2 вариант реализации выборки!"""
    query = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale)\
        .select_from(Book)\
        .join(Stock, Book.id == Stock.id_book)\
        .join(Sale, Stock.id == Sale.id_stock)\
        .join(Publisher, Book.id_publisher == Publisher.id)
    if input_name_or_id.isdigit():
        query_ = query.filter(Publisher.id == input_name_or_id)
    else:
        query_ = query.filter(Publisher.name == input_name_or_id)
    query_result = query_.all()
    for title, name, price, count, date_sale in query_result:
        print(title.ljust(20) + '|' + name.ljust(15) + '|' + str(price).ljust(10) + '|' + (date_sale).strftime('%m/%d/%Y').ljust(30))


if __name__ == '__main__':
    input_name_or_id = input("Введите id или name одного из издателей: ")
    get_shops(input_name_or_id)
    print(load_publisher_from_json())
    info_sale()

session.close()


"""Для будущей реализации выборки!"""
# def create_db(data):
#     session = Session()
#     for item in data:
#         if item['model'] == 'publisher':
#             publisher = Publisher(
#                 name=item['fields']['name'],
#                 id=item['pk']
#             )
#             session.add(publisher)
#             print(publisher)
#
#         elif item['model'] == 'book':
#             book = Book(
#                 id=item['pk'],
#                 title=item['fields']['title'],
#                 id_publisher=item['fields']['id_publisher']
#             )
#             session.add(book)
#             print(book)
#
#         elif item['model'] == 'shop':
#             shop = Shop(
#                 id=item['pk'],
#                 name=item['fields']['name']
#             )
#             session.add(shop)
#             print(shop)
#
#         elif item['model'] == 'stock':
#             stock = Stock(
#                 id=item['pk'],
#                 id_shop=item['fields']['id_shop'],
#                 id_book=item['fields']['id_book'],
#                 count=item['fields']['count']
#             )
#             session.add(stock)
#             print(stock)
#
#         elif item['model'] == 'sale':
#             sale = Sale(
#                 id=item['pk'],
#                 price=item['fields']['price'],
#                 date_sale=item['fields']['date_sale'],
#                 count=item['fields']['count'],
#                 id_stock=item['fields']['id_stock']
#             )
#             session.add(sale)
#             print(sale)
#         session.commit()
#     session.close()