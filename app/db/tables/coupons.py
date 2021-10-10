from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Coupon(Base):
    __tablename__ = "coupon"

    code = Column(String, nullable=False, unique=True)
    init_count = Column(Integer, nullable=False)
    remaining_count = Column(Integer, nullable=False)
