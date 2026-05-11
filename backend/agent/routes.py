from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Chat"])

class ChatMessage(BaseModel):
    role: str
    text: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    success: bool
    reply: str
    error: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle follow-up chat questions using the configured LLM.
    """
    if not settings.gemini_api_key and not settings.openai_api_key:
        return ChatResponse(
            success=False, 
            reply="I'm sorry, my AI brain (LLM) isn't connected right now. Please add an API key to the .env file!"
        )

    system_instruction = (
        "You are PlantBot, a friendly and knowledgeable AI plant pathologist assistant. "
        "You help farmers, gardeners, and plant enthusiasts with plant disease diagnosis, "
        "treatment advice, prevention strategies, and general plant care.\n\n"

        "## Response Guidelines\n"
        "1. **For new disease diagnosis requests** (e.g. when a user first describes symptoms or "
        "asks about a specific disease), use this structured format:\n"
        "   ***Plant Disease:*** [Name]\n"
        "   ***Reasons:*** bullet list\n"
        "   ***Treatments:*** bullet list\n"
        "   ***Preventions:*** bullet list\n"
        "   ***Summary Advices:*** bullet list\n\n"

        "2. **For ALL follow-up questions**, respond naturally and conversationally. "
        "Follow-ups include (but are not limited to):\n"
        "   - \"Any other tips?\" → give additional practical advice\n"
        "   - \"Can I use X instead of Y?\" → compare alternatives, explain pros/cons\n"
        "   - \"I need more information about ...\" → expand on the topic in depth\n"
        "   - \"What if ...?\" → address the hypothetical scenario\n"
        "   - \"How long does ...?\" → give timeline estimates\n"
        "   - \"Is it safe to ...?\" → give safety guidance\n"
        "   - Clarification questions → explain more clearly\n"
        "   - Gratitude (\"thanks\", \"thank you\") → respond warmly\n"
        "   - Greetings → greet back and offer help\n\n"

        "3. **Conversation rules:**\n"
        "   - Always consider the full conversation history to understand context.\n"
        "   - Reference previous messages when relevant (e.g. 'As I mentioned earlier...').\n"
        "   - Be warm, supportive, and encouraging.\n"
        "   - Use markdown formatting (bold, lists, headers) to keep answers readable.\n"
        "   - Keep answers concise but thorough — typically 100-300 words.\n"
        "   - If you don't know something, say so honestly and suggest alternatives.\n"
        "   - Stay on topic: plant diseases, plant care, gardening, and agriculture.\n"
        "   - If the user asks something completely unrelated to plants, "
        "politely redirect them back to plant-related topics.\n"
    )

    # Build conversation context
    prompt = f"{system_instruction}\n\n"

    # Add history (keep last 10 messages for better conversational context)
    for msg in request.history[-10:]:
        role_name = "User" if msg.role == "user" else "PlantBot"
        prompt += f"{role_name}: {msg.text}\n"

    prompt += f"User: {request.message}\nPlantBot:"

    try:
        if settings.llm_provider == "gemini" and settings.gemini_api_key:
            from google import genai
            client = genai.Client(api_key=settings.gemini_api_key)
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
            )
            return ChatResponse(success=True, reply=response.text)

        elif settings.llm_provider == "openai" and settings.openai_api_key:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            completion = client.chat.completions.create(
                model=settings.openai_model,
                messages=[{"role": "system", "content": system_instruction}] + 
                         [{"role": "user" if m.role == "user" else "assistant", "content": m.text} for m in request.history[-10:]] +
                         [{"role": "user", "content": request.message}],
            )
            return ChatResponse(success=True, reply=completion.choices[0].message.content)
            
    except Exception as exc:
        logger.error(f"LLM Error: {exc}")
        return ChatResponse(success=False, reply="Sorry, I encountered an error while thinking. Please try again.", error=str(exc))

    return ChatResponse(success=False, reply="No valid LLM configuration found.")
