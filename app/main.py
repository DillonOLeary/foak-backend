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
            location_name="Industrial Complex - Houston, TX",
            latitude=29.7604,
            longitude=-95.3698,
            energy_pricing=EnergyPricing(
                electricity_price_per_kwh=Decimal("0.12"),
                co2_price_per_ton=Decimal("85.50"),
                summary="Competitive electricity rates with high CO2 credit prices",
            ),
            market_demand=MarketDemand(
                can_sell_1000_tons_annually=True,
                customer_count_within_50km=8,
                summary="Strong industrial customer base with proven demand capacity",
            ),
            financial_incentives=FinancialIncentives(
                available_incentives_usd=750000,
                incentive_summary="Federal ITC 30%, state renewable energy grants, EPA methane reduction incentives",
                summary="Excellent federal and state incentive package available",
            ),
            summary="High-potential site with strong market demand and excellent incentives",
        ),
        SiteAnalysis(
            location_name="Waste Management Facility - Denver, CO",
            latitude=39.7392,
            longitude=-104.9903,
            energy_pricing=EnergyPricing(
                electricity_price_per_kwh=Decimal("0.09"),
                co2_price_per_ton=Decimal("92.25"),
                summary="Lower electricity costs but premium CO2 credit market",
            ),
            market_demand=MarketDemand(
                can_sell_1000_tons_annually=False,
                customer_count_within_50km=3,
                summary="Limited local demand, may require transport to larger markets",
            ),
            financial_incentives=FinancialIncentives(
                available_incentives_usd=350000,
                incentive_summary="State RPS incentives, local utility rebates",
                summary="Moderate incentive package focused on renewable energy credits",
            ),
            summary="Medium-potential site with transport challenges but good energy economics",
        ),
    ]
