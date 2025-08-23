from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field


class EnergyPricing(BaseModel):
    # FIXME cost of production
    # fields
    # difference in what it costs to produce vs sell
    # emphasise margin
    # is someone willing to pay higher
    electricity_price_per_kwh: Decimal = Field(
        ..., description="Current electricity price in $/kWh for the location"
    )
    co2_price_per_ton: Decimal = Field(
        ..., description="Carbon credit price in $/ton CO2 equivalent"
    )
    summary: str = Field(..., description="Brief summary of energy pricing conditions")


class MarketDemand(BaseModel):
    can_sell_1000_tons_annually: bool = Field(
        ..., description="Whether we can sell 1000 tons of methane within 50km per year"
    )  # long term 1000, short term 100. maybe diversity so not super important. Might be difficult if diverse
    customer_count_within_50km: int = Field(
        ..., description="Number of potential industrial customers within 50km radius"
    )
    summary: str = Field(..., description="Brief summary of market demand conditions")


class FinancialIncentives(BaseModel):
    # know if the gov is willing to pay a percent
    # tax breaks
    available_incentives_usd: int = Field(
        ..., description="Total financial incentives available in USD"
    )
    incentive_summary: str = Field(
        ..., description="Brief summary of key financial incentives"
    )


class SiteAnalysis(BaseModel):
    location_name: str = Field(..., description="Human-readable site location")
    latitude: float
    longitude: float
    market_demand: MarketDemand
    financial_incentives: FinancialIncentives
    summary: str = Field(..., description="Overall site analysis summary")

    @computed_field
    @property
    def site_id(self) -> UUID:
        """Unique identifier for the analyzed site"""
        return uuid4()

    @computed_field
    @property
    def last_updated(self) -> str:
        """ISO timestamp of when analysis was performed"""
        return datetime.now().isoformat()
