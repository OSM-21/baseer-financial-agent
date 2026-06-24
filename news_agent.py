import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


async def news_agent(query: str) -> dict:
    """Agent يبحث عن أخبار مالية حقيقية من الويب"""
    
    # بحث بالعربي والإنجليزي
    results_ar = client.search(
        query=f"{query} أخبار مالية اقتصادية",
        max_results=3,
        search_depth="advanced"
    )
    
    results_en = client.search(
        query=f"{query} financial news market",
        max_results=3,
        search_depth="advanced"
    )
    
    # دمج النتائج
    all_results = []
    
    for r in results_ar.get("results", []):
        all_results.append({
            "title": r.get("title"),
            "content": r.get("content"),
            "url": r.get("url"),
            "language": "ar"
        })
    
    for r in results_en.get("results", []):
        all_results.append({
            "title": r.get("title"),
            "content": r.get("content"),
            "url": r.get("url"),
            "language": "en"
        })
    
    return {
        "agent": "News Agent",
        "query": query,
        "results_count": len(all_results),
        "news": all_results
    }