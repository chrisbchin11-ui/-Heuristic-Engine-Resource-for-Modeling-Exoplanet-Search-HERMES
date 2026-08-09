import requests
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from the .env file
load_dotenv()

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

def get_llm():
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key
        )
    else:
        print("GROQ_API_KEY not found — falling back to local Ollama")
        from langchain_ollama import OllamaLLM
        return OllamaLLM(model="llama3.2:1b")

def get_response(llm, prompt):
    response = llm.invoke(prompt)
    if hasattr(response, 'content'):
        return response.content
    return str(response)

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
    
    summary = f"Star: {star_name}\nStellar Mass: {stellar_mass} solar masses\nStellar Luminosity: {stellar_luminosity:.3f} solar luminosities\nNumber of planets: {len(planets)}\n"
    for planet in planets:
        hz = habitable_zone_check(planet['pl_orbper'], stellar_mass, stellar_luminosity)
        summary += f"  - {planet['pl_name']}: orbital period {planet['pl_orbper']} days | {hz}\n"
    
    llm = get_llm()
    
    prompt = f"""
You are an expert exoplanet research assistant with deep knowledge of planetary science,
stellar physics, and astrobiology.

Here is real NASA data for the {star_name} planetary system:

{summary}

Please provide a thorough scientific analysis covering:

1. SYSTEM OVERVIEW
   - What type of star is this based on its mass and luminosity?
   - How does it compare to our Sun?
   - What does this mean for potential habitability?

2. PLANETARY ANALYSIS
   - For each planet, what does its orbital period suggest about its environment?
   - Which planets are most scientifically interesting and why?
   - Are there any unusual orbital configurations worth noting?

3. HABITABILITY ASSESSMENT
   - For any planets in the habitable zone, what conditions might they have?
   - Could liquid water exist? What factors support or challenge this?
   - How does stellar luminosity affect habitability in this system?

4. COMPARATIVE CONTEXT
   - How does this system compare to our Solar System?
   - What makes this system unique or noteworthy in the broader context of exoplanet research?

5. FUTURE RESEARCH
   - What specific observations would most advance our understanding?
   - Which space missions or instruments would be best suited to study this system?
   - What are the most important unanswered questions about this system?

Please go beyond restating the data — provide genuine scientific insight and analysis.
"""
    
    print(f"\n--- HERMES AI Analysis ---\n")
    response = get_response(llm, prompt)
    print(response)

def get_candidate_planets(star_id):
    """
    Queries the TESS Objects of Interest (TOI) table for unconfirmed candidates.
    Note: The TOI table uses 'tid' (TESS Input Catalog ID) instead of 'hostname'.
    """
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": f"select toi, tid, pl_orbper, pl_rade, pl_eqt from toi where tid like '{star_id}%'",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params, timeout=30)
        return response.json()
    except Exception as e:
        print(f"Error fetching candidate data for {star_id}: {e}")
        return []

def analyze_candidates(star_id):
    candidates = get_candidate_planets(star_id)
    
    if not candidates:
        print(f"\nNo unconfirmed candidates found in the TOI database for TIC ID {star_id}")
        return
        
    print(f"\n--- Raw Candidate Data for TIC {star_id} ---")
    summary = f"Target ID: TIC {star_id}\nNumber of candidate signals: {len(candidates)}\n"
    
    for cand in candidates:
        print(f"Candidate: TOI {cand.get('toi')}")
        print(f"Orbital Period: {cand.get('pl_orbper')} days")
        print(f"Radius: {cand.get('pl_rade')} Earth radii")
        print("---")
        summary += f"  - TOI {cand.get('toi')}: orbital period {cand.get('pl_orbper')} days, radius {cand.get('pl_rade')} R_Earth\n"
        
    llm = get_llm()
    
    prompt = f"""
You are an expert exoplanet research assistant evaluating unconfirmed planetary candidate signals.

Here is real NASA data for unconfirmed candidates orbiting TIC {star_id}:

{summary}

Please provide a scientific analysis covering:
1. FALSE POSITIVE PROBABILITY
   - What are the chances these signals are just stellar activity or eclipsing binaries?
2. OBSERVATIONAL FOLLOW-UP
   - What specific radial velocity instruments or observation schedules are needed to confirm these candidates?
3. HABITABILITY POTENTIAL
   - If confirmed, what would the environment of these planets look like based on their periods and radii?
"""
    
    print(f"\n--- HERMES Candidate Analysis ---\n")
    response = get_response(llm, prompt)
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

    llm = get_llm()
    
    prompt = f"""
You are an expert exoplanet research scientist comparing multiple planetary systems.

Here is real NASA data for multiple planetary systems:

{summary}

Please provide a comprehensive scientific comparison covering:

1. SYSTEM COMPARISON
   - How do these stars differ from each other and from our Sun?
   - Which system has the most complex planetary architecture?
   - How do the stellar properties influence each system's potential for life?

2. HABITABILITY RANKING
   - Rank these systems by their potential to host habitable planets
   - For each habitable zone planet, assess its likelihood of supporting life
   - What factors make some systems more promising than others?

3. SCIENTIFIC SIGNIFICANCE
   - Which system is most valuable for future research and why?
   - What has each system taught us about planetary formation?
   - Are there any surprising or unusual characteristics worth highlighting?

4. RESEARCH RECOMMENDATIONS
   - Which specific planets deserve the most observational attention?
   - What instruments or missions would best advance our understanding?
   - What are the key open questions for each system?

Please provide genuine scientific insight — go well beyond restating the numbers.
"""
    
    print(f"\n--- HERMES Comparative Analysis ---\n")
    response = get_response(llm, prompt)
    print(response)

def main():
    print("\n=== Welcome to HERMES ===")
    print("Heuristic Engine Resource for Modeling Exoplanet Search")
    print("=========================================\n")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Analyze a single star system (Confirmed)")
        print("2. Search for unconfirmed candidate signals")
        print("3. Compare multiple star systems")
        print("4. Exit")
        
        choice = input("\nEnter choice (1/2/3/4): ").strip()
        
        if choice == "1":
            star = input("Enter star name: ").strip()
            analyze_system(star)
            
        elif choice == "2":
            print("\nTo find TIC ID, go to https://exofop.ipac.caltech.edu/tess/")
            star_id = input("Enter TESS Input Catalog (TIC) ID (e.g., 270636838): ").strip()
            analyze_candidates(star_id)
            
        elif choice == "3":
            stars_input = input("Enter star names separated by commas: ").strip()
            star_list = [s.strip() for s in stars_input.split(",")]
            compare_systems(star_list)
            
        elif choice == "4":
            print("\nExiting HERMES. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

main()