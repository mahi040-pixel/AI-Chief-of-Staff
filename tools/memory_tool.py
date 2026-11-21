from agents import function_tool
from memory.memory import load_memory, save_memory


@function_tool
def save_conversation_memory(user_message: str, assistant_response: str) -> str:
    """
    Save a user message and assistant response to conversation memory.
    """
    try:
        save_memory(user_message, assistant_response)
        return "Conversation successfully saved to memory."
    except Exception as e:
        return f"Unable to save memory: {str(e)}"


@function_tool
def retrieve_recent_memory(limit: int = 5) -> str:
    """
    Retrieve recent conversation history from memory.
    """
    try:
        history = load_memory()

        if not history:
            return "No conversation memory available."

        limit = max(1, min(limit, 20))
        recent_history = history[-limit:]

        result = []

        for item in recent_history:
            result.append(
                f"User: {item.get('user', '')}\n"
                f"Assistant: {item.get('assistant', '')}"
            )

        return "\n\n".join(result)

    except Exception as e:
        return f"Unable to retrieve memory: {str(e)}"