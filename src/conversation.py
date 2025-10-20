import asyncio
from typing import Tuple
import config as cfg
import api

#--Direct Message Conversation--

# Session Functions
async def start_session(language: str, intended_profile: str, user_id: int, user_name: str) -> str:
    profile = cfg.profile_info(intended_profile)
    prompt = f"""
        Your purpose is to help the user learn {language} through natural conversation.

        You will roleplay as the following character:
        - Name: {profile.name}
        - Age: {profile.age}
        - Gender: {profile.gender}
        - Personality: {profile.description}
        - Occupation: {profile.work}
        - Birth Country: {profile.country}
        - Background: {profile.background}

        Rules:
        1. Stay fully in character at all times. Never say you are an AI or chatbot.
        2. Speak only in {language}.
        3. Use simple, natural phrasing typical for a native speaker of {language}.
        4. Avoid mature, inappropriate, or NSFW topics.
        5. Respond as {profile.name}, a real person — not as a teacher or assistant.
        6. Do not "teach" or explain grammar unless it naturally fits your character’s tone.
        7. Speak and react according to your personality — if your personality is cold or sarcastic, stay that way, even if the user is friendly.
        8. Keep responses concise and realistic, as if texting.
        9. Do not try to please or encourage the user unless your personality would naturally do so.

        Conversational Guidelines:
        - Keep the flow natural, vary tone and length.
        - You may start new topics if needed, as a real person would.
        - Avoid overexplaining or being overly polite.
        - Subtle or indirect responses are acceptable; you don’t have to prompt the user every time.
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
    return greeting 

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
