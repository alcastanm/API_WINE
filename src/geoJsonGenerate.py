from osm2geojson import json2geojson
import random
import requests
import os
import time
import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db
from ENTITIES.dto.DTO_region import DTO_region
from src.ENTITIES.domine.regions import regions


# ==============================
# CONFIG
# ==============================

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter"
]

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "geojson"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# DB
# ==============================

async def getWineList(db: AsyncSession):
    query = select(regions).where(regions.mapeable == True)
    result = (await db.execute(query)).scalars().all()

    REGIONS = []

    if result:
        for item in result:
            dto = DTO_region.model_validate(item)

            REGIONS.append({
                "name": dto.name,
                "country": dto.country,
                "admin_level": 4  # puedes ajustar luego dinámicamente
            })

    return REGIONS


# ==============================
# QUERY BUILDER
# ==============================

def build_query(name, country, admin_level=None):
    admin_filter = f'["admin_level"="{admin_level}"]' if admin_level else ""

    return f"""
            [out:json][timeout:60];
            area["name"="Chile"]->.searchArea;
            relation["name"~"Colchagua"]["boundary"="administrative"](area.searchArea);
            out body;
            >;
            out skel qt;
    """


# ==============================
# OVERPASS (RETRY + BACKOFF)
# ==============================

def consultar_overpass(query, max_retries=5):
    for intento in range(max_retries):
        url = random.choice(OVERPASS_URLS)

        try:
            print(f"🔄 Intento {intento+1} usando {url}")

            response = requests.post(url, data=query, timeout=120)

            if response.status_code == 200:
                return response.json()

            elif response.status_code in [429, 504]:
                espera = (2 ** intento) + random.uniform(0.5, 2)
                print(f"⚠️ Rate limit/timeout ({response.status_code}). Esperando {espera:.2f}s...")
                time.sleep(espera)

            else:
                print(f"❌ Error inesperado: {response.status_code}")
                time.sleep(2)

        except requests.exceptions.RequestException as e:
            espera = (2 ** intento)
            print(f"🌐 Error de red: {e}. Esperando {espera}s...")
            time.sleep(espera)

    raise Exception("❌ Falló después de varios intentos")


# ==============================
# GEOJSON
# ==============================

def convert_to_geojson(osm_data):
    return json2geojson(osm_data)


def save_geojson(data, country, name):
    country_folder = OUTPUT_DIR / country.lower().replace(" ", "_")
    country_folder.mkdir(parents=True, exist_ok=True)

    filename = name.lower().replace(" ", "_") + ".geojson"
    filepath = country_folder / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)

    print(f"✅ Guardado: {filepath}")


# ==============================
# PROCESS
# ==============================

def process_region(region):
    try:
        name = region["name"]
        country = region["country"]
        admin_level = region.get("admin_level")

        print(f"\n🌍 Procesando: {name} ({country})")

        query = build_query(name, country, admin_level)

        osm_data = consultar_overpass(query)

        if not osm_data or not osm_data.get("elements"):
            print(f"⚠️ No encontrado: {name}")
            return

        geojson = convert_to_geojson(osm_data)

        if not geojson.get("features"):
            print(f"⚠️ GeoJSON vacío: {name}")
            return

        save_geojson(geojson, country, name)

    except Exception as e:
        print(f"❌ Error con {region['name']}: {e}")


# ==============================
# MAIN
# ==============================

async def main():
    async for db in get_db():
        regions_list = await getWineList(db)

    for region in regions_list:
        process_region(region)

        # 🔥 IMPORTANTE: evitar bloqueo
        time.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())




# from osm2geojson import json2geojson
# import random
# import requests
# import os
# import time
# import asyncio
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db
# from ENTITIES.dto.DTO_region import DTO_region
# from src.ENTITIES.domine.regions import regions

# REGIONS = []

# OVERPASS_URL = ["https://overpass-api.de/api/interpreter",
#                 "https://overpass.kumi.systems/api/interpreter",
#                 "https://lz4.overpass-api.de/api/interpreter"
#                ]

# OUTPUT_DIR = "geojson"

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# async def getWineList(db: AsyncSession):
#     query = select(regions).where(regions.mapeable == True)
#     result = (await db.execute(query)).scalars().all()
    
#     iterable = [DTO_region.model_validate(r) for r in result] if result else None
        
#     if iterable:
#         for item in iterable:
#             nwNode = {'name': item.name,'country':item.country,'admin_level':4}
#             REGIONS.append(nwNode)
            
#     return REGIONS

# def build_query(name, country, admin_level):
#     return f"""
#             [out:json][timeout:60];
#             area["name"="Chile"]->.searchArea;
#             relation["name"~"Colchagua"]["boundary"="administrative"](area.searchArea);
#             out body;
#             >;
#             out skel qt;
#     """
    


# def fetch_osm_data(query):
#     response = requests.post(OVERPASS_URL, data=query)
    
#     if response.status_code != 200:
#         raise Exception(f"Error en Overpass: {response.status_code}")
    
#     return response.json()


# def convert_to_geojson(osm_data):
#     return json2geojson(osm_data)


# def save_geojson(data, country, name):
#     country_folder = os.path.join(OUTPUT_DIR, country.lower().replace(" ", "_"))
#     os.makedirs(country_folder, exist_ok=True)

#     filename = name.lower().replace(" ", "_") + ".geojson"
#     filepath = os.path.join(country_folder, filename)

#     with open(filepath, "w", encoding="utf-8") as f:
#         import json
#         json.dump(data, f)

#     print(f"✅ Guardado: {filepath}")


# def process_region(region):
#     try:
#         print(f"🌍 Procesando: {region['name']} ({region['country']})")

#         query = build_query(region["name"], region["country"], region["admin_level"])
#         osm_data = fetch_osm_data(query)

#         if not osm_data.get("elements"):
#             print(f"⚠️ No encontrado: {region['name']}")
#             return

#         geojson = convert_to_geojson(osm_data)
#         save_geojson(geojson, region["country"], region["name"])

#     except Exception as e:
#         print(f"❌ Error con {region['name']}: {e}")


# def consultar_overpass(query, max_retries=5):
#     for intento in range(max_retries):
#         url = random.choice(OVERPASS_URLS)

#         try:
#             print(f"Intento {intento+1} usando {url}")

#             response = requests.post(url, data=query, timeout=120)

#             if response.status_code == 200:
#                 return response.json()

#             elif response.status_code in [429, 504]:
#                 espera = (2 ** intento) + random.uniform(0.5, 2)
#                 print(f"Rate limit/timeout ({response.status_code}). Esperando {espera:.2f}s...")
#                 time.sleep(espera)

#             else:
#                 print(f"Error inesperado: {response.status_code}")
#                 time.sleep(2)

#         except requests.exceptions.RequestException as e:
#             espera = (2 ** intento)
#             print(f"Error de red: {e}. Esperando {espera}s...")
#             time.sleep(espera)

#     raise Exception("❌ Falló después de varios intentos")





# async def main():
#     async for db in get_db():
#         data = await getWineList(db)
#     try:
#         for region in REGIONS:
#             process_region(region)

#             # 🔥 IMPORTANTE: evitar bloqueo de Overpass
#             time.sleep(10)   
#     except Exception as e:
#       print(str(e))    
     

# if __name__ == "__main__":
#     asyncio.run(main())
       
