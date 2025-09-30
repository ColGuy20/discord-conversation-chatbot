import config as cfg
import api

#--Direct Message Conversation--

# IN DEVELOPMENT
async def conversation_start(language: str, intended_profile: str) -> str:
    p = cfg.profile_info(intended_profile)

    response = await api.first_prompt(p, language)
    return response  

async def conversation():
    return
