from datetime import datetime
from decimal import Decimal
from enum import Enum
from functools import cached_property
from typing import List, Optional
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


class BaseSiteAnalysis(BaseModel):
    # Basic Site Information
    location_name: str = Field(..., description="Human-readable site location")
    latitude: float = Field(..., description="Latitude coordinate of the site")
    longitude: float = Field(..., description="Longitude coordinate of the site")

    # Business Opportunity Assessment
    primary_product: CO2Product = Field(
        ..., description="Most viable product to produce from CO2 at this location"
    )
    primary_product_market_price_per_ton_usd: Decimal = Field(
        ...,
        description="Current market price for the primary product in USD per metric ton",
    )
    electricity_price_per_kwh_usd: Decimal = Field(
        ...,
        description="Industrial electricity price at this location in USD per kWh",
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
    business_analysis: str = Field(
        ...,
        description="Comprehensive evidence-backed analysis covering market opportunity, technical feasibility, economics, risks, and strategic advantages. All claims must be supported by cited sources.",
    )
    executive_summary: str = Field(
        ...,
        description="Concise 2-3 sentence investment thesis summarizing the opportunity",
    )
    cited_sources: List[CitedSource] = Field(
        ..., description="Research sources with relevant quotes supporting the analysis"
    )


class IndividualSiteAnalysis(BaseSiteAnalysis):
    """Site analysis without comparative viability score"""

    pass


class SiteScore(BaseModel):
    """Site score for comparative ranking"""

    location_name: str = Field(
        ...,
        description="EXACT location name from the site analysis - must match precisely as this is used as an ID for matching",
    )
    viability_score: int = Field(
        ...,
        ge=1,
        le=10,
        description="Comparative business viability score from 1 (poor) to 10 (excellent)",
    )
    ranking_rationale: str = Field(
        ...,
        description="Brief explanation of why this site received this score relative to others",
    )


class SiteAnalysis(BaseSiteAnalysis):
    """Complete site analysis with viability score (for backward compatibility)"""

    viability_score: Optional[int] = Field(
        None,
        ge=1,
        le=10,
        description="Overall business viability score from 1 (poor) to 10 (excellent)",
    )

    # Auto-generated fields
    @computed_field
    @cached_property
    def site_id(self) -> UUID:
        """Unique identifier for the analyzed site"""
        return uuid4()

    @computed_field
    @property
    def last_updated(self) -> str:
        """ISO timestamp of when analysis was performed"""
        return datetime.now().isoformat()
