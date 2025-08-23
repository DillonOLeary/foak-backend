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


async def analyze_site(site_description: str):
    """Analyze a site for methane utilization potential."""
    
    site_context = f"""
    Analyze this industrial site for methane capture and utilization opportunities:
    
    Site: {site_description}
    
    Conduct thorough research and provide a comprehensive analysis.
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
