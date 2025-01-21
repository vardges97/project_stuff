# services-order

@staticmethod
async def cancel_order(db: AsyncSession, order_id: int, status: str):

        order = await db.get(Order, order_id)       
        if order.status == Pending:            
            order.status = status
            order.updated_at = datetime.utcnow()            
            await db.commit()
            await db.refresh(order)
            return OrderResponse.from_orm(order)
            
        for item in order.order_items:
            product = await db.get(Product,item.product_id)
            if not product: 
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Product '{product.name}' (ID: {product.id}) does not exist."
                    )
            product.stock += 1
            await db.commit()
            await db.refresh
            return product
        
#routes
async def Cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Get details of a specific order by its ID.
    """
    return await OrderService.cancel_order(db, order_id, current_user.id, current_user.is_admin)