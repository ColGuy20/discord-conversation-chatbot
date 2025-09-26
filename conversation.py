import config as cfg

#--Direct Message Conversation--

# IN DEVELOPMENT
def conversation_start(language: str, intended_profile: str) -> str:
    p = cfg.profile_info(intended_profile)

    first_msg = f"Hello! I am {p.name}. I am {p.age} years old. I will be speaking {language} with you!"
    # TOKEN is p.token
