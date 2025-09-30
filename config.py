import os
from dotenv import load_dotenv

#--Store Config (Variables/Classes/etc.)--

# VARIABLES
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("DISCORD_ID"))
API_KEY = os.getenv("API_KEY")

# PROFILE TOKENS
TOKEN_P1 = os.getenv("PROFILE_TOKEN_1")
TOKEN_P2 = os.getenv("PROFILE_TOKEN_2")
TOKEN_P3 = os.getenv("PROFILE_TOKEN_3")

# Profile Constructor
class Profile:
    def __init__(self, name: str, age: int, token: str, gender: str, description: str, work: str, language: str):
        self.name = name
        self.age = age
        self.token = token
        self.gender = gender
        self.description = description
        self.work = work
        self.language = language

# PROFILES
profiles_array = [
    Profile("Bob", 24, TOKEN_P1, "male", "friendly", "teacher", "english"),
    Profile("Amy", 31, TOKEN_P2, "female", "witty", "secretary at finance company", "english"),
    Profile("Jorge", 38, TOKEN_P3, "male", "hardworking", "construction", "spanish")
]

# Profile Functions
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

# LANGUAGES
lang_array = [
    "English",
    "Spanish",
    "Japanese",
    "Korean"
]
