from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EnergyPricing(BaseModel):
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
    )
    customer_count_within_50km: int = Field(
        ..., description="Number of potential industrial customers within 50km radius"
    )
    summary: str = Field(..., description="Brief summary of market demand conditions")


class FinancialIncentives(BaseModel):
    available_incentives_usd: int = Field(
        ..., description="Total financial incentives available in USD"
    )
    incentive_summary: str = Field(
        ..., description="Brief summary of key financial incentives"
    )
    summary: str = Field(
        ..., description="Brief summary of financial incentive conditions"
    )


class SiteAnalysis(BaseModel):
    site_id: UUID = Field(
        default_factory=uuid4, description="Unique identifier for the analyzed site"
    )
    location_name: str = Field(..., description="Human-readable site location")
    latitude: float
    longitude: float
    market_demand: MarketDemand
    financial_incentives: FinancialIncentives
    summary: str = Field(..., description="Overall site analysis summary")
    last_updated: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO timestamp of when analysis was performed",
    )
