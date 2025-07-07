import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim

# --- Konfiguration ---
INPUT_FOLDER = "input_Image"
OUTPUT_FOLDER = "Bilder_Sortiert"
DEFAULT_LOCATION_NAME = "Unbekannter_Ort"
MONTH_NAMES = {
    1: "01_Januar", 2: "02_Februar", 3: "03_Maerz", 4: "04_April",
    5: "05_Mai", 6: "06_Juni", 7: "07_Juli", 8: "08_August",
    9: "09_September", 10: "10_Oktober", 11: "11_November", 12: "12_Dezember"
}
# --- Ende Konfiguration ---


# Cache für Geocoding, um wiederholte API-Anfragen zu vermeiden
location_cache = {}
geolocator = Nominatim(user_agent="image_sorter_script")

def get_decimal_from_dms(dms, ref):
    """Wandelt GPS-Koordinaten von Grad/Minuten/Sekunden in Dezimal um."""
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0
    decimal = degrees + minutes + seconds
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal

def get_location_from_exif(file_path):
    """
    Extrahiert GPS-Koordinaten aus den EXIF-Daten und wandelt sie in einen Ort um.
    """
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if not exif_data:
                return DEFAULT_LOCATION_NAME

            gps_info = {}
            for tag, value in exif_data.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_info[sub_decoded] = value[t]
                    break
            
            if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                lat_dms = gps_info["GPSLatitude"]
                lon_dms = gps_info["GPSLongitude"]
                lat_ref = gps_info["GPSLatitudeRef"]
                lon_ref = gps_info["GPSLongitudeRef"]

                lat = get_decimal_from_dms(lat_dms, lat_ref)
                lon = get_decimal_from_dms(lon_dms, lon_ref)
                
                # Prüfe den Cache, bevor eine neue Anfrage gesendet wird
                if (lat, lon) in location_cache:
                    return location_cache[(lat, lon)]

                # Standort per Reverse Geocoding ermitteln
                # timeout erhöht, um Fehler bei langsamer Verbindung zu vermeiden
                location = geolocator.reverse((lat, lon), exactly_one=True, language='de', timeout=10)
                
                if location and location.raw.get('address'):
                    address = location.raw['address']
                    # Versuche Stadt, Dorf oder Gemeinde zu finden
                    city = address.get('city', address.get('town', address.get('village', '')))
                    if city:
                        # Unerwünschte Zeichen aus Ordnernamen entfernen
                        clean_city = "".join(c for c in city if c.isalnum() or c in (' ', '-')).rstrip()
                        location_cache[(lat, lon)] = clean_city # Im Cache speichern
                        return clean_city

    except Exception as e:
        # print(f"Fehler beim Auslesen des Ortes für {os.path.basename(file_path)}: {e}")
        pass
    
    return DEFAULT_LOCATION_NAME

def get_date_info(file_path):
    """
    Liest Jahr und Monat aus den EXIF-Daten. Fällt auf Dateidatum zurück.
    """
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                date_str = exif_data.get(36867) or exif_data.get(306)
                if date_str:
                    dt_object = datetime.strptime(date_str.split(" ")[0], "%Y:%m:%d")
                    return dt_object.year, dt_object.month
    except Exception:
        pass

    mod_time = os.path.getmtime(file_path)
    dt_object = datetime.fromtimestamp(mod_time)
    return dt_object.year, dt_object.month

def sort_images_by_date_and_location():
    """
    Sortiert Bilder nach der Struktur: Jahr -> Monat -> Ort.
    """
    if not os.path.isdir(INPUT_FOLDER):
        print(f"Fehler: Der Eingabeordner '{INPUT_FOLDER}' wurde nicht gefunden.")
        os.makedirs(INPUT_FOLDER)
        print(f"Ein leerer Ordner '{INPUT_FOLDER}' wurde erstellt. Bitte füge deine Bilder hinzu.")
        return

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    print(f"Starte Sortierung für Bilder im Ordner: '{INPUT_FOLDER}'...")

    for filename in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, filename)
        if not os.path.isfile(file_path):
            continue

        try:
            # 1. Datum (Jahr & Monat) ermitteln
            year, month_num = get_date_info(file_path)
            month_name = MONTH_NAMES.get(month_num, f"{month_num:02d}")

            # 2. Ort ermitteln
            location = get_location_from_exif(file_path)
            
            # 3. Zielpfad erstellen
            target_folder = os.path.join(OUTPUT_FOLDER, str(year), month_name, location)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            
            # 4. Datei verschieben und umbenennen
            new_filename = f"{year}_{filename}"
            destination_path = os.path.join(target_folder, new_filename)
            
            shutil.move(file_path, destination_path)
            print(f"Verschoben: {filename} -> {os.path.relpath(destination_path)}")

        except Exception as e:
            print(f"Fehler bei der Verarbeitung von {filename}: {e}")

    print("\nSortierung erfolgreich abgeschlossen. ✅")

# --- Skriptausführung ---
if __name__ == "__main__":
    sort_images_by_date_and_location()