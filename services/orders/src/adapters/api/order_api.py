from typing import List

from fastapi import APIRouter, Depends, HTTPException
from src.adapters.dependencies import get_order_service
from src.application.dto.order_dto import (
    EstimatedTimeUpdate,
    OrderCreate,
    OrderResponse,
    OrdersPaginatedResponse,
    OrderStatusUpdate,
    PaginationMeta,
)
from src.application.dto.serializers import serialize_order
from src.application.services.order_service import OrderService
from src.domain.entities.customer_entity import CustomerEntity
from src.domain.entities.order_entity import OrderStatus
from src.domain.entities.order_item_entity import OrderItemEntity
from src.domain.exceptions import EntityNotFound, InvalidEntity

router = APIRouter()


@router.post("/orders/", tags=["Orders"], response_model=OrderResponse)
async def create_order(
    order: OrderCreate, service: OrderService = Depends(get_order_service)
):
    customer_entity = CustomerEntity(
        name=order.customer.name,
        email=order.customer.email,
        phone_number=order.customer.phone_number,
    )
    order_items = [
        OrderItemEntity(product_sku=item.product_sku, quantity=item.quantity)
        for item in order.order_items
    ]
    created_order = await service.create_order(customer_entity, order_items)
    return serialize_order(created_order, created_order.total_amount)


@router.get(
    "/orders/", tags=["Orders"], response_model=OrdersPaginatedResponse
)
async def read_orders(
    current_page: int = 1,
    records_per_page: int = 10,  # Default to 10 records per page
    service: OrderService = Depends(get_order_service),
):
    orders, current_page, records_per_page, number_of_pages, total_records = (
        await service.list_orders_paginated(current_page, records_per_page)
    )

    response = OrdersPaginatedResponse(
        orders=[
            serialize_order(order, await service.calculate_order_total(order))
            for order in orders
        ],
        pagination=PaginationMeta(
            current_page=current_page,
            records_per_page=records_per_page,
            number_of_pages=number_of_pages,
            total_records=total_records,
        ),
    )

    return response


@router.get(
    "/orders/{order_id}", tags=["Orders"], response_model=OrderResponse
)
async def read_order(
    order_id: int, service: OrderService = Depends(get_order_service)
):
    try:
        order = await service.get_order_by_id(order_id)
        total_amount = await service.calculate_order_total(order)
        return serialize_order(order, total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/orders/by-order-number/{order_number}",
    tags=["Orders"],
    response_model=OrderResponse,
)
async def read_order_by_order_number(
    order_number: str, service: OrderService = Depends(get_order_service)
):
    try:
        order = await service.get_order_by_order_number(order_number)
        total_amount = await service.calculate_order_total(order)
        return serialize_order(order, total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/orders/{order_id}", tags=["Orders"], response_model=OrderResponse
)
async def update_order(
    order_id: int,
    order: OrderCreate,
    service: OrderService = Depends(get_order_service),
):
    customer_entity = CustomerEntity(
        name=order.customer.name, email=order.customer.email
    )
    order_items = [
        OrderItemEntity(product_sku=item.product_sku, quantity=item.quantity)
        for item in order.order_items
    ]
    try:
        updated_order = await service.update_order(
            order_id, customer_entity, order_items
        )
        return serialize_order(updated_order, updated_order.total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/orders/{order_id}/status", tags=["Orders"], response_model=OrderResponse
)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    service: OrderService = Depends(get_order_service),
):
    try:
        updated_order = await service.update_order_status(
            order_id, status_update.status
        )
        total_amount = await service.calculate_order_total(updated_order)
        return serialize_order(updated_order, total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/orders/{order_id}/confirm", tags=["Orders"], response_model=OrderResponse
)
async def confirm_order(
    order_id: int, service: OrderService = Depends(get_order_service)
):
    try:
        confirmed_order = await service.confirm_order(order_id)
        total_amount = await service.calculate_order_total(confirmed_order)
        return serialize_order(confirmed_order, total_amount)
    except (EntityNotFound, InvalidEntity) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(
    "/orders/{order_id}/cancel", tags=["Orders"], response_model=OrderResponse
)
async def cancel_order(
    order_id: int, service: OrderService = Depends(get_order_service)
):
    try:
        canceled_order = await service.cancel_order(order_id)
        total_amount = await service.calculate_order_total(canceled_order)
        return serialize_order(canceled_order, total_amount)
    except (EntityNotFound, InvalidEntity) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/orders/{order_id}", tags=["Orders"], status_code=204)
async def delete_order(
    order_id: int, service: OrderService = Depends(get_order_service)
):
    try:
        await service.delete_order(order_id)
        return {"message": "Order deleted successfully"}
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/orders/{order_id}/estimated-time",
    tags=["Orders"],
    response_model=OrderResponse,
)
async def set_estimated_time(
    order_id: int,
    estimated_time_update: EstimatedTimeUpdate,
    service: OrderService = Depends(get_order_service),
):
    try:
        updated_order = await service.set_estimated_time(
            order_id, estimated_time_update.estimated_time
        )
        total_amount = await service.calculate_order_total(updated_order)
        return serialize_order(updated_order, total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/orders/{order_id}/received",
    tags=["Orders"],
    response_model=OrderResponse,
)
async def update_order_to_received(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    try:
        updated_order = await service.update_order_status(
            order_id, OrderStatus.RECEIVED
        )
        total_amount = await service.calculate_order_total(updated_order)
        return serialize_order(updated_order, total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/orders/{order_id}/preparing",
    tags=["Orders"],
    response_model=OrderResponse,
)
async def update_order_to_preparing(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    try:
        updated_order = await service.update_order_status(
            order_id, OrderStatus.PREPARING
        )
        total_amount = await service.calculate_order_total(updated_order)
        return serialize_order(updated_order, total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/orders/{order_id}/ready", tags=["Orders"], response_model=OrderResponse
)
async def update_order_to_ready(
    order_id: int,
    service: OrderService = Depends(get_order_service),
):
    try:
        updated_order = await service.update_order_status(
            order_id, OrderStatus.READY
        )
        total_amount = await service.calculate_order_total(updated_order)
        return serialize_order(updated_order, total_amount)
    except EntityNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
