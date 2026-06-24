from fastapi import APIRouter
from pydantic import BaseModel
from agents.news_agent import news_agent
from agents.analyst_agent import analyst_agent
from agents.report_agent import report_agent

router = APIRouter()


class QueryInput(BaseModel):
    query: str


@router.post("/analyze", summary="تحليل مالي شامل")
async def analyze(body: QueryInput):
    """
    نظام Multi-Agent للتحليل المالي:
    - Agent 1: جمع الأخبار من الويب
    - Agent 2: تحليل البيانات
    - Agent 3: توليد التقرير التنفيذي
    """
    news = await news_agent(body.query)
    analysis = await analyst_agent(news, body.query)
    report = await report_agent(analysis, news, body.query)

    return {
        "success": True,
        "query": body.query,
        "data": {
            "news_count": news["results_count"],
            "analysis": analysis["analysis"],
            "report": report["report"],
            "generated_at": report["generated_at"],
            "sources": report["sources"]
        }
    }


@router.get("/health")
async def health():
    return {"status": "healthy", "system": "Baseer Financial Intelligence"}