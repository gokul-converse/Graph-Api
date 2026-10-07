import json
from pathlib import Path
from datetime import datetime, timezone

REGISTRY_FILE = Path("conversation_registry.json")

def create_conversation(session_id: str, title: str):
    if REGISTRY_FILE.exists():
        with open(REGISTRY_FILE, "r") as file:
            conversations = json.load(file)
    else:
        conversations = []

    # Check whether this session already exists
    for conversation in conversations:
        if conversation["session_id"] == session_id:
            return conversation

    now = datetime.now(timezone.utc).isoformat()

    conversation = {
        "session_id": session_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
    }

    conversations.append(conversation)

    with open(REGISTRY_FILE, "w") as file:
        json.dump(conversations, file, indent=2)

    return conversation

def get_conversations():
    if not REGISTRY_FILE.exists():
        return []

    with open(REGISTRY_FILE, "r") as file:
        conversations = json.load(file)

    return conversations


if __name__ == "__main__":
    result = create_conversation(
        session_id="test-session-221",
        title="My second chat"
    )

    print("Created:")
    print(result)

    print("\nAll conversations:")
    print(get_conversations())