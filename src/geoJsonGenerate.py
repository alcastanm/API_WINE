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
    "https://overpass-api.kumi.systems/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter"
]

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "geojson"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==============================
# DB
# ==============================

async def getWineList(db: AsyncSession):
    query = select(regions).where(regions.mapeable==True)
    result = (await db.execute(query)).scalars().all()

    REGIONS = []

    if result:
        for item in result:
            dto = DTO_region.model_validate(item)

            REGIONS.append({
                "name": dto.name,
                "country": dto.country,
                "admin_level": getattr(dto, "admin_level", None)  # usar admin_level del DTO si existe
            })

    return REGIONS


# ==============================
# QUERY BUILDER
# ==============================

def build_query(name, country=None, admin_level=None, use_alt_name=False):
    # """
    # Construye una query de Overpass para obtener una región por nombre o alt_name.
    # """
    # admin_filter = f'["admin_level"="{admin_level}"]' if admin_level else ""
    # name_field = "alt_name" if use_alt_name else "name"

    # return f"""
    # [out:json][timeout:60];
    # relation["{name_field}"~"{name}",i]["boundary"="administrative"]{admin_filter};
    # out body;
    # >;
    # out skel qt;
    # """
    
    name = "Provence-Alpes-Côte d'Azur"
    return  f"""
[out:json][timeout:60];
relation["boundary"="administrative"]["name"~"{name}",i];
out body;
>;
out skel qt;
    """    


# ==============================
# OVERPASS (RETRY + BACKOFF)
# ==============================

def consultar_overpass(query, max_retries=10):
    for intento in range(max_retries):
        url = random.choice(OVERPASS_URLS)

        try:
            print(f"🔄 Intento {intento+1} usando {url}")
            response = requests.post(url, data=query, timeout=120)

            if response.status_code == 200:
                return response.json()

            elif response.status_code in [429, 504]:
                # espera = (2 ** intento) + random.uniform(0.5, 2)
                espera = (2 ** intento) + random.uniform(1,3)
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
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Guardado: {filepath}")


# ==============================
# PROCESS REGION
# ==============================

def process_region(region):
    name = region["name"]
    country = region["country"]
    admin_level = region.get("admin_level")

    print(f"\n🌍 Procesando: {name} ({country})")

    # Intentar con admin_level y name
    queries = [
        build_query(name, country, admin_level, use_alt_name=False),
        build_query(name, country, admin_level, use_alt_name=True)
    ]

    # Si admin_level existe, agregar intento sin admin_level
    if admin_level:
        queries.append(build_query(name, country, None, use_alt_name=False))
        queries.append(build_query(name, country, None, use_alt_name=True))

    osm_data = None
    for q in queries:
        osm_data = consultar_overpass(q)
        if osm_data.get("elements"):
            break  # Encontrado

    if not osm_data or not osm_data.get("elements"):
        print(f"⚠️ No se encontró la región: {name}")
        return

    geojson = convert_to_geojson(osm_data)

    if not geojson.get("features"):
        print(f"⚠️ GeoJSON vacío para {name}")
        return

    save_geojson(geojson, country, name)


# ==============================
# MAIN
# ==============================

async def main():
    
    
    async for db in get_db():
        regions_list = await getWineList(db)


    for region in regions_list:
        
        # se revisa si el path existe
        country_folder = OUTPUT_DIR / region["country"].lower().replace(" ", "_")
        country_folder.mkdir(parents=True, exist_ok=True)
        filename = region["name"].lower().replace(" ", "_") + ".geojson"
        filepath = country_folder / filename
        
        filecheck = Path(filepath)
                
        if not (filecheck).exists():
            process_region(region)
            time.sleep(2)  # Evitar bloqueo y rate limits


if __name__ == "__main__":
    asyncio.run(main())





# from osm2geojson import json2geojson
# import random
# import requests
# import os
# import time
# import asyncio
# import json
# from pathlib import Path

# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db
# from ENTITIES.dto.DTO_region import DTO_region
# from src.ENTITIES.domine.regions import regions


# # ==============================
# # CONFIG
# # ==============================

# OVERPASS_URLS = [
#     "https://overpass-api.de/api/interpreter",
#     "https://overpass.kumi.systems/api/interpreter",
#     "https://lz4.overpass-api.de/api/interpreter"
# ]

# BASE_DIR = Path(__file__).resolve().parent.parent
# OUTPUT_DIR = BASE_DIR / "geojson"

# OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# # ==============================
# # DB
# # ==============================

