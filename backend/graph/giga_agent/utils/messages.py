from langchain_core.messages import ToolMessage, AIMessage


def filter_tool_messages(messages):
    filtered_messages = []
    for idx, msg in enumerate(messages):
        if isinstance(msg, ToolMessage):
            if idx - 1 <= 0:
                continue
            ai_message_tool_called = (
                messages[idx - 1].additional_kwargs.get("function_call")
                or messages[idx - 1].tool_calls
            )
            if not ai_message_tool_called:
                continue
        filtered_messages.append(msg)
    return filtered_messages
