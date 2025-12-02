from app.rag.embeddings import embed_text

def summarize_messages(messages):
    """
    Simple summarizer that keeps the last 5 messages
    and compresses older ones into a small summary.
    """

    if len(messages) <= 5:
        return messages

    main_content = " ".join(m["content"] for m in messages[:-5])
    summary = f"Conversation summary: {main_content[:300]}..."

    new_messages = [
        {"role": "system", "content": summary}
    ] + messages[-5:]

    return new_messages
