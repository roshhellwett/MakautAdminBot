import os
from typing import Optional
from groq import AsyncGroq
from zenith_ai_bot.prompts import ZENITH_SYSTEM_PROMPT
from zenith_ai_bot.search import perform_web_search
from zenith_ai_bot.youtube import get_youtube_transcript
from core.logger import setup_logger

logger = setup_logger("LLM_ENGINE")
_groq_client: Optional[AsyncGroq] = None

def get_groq_client() -> AsyncGroq:
    """Singleton Groq client to reuse SSL connections."""
    global _groq_client
    if _groq_client is None:
        _groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"), max_retries=2)
    return _groq_client

async def process_ai_query(user_text: str, context_data: str = None) -> str:
    client = get_groq_client()
    external_context = ""
    
    if "youtube.com/watch" in user_text or "youtu.be/" in user_text:
        transcript = await get_youtube_transcript(user_text)
        if transcript: external_context = f"\n\n[YOUTUBE TRANSCRIPT]\n{transcript}"
    elif any(keyword in user_text.lower() for keyword in ["today", "current", "news", "price", "latest", "search"]):
        search_results = await perform_web_search(user_text)
        if search_results: external_context = f"\n\n[LIVE WEB DATA]\n{search_results}\nCite your sources using HTML <a href>."

    final_context = ""
    if context_data:
        short_context = context_data[:2000] + "..." if len(context_data) > 2000 else context_data
        final_context += f"\n\n[CONVERSATION CONTEXT]\n{short_context}"
    
    final_prompt = f"{user_text}{final_context}{external_context}"
    
    try:
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": ZENITH_SYSTEM_PROMPT},
                {"role": "user", "content": final_prompt}
            ],
            model="llama-3.3-70b-versatile", 
            temperature=0.5, 
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq API Error: {e}")
        return "📡 Connection to AI servers lost. Please try again."