import time

from openai import (
    OpenAI,
    AuthenticationError,
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
    BadRequestError,
)

from config import OPENAI_API_KEY, DEFAULT_MODEL


def get_client():
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it to the .env file."
        )

    return OpenAI(
        api_key=OPENAI_API_KEY
    )


def generate_response(
    system_prompt,
    messages,
    model=DEFAULT_MODEL,
    max_output_tokens=700,
    max_retries=3
):
    client = get_client()

    for attempt in range(max_retries):

        try:
            response = client.responses.create(
                model=model,
                instructions=system_prompt,
                input=messages,
                max_output_tokens=max_output_tokens,
            )

            return response.output_text

        except AuthenticationError:
            return (
                "Authentication failed. "
                "Please check the API key."
            )

        except RateLimitError:

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)

            else:
                return (
                    "The AI service is temporarily busy. "
                    "Please try again shortly."
                )

        except APITimeoutError:
            return (
                "The AI service took too long to respond. "
                "Please try again."
            )

        except APIConnectionError:
            return (
                "Unable to connect to the AI service. "
                "Please check your internet connection."
            )

        except BadRequestError:
            return (
                "The request could not be processed. "
                "Please try again."
            )

        except Exception:
            return (
                "Something went wrong while generating the response. "
                "Please try again."
            )