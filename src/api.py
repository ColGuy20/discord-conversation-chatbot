from openai import AsyncOpenAI
import config as cfg

#--API Implementation--

_client = AsyncOpenAI(api_key=cfg.API_KEY)

async def fetch_api(messages: list[dict]) -> str:
    resp = await _client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return str(resp.choices[0].message.content)

# NEW: force lazy imports before the Discord event loop starts
def prime_imports():
    _ = _client.chat
