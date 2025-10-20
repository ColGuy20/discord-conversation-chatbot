import os
from dataclasses import dataclass, field
import asyncio
from typing import Dict, List
from dotenv import load_dotenv

#--Store Config (Variables/Classes/etc.)--

# Profile Class
@dataclass
class Profile:
    name: str
    age: int
    token: str
    gender: str
    description: str
    work: str
    language: str

# Session Class
@dataclass
class Session:
    user_id: int
    user_name: str
    language: str
    profile: Profile
    messages: List[dict] = field(default_factory=list)
    active: bool = True
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

# VARIABLES
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("DISCORD_ID"))
API_KEY = os.getenv("API_KEY")
SESSIONS: Dict[int, Session] = {}
STOP_WORDS = {
    "end",
    "/end",
    "quit",
    "exit",
    "stop"
    }

# PROFILE TOKENS
TOKEN_P1 = os.getenv("PROFILE_TOKEN_1")
TOKEN_P2 = os.getenv("PROFILE_TOKEN_2")
TOKEN_P3 = os.getenv("PROFILE_TOKEN_3")

# PROFILES
profiles_array = [
    Profile("Bob", 24, TOKEN_P1, "male", "friendly", "teacher", "english"),
    Profile("Amy", 31, TOKEN_P2, "female", "witty", "secretary at finance company", "english"),
    Profile("Jorge", 38, TOKEN_P3, "male", "hardworking", "construction", "spanish")
]

# LANGUAGES
lang_array = [
    "English",
    "Spanish",
    "Japanese",
    "Korean",
    "Arabic"
]

# Functions
def list_profile_names() -> list[str]:
    return [p.name for p in profiles_array]

def profile_info(intended_profile) -> Profile:
    for p in profiles_array:
        if p.name.lower() == intended_profile.lower():
            return p

# To be worked on later
def recommended_language(chosen_language):
    for p in profiles_array:
        if p.language.lower() == chosen_language:
            # Add profile
            return ""

def temp_log(chp: str):
    print(f"[LOG] Checkpoint {chp}")
