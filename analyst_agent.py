import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


async def analyst_agent(news_data: dict, query: str) -> dict:
    """Agent يحلل الأخبار ويستخرج insights مالية"""
    
    # تجميع الأخبار في نص واحد
    news_text = ""
    for item in news_data.get("news", []):
        news_text += f"- {item['title']}: {item['content'][:300]}\n"
    
    prompt = f"""أنت محلل مالي خبير. بناءً على هذه الأخبار، حلل الوضع المالي لـ: {query}

الأخبار:
{news_text}

قدم تحليلاً شاملاً يتضمن:
1. الوضع الحالي
2. المؤشرات الإيجابية
3. المخاطر والتحديات
4. التوقعات قصيرة المدى
5. التوصيات

الرد يجب أن يكون باللغة العربية."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "أنت محلل مالي خبير متخصص في الأسواق العربية والخليجية."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=2000
    )
    
    analysis = response.choices[0].message.content
    
    return {
        "agent": "Analyst Agent",
        "query": query,
        "analysis": analysis,
        "sources_used": len(news_data.get("news", []))
    }