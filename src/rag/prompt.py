def build_prompt(question, retrieved_docs):
    """Combine retrieved knowledge and the user's question into one prompt."""
    context = "\n\n".join(doc["content"] for doc in retrieved_docs)

    prompt = f"""Use the following context to answer the question.
If the context doesn't contain enough information, say so honestly instead of guessing.

Context:
{context}

Question: {question}
"""
    return prompt