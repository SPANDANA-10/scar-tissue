import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

BANK_ID = os.getenv("HINDSIGHT_BANK_ID")


def get_client():
    api_url = os.getenv("HINDSIGHT_API_URL")
    api_key = os.getenv("HINDSIGHT_API_KEY")

    if not api_url or not api_key or not BANK_ID:
        raise ValueError("Missing Hindsight configuration in .env")

    return Hindsight(
        base_url=api_url,
        api_key=api_key
    )


def retain_memory(content, context="Scar Tissue incident history"):
    client = get_client()

    try:
        return client.retain(
            bank_id=BANK_ID,
            content=content,
            context=context
        )
    finally:
        client.close()


def recall_memories(query):
    client = get_client()

    try:
        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        memories = []

        for memory in result.results:
            memories.append({
                "text": memory.text,
                "type": memory.type
            })

        return memories

    finally:
        client.close()