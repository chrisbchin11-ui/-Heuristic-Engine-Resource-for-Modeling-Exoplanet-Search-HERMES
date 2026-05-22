import requests
from langchain_ollama import OllamaLLM

def get_confirmed_planets(star_name):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": f"select pl_name,hostname,pl_orbper,pl_rade,pl_masse,discoverymethod from ps where hostname like '{star_name}%'",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        return response.json()
    except Exception as e:
        print(f"Error fetching data for {star_name}: {e}")
        return []

def deduplicate_planets(planets):
    seen = set()
    unique = []
    for planet in planets:
        name = planet['pl_name']
        if name not in seen:
            seen.add(name)
            unique.append(planet)
    return unique

def habitable_zone_check(orbital_period_days, stellar_mass=1.0):
    if orbital_period_days is None:
        return "Unknown - no orbital period data"
    
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
    planets = deduplicate_planets(planets)
    
    if not planets:
        print(f"No confirmed planets found for {star_name}")
        print(f"Note: This star may have planetary candidates awaiting confirmation")
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
    
    # Build simplified summary for AI
    summary = f"Star: {star_name}\nNumber of planets: {len(planets)}\n"
    for planet in planets:
        hz = habitable_zone_check(planet['pl_orbper'])
        summary += f"  - {planet['pl_name']}: orbital period {planet['pl_orbper']} days | {hz}\n"
    
    # Send to AI for analysis
    llm = OllamaLLM(model="llama3.2:1b")
    
    prompt = f"""
    You are an exoplanet research assistant. Analyze this planetary system:

    {summary}

    Please:
    1. Summarize what we know about this planetary system
    2. Comment on the orbital periods and what they suggest
    3. Suggest what future observations might reveal
    """
    
    print(f"\n--- HERMES AI Analysis ---\n")
    response = llm.invoke(prompt)
    print(response)

def compare_systems(star_list):
    print(f"\n=== HERMES Multi-Star Comparison ===\n")
    
    all_systems = {}
    
    for star in star_list:
        planets = get_confirmed_planets(star)
        planets = deduplicate_planets(planets)
        all_systems[star] = planets
        
        print(f"\n--- {star} ---")
        if not planets:
            print(f"No confirmed planets found in NASA archive for {star}")
            print(f"Note: This star may have planetary candidates awaiting confirmation")
            continue
            
        print(f"Number of confirmed planets: {len(planets)}")
        for planet in planets:
            hz_status = habitable_zone_check(planet['pl_orbper'])
            print(f"  {planet['pl_name']} | Period: {planet['pl_orbper']} days | {hz_status}")
    
    # Build simplified summary for AI
    summary = ""
    for star, planets in all_systems.items():
        if not planets:
            summary += f"\n{star}: No confirmed planets found\n"
            continue
        summary += f"\n{star}: {len(planets)} confirmed planets\n"
        for planet in planets:
            hz = habitable_zone_check(planet['pl_orbper'])
            summary += f"  - {planet['pl_name']}: {planet['pl_orbper']} days | {hz}\n"

    # Ask AI to compare all systems
    llm = OllamaLLM(model="llama3.2:1b")
    
    prompt = f"""
    You are an exoplanet research assistant. Compare these planetary systems:

    {summary}

    Please:
    1. Which system has the most planets?
    2. Which planets fall in the habitable zone?
    3. Which system is most interesting for future research and why?
    """
    
    print(f"\n--- HERMES Comparative Analysis ---\n")
    response = llm.invoke(prompt)
    print(response)

# Run comparison
compare_systems(["tau Cet", "HD 192310", "55 Cnc"])