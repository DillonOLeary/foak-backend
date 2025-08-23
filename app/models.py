from decimal import Decimal

from pydantic import BaseModel, Field


class EnergyPricing(BaseModel):
    electricity_price_per_kwh: Decimal = Field(
        ..., description="Current electricity price in $/kWh for the location"
    )
    co2_price_per_ton: Decimal = Field(
        ..., description="Carbon credit price in $/ton CO2 equivalent"
    )


class MarketDemand(BaseModel):
    methane_capacity_tons: int = Field(
        ..., description="Annual methane production capacity in tons"
    )
    customer_count_within_50km: int = Field(
        ..., description="Number of potential industrial customers within 50km radius"
    )
    has_pipeline_access: bool = Field(
        ...,
        description="Whether site has access to existing gas pipeline infrastructure",
    )
    scalability_rating: int = Field(
        ...,
        ge=1,
        le=5,
        description="Scalability potential from 1 (limited) to 5 (high growth potential)",
    )


class FinancialIncentives(BaseModel):
    available_grants_usd: int = Field(
        ..., description="Total available government grants and subsidies in USD"
    )
    tax_credits_available: bool = Field(
        ..., description="Whether renewable energy tax credits are available"
    )
    incentive_summary: str = Field(
        ..., description="Brief summary of key financial incentives"
    )


class SiteAnalysis(BaseModel):
    site_id: str = Field(..., description="Unique identifier for the analyzed site")
    location_name: str = Field(..., description="Human-readable site location")
    energy_pricing: EnergyPricing
    market_demand: MarketDemand
    financial_incentives: FinancialIncentives
    last_updated: str = Field(
        ..., description="ISO timestamp of when analysis was performed"
    )
