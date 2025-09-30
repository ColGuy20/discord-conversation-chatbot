from openai import AsyncOpenAI
import config as cfg

#--API Implementation--

client = AsyncOpenAI(api_key=cfg.API_KEY)

async def fetch_api(desc: str, prompt: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": desc},
            {"role": "user", "content": prompt}
        ]
    )
    return str(response.choices[0].message.content)

async def first_prompt(profile, language: str) -> str:
    return await fetch_api(
        f"""
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
        """.strip(),
        f"Hello. What is your name and age?"
    )