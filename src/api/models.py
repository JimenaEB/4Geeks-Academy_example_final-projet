import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import VARCHAR, ARRAY
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR, unique=True, nullable=False)
    first_name = db.Column(db.VARCHAR, unique=False, nullable=False)
    last_name = db.Column(db.VARCHAR, unique=False, nullable=False)
    _password = db.Column(db.VARCHAR, unique=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, unique=False, nullable=False)  
    has_ad = db.relationship('Ad', backref='person',lazy=True)

    def __repr__(self):
        return f'User {self.email}'

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(
                password, 
                method='pbkdf2:sha256', 
                salt_length=16
            )

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email):
        user = cls.query.filter_by(email=email).one_or_none()
        return user

    @classmethod
    def get_by_id(cls, id):
        user = cls.query.get(id)
        return user

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        return self

    def delete(self):
        self.is_active = False
        db.session.commit()

    def reactive_account(self, first_name, last_name, password):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_active = True
        db.session.commit()


class Ad_category(str, enum.Enum):
    option_1 = "To Sell"
    option_2 = "I want"
    option_3 = "Exchange"

    @classmethod
    def get(cls):
        return [cls.option_1, cls.option_2, cls.option_3]


class Ad(db.Model):
    __tablename__='ad'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR, unique=False, nullable=False)
    text = db.Column(db.VARCHAR, unique=False, nullable=False)
    #pictures = db.Column(db.ARRAY(db.VARCHAR), unique=True, nullable=True)
    category = db.Column(db.Enum(Ad_category), nullable=False)
    price = db.Column(db.Float, unique=False, nullable=True)
    is_active = db.Column(db.Boolean, default=True, unique=False, nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)

    def __repr__(self):
        return f'Ad {self.title}'
