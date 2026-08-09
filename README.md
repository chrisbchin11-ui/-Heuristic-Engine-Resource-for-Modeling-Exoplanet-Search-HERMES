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
(Vol. 170, Issue 6, id.343, 56 pp.) — inspired me to build HERMES to explore how agentic 
AI can automate astronomical research workflows.

## Tech Stack
- Python
- LangChain
- Groq API
- Meta's Llama 3.3 (70B parameter model)
- NASA Exoplanet Archive TAP API
- ExoFOP-TESS
- Requests Library
- Python-Dotenv
- Lightkurve
- Matplotlib

## Features
- Real-time queries to NASA's Exoplanet Archive Planetary Systems database and TESS Objects of Interest (TOI) database 
- Retrieves confirmed planet data including orbital periods, radius, mass and discovery method for any star in the archive
- Retrieves unconfirmed exoplanet signal data from TOI database
- Habitable zone classification using Kepler's Third Law and real NASA stellar luminosity data to accurately calculate each planet's orbital distance and classify whether it falls within its star's habitable zone
- Multi-star comparison — analyze and compare multiple planetary systems simultaneously
- Automatic deduplication of multiple measurements for the same planet
- Deep AI-powered scientific analysis using Meta's Llama 3.3 70B via Groq API including:
  - Star type classification and solar comparison
  - Per-planet environmental assessment based on orbital characteristics
  - Habitability evaluation including liquid water potential
  - Comparative context against our Solar System
  - Specific future observation and mission recommendations
- Error handling for network timeouts and missing data
- Local Ollama fallback (Llama 3.2 1B) if Groq API is unavailable (no API key found)
- Works on any confirmed planet hosting star in NASA's database
- Runs completely free using Groq's free API tier

## Example Output
Running HERMES on tau Ceti, HD 192310, and 55 Cancri returns:
- Real confirmed planet data from NASA's Exoplanet Archive
- Habitable zone classification for each planet
- Side by side comparison of all three systems
- AI generated comparative analysis

Notable findings:
- tau Cet f: 1.45 AU — IN habitable zone ✓
- HD 192310 c: 1.27 AU — IN habitable zone ✓

PS: I analyzed data for HD 192310, Tau Ceti, and the Alpha Centauri system during the 
SPORES-HWO research project.

## Current Limitations
- **Real Time Literature** — model relies on training data cutoff and cannot access papers or discoveries published after its training date
- **Habitable Zone Accuracy** — calculations are optimized for F, G, and K type main sequence stars; M-type stars, binary systems, white dwarfs, and supergiants produce less accurate results
- **Missing Stellar Data** — some stars in NASA's archive have null values for luminosity, mass, or temperature; HERMES defaults to solar values when data is missing which reduces accuracy
- **No Atmospheric Analysis** — HERMES assesses orbital habitability but cannot evaluate atmospheric composition, a critical factor for true habitability determination
- **Confirmed Planets Only** — queries confirmed planets only; candidate signals and unconfirmed detections are not included
- **Groq API Dependency** — full analysis quality requires active internet connection and Groq API access; falls back to local Llama 3.2 1B without it

## Next Steps
- Connect to additional NASA databases beyond confirmed planets
- Add web search for recent literature on specific star systems
- Add memory so HERMES can track and compare queries across sessions
- Build a simple command line interface for interactive use

## Changelog

### agent.py — Base Agent (Starting Point)
- First working AI agent built using LangChain and Ollama
- Connects to Meta's Llama 3.2 1B model running locally through Ollama
- Sends a multi-step research prompt asking the AI to:
  1. Find information about exoplanets
  2. Summarize key points
  3. Suggest next steps for research
- AI generates responses purely from training data; no real data sources
- No tools, no APIs, no external data, just prompt and response
- Establishes the foundation that all subsequent HERMES versions build upon
- Runs completely free with no API costs

### hermes.py — Base Model
- Connected to NASA Exoplanet Archive TAP API
- Pulls confirmed planet data including name, orbital period, discovery method, radius and mass
- Basic AI analysis using Llama 3.2 via Ollama

### hermes2.py — Habitable Zone Update
- Added habitable zone calculator using Kepler's Third Law
- Classifies each planet as too close, in habitable zone, or too far
- Added None handling for missing orbital period data

### hermes3.py — Multi-Star Comparison
- Added compare_systems function to analyze multiple stars simultaneously
- Added deduplication to remove duplicate planet measurements
- Simplified AI prompt for cleaner more accurate analysis
- Added graceful error handling for network timeouts

### hermes4.py — Full Interactive Tool (Llama 3.2 1B Model)
- Added stellar mass lookup from NASA database for more accurate HZ calculations
- Updated habitable zone calculator to use real stellar mass instead of assuming solar mass
- Added interactive command line interface with menu
- User can now type any star name and get results instantly

### hermes5.py - Stellar Luminosity Update
- Added stellar luminosity search query for more accurate habitable zone calculations

### hermes6.py - Full Interactive Tool (Llama 3.3 70B Model via Groq API)
- Interchanged Llama 3.2 1B model for Llama 3.3 70B model for more accurate scientific analysis

### hermes7.py - Querying TESS Objects of Interest (TOI) Database Capability
- Added TOI database for user to query unconfirmed exoplanet signals and Llama 3.3 70B model analysis

### hermes8.py - TESS Light Curve Plotting and Binning Capability
- Integrated lightkurve and matplotlib to fetch, stitch, and render photometric light curve data from NASA's MAST archive
- Added an automated TAP query function to pull orbital periods and transit midpoints directly from the NASA Exoplanet Archive TOI database
- Implemented phase-folding and 15-minute data binning (.fold() and .bin()) to extract faint exoplanet transits from background noise.  

### nasa_test_data.py — Calling Data from NASA Exoplanet API
- Tested to see if confirmed exoplanet data from the API could be extracted 
- Received variables such as Planet Name, Orbital Period, Discovery Method, Radius and Mass

## Author
Christopher Chin
UC Berkeley Class of 2028 | Applied Mathematics (cluster in Numerical Analysis)
| Agentic AI Research Assistant @ Lawrence Berkeley National Laboratory
| Co-author, The Astronomical Journal (Volume 170, Issue 6, id.343, 56 pp.)
| GitHub:(https://github.com/chrisbchin11-ui)
| Email: chrisbchin11@gmail.com
