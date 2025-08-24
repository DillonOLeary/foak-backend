from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl, computed_field


class CO2Product(str, Enum):
    # High-priority products (largest markets/best economics)
    METHANOL = "Methanol"
    ETHYLENE = "Ethylene"
    PROPYLENE = "Propylene"
    POLYETHYLENE_PE = "Polyethylene PE"
    POLYPROPYLENE_PP = "Polypropylene (PP)"

    # Medium-priority products
    ETHYLENE_GLYCOL = "Ethylene Glycol"
    POLYETHYLENE_TEREPHTHALATE_PET = "Polyethylene Terephthalate (PET)"
    POLYCARBONATE = "Polycarbonate"
    FORMIC_ACID = "Formic Acid"
    DIMETHYL_CARBONATE = "Dimethyl Carbonate"

    # Specialized/niche products
    MTO_OLEFINS = "MTO Olefins"
    POLYURETHANE = "Polyurethane"
    ALDEHYDES = "Aldehydes"
    ACETYLS = "Acetyls"
    DRI_EAR_STEEL = "DRI-EAR Steel"
    OXALATE = "Oxalate"
    PHOSGENE = "Phosgene"


class CitedSource(BaseModel):
    url: HttpUrl = Field(..., description="Source website URL")
    extracted_quote: str = Field(
        ..., description="Relevant quote or data point from the source"
    )


class SiteAnalysis(BaseModel):
    # Basic Site Information
    location_name: str = Field(..., description="Human-readable site location")
    latitude: float = Field(..., description="Latitude coordinate of the site")
    longitude: float = Field(..., description="Longitude coordinate of the site")

    # Business Opportunity Assessment
    viability_score: int = Field(
        ...,
        ge=1,
        le=10,
        description="Overall business viability score from 1 (poor) to 10 (excellent)",
    )
    primary_product: CO2Product = Field(
        ..., description="Most viable product to produce from CO2 at this location"
    )
    primary_product_market_price_per_ton_usd: Decimal = Field(
        ...,
        description="Current market price for the primary product in USD per metric ton",
    )
    can_sell_100_tons_primary_product_within_100_km: bool = Field(
        ...,
        description="Whether there's demand to sell 100 tons of the primary product annually within 100 km",
    )
    other_viable_products: List[CO2Product] = Field(
        ...,
        description="Other products that could be produced from CO2 at this location",
    )

    # Financial Support
    available_incentives: List[str] = Field(
        ..., description="List of available financial incentives and their amounts"
    )

    # Analysis Documentation
    analysis_defense: str = Field(
        ...,
        description="Rigorous technical justification linking cited sources to prove each field value is correct",
    )
    site_summary: str = Field(
        ...,
        description="Contextual overview of the industrial site and business opportunity",
    )
    cited_sources: List[CitedSource] = Field(
        ..., description="Research sources with relevant quotes supporting the analysis"
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
