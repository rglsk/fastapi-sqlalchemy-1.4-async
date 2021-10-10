from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.tables.coupons import Coupon
from app.models.schema.coupons import InCouponSchema, CouponSchema


class CouponsRepository(BaseRepository[InCouponSchema, CouponSchema, Coupon]):
    @property
    def _in_schema(self) -> Type[InCouponSchema]:
        return InCouponSchema

    @property
    def _schema(self) -> Type[CouponSchema]:
        return CouponSchema

    @property
    def _table(self) -> Type[Coupon]:
        return Coupon
