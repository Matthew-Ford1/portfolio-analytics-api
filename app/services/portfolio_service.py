from decimal import Decimal

from sqlalchemy import select

from app.models import Asset, Holding, Portfolio, User
from sqlalchemy.ext.asyncio import AsyncSession


# fmt: off
class PortfolioDoesNotExist(Exception): ...
class PortfolioInvalidAccess(Exception): ...
# fmt: on


# TODO: decide if portfolio name should be unique per user
async def create_portfolio(
    db: AsyncSession,
    user: User,
    name: str,
    currency: str,
    is_default: bool,
    description: str | None,
) -> Portfolio:
    default_portfolio: Portfolio = await db.scalar(
        select(Portfolio).where(Portfolio.owner_id == user.id).where(Portfolio.is_default)
    )

    # replace default portfolio if new is set as default
    if is_default and default_portfolio is not None:
        default_portfolio.is_default = False

    portfolio = Portfolio(
        owner_id=user.id,
        name=name,
        currency=currency,
        is_default=is_default,
        description=description,
    )
    db.add(portfolio)
    await db.commit()
    await db.refresh(portfolio)

    return portfolio


async def get_portfolio(db: AsyncSession, user: User, id: int) -> Portfolio:
    portfolio: Portfolio = await db.scalar(select(Portfolio).where(Portfolio.id == id))

    if portfolio is None:
        raise PortfolioDoesNotExist(f"Portfolio {id} does not exist")
    if portfolio.owner_id != user.id:
        raise PortfolioInvalidAccess(f"User {user.id} does not have access to Portfolio {id}")

    return portfolio


async def get_user_portfolios(db: AsyncSession, user: User) -> list[Portfolio]:
    results = await db.execute(select(Portfolio).where(Portfolio.owner_id == user.id))
    return results.scalars().all()


async def update_portfolio(
    db: AsyncSession,
    user: User,
    id: int,
    name: str,
    currency: str,
    is_default: bool,
    description: str | None,
) -> Portfolio:
    default_portfolio: Portfolio = await db.scalar(
        select(Portfolio).where(Portfolio.owner_id == user.id).where(Portfolio.is_default)
    )

    # replace default portfolio if updated to be set as default
    if is_default and default_portfolio is not None:
        default_portfolio.is_default = False

    portfolio = await get_portfolio(db, user, id)
    portfolio.name = name
    portfolio.currency = currency
    portfolio.is_default = is_default
    portfolio.description = description

    await db.commit()
    await db.refresh(portfolio)

    return portfolio


# TODO: determine if should block if it has holdings or should cascade
async def delete_portfolio(db: AsyncSession, id: int):
    portfolio: Portfolio = await db.scalar(select(Portfolio).where(Portfolio.id == id))
    if portfolio:
        await db.delete(portfolio)
        await db.commit()


async def add_or_update_holding(
    db: AsyncSession,
    portfolio: Portfolio,
    ticker: str,
    exchange: str,
    quantity: Decimal,
    purchase_price: Decimal,
    notes: str | None,
) -> Holding:
    # checking if asset exists
    asset: Asset = await db.scalar(
        select(Asset).where(Asset.ticker == ticker).where(Asset.exchange == exchange)
    )

    # if not exists, use price service to retrieve the asset
    if asset is None:
        # TODO: the below
        # asset = price_service.get_asset(db, ticker, exchange)

        if asset is None:
            raise

    # check if holding with asset_id exists in portfolio
    holding: Holding = await db.scalar(
        select(Holding)
        .where(Holding.portfolio_id == portfolio.id)
        .where(Holding.asset_id == asset.id)
    )

    if holding is None:
        # create holding
        holding = Holding(
            portfolio_id=portfolio.id,
            asset_id=asset.id,
            quantity=quantity,
            average_cost_price=purchase_price,
            notes=notes,
        )
        db.add(holding)
    else:
        # update holding: recalcualte average cost price and qantity
        old_cost = holding.quantity * holding.average_cost_price
        added_cost = quantity * purchase_price

        holding.average_cost_price = (old_cost + added_cost) / (holding.quantity + quantity)
        holding.quantity += quantity

        # append to notes
        if notes:
            holding.notes += ";" + notes

    await db.commit()
    await db.refresh(holding)

    return holding


async def reduce_holding(
    db: AsyncSession, portfolio: Portfolio, ticker: str, exchange: str, quantity: Decimal
) -> Holding:
    """Reduce holding by sale quantity (`quantity`)"""
    raise NotImplementedError("portfolio_service.reduce_holding")


# TODO:
async def get_holdings(db: AsyncSession, portfolio: Portfolio) -> dict:
    """Return all holdings for a portfolio with current prices attached"""
    raise NotImplementedError("portfolio_service.get_holdings")


# TODO: determine if/how the asset should be deleted if no longer referenced by any holding
async def delete_holding(
    db: AsyncSession,
    portfolio: Portfolio,
    ticker: str,
    exchange: str,
):
    holding: Holding = await db.scalar(
        select(Holding)
        .join(Holding.asset)
        .where(Asset.ticker == ticker)
        .where(Asset.exchange == exchange)
    )

    await db.delete(holding)
    await db.commit()
