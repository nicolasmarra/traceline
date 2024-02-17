import phonenumbers
from phonenumbers import timezone, geocoder, carrier
import os
from dotenv import load_dotenv
from opencage.geocoder import OpenCageGeocode
import folium
import webbrowser
import sys

# Chargement les variables d'environnement
load_dotenv()
api_key_folium = os.getenv("API_KEY_FOLIUM")

def recuperer_infos(num_tel):
    """
    Récupère les informations associées à un numéro de téléphone.
    """
    try:
        tel_parse = phonenumbers.parse(num_tel)
        if phonenumbers.is_valid_number(tel_parse):
            time_zone = timezone.time_zones_for_number(tel_parse)
            operateur = carrier.name_for_number(tel_parse, 'fr')
            region = geocoder.description_for_number(tel_parse, 'fr')
            return {
                "num_tel": num_tel,
                "tel_parse": tel_parse,
                "time_zone": time_zone,
                "operateur": operateur,
                "region": region
            }
        else:
            print("Le numéro de téléphone n'est pas valide.")
            return None
    except Exception as e:
        print("On n'a pas pu récupérer les informations sur ce numéro de téléphone :", e)
        return None

def afficher_infos(info):
    """
    Affiche les informations d'un numéro de téléphone.
    """
    if info:
        print("Informations sur le numéro de téléphone:")
        print("-" * 40)
        print("Numéro de téléphone:", info["num_tel"])
        print("Fuseau horaire :", ", ".join(info["time_zone"]))
        print("Opérateur:", info["operateur"])
        print("Région:", info["region"])
        print("-" * 40)
    else:
        print("Numéro de téléphone invalide.")


def geolocaliser(region, nom_fichier):
    geocoder = OpenCageGeocode(api_key_folium)
    
    resultats = geocoder.geocode(str(region))

    latitute = resultats[0]['geometry']['lat']
    longitude = resultats[0]['geometry']['lng']

    carte = folium.Map(location=[latitute, longitude], zoom_start=9)
    folium.Marker([latitute, longitude], popup=region).add_to(map)
    carte.save(nom_fichier+".html")

    webbrowser.open(nom_fichier+".html")

def main():
    """
    Fonction principale du programme.
    """
    if len(sys.argv) != 3:
        print("Usage: python3 traceline.py <numéro de téléphone> <nom du fichier>")
        sys.exit(1)
    
    tel = sys.argv[1]
    nom_fichier = sys.argv[2]
    
    tel_info = recuperer_infos(tel)
    afficher_infos(tel_info)
    geolocaliser(tel_info["region"],nom_fichier)

if __name__ == "__main__":
    main()
