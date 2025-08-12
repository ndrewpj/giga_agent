from langchain_core.messages import ToolMessage


def filter_tool_messages(messages):
    filtered_messages = []
    for idx, msg in enumerate(messages):
        if isinstance(msg, ToolMessage):
            if idx - 1 > 0 and not messages[idx - 1].additional_kwargs.get(
                "function_call"
            ):
                continue
        filtered_messages.append(msg)
    return filtered_messages
