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
    You are an expert energy analyst specializing in methane capture and utilization projects.
    
    For each site analysis, conduct thorough web research to find current, accurate data. Search multiple times for different aspects - don't rely on single searches.
    
    Research and analyze:
    - Current energy pricing and carbon markets
    - Local industrial customers and their methane demand
    - Financial incentives, grants, and policy changes
    - Infrastructure and transportation costs
    
    Provide data-driven assessments based on your research findings.
    """,
)


async def analyze_louisiana_gulf_coast():
    """Analyze Louisiana Gulf Coast industrial complex for methane utilization potential."""

    site_context = """
    Analyze this major industrial site in Louisiana:
    
    Location: Louisiana Gulf Coast Industrial Complex (near Lake Charles/Cameron Parish)
    Coordinates: 29.8917° N, 93.2578° W
    
    Site Details:
    - Part of Louisiana's massive petrochemical corridor
    - Home to multiple LNG export terminals and processing facilities
    - Major natural gas pipeline hub with 50,000+ miles of integrated pipelines
    - 4 of the nation's LNG export terminals located in the region
    - Access to Port of Lake Charles and deep water shipping
    - Strong industrial customer base including petrochemical plants, refineries
    - Louisiana electricity rates ~18% below national average
    - State offers competitive industrial natural gas rates
    
    Current methane sources: Flaring from oil/gas operations, waste gas from petrochemical processes
    Market: Established industrial customers, export terminals, chemical manufacturers
    Regulations: EPA methane reduction programs, state renewable energy incentives
    """

    result = await analysis_agent.run(site_context)
    return result.output


async def analyze_fort_mcmurray_oil_sands():
    """Analyze Fort McMurray Oil Sands industrial park for methane utilization potential."""

    site_context = """
    Analyze this major industrial site in Alberta, Canada:
    
    Location: Fort McMurray Oil Sands Industrial Park (Athabasca region)
    Coordinates: 56.7264° N, 111.3790° W
    
    Site Details:
    - World's largest industrial project with multiple upgraders (Syncrude, Suncor, CNRL Horizon)
    - Produces 3+ million barrels oil/day consuming 30% of Canada's natural gas
    - Massive industrial infrastructure and energy consumption
    - Some methane produced as byproduct of bitumen processing
    - Limited local industrial customers beyond oil sands operations
    - Remote location ~435km from Edmonton
    - Harsh climate conditions affecting operations
    - High transportation costs for products
    
    Current methane sources: Byproduct gas from oil sands processing, equipment fugitive emissions
    Market: Oil sands operations, limited external industrial demand, potential export to south
    Regulations: Canadian federal carbon pricing, Alberta emissions regulations, Indigenous consultation requirements
    """

    result = await analysis_agent.run(site_context)
    return result.output


async def main():
    """Run analysis and save results."""
    # Run both analyses
    louisiana_analysis = await analyze_louisiana_gulf_coast()
    alberta_analysis = await analyze_fort_mcmurray_oil_sands()

    # Create data directory if it doesn't exist
    data_dir = Path("app/data")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Save results to JSON file
    analyzed_sites = [louisiana_analysis.model_dump(), alberta_analysis.model_dump()]

    output_file = data_dir / "analyzed_sites.json"
    with open(output_file, "w") as f:
        json.dump(analyzed_sites, f, indent=2, default=str)


if __name__ == "__main__":
    asyncio.run(main())
