import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import SiteAnalysis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/site-analyses/latest", response_model=List[SiteAnalysis])
async def get_site_analyses():
    """Load site analyses from both manual data and analyzed sites JSON files."""
    manual_data_file = Path("app/data/manual_data.json")
    analyzed_data_file = Path("app/data/analyzed_sites.json")

    all_sites = []

    # Load manual data if it exists
    if manual_data_file.exists():
        try:
            with open(manual_data_file, "r") as f:
                manual_sites_data = json.load(f)
            manual_sites = [
                SiteAnalysis.model_validate(site_data)
                for site_data in manual_sites_data
            ]
            all_sites.extend(manual_sites)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=500, detail=f"Error loading manual sites data: {str(e)}"
            )

    # Load analyzed data if it exists
    if analyzed_data_file.exists():
        try:
            with open(analyzed_data_file, "r") as f:
                analyzed_sites_data = json.load(f)
            analyzed_sites = [
                SiteAnalysis.model_validate(site_data)
                for site_data in analyzed_sites_data
            ]
            all_sites.extend(analyzed_sites)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=500, detail=f"Error loading analyzed sites data: {str(e)}"
            )

    if not all_sites:
        raise HTTPException(
            status_code=404,
            detail="No site analysis data found. Make sure manual_data.json or analyzed_sites.json exist.",
        )

    return all_sites
