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


def geolocaliser(info, nom_fichier):
    geocoder = OpenCageGeocode(api_key_folium)
    
    resultats = geocoder.geocode(str(info["region"]))

    latitude = resultats[0]['geometry']['lat']
    longitude = resultats[0]['geometry']['lng']

    carte = folium.Map(location=[latitude, longitude], zoom_start=9)
    
    popup_contenu = f"Numéro de téléphone : {info['num_tel']}\nOpérateur : {info['operateur']}\nRégion : {info['region']}"

    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_contenu, parse_html=True, max_width=300),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(carte)

    legende = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; font-size:14px; background-color:white; border:2px solid grey; padding: 5px;">
      <b>Légende</b><br>
      <span style="color:blue">&#9632;</span> Emplacement du numéro de téléphone
    </div>
    '''
    carte.get_root().html.add_child(folium.Element(legende))

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
    geolocaliser(tel_info,nom_fichier)

if __name__ == "__main__":
    main()
