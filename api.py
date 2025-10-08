from openai import AsyncOpenAI
import config as cfg

#--API Implementation--

client = AsyncOpenAI(api_key=cfg.API_KEY)

async def fetch_api(messages: list[dict]) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return str(response.choices[0].message.content)
