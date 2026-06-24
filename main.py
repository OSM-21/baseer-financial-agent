import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
load_dotenv()

app = FastAPI(
    title="Baseer — Financial Intelligence API",
    description="Multi-Agent Arabic Financial Analysis System",
    version="1.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api/v1", tags=["Analysis"])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/app")
def serve_app():
    return FileResponse("static/index.html")

@app.get("/")
def root():
    return {"service": "Baseer Financial Intelligence", "status": "running", "agents": 3}


async def baseer_pipeline(query: str) -> dict:
    from agents.news_agent import news_agent
    from agents.analyst_agent import analyst_agent
    from agents.report_agent import report_agent

    print(f"\n🔍 Baseer Financial Intelligence System")
    print(f"📊 تحليل: {query}")
    print("=" * 50)

    print("\n⚡ Agent 1: جمع الأخبار المالية...")
    news = await news_agent(query)
    print(f"✅ تم جمع {news['results_count']} خبر")

    print("\n⚡ Agent 2: تحليل البيانات...")
    analysis = await analyst_agent(news, query)
    print("✅ تم التحليل")

    print("\n⚡ Agent 3: توليد التقرير التنفيذي...")
    report = await report_agent(analysis, news, query)
    print("✅ تم توليد التقرير")

    return {"query": query, "news": news, "analysis": analysis, "report": report}


if __name__ == "__main__":
    query = "أسعار النفط السعودي وتأثيرها على الاقتصاد"
    asyncio.run(baseer_pipeline(query))