import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(length=100), nullable=False)

    def __str__(self):
        return f"Publisher {self.id}: ({self.name})"


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    title = sq.Column(sq.String(length=100), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="book")

    def __str__(self) -> str:
        return f"Book {self.id}: ({self.title}, {self.id_publisher})"


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    name = sq.Column(sq.String(length=100), nullable=False)

    def __str__(self) -> str:
        return f"Shop {self.id}: ({self.name})"


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    shop = relationship(Shop, backref="stock")
    book = relationship(Book, backref="stock")

    def __str__(self) -> str:
        return f"Stock {self.id}: ({self.id_Book}, {self.id_Shop}, {self.count})"


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    price = sq.Column(sq.Numeric, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="sale")

    def __str__(self) -> str:
        return f"Sale {self.id}: ({self.price}, {self.date_sale}, {self.id_stock}, {self.count})"


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    DSN = "postgresql://postgres:Pro23242pro@localhost:5432/ORM_db"
    engine = sq.create_engine(DSN)
    create_tables(engine)
