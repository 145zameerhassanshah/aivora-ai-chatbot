# Aivora AI

**Aivora AI** is a professional multi-role AI chatbot built with Python, Streamlit, and an LLM API.

The project demonstrates how modern AI applications can securely connect to a hosted Large Language Model while combining dynamic system prompts, conversation context, multilingual interaction, error handling, and an interactive chatbot interface.

---

## Project Objective

The objective of this project was to learn and practically implement secure LLM API integration in Python.

The project covers:

- Secure API authentication
- Environment variables
- LLM request and response handling
- System prompts
- Prompt design patterns
- Multi-turn conversation context
- Error handling
- Rate-limit handling
- Retry logic
- Streamlit chatbot development
- UI/UX design
- Multilingual interaction
- Modular project architecture

---

## Features

### Multi-Role AI Assistant

Aivora AI supports multiple assistant modes:

- General Assistant
- AI Tutor
- Health Education
- Research Assistant
- Marketing Assistant
- Coding Assistant
- Politics & Civic Information

Each mode uses a different system prompt with its own:

- Role
- Audience
- Tone
- Rules
- Response behavior
- Safety boundaries

---

## Dynamic System Prompts

The chatbot dynamically selects a system prompt based on the assistant mode chosen by the user.

For example:

- AI Tutor provides beginner-to-advanced explanations.
- Marketing Assistant focuses on strategy and creative marketing.
- Coding Assistant provides technical and debugging support.
- Research Assistant provides academic and methodology-oriented guidance.
- Health Education provides general healthcare education with safety boundaries.

---

## Conversation Context

The chatbot supports multi-turn conversations.

This allows short follow-up messages such as:

```text
Who is Babar Azam?