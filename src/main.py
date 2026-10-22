from fastapi import FastAPI
from src.core.database import Base, engine
from src.api import cases, documents, summaries

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Case Management Assistant API",
    description="Regulatory investigation assistant for document ingestion, analysis and summarisation.",
    version="0.1.0",
)

app.include_router(cases.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(summaries.router, prefix="/api/v1")


@app.get("/health", tags=["Health Check"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "case-management-assistant"}