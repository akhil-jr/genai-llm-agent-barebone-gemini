# genai-llm-agent-barebone-gemini

This is a functioning LLM agent built for unerstanding inner working of AI agent. This agent is made as barebone as possible with the aim to undestand each step/API calls happening between the client and the LLM model.

## Features
- Built from scratch
- Does not use any frameworks
- Does not use any modules (except for making LLM API calls)
- Does not follow LLM model specific prompt structure

## This shows:
- how an agent works internally
- how LLM decide to call tools
- Full transparency of input and output prompts at each step

## Quick Start
```bash
git clone https://github.com/akhil-jr/genai-llm-agent-barebone-gemini.git
```
```bash
cd genai-llm-agent-barebone-gemini
```
```bash
pip install -r requirements.txt
```
```bash
cp .env.example .env
#Add your gemini API key in .env file
```
```bash
python -m src.main

```