from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, computed_field


class CitedSource(BaseModel):
    url: HttpUrl = Field(..., description="Source website URL")
    extracted_quote: str = Field(..., description="Relevant quote or data point from the source")


class SiteAnalysis(BaseModel):
    # Basic Site Information
    location_name: str = Field(..., description="Human-readable site location")
    latitude: float = Field(..., description="Latitude coordinate of the site")
    longitude: float = Field(..., description="Longitude coordinate of the site")
    
    # Business Opportunity Assessment
    viability_score: int = Field(..., ge=1, le=10, description="Overall business viability score from 1 (poor) to 10 (excellent)")
    primary_product_type: str = Field(..., description="Most viable product to produce from CO2 at this location")
    product_market_price: Decimal = Field(..., description="Current market price for this product in the region")
    
    # Market Demand
    can_sell_100_tons_co2_equivalent_within_100_km: bool = Field(
        ..., description="Whether there's demand to convert 100 tons of CO2 annually within 100 km"
    )
    
    # Financial Support
    available_incentives: List[str] = Field(
        ..., description="List of available financial incentives and their amounts"
    )
    
    # Analysis Documentation
    cited_sources: List[CitedSource] = Field(
        ..., description="Research sources with relevant quotes supporting the analysis"
    )
    analysis_defense: str = Field(
        ..., description="Technical defense of each field's value with references to specific cited sources"
    )
    site_summary: str = Field(
        ..., description="Executive summary of the business opportunity and recommendation"
    )

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
