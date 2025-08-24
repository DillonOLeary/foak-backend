import json
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException

from app.models import SiteAnalysis

app = FastAPI()


@app.get("/site-analyses/latest", response_model=List[SiteAnalysis])
async def get_site_analyses():
    """Load site analyses from manual data JSON file."""
    data_file = Path("app/data/manual_data.json")

    if not data_file.exists():
        raise HTTPException(
            status_code=404,
            detail="Manual data file not found.",
        )

    try:
        with open(data_file, "r") as f:
            sites_data = json.load(f)

        # Convert JSON data back to Pydantic models
        analyzed_sites = [
            SiteAnalysis.model_validate(site_data) for site_data in sites_data
        ]
        return analyzed_sites

    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading analyzed sites data: {str(e)}"
        )
