# Get all orders for the current user
@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        query = select(Order).where(Order.user_id == current_user.id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    except HTTPException as e:
        logger.warning(f"HTTP Exception during order lookup: {e.detail}")
        return
    except Exception as e:
        logger.error(f"Unexpected error during order lookup: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        return


# Get a specific order by ID
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        order = await db.get(Order, order_id)
        return order
    except HTTPException as e:
        logger.warning(f"HTTP Exception during order lookup: {e.detail}")
        return
    except Exception as e:
        logger.error(f"Unexpected error during order lookup: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        return
       