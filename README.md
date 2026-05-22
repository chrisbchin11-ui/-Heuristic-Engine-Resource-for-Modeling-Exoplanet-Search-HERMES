# HERMES
### Heuristic Engine Resource for Modeling Exoplanet Search

## Overview
HERMES is a local agentic AI research assistant designed to automate 
multi-step astronomical research tasks. It combines real-time data 
retrieval from NASA's Exoplanet Archive with local AI analysis to 
provide structured insights on confirmed exoplanetary systems.

## Motivation
My experience as an undergraduate researcher on the SPORES-HWO 
project (led by Professor Courntey Dressing and Ph.d candidate Caleb Harada at Berkeley)
— a NASA-funded initiative analyzing radial velocity data for 
120 exoplanet imaging targets published in The Astronomical Journal 
(Volume 170, Issue 6, 2025) — inspired me to build HERMES to explore how agentic 
AI can automate astronomical research workflows.

Named after Hermes, the Greek messenger god who traveled between worlds,
HERMES travels between NASA databases to retrieve and analyze exoplanetary
data autonomously.

## Tech Stack
- Python
- Ollama (local LLM inference)
- LangChain
- Meta's Llama 3.2 (1B parameter model)
- NASA Exoplanet Archive TAP API

## Features
- Real-time queries to NASA's Exoplanet Archive Planetary Systems database
- Retrieves confirmed planet data including orbital periods, radius, mass, 
  and discovery method
- Habitable zone classification using Kepler's Third Law to determine if 
  confirmed planets fall within their star's habitable zone
- Multi-star comparison — analyze and compare multiple planetary systems 
  simultaneously
- Automatic deduplication of multiple measurements for the same planet
- AI-powered analysis and commentary using local LLM inference
- Graceful error handling for network timeouts and missing data
- Runs completely free with no API costs
- Works on any star in NASA's confirmed planets database

## Example Output
Running HERMES on tau Ceti, HD 192310, and 55 Cancri returns:
- Real confirmed planet data from NASA's Exoplanet Archive
- Habitable zone classification for each planet
- Side by side comparison of all three systems
- AI generated comparative analysis

Notable findings:
- tau Cet f: 1.45 AU — IN habitable zone ✓
- HD 192310 c: 1.27 AU — IN habitable zone ✓

HD 192310 is a star personally analyzed by the author during the 
SPORES-HWO research project.

## Current Limitations
- Llama 3.2 1B parameter model occasionally makes factual errors 
  in analysis — a larger model would improve accuracy
- Habitable zone calculation assumes solar mass stellar properties 
  by default — stellar mass data would improve precision
- AI analysis draws from training data for context, not real time 
  literature

## Next Steps
- Upgrade to a more powerful model for more accurate analysis
- Add stellar mass data to improve habitable zone calculations
- Connect to additional NASA databases beyond confirmed planets
- Add web search for recent literature on specific star systems
- Add memory so HERMES can track and compare queries across sessions
- Build a simple command line interface for interactive use

## Author
Christopher Chin
UC Berkeley Class of 2028 | Applied Mathematics (cluster in Numerical Analysis)
| Co-author, The Astronomical Journal (Volume 170, Issue 6, id.343, 56 pp.)
| GitHub:(https://github.com/chrisbchin11-ui)
| Email: chrisbchin11@gmail.com
