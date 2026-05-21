import requests
from langchain_ollama import OllamaLLM

def get_confirmed_planets(star_name):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": f"select pl_name,hostname,pl_orbper,pl_rade,pl_masse,discoverymethod from ps where hostname like '{star_name}%'",
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()

def analyze_system(star_name):
    # Get real NASA data
    planets = get_confirmed_planets(star_name)
    
    # Print raw data first
    print(f"\n--- Raw NASA Data for {star_name} ---\n")
    for planet in planets:
        print(f"Planet: {planet['pl_name']}")
        print(f"Orbital Period: {planet['pl_orbper']} days")
        print(f"Discovery Method: {planet['discoverymethod']}")
        print(f"Radius: {planet['pl_rade']} Earth radii")
        print(f"Mass: {planet['pl_masse']} Earth masses")
        print("---")
    
    # Send to AI for analysis
    llm = OllamaLLM(model="llama3.2:1b")
    
    prompt = f"""
    You are an exoplanet research assistant. Analyze this real NASA data for {star_name}:
    
    {planets}
    
    Please:
    1. Summarize what we know about this planetary system
    2. Comment on the orbital periods and what they suggest
    3. Suggest what future observations might reveal
    """
    
    print(f"\n--- HERMES AI Analysis ---\n")
    response = llm.invoke(prompt)
    return response

print(analyze_system("tau Cet"))