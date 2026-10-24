from openai import OpenAI

from app.core.config import settings

_client = OpenAI(
    api_key=settings.llm_api_key,
    base_url=settings.llm_base_url,
    timeout=30.0,
    max_retries=2,
)


def ask_llm(system_prompt: str, user_prompt: str, temperature: float = 0.0) -> str:
    """Send a prompt to the model and return its text reply.

    temperature=0 means 'be consistent, don't get creative', which is what we want for SQL.
    """
    response = _client.chat.completions.create(
        model=settings.llm_model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""