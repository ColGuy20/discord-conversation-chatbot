import os
from dotenv import load_dotenv

#--Store Config (Variables/Classes/etc.)--

# VARIABLES
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("DISCORD_ID"))
#TIMEOUT_SECONDS = 900 [TO-DO]

# PROFILE TOKENS
TOKEN_P1 = os.getenv("PROFILE_TOKEN_1")
TOKEN_P2 = os.getenv("PROFILE_TOKEN_2")
TOKEN_P3 = os.getenv("PROFILE_TOKEN_3")

# Profile Constructor
class Profile:
    def __init__(self, name: str, age: int, token: str):
        self.name = name
        self.age = age
        self.token = token

# PROFILES
profiles_array = [
    Profile("Bob", 24, TOKEN_P1),
    Profile("Amy", 31, TOKEN_P2),
    Profile("Jorge", 38, TOKEN_P3)
]


# Profile Functions
def list_profile_names() -> list[str]:
    return [p.name for p in profiles_array]

def profile_info(intended_profile) -> Profile:
    for p in profiles_array:
        if p.name.lower() == intended_profile.lower():
            return p

# LANGUAGES
lang_array = [
    "English",
    "Spanish",
    "Japanese",
    "Korean"
]
