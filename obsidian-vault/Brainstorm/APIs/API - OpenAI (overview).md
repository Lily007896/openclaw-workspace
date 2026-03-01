# API - OpenAI (overview)

## What it enables
- Text: chat/agents for reasoning + generation
- Speech: transcription + text-to-speech
- Vision: image understanding
- Embeddings: semantic search / retrieval

## Product patterns
- "Wrapper" apps around a specific workflow (e.g., meeting notes, support triage)
- Niche copilots with domain context (documents + RAG)
- Automation: classify/route/summarize

## Notes
- Always evaluate cost per user action (per message / per minute / per image)
- Prefer workflows where user value >> model cost
