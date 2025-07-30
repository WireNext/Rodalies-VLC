import zipfile
import requests
import csv
import json
import os

url = "https://ssl.renfe.com/gtransit/Fichero_AV_LD/google_transit.zip"

print("📦 Descargando fomento_transit...")
r = requests.get(url)
with open("fomento_transit.zip", "wb") as f:
    f.write(r.content)

# Asegurarse de que existe la carpeta antes de extraer
os.makedirs("fomento_transit", exist_ok=True)

print("📂 Extrayendo archivos...")
with zipfile.ZipFile("fomento_transit.zip", 'r') as zip_ref:
    zip_ref.extractall("fomento_transit")

# ✅ Route IDs deseados (sin espacios)
rutas_deseadas = {
    "40T0001C1", "40T0002C1", "40T0005C2", "40T0006C2", "40T0007C3", "40T0008C3",
    "40T0009C4", "40T0010C4", "40T0011C5", "40T0012C5", "40T0013C6", "40T0014C6",
    "40T0015C6", "40T0016C6", "40T0017C3", "40T0018C3", "40T0019C5", "40T0020C5",
    "40T0021C6", "40T0022C6", "40T0023C2", "40T0024C2", "40T0025C3", "40T0026C3",
    "40T0027C1", "40T0028C1", "40T0029C2", "40T0030C2", "40T0031C5", "40T0032C5",
    "40T0033C3", "40T0034C3", "40T0035C2", "40T0036C2", "40T0037C2", "40T0038C2",
    "41T0001C1", "41T0002C1", "41T0005C3", "41T0006C3", "41T0009C2", "41T0010C2"
}

# 1. Filtrar rutas
route_ids = set()
with open("fomento_transit/routes.txt", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    routes_filtradas = []
    for row in reader:
        route_id = row["route_id"].strip()
        if route_id in rutas_deseadas:
            row["route_id"] = route_id
            routes_filtradas.append(row)
            route_ids.add(route_id)

# 2. Filtrar trips por route_id
trip_ids = set()
with open("fomento_transit/trips.txt", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    trips_filtrados = []
    for row in reader:
        if row["route_id"].strip() in route_ids:
            row["route_id"] = row["route_id"].strip()
            trips_filtrados.append(row)
            trip_ids.add(row["trip_id"].strip())

# 3. Filtrar stop_times por trip_id
stop_ids = set()
with open("fomento_transit/stop_times.txt", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    stop_times_filtrados = []
    for row in reader:
        if row["trip_id"].strip() in trip_ids:
            stop_times_filtrados.append(row)
            stop_ids.add(row["stop_id"].strip())

# 4. Filtrar stops por stop_id
with open("fomento_transit/stops.txt", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    stops_filtrados = [row for row in reader if row["stop_id"].strip() in stop_ids]

# 5. Guardar resultados
def guardar(nombre, datos):
    with open(f"fomento_transit/{nombre}.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"✅ Guardado {nombre}.json con {len(datos)} registros")

guardar("routes", routes_filtradas)
guardar("trips", trips_filtrados)
guardar("stop_times", stop_times_filtrados)
guardar("stops", stops_filtrados)
