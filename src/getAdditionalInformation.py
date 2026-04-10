from osm2geojson import json2geojson
import random
import requests
import os
import time
import asyncio
import json
from pathlib import Path
from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.INFRASTRUCTURE.REPOSITORIES.db_connection import get_db
from ENTITIES.dto.DTO_region import DTO_region
from src.ENTITIES.domine.regions import regions
import httpx

UNSPLASH_KEY = "7jFmC90ViBCnFutzuPZ9Jr7ND_St1zJNFW9rI0E6MrQ"
CLIMATE_KEY = "e41b56b4ed9e7c6f4937fda3870e12cd"
VINERADAR_KEY = ""


# =========================
# 🔥 QUERY BUILDER
# =========================
def build_queries(region_name: str, country: str):
    region_name = (region_name or "").lower().replace("í", "i")

    return [
        f"{region_name} valley vineyard {country}",
        f"{region_name} vineyard",
        f"{country} vineyard",
        f"{country} wine region vineyard",
        "vineyard mountains"
    ]


# =========================
# 🌐 SAFE REQUEST
# =========================
async def safe_get_json(client, url, params=None, headers=None):
    try:
        response = await client.get(url, params=params, headers=headers, timeout=20)

        if response.status_code != 200:
            print(f"❌ Error HTTP {response.status_code} - {url}")
            return None

        return response.json()

    except Exception as e:
        print(f"❌ Error request: {str(e)}")
        return None


# =========================
# 🌍 WIKIMEDIA SEARCH
# =========================
async def search_wikimedia(client, query):
    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": 5,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }

    data = await safe_get_json(client, url, params=params)

    if not data:
        return []

    pages = data.get("query", {}).get("pages", {})

    images = []
    for page in pages.values():
        if "imageinfo" in page:
            images.append(page["imageinfo"][0]["url"])

    return images


# =========================
# 🧠 CORE LOGIC
# =========================
async def getPhotoInfo(db: AsyncSession):
    query = select(regions).where(
        and_(regions.mapeable)
    ).order_by(regions.country, regions.name)

    results = (await db.execute(query)).scalars().all()
    iterable = [DTO_region.model_validate(r) for r in results] if results else []

    for item in iterable:
        
        # se obtiene altitud y temperatura
        returnedObj = await get_region_info(item.name, item.country,item.lat,item.long)
        
        queryUpdate = update(regions).where(regions.regions_id == item.regions_id)\
            .values(altitude=returnedObj["elevation"],climate=returnedObj["temperature"])
        await db.execute(queryUpdate)
        await db.commit()    
        
        
        
        # if not item.url:
        #     await obtener_fotos(db, item.regions_id, item.country, item.name)



# ===========================
# TEMPERATURA Y ALTITUD
# ===========================

async def get_region_info(region_name: str, country: str, lat: float, lon: float):

    async with httpx.AsyncClient() as client:

        # 🌡️ CLIMA
        weather_url = "https://api.openweathermap.org/data/2.5/weather"

        weather_params = {
            "q": f"{region_name},{country}",
            "appid": CLIMATE_KEY,
            "units": "metric"
        }

        weather_res = await client.get(weather_url, params=weather_params)

        print("WEATHER STATUS:", weather_res.status_code)
        print("WEATHER RESPONSE:", weather_res.text)

        weather_data = weather_res.json() if weather_res.status_code == 200 else {}

        temp = weather_data.get("main", {}).get("temp")


        # ⛰️ ALTITUD
        elevation_url = "https://api.open-elevation.com/api/v1/lookup"

        elevation_params = {
            "locations": f"{lat},{lon}"
        }

        elevation_res = await client.get(elevation_url, params=elevation_params)

        print("ELEVATION STATUS:", elevation_res.status_code)
        print("ELEVATION RESPONSE:", elevation_res.text)

        elevation_data = elevation_res.json() if elevation_res.status_code == 200 else {}

        elevation = elevation_data.get("results", [{}])[0].get("elevation")

        return {
            "region": region_name,
            "temperature": temp,
            "elevation": elevation
        }
        
# ===========================
# VARIEDAD EN CEPAS
# ===========================
async def getVarieties():
    BASE_URL = "https://api.vineradar.com/v1"
    
    
    




# =========================
# 🚀 MAIN IMAGE FETCHER
# =========================
async def obtener_fotos(db: AsyncSession, region_id: int, pais: str, region_name: str):

    unsplash_url = "https://api.unsplash.com/search/photos"

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_KEY}"
    }

    queries = build_queries(region_name, pais)

    async with httpx.AsyncClient() as client:
        imgUrl = None

        # =========================
        # 🔥 1. UNSPLASH
        # =========================
        for query in queries:
            params = {
                "query": query,
                "per_page": 10
            }

            data = await safe_get_json(client, unsplash_url, params=params, headers=headers)

            if not data or "results" not in data:
                continue

            if data["results"]:
                print(f"✅ Unsplash usando: {query}")

                for item in data["results"]:
                    try:
                        imgUrl = item.get("urls", {}).get("small")
                        if not imgUrl:
                            continue

                        findObj = await checkExists(db, imgUrl)

                        if not findObj:
                            queryUpdate = update(regions)\
                                .where(regions.regions_id == region_id)\
                                .values(url=imgUrl)

                            await db.execute(queryUpdate)
                            await db.commit()
                            return

                    except Exception as e:
                        print(f"⚠️ Error procesando imagen: {str(e)}")

        # =========================
        # 🌍 2. WIKIMEDIA FALLBACK
        # =========================
        for query in queries:
            images = await search_wikimedia(client, query)

            if images:
                print(f"🌍 Wikimedia usando: {query}")

                for imgUrl in images:
                    try:
                        findObj = await checkExists(db, imgUrl)

                        if not findObj:
                            queryUpdate = update(regions)\
                                .where(regions.regions_id == region_id)\
                                .values(url=imgUrl)

                            await db.execute(queryUpdate)
                            await db.commit()
                            return

                    except Exception as e:
                        print(f"⚠️ Error procesando imagen Wikimedia: {str(e)}")

        # =========================
        # ⚠️ 3. FALLBACK FINAL
        # =========================
        if imgUrl:
            try:
                queryUpdate = update(regions)\
                    .where(regions.regions_id == region_id)\
                    .values(url=imgUrl)

                await db.execute(queryUpdate)
                await db.commit()
            except Exception as e:
                print(f"❌ Error guardando fallback: {str(e)}")


# =========================
# 🔍 CHECK DUPLICATES
# =========================
async def checkExists(db: AsyncSession, imgUrl: str):

    query = select(regions).where(regions.url == imgUrl)
    result = (await db.execute(query)).scalars().all()

    return True if result else False


# =========================
# ▶️ MAIN
# =========================
async def main():
    async for db in get_db():
        await getPhotoInfo(db)


if __name__ == "__main__":
    asyncio.run(main())