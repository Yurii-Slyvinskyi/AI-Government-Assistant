from openai import AsyncOpenAI
from fastapi import HTTPException
from ..core.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def get_answer_from_llm(question: str, context_chunks: list[str]) -> str:
    if not question:
        raise HTTPException(status_code=400, detail="No question provided")
    if not context_chunks:
        raise HTTPException(status_code=400, detail="No context_chunks provided")

    context = "\n\n".join(context_chunks)
    prompt = f"""
    You are an expert AI assistant for the Government of Alberta. 
    Thousands of people will use you, so your answers must be:
    - Accurate and based ONLY on the provided context.
    - Friendly, professional, and easy to read.
    - Helpful even when the question is vague or off-topic.

    ## Core Guidelines:
    1. If the question is off-topic (e.g., about cars, brands, etc.):
       - Politely acknowledge this.
       - Redirect to a relevant Alberta-related service (e.g., vehicle registration, insurance, regulations).
    2. If the question is vague:
       - Ask politely for clarification.
       - Meanwhile, give a small piece of useful info from the context.
    3. If no relevant context is found:
       - Do NOT say only "I don’t know".
       - Instead, explain what type of Alberta information you *can* provide, and invite them to ask.
    4. Never invent facts or URLs. Use only what is in the context.
    5. Always keep the tone polite, approachable, and human-like.

    ## Answer Structure:
    - **Brief Definition**: 1–2 sentences that summarize the concept (if applicable).
    - **Key Points**: bullet points with the most important facts or steps.
    - **Sources**: always show the original URLs from the context exactly as they appear.
    - **Invitation**: end with a friendly offer to provide more details if needed.

    ## Important:
    - Support multiple languages (answer in the user’s language).
    - Be concise but structured.
    - Always look like a knowledgeable, approachable expert.

    ---
    Context:
    {context}

    Question:
    {question}
    """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.2,
    )

    return response.choices[0].message.content
