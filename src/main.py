from fastapi import FastAPI

from fastapi.responses import RedirectResponse

from src.api import cases, documents, summaries

app = FastAPI(
    title="Case Management Assistant API",
    description="Regulatory investigation assistant for document ingestion, analysis and summarisation.",
    version="0.1.0",
)

# Register routers with API v1 prefix
app.include_router(cases.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(summaries.router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Health Check"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "case-management-assistant"}