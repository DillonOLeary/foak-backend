from fastapi import FastAPI
from app.models import SiteAnalysisResponse

app = FastAPI()


@app.get("/site-analyses/latest", response_model=SiteAnalysisResponse)
async def get_site_analyses():
    return SiteAnalysisResponse(message="Welcome to the FOAK Backend!")
