from pydantic import BaseModel


class SiteAnalysisResponse(BaseModel):
    message: str