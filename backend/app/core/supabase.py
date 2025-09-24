from app.core.config import get_settings
from supabase import create_client, Client

settings = get_settings()


url = settings.SUPABASE_URL
key = settings.SUPABASE_KEY

client: Client = create_client(url, key)


def get_supabase_client() -> Client:
    return client
