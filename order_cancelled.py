# services-order

@staticmethod
async def cancel_order(db: AsyncSession, order_id: int):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )
    if order.status == OrderStatus.SHIPPED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel an order that has already been shipped."
        )
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel an order with status '{order.status.name}'. Only 'Pending' orders can be canceled."
        )
    order.status = OrderStatus.CANCELLED
    order.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(order)
    for item in order.order_items:
        product = await db.get(Product, item.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with ID {item.product_id} not found."
            )
        product.stock += item.quantity
        await db.commit()
        await db.refresh(product)
    return OrderResponse.from_orm(order)
#routing
@router.put("/orders/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await OrderService.cancel_order(db, order_id)
