import logging
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db import get_db
from app.db.repositories.coupons import CouponsRepository
from app.models.schema.coupons import OutCouponSchema, InCouponSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OutCouponSchema)
async def create_coupon(
    payload: InCouponSchema, db: AsyncSession = Depends(get_db)
) -> OutCouponSchema:
    coupons_repository = CouponsRepository(db)
    coupon = await coupons_repository.create(payload)
    return OutCouponSchema(**coupon.dict())


@router.get(
    "/{coupon_id}", status_code=status.HTTP_200_OK, response_model=OutCouponSchema
)
async def create_coupon(
    coupon_id: UUID, db: AsyncSession = Depends(get_db)
) -> OutCouponSchema:
    coupons_repository = CouponsRepository(db)
    coupon = await coupons_repository.get_by_id(coupon_id)
    return OutCouponSchema(**coupon.dict())
