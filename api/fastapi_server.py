from fastapi import FastAPI

app = FastAPI(
    title="Graphmaster API",
    description="Semantic BIM Knowledge Platform",
    version="0.1"
)

@app.get("/")
def root():
    return {
        "system": "Graphmaster",
        "status": "running",
        "message": "Semantic BIM Knowledge Platform API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/modules")
def modules():
    return {
        "modules": [
            "core",
            "ifc",
            "bsdd",
            "owl",
            "ids",
            "xls",
            "bcf",
            "bim4hvac",
            "pdf_regulations"
        ]
    }
