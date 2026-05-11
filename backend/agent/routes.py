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
        "You are PlantBot, a helpful AI plant pathologist. "
        "You must output your answer STRICTLY in the following format:\n\n"
        "***Plant Disease:*** [Name of the disease]\n\n"
        "***Reasons:***\n"
        "- [Reason 1]\n"
        "- [Reason 2]\n\n"
        "***Treatments:***\n"
        "- [Treatment 1]\n"
        "- [Treatment 2]\n\n"
        "***Preventions:***\n"
        "- [Prevention 1]\n"
        "- [Prevention 2]\n\n"
        "***Summary Advices:***\n"
        "- [Advice 1]\n"
        "- [Advice 2]\n\n"
        "Do not include any other conversational filler or extra paragraphs outside of this structure."
    )

    # Build conversation context
    prompt = f"{system_instruction}\n\n"
    
    # Add history
    for msg in request.history[-5:]: # Keep last 5 messages for context
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
                         [{"role": "user" if m.role == "user" else "assistant", "content": m.text} for m in request.history[-5:]] +
                         [{"role": "user", "content": request.message}],
            )
            return ChatResponse(success=True, reply=completion.choices[0].message.content)
            
    except Exception as exc:
        logger.error(f"LLM Error: {exc}")
        return ChatResponse(success=False, reply="Sorry, I encountered an error while thinking. Please try again.", error=str(exc))

    return ChatResponse(success=False, reply="No valid LLM configuration found.")
