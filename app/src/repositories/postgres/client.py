import os
import psycopg
from dotenv import load_dotenv
from psycopg import AsyncConnection

async def get_postgres_client() -> AsyncConnection:
    """
    Create and return a Postgres connection instance.

    Returns:
        AsyncConnection: A psycopg AsyncConnection instance.
    """
    load_dotenv()
    
    # Try getting DSN from environment
    dsn = os.environ.get("POSTGRES_URL")
    
    if not dsn:
        # Construct DSN from individual components
        host = os.environ.get("POSTGRES_HOST", "localhost")
        port = os.environ.get("POSTGRES_PORT", "5432")
        db = os.environ.get("POSTGRES_DB")
        user = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")
        
        if not db or not user or not password:
            raise ValueError(
                "POSTGRES_URL or (POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD) "
                "must be set in environment variables."
            )
        
        dsn = f"postgresql://{user}:{password}@{host}:{port}/{db}"

    print(dsn)
    return await psycopg.AsyncConnection.connect(dsn)
