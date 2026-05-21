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

def habitable_zone_check(orbital_period_days, stellar_mass=1.0):
    # Convert days to years
    period_years = orbital_period_days / 365.25
    
    # Kepler's Third Law — calculate orbital distance in AU
    distance_au = (period_years ** 2 * stellar_mass) ** (1/3)
    
    # Habitable zone boundaries
    inner_edge = 0.95 * (stellar_mass ** 0.5)
    outer_edge = 1.67 * (stellar_mass ** 0.5)
    
    if inner_edge <= distance_au <= outer_edge:
        return f"{distance_au:.2f} AU - IN habitable zone ✓"
    elif distance_au < inner_edge:
        return f"{distance_au:.2f} AU - too close to star"
    else:
        return f"{distance_au:.2f} AU - too far from star"

def analyze_system(star_name):
    # Get real NASA data
    planets = get_confirmed_planets(star_name)
    
    if not planets:
        print(f"No confirmed planets found for {star_name}")
        return
    
    # Print raw data
    print(f"\n--- Raw NASA Data for {star_name} ---\n")
    for planet in planets:
        print(f"Planet: {planet['pl_name']}")
        print(f"Orbital Period: {planet['pl_orbper']} days")
        print(f"Discovery Method: {planet['discoverymethod']}")
        print(f"Radius: {planet['pl_rade']} Earth radii")
        print(f"Mass: {planet['pl_masse']} Earth masses")
        hz_status = habitable_zone_check(planet['pl_orbper'])
        print(f"Habitable Zone Status: {hz_status}")
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
    print(response)

analyze_system("tau Cet")