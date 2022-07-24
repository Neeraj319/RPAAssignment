from sqlalchemy import Column, Float, Integer, String, DateTime, Boolean, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types


Base = declarative_base()

metadata = Base.metadata


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(VARCHAR(length=200), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )
    status = Column(
        ChoiceType(
            choices=(
                ("on queue", "on queue"),
                ("processing", "processing"),
                ("done", "done"),
                ("canceled", "canceled"),
            )
        ),
        nullable=False,
    )
    size = Column(Float, nullable=True)
    length = Column(Float, nullable=True)
    remarks = Column(String(length=100), nullable=True)
