from openai import AsyncOpenAI
import config as cfg
import asyncio

#--API Implementation--

_client = AsyncOpenAI(api_key=cfg.API_KEY)

def _sync_fetch(messages: list[dict]) -> str:
    cfg.log_checkpoint() # 2
    resp = _client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return str(resp.choices[0].message.content)

async def fetch_api(messages: list[dict]) -> str:
    cfg.log_checkpoint() # 3
    # Run the blocking import+HTTP work off the event loop:
    return await asyncio.to_thread(_sync_fetch, messages)
