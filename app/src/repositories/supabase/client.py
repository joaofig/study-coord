import os

from dotenv import load_dotenv
from supabase._async.client import AsyncClient as Client, create_client


async def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance.

    Returns:
        Client: A Supabase client instance.
    """
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables."
        )

    return await create_client(url, key)
