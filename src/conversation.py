import asyncio
from typing import Tuple
import config as cfg
import api

#--Direct Message Conversation--

LOCK = asyncio.Lock()

# Session Functions
async def start_session(language: str, intended_profile: str, user_id: int) -> str:
    profile = cfg.profile_info(intended_profile)

    prompt = f"""
        You are an educational language tutor. 
        Your purpose is to help the user learn {language} through natural conversation. 

        You will roleplay as the following character:
        - Name: {profile.name}
        - Age: {profile.age}
        - Gender: {profile.gender}
        - Occupation: {profile.work}
        - Personality: {profile.description}

        Rules:
        1. Stay in character at all times. Do not mention you are an AI or chatbot.
        2. Speak only in {language}.
        3. Use simple, traditional phrases when starting conversations.
        4. Occasionally explain meanings or correct the user, but keep the tone friendly and encouraging.
        5. Respond as if you are {profile.name}, not as an assistant.
    """.strip()

    async with LOCK:
        cfg.SESSIONS[user_id] = cfg.Session(
            user_id=user_id,
            language=language,
            profile=profile,
            messages=[{"role": "system", "content": prompt}],
            active=True,
        )

    greeting = "Hello. What is your name and age?"
    resp = await append_and_reply(user_id, {"role": "user", "content": greeting})
    return resp 

def has_session(user_id: int) -> bool:
    s = cfg.SESSIONS.get(user_id)
    return bool(s and s.active)

async def end_session(user_id: int) -> str:
    async with LOCK:
        s = cfg.SESSIONS.get(user_id)
        if not s:
            return "No active session. Use /launch to start one."
        s.active = False
    return "Session ended. Thanks for chatting!"

# Conversation Functions
async def conversation(user_id: int, incoming_text: str) -> Tuple[str, bool]:
    s = cfg.SESSIONS.get(user_id)
    if not s or not s.active:
        return ("No active session. Use /launch to start one.", False)

    if incoming_text.strip().lower() in cfg.STOP_WORDS:
        end_msg = await end_session(user_id)
        return (end_msg, False)

    reply = await append_and_reply(user_id, {"role": "user", "content": incoming_text})
    return (reply, cfg.SESSIONS.get(user_id, s).active)

async def append_and_reply(user_id: int, new_message: dict) -> str:
    s = cfg.SESSIONS.get(user_id)
    if not s or not s.active:
        return "No active session. Use /launch to start one."

    async with LOCK:
        s.messages.append(new_message)

    response = await api.fetch_api(s.messages)

    async with LOCK:
        s.messages.append({"role": "assistant", "content": response})

    return response
