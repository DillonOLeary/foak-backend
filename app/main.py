from datetime import datetime
from decimal import Decimal
from typing import List

from fastapi import FastAPI

from app.models import EnergyPricing, FinancialIncentives, MarketDemand, SiteAnalysis

app = FastAPI()


@app.get("/site-analyses/latest", response_model=List[SiteAnalysis])
async def get_site_analyses():
    # Sample data demonstrating multiple site analyses
    return [
        SiteAnalysis(
            site_id="site_001",
            location_name="Industrial Complex - Houston, TX",
            energy_pricing=EnergyPricing(
                electricity_price_per_kwh=Decimal("0.12"),
                co2_price_per_ton=Decimal("85.50"),
            ),
            market_demand=MarketDemand(
                methane_capacity_tons=1500,
                customer_count_within_50km=8,
                has_pipeline_access=True,
                scalability_rating=4,
            ),
            financial_incentives=FinancialIncentives(
                available_grants_usd=750000,
                tax_credits_available=True,
                incentive_summary="Federal ITC 30%, state renewable energy grants, EPA methane reduction incentives",
            ),
            analysis_confidence=4,
            last_updated=datetime.now().isoformat(),
        ),
        SiteAnalysis(
            site_id="site_002",
            location_name="Waste Management Facility - Denver, CO",
            energy_pricing=EnergyPricing(
                electricity_price_per_kwh=Decimal("0.09"),
                co2_price_per_ton=Decimal("92.25"),
            ),
            market_demand=MarketDemand(
                methane_capacity_tons=800,
                customer_count_within_50km=3,
                has_pipeline_access=False,
                scalability_rating=2,
            ),
            financial_incentives=FinancialIncentives(
                available_grants_usd=350000,
                tax_credits_available=True,
                incentive_summary="State RPS incentives, local utility rebates",
            ),
            analysis_confidence=3,
            last_updated=datetime.now().isoformat(),
        ),
    ]
