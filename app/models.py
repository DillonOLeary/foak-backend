from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field


class SiteAnalysis(BaseModel):
    # Location
    location_name: str = Field(..., description="Human-readable site location")
    latitude: float = Field(..., description="Latitude coordinate of the site")
    longitude: float = Field(..., description="Longitude coordinate of the site")

    # CO2 Conversion Economics
    co2_conversion_cost_per_ton: Decimal = Field(
        ...,
        description="Cost to convert 1 ton of CO2 including electricity, materials, labor",
    )
    primary_product_type: str = Field(
        ..., description="Most viable product to produce from CO2 at this location"
    )
    product_market_price: Decimal = Field(
        ..., description="Current market price for this product in the region"
    )
    profit_margin_per_ton_co2: Decimal = Field(
        ...,
        description="Profit per ton of CO2 converted (market price - conversion cost)",
    )

    # Market Analysis
    primary_product_customers: int = Field(
        ...,
        description="Number of potential customers for CO2-derived products within 50km",
    )
    can_sell_1000_tons_co2_equivalent: bool = Field(
        ..., description="Whether there's demand to convert 1000 tons of CO2 annually"
    )

    # Financial Support
    available_incentives_usd: int = Field(
        ..., description="Total financial incentives available in USD"
    )
    incentive_summary: str = Field(
        ..., description="Brief summary of key financial incentives"
    )

    # Overall Assessment
    summary: str = Field(..., description="Overall site analysis summary")

    # Auto-generated fields
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
