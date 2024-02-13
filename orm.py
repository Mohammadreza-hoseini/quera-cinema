import mysql.connector as my_sql
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func

import mysql.connector as my_sql



cnx = my_sql.connect(
            user='root', 
            password='123456', 
            database='mysql',
            host="172.17.0.2", 
            port=3306
        )
mycursor = cnx.cursor()

try:
    mycursor.execute(
    
    )
except:
    pass


engine = create_engine('mysql+mysqlconnector://root:123456@172.17.0.2/test')


Base = declarative_base()


class Movie(Base):
    __tablename__ = 'Movie'

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    average_rate = Column(DECIMAL(15, 5), default=-1.00000)
    on_screen_count = Column(Integer, nullable=False)
    age_limit = Column(Integer, nullable=False)
    price = Column(String(255), nullable=False)


class Theater(Base):
    __tablename__ = 'Theater'

    id = Column(String(36), primary_key=True)
    capacity = Column(Integer, nullable=False)
    average_rate = Column(DECIMAL(15, 5), default=-1.00000)
    name = Column(String(255), nullable=False, unique=True)


class Schedule(Base):
    __tablename__ = 'Schedule'

    id = Column(String(36), primary_key=True)
    movie_name = Column(String(255), nullable=False)
    theater_name = Column(String(255), nullable=False)
    on_screen_time = Column(TIMESTAMP, nullable=False)
    movie = relationship("Movie", backref="schedules")
    theater = relationship("Theater", backref="schedules")


class Sit(Base):
    __tablename__ = 'Sit'

    id = Column(String(36), primary_key=True)
    theater_id = Column(String(36), ForeignKey('Theater.id'), nullable=False)
    status = Column(Enum('0', '1'), default='0')


class User(Base):
    __tablename__ = 'User'

    id = Column(String(36), primary_key=True)
    avatar = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    birth_date = Column(TIMESTAMP, nullable=False)
    phone_number = Column(String(255), default='None', unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    register_date = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)
    subscription = Column(Enum('2', '3', '4'), default='2')
    bought_subscription_date = Column(TIMESTAMP)
    role = Column(Enum('admin', 'user'), default='user')
    logged_in = Column(Integer, default=0)


class BankAccount(Base):
    __tablename__ = 'BankAccount'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('User.id'), nullable=False)
    amount = Column(DECIMAL, nullable=False)
    cvv2 = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    password = Column(String(255), nullable=False)
    card_number = Column(Integer, nullable=False)
    logged_in = Column(Integer, default=0)


class Comment(Base):
    __tablename__ = 'Comment'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('User.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    body = Column(String(255), nullable=False)
    p_comment_id = Column(String(255))
    movie_name = Column(String(255), ForeignKey('Movie.name'), nullable=False)
    movie = relationship("Movie", backref="comments")
    parent_comment = relationship("Comment", remote_side=[id])


class MovieRateTable(Base):
    __tablename__ = 'MovieRateTable'

    movie_id = Column(String(36), ForeignKey('Movie.id'), primary_key=True)
    user_id = Column(String(36), ForeignKey('User.id'), primary_key=True)
    rate = Column(Enum('1', '2', '3', '4', '5'), nullable=False)


class TheaterRateTable(Base):
    __tablename__ = 'TheaterRateTable'

    user_id = Column(String(36), ForeignKey('User.id'), primary_key=True)
    theater_id = Column(String(36), ForeignKey('Theater.id'), primary_key=True)
    rate = Column(Enum('1', '2', '3', '4', '5'), nullable=False)


class Ticket(Base):
    __tablename__ = 'Ticket'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('User.id'), nullable=False)
    schedule_id = Column(String(36), ForeignKey('Schedule.id'), nullable=False)
    sit_id = Column(String(36), ForeignKey('Sit.id'), nullable=False)
    price = Column(DECIMAL(15, 5), nullable=False)
    bought_time = Column(TIMESTAMP, default=func.current_timestamp())


class Wallet(Base):
    __tablename__ = 'Wallet'

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('User.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    amount = Column(DECIMAL, nullable=False)


Base.metadata.create_all(engine)