# async def getWineList(db: AsyncSession):
#     query = select(regions).where(regions.mapeable == True)
#     result = (await db.execute(query)).scalars().all()

#     REGIONS = []

#     if result:
#         for item in result:
#             dto = DTO_region.model_validate(item)

#             REGIONS.append({
#                 "name": dto.name,
#                 "country": dto.country,
#                 "admin_level": 4  # puedes ajustar luego dinámicamente
#             })

#     return REGIONS


# # ==============================
# # QUERY BUILDER
# # ==============================

# # def build_query(name, country, admin_level=None):
# #     admin_filter = f'["admin_level"="{admin_level}"]' if admin_level else ""

# #     return f"""
# #             [out:json][timeout:60];
# #             area["name"="Chile"]->.searchArea;
# #             relation["name"~"Colchagua"]["boundary"="administrative"](area.searchArea);
# #             out body;
# #             >;
# #             out skel qt;
# #     """


# def build_query(name, country=None, admin_level=None):
#     """
#     Construye una query de Overpass para obtener una región por nombre.
    
#     Args:
#         name (str): Nombre de la región/provincia a buscar.
#         country (str, opcional): Ignorado en esta versión, ya que buscar por área puede fallar.
#         admin_level (str, opcional): Nivel administrativo, p.ej. "4" para provincias.

#     Returns:
#         str: Query de Overpass lista para usar.
#     """
#     # Filtro de admin_level si se proporciona
#     admin_filter = f'["admin_level"="{admin_level}"]' if admin_level else ""
    
#     # Query: buscamos directamente la relación con nombre case-insensitive
#     return f"""
#     [out:json][timeout:60];
#     relation["name"~"{name}",i]["boundary"="administrative"]{admin_filter};
#     out body;
#     >;
#     out skel qt;
#     """


# # ==============================
# # OVERPASS (RETRY + BACKOFF)
# # ==============================

# def consultar_overpass(query, max_retries=5):
#     for intento in range(max_retries):
#         url = random.choice(OVERPASS_URLS)

#         try:
#             print(f"🔄 Intento {intento+1} usando {url}")

#             response = requests.post(url, data=query, timeout=120)

#             if response.status_code == 200:
#                 return response.json()

#             elif response.status_code in [429, 504]:
#                 espera = (2 ** intento) + random.uniform(0.5, 2)
#                 print(f"⚠️ Rate limit/timeout ({response.status_code}). Esperando {espera:.2f}s...")
#                 time.sleep(espera)

#             else:
#                 print(f"❌ Error inesperado: {response.status_code}")
#                 time.sleep(2)

#         except requests.exceptions.RequestException as e:
#             espera = (2 ** intento)
#             print(f"🌐 Error de red: {e}. Esperando {espera}s...")
#             time.sleep(espera)

#     raise Exception("❌ Falló después de varios intentos")


# # ==============================
# # GEOJSON
# # ==============================

# def convert_to_geojson(osm_data):
#     return json2geojson(osm_data)


# def save_geojson(data, country, name):
#     country_folder = OUTPUT_DIR / country.lower().replace(" ", "_")
#     country_folder.mkdir(parents=True, exist_ok=True)

#     filename = name.lower().replace(" ", "_") + ".geojson"
#     filepath = country_folder / filename

#     with open(filepath, "w", encoding="utf-8") as f:
#         json.dump(data, f)

#     print(f"✅ Guardado: {filepath}")


# # ==============================
# # PROCESS
# # ==============================

# def process_region(region):
#     try:
#         name = region["name"]
#         country = region["country"]
#         admin_level = region.get("admin_level")

#         print(f"\n🌍 Procesando: {name} ({country})")

#         query = build_query(name, country, admin_level)

#         osm_data = consultar_overpass(query)

#         if not osm_data or not osm_data.get("elements"):
#             print(f"⚠️ No encontrado: {name}")
#             return

#         geojson = convert_to_geojson(osm_data)

#         if not geojson.get("features"):
#             print(f"⚠️ GeoJSON vacío: {name}")
#             return

#         save_geojson(geojson, country, name)

#     except Exception as e:
#         print(f"❌ Error con {region['name']}: {e}")


# # ==============================
# # MAIN
# # ==============================

# async def main():
#     async for db in get_db():
#         regions_list = await getWineList(db)

#     for region in regions_list:
#         process_region(region)

#         # 🔥 IMPORTANTE: evitar bloqueo
#         time.sleep(2)


# if __name__ == "__main__":
#     asyncio.run(main())