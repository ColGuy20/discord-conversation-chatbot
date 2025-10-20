import asyncio
from typing import Tuple
import config as cfg
import api

#--Direct Message Conversation--

# Session Functions
async def start_session(language: str, intended_profile: str, user_id: int, user_name: str) -> str:
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

    new_session = cfg.Session(
        user_id=user_id,
        user_name=user_name,
        language=language,
        profile=profile,
        messages=[{"role": "system", "content": prompt}],
        active=True,
    )

    cfg.SESSIONS[user_id] = new_session
    greeting = "Hello. What is your name and age?"
    resp = await append_and_reply(user_id, {"role": "user", "content": greeting})
    return resp 

def has_session(user_id: int) -> bool:
    s = cfg.SESSIONS.get(user_id)
    return bool(s and s.active)

async def end_session(user_id: int) -> str:
    s = cfg.SESSIONS.get(user_id)
    if not s or not s.active:
        return "No active session. Use /launch to start one."
    async with s.lock:
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

    async with s.lock:
        s.messages.append(new_message)

    response = await api.fetch_api(s.messages)

    async with s.lock:
        s.messages.append({"role": "assistant", "content": response})

    return response
