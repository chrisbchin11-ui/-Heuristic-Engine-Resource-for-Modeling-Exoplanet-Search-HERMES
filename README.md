# HERMES
### Heuristic Engine Resource for Modeling Exoplanet Search

## Overview
HERMES is a local agentic AI research assistant designed to automate 
multi-step astronomical research tasks. It combines real-time data 
retrieval from NASA's Exoplanet Archive with local AI analysis to 
provide structured insights on confirmed exoplanetary systems.

## Motivation
Inspired by my work as an undergraduate researcher on the SPORES-HWO 
project — a NASA-funded initiative analyzing radial velocity data for 
120 exoplanet imaging targets published in The Astronomical Journal 
(Volume 170, Issue 6, 2025) — I built HERMES to explore how agentic 
AI can automate astronomical research workflows.

## Tech Stack
- Python
- Ollama (local LLM inference)
- LangChain
- Meta's Llama 3.2 (1B parameter model)
- NASA Exoplanet Archive TAP API

## Features
- Real-time queries to NASA's Exoplanet Archive Planetary Systems database
- Retrieves confirmed planet data including orbital periods, radius, mass, and discovery method
- AI-powered analysis of planetary systems using local LLM inference
- Clean structured data output
- Runs completely free with no API costs
- Works on any star in NASA's database

## Current Limitations
- Relies on Llama 3.2 1B parameter model which occasionally misinterprets 
  units or makes factual errors in analysis
- A larger model or fact-checking tool would improve accuracy
- AI analysis draws from training data for context, not real-time literature

## Next Steps
- Upgrade to a more powerful model for more accurate analysis
- Add multiple tools including web search and literature retrieval
- Connect to additional NASA databases beyond confirmed planets
- Add memory so HERMES can compare multiple star systems
- Build a simple user interface for easier interaction

## Example Output
Running HERMES on tau Ceti — a star analyzed in the SPORES-HWO paper —
returns real confirmed planet data from NASA's database along with 
AI-generated analysis of the planetary system.

## Author
Christopher Chin
UC Berkeley | Applied Mathematics
Co-author, The Astronomical Journal (Volume 170, Issue 6, 2025)
GitHub: [your github here]
Email: chrisbchin11@gmail.com
