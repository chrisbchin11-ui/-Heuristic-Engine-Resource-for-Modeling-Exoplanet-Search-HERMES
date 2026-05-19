# HERMES
### Heuristic Engine Resource for Modeling Exoplanet Search

## Overview
HERMES is a local agentic AI research assistant designed to automate 
multi-step astronomical research tasks. Built using Ollama and LangChain, 
it autonomously breaks down complex research queries and works through 
them step by step.

## Motivation
Inspired by my work as an undergraduate researcher on the SPORES-HWO 
project — a NASA-funded initiative analyzing radial velocity data for 
120 exoplanet imaging targets — I built HERMES to explore how agentic 
AI can automate astronomical research workflows.

## Tech Stack
- Python
- Ollama (local LLM inference)
- LangChain
- Llama 3.2 (1B parameter model)

## Features
- Autonomous multi-step task completion
- Local inference — runs completely free with no API costs
- Customizable research prompts
- Extensible tool architecture

## Current Limitations
- Relies on training data, not real time database access
- Small model size limits reasoning complexity

## Next Steps
- Connect to NASA Exoplanet Archive API
- Add real time data retrieval tools
- Expand to analyze radial velocity datasets

## Author
Christopher Chin
UC Berkeley | Applied Mathematics
