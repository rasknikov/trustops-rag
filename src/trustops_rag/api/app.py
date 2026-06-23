from fastapi import FastAPI
import uvicorn

from trustops_rag.api.ask import router as ask_router

app = FastAPI(
    title="TrustOps RAG API",
    version="0.1.0",
)


@app.get("/health", tags=["health"], summary="Health check")
def health() -> dict:
    return {"status": "ok"}


app.include_router(ask_router)


if __name__ == "__main__":
    uvicorn.run("trustops_rag.api.app:app", host="127.0.0.1", port=8000, reload=True)