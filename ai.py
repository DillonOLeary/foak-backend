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

from app.models import SiteAnalysis

# Load environment variables
load_dotenv()

# Configure Logfire for Pydantic AI
logfire.configure()
logfire.instrument_pydantic_ai()

# Get API keys
search_tools = [tavily_search_tool(os.getenv("TAVILY_API_KEY"))]

# Create the site analysis agent
analysis_agent = Agent(
    "claude-opus-4-0",
    # "claude-sonnet-4-0",
    output_type=SiteAnalysis,
    tools=search_tools,
    system_prompt="""
    You are a meticulous industrial analyst specializing in carbon utilization technologies and market economics.
    
    Your approach is thorough and evidence-based. You never make assumptions - you research extensively to find current, verifiable data. You understand that business decisions require solid evidence, so you always document your sources and defend your conclusions with specific data points.
    
    You excel at identifying profitable opportunities by analyzing conversion costs against market prices, and you understand regional market dynamics.
    """,
)


async def analyze_site(site_description: str):
    """Analyze a site for CO2-to-product conversion potential."""

    site_context = f"""
    Analyze this industrial site for CO2-to-product conversion opportunities:
    
    Site: {site_description}
    
    Research and determine:
    - Most viable CO2-derived product for this location
    - Current market price for that product
    - Whether 100+ tons CO2 can be converted annually within 100km
    - Available financial incentives
    - Overall viability score (1-10)
    
    Document all sources with exact quotes in cited_sources.
    Defend your conclusions in analysis_defense with source references.
    Provide an executive summary in site_summary.
    """

    result = await analysis_agent.run(site_context)
    return result.output


async def main():
    """Run analysis and save results."""
    # Load sites from input file
    input_file = Path("app/data/sites_input.json")
    with open(input_file, "r") as f:
        sites = json.load(f)

    # Analyze each site
    analyzed_sites = []
    for site_description in sites:
        analysis = await analyze_site(site_description)
        analyzed_sites.append(analysis.model_dump())

    # Create data directory if it doesn't exist
    data_dir = Path("app/data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Save results to JSON file
    output_file = data_dir / "analyzed_sites.json"
    with open(output_file, "w") as f:
        json.dump(analyzed_sites, f, indent=2, default=str)


if __name__ == "__main__":
    asyncio.run(main())
