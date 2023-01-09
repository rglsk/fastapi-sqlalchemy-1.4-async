from unittest import mock

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.repositories.coupons import CouponsRepository
from app.models.schema.coupons import InCouponSchema

pytestmark = pytest.mark.anyio


async def test_coupon_create(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:
    coupons_repository = CouponsRepository(db_session)
    payload = {
        "code": "PIOTR",
        "init_count": 100,
    }

    response = await async_client.post("/v1/coupons/", json=payload)
    coupon = await coupons_repository.get_by_id(response.json()["id"])

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "code": payload["code"],
        "init_count": payload["init_count"],
        "remaining_count": payload["init_count"],
        "id": str(coupon.id),
    }


async def test_coupon_get_by_id(
    async_client: AsyncClient, db_session: AsyncSession
) -> None:
    payload = {
        "code": "PIOTR",
        "init_count": 100,
    }
    coupons_repository = CouponsRepository(db_session)
    coupon = await coupons_repository.create(InCouponSchema(**payload))

    response = await async_client.get(f"/v1/coupons/{coupon.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "code": payload["code"],
        "init_count": payload["init_count"],
        "remaining_count": payload["init_count"],
        "id": mock.ANY,
    }
