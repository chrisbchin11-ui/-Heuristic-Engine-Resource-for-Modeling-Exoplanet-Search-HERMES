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

def get_stellar_mass(star_name):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": f"select st_mass from ps where hostname like '{star_name}%'",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        for entry in data:
            if entry['st_mass'] is not None:
                return entry['st_mass']
        return 1.0
    except Exception as e:
        print(f"Could not retrieve stellar mass for {star_name}, defaulting to 1.0")
        return 1.0

def get_stellar_luminosity(star_name):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": f"select st_lum from ps where hostname like '{star_name}%'",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        for entry in data:
            if entry['st_lum'] is not None:
                # NASA stores luminosity as log10(L/L_sun)
                return 10 ** entry['st_lum']
        return 1.0
    except Exception as e:
        print(f"Could not retrieve stellar luminosity for {star_name}, defaulting to 1.0")
        return 1.0

def deduplicate_planets(planets):
    seen = set()
    unique = []
    for planet in planets:
        name = planet['pl_name']
        if name not in seen:
            seen.add(name)
            unique.append(planet)
    return unique

def habitable_zone_check(orbital_period_days, stellar_mass=1.0, stellar_luminosity=1.0):
    if orbital_period_days is None:
        return "Unknown - no orbital period data"
    
    # Convert days to years
    period_years = orbital_period_days / 365.25
    
    # Kepler's Third Law — calculate orbital distance in AU
    distance_au = (period_years ** 2 * stellar_mass) ** (1/3)
    
    # Habitable zone boundaries using actual stellar luminosity
    inner_edge = 0.95 * (stellar_luminosity ** 0.5)
    outer_edge = 1.67 * (stellar_luminosity ** 0.5)
    
    if inner_edge <= distance_au <= outer_edge:
        return f"{distance_au:.2f} AU - IN habitable zone ✓"
    elif distance_au < inner_edge:
        return f"{distance_au:.2f} AU - too close to star"
    else:
        return f"{distance_au:.2f} AU - too far from star"

def analyze_system(star_name):
    planets = get_confirmed_planets(star_name)
    planets = deduplicate_planets(planets)
    stellar_mass = get_stellar_mass(star_name)
    stellar_luminosity = get_stellar_luminosity(star_name)
    
    if not planets:
        print(f"\nNo confirmed planets found for {star_name}")
        print(f"Note: This star may have planetary candidates awaiting confirmation")
        return
    
    print(f"\n--- Raw NASA Data for {star_name} ---")
    print(f"Stellar Mass: {stellar_mass} solar masses")
    print(f"Stellar Luminosity: {stellar_luminosity:.3f} solar luminosities\n")
    for planet in planets:
        print(f"Planet: {planet['pl_name']}")
        print(f"Orbital Period: {planet['pl_orbper']} days")
        print(f"Discovery Method: {planet['discoverymethod']}")
        print(f"Radius: {planet['pl_rade']} Earth radii")
        print(f"Mass: {planet['pl_masse']} Earth masses")
        hz_status = habitable_zone_check(planet['pl_orbper'], stellar_mass, stellar_luminosity)
        print(f"Habitable Zone Status: {hz_status}")
        print("---")
    
    # Build simplified summary for AI
    summary = f"Star: {star_name}\nStellar Mass: {stellar_mass} solar masses\nStellar Luminosity: {stellar_luminosity:.3f} solar luminosities\nNumber of planets: {len(planets)}\n"
    for planet in planets:
        hz = habitable_zone_check(planet['pl_orbper'], stellar_mass, stellar_luminosity)
        summary += f"  - {planet['pl_name']}: orbital period {planet['pl_orbper']} days | {hz}\n"
    
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
    stellar_masses = {}
    stellar_luminosities = {}
    
    for star in star_list:
        planets = get_confirmed_planets(star)
        planets = deduplicate_planets(planets)
        stellar_mass = get_stellar_mass(star)
        stellar_luminosity = get_stellar_luminosity(star)
        all_systems[star] = planets
        stellar_masses[star] = stellar_mass
        stellar_luminosities[star] = stellar_luminosity
        
        print(f"\n--- {star} ---")
        print(f"Stellar Mass: {stellar_mass} solar masses")
        print(f"Stellar Luminosity: {stellar_luminosity:.3f} solar luminosities")
        if not planets:
            print(f"No confirmed planets found in NASA archive for {star}")
            print(f"Note: This star may have planetary candidates awaiting confirmation")
            continue
            
        print(f"Number of confirmed planets: {len(planets)}")
        for planet in planets:
            hz_status = habitable_zone_check(planet['pl_orbper'], stellar_mass, stellar_luminosity)
            print(f"  {planet['pl_name']} | Period: {planet['pl_orbper']} days | {hz_status}")
    
    # Build simplified summary for AI
    summary = ""
    for star, planets in all_systems.items():
        stellar_mass = stellar_masses[star]
        stellar_luminosity = stellar_luminosities[star]
        if not planets:
            summary += f"\n{star}: No confirmed planets found\n"
            continue
        summary += f"\n{star} (mass: {stellar_mass} solar masses, luminosity: {stellar_luminosity:.3f} solar): {len(planets)} confirmed planets\n"
        for planet in planets:
            hz = habitable_zone_check(planet['pl_orbper'], stellar_mass, stellar_luminosity)
            summary += f"  - {planet['pl_name']}: {planet['pl_orbper']} days | {hz}\n"

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

def main():
    print("\n=== Welcome to HERMES ===")
    print("Heuristic Engine Resource for Modeling Exoplanet Search")
    print("=========================================\n")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Analyze a single star system")
        print("2. Compare multiple star systems")
        print("3. Exit")
        
        choice = input("\nEnter choice (1/2/3): ").strip()
        
        if choice == "1":
            star = input("Enter star name: ").strip()
            analyze_system(star)
            
        elif choice == "2":
            stars_input = input("Enter star names separated by commas: ").strip()
            star_list = [s.strip() for s in stars_input.split(",")]
            compare_systems(star_list)
            
        elif choice == "3":
            print("\nExiting HERMES. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

main()