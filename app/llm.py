"""Gemini (text generation) client. Uses the "global" location, see .env."""

from typing import TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel

from app import config

_client = genai.Client(vertexai=True, project=config.PROJECT, location=config.GEN_LOCATION)

T = TypeVar("T", bound=BaseModel)


def _config(system: str, temperature: float, **extra) -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        system_instruction=system,
        temperature=temperature,
        # We pass no tools, and LangGraph (not the SDK) controls our agent loop,
        # so switch the SDK's automatic function calling off explicitly.
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        **extra,
    )


def generate(prompt: str, system: str, temperature: float = 0.2) -> str:
    """One Gemini call returning free text. Low temperature = more factual wording."""
    resp = _client.models.generate_content(
        model=config.GEMINI_MODEL, contents=prompt, config=_config(system, temperature)
    )
    return (resp.text or "").strip()


def generate_json(prompt: str, system: str, schema: type[T], temperature: float = 0.0) -> T:
    """
    One Gemini call returning a typed object (structured output).
    Gemini is constrained to produce JSON matching `schema`, and the SDK parses
    it into an instance of that Pydantic class, so there's no text cleanup needed.
    """
    resp = _client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt,
        config=_config(
            system,
            temperature,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    return resp.parsed
