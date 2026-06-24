import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


async def report_agent(analysis_data: dict, news_data: dict, query: str) -> dict:
    """Agent يولد تقرير تنفيذي احترافي"""

    sources = []
    for item in news_data.get("news", []):
        if item.get("url"):
            sources.append(item["url"])

    prompt = f"""أنت خبير في كتابة التقارير المالية التنفيذية.

بناءً على هذا التحليل:
{analysis_data.get("analysis", "")}

اكتب تقريراً تنفيذياً احترافياً عن: {query}

التقرير يجب أن يتضمن:
1. **ملخص تنفيذي** (3-4 جمل)
2. **أبرز المستجدات**
3. **التحليل المالي**
4. **المخاطر الرئيسية**
5. **التوصيات الاستراتيجية**
6. **الخلاصة**

اكتب بأسلوب احترافي مناسب للمديرين التنفيذيين."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "أنت خبير في كتابة التقارير المالية التنفيذية للشركات الكبرى."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=3000
    )

    report = response.choices[0].message.content

    return {
        "agent": "Report Agent",
        "query": query,
        "report": report,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sources": sources[:5]
    }