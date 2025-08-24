"""
AI-powered site analysis for methane capture and utilization opportunities.
Analyzes Louisiana Gulf Coast industrial site.
"""

import asyncio
import json
import os
from pathlib import Path

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool

from app.models import IndividualSiteAnalysis, SiteScore

# Load environment variables
load_dotenv()

# Configure Logfire for Pydantic AI
logfire.configure()
logfire.instrument_pydantic_ai()

# Get API keys
search_tools = [tavily_search_tool(os.getenv("TAVILY_API_KEY"))]

# Create the individual site analysis agent
individual_analysis_agent = Agent(
    "claude-opus-4-0",
    # "claude-sonnet-4-0",
    output_type=IndividualSiteAnalysis,
    tools=search_tools,
    system_prompt="""
You are a meticulous industrial analyst specializing in carbon utilization technologies and market economics.
    
Your approach is thorough and evidence-based. You never make assumptions - you research extensively to find current, verifiable data. You understand that business decisions require solid evidence, so you always document your sources and defend your conclusions with specific data points.
    
You excel at identifying profitable opportunities by analyzing conversion costs against market prices, and you understand regional market dynamics.
    """,
)

# Create the comparative scoring agent
scoring_agent = Agent(
    "claude-opus-4-0",
    output_type=list[SiteScore],
    system_prompt="""
You are a senior investment analyst specializing in industrial project evaluation. You apply consistent, objective criteria and avoid anchoring bias. Your scoring is based on universal benchmarks that scale across any portfolio size, focusing on fundamental economics rather than relative comparisons.
    """,
)


async def analyze_site(site_description: str):
    """Analyze a site for CO2-to-product conversion potential (without viability score)."""

    site_context = f"""
Analyze this industrial site for CO2-to-product conversion opportunities:

Site: {site_description}
    
Research and determine:
- Most viable CO2-derived product for this specific location considering existing operations and local demand
- Current market price for that product in USD per metric ton
- Industrial electricity price at this location in USD per kWh
- Whether there's demand to sell 100+ tons of product annually within 100km
- Other viable products that could be produced
- Available financial incentives and amounts

Document all sources with exact quotes in cited_sources.
Provide comprehensive evidence-backed analysis in business_analysis covering market opportunity, technical feasibility, economics, risks, and strategic advantages. Explain why your chosen product is optimal for this specific site.
Provide a concise 2-3 sentence investment thesis in executive_summary.
    """

    result = await individual_analysis_agent.run(site_context)
    return result.output


async def score_sites(analyses: list[IndividualSiteAnalysis]):
    """Score sites comparatively based on their individual analyses."""

    analyses_summary = "\n\n".join(
        [
            f"Site: {analysis.location_name}\n"
            f"Product: {analysis.primary_product} @ ${analysis.primary_product_market_price_per_ton_usd}/ton\n"
            f"Electricity: ${analysis.electricity_price_per_kwh_usd}/kWh\n"
            f"Business Analysis: {analysis.business_analysis[:500]}...\n"
            f"Executive Summary: {analysis.executive_summary}"
            for analysis in analyses
        ]
    )

    scoring_context = f"""
Score these {len(analyses)} industrial sites using these universal benchmarks:

9-10: Exceptional (electricity <$0.05/kWh, incentives >60% capex, established infrastructure, pricing >$600/MT)
7-8: Very viable (electricity $0.05-0.10/kWh, incentives 30-60%, good infrastructure, pricing $400-600/MT)  
5-6: Challenging (electricity $0.10-0.15/kWh, incentives <30%, moderate infrastructure, pricing $300-400/MT)
3-4: Marginal (electricity $0.15-0.20/kWh, minimal incentives, poor infrastructure, pricing <$300/MT)
1-2: Poor (electricity >$0.20/kWh, no incentives, greenfield required, very low pricing)

{analyses_summary}

For each site, provide the EXACT location_name (copy it precisely from the input - this is used as an ID), viability_score, and ranking_rationale based on objective criteria only. Do not reference other sites in rationales.
    """

    result = await scoring_agent.run(scoring_context)
    return result.output


async def main():
    """Run two-stage analysis and save results."""
    # Load sites from input file
    input_file = Path("app/data/sites_input.json")
    with open(input_file, "r") as f:
        sites = json.load(f)

    # Stage 1: Analyze each site individually (without scores) in parallel
    individual_analyses = await asyncio.gather(
        *[analyze_site(site_description) for site_description in sites]
    )

    # Stage 2: Score sites comparatively
    site_scores = await score_sites(individual_analyses)

    # Create data directory if it doesn't exist
    data_dir = Path("app/data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Combine individual analyses with their scores using location_name
    combined_results = []
    for analysis in individual_analyses:
        analysis_dict = analysis.model_dump()

        # Find the matching score by exact location_name
        matching_score = next(
            (
                score
                for score in site_scores
                if score.location_name == analysis.location_name
            ),
            None,
        )

        # Add viability score and ranking rationale to the analysis
        if matching_score:
            analysis_dict["viability_score"] = matching_score.viability_score
            analysis_dict["ranking_rationale"] = matching_score.ranking_rationale

        combined_results.append(analysis_dict)

    # Save combined results to single file
    output_file = data_dir / "analyzed_sites.json"
    with open(output_file, "w") as f:
        json.dump(combined_results, f, indent=2, default=str)

    print("Analysis complete:")
    print(f"- Combined results: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
