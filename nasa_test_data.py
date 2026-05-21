import requests

def get_confirmed_planets(star_name):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    params = {
        "query": f"select pl_name,hostname,pl_orbper,pl_rade,pl_masse,discoverymethod from ps where hostname like '{star_name}%'",
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()

result = get_confirmed_planets("tau Cet")

print(f"\nPlanets found around tau Ceti:\n")
for planet in result:
    print(f"Planet: {planet['pl_name']}")
    print(f"Orbital Period: {planet['pl_orbper']} days")
    print(f"Discovery Method: {planet['discoverymethod']}")
    print(f"Radius: {planet['pl_rade']} Earth radii")
    print(f"Mass: {planet['pl_masse']} Earth masses")
    print("---")