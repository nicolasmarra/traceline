import phonenumbers
from phonenumbers import timezone, geocoder, carrier
import os
from dotenv import load_dotenv

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

def main():
    """
    Fonction principale du programme.
    """
    #tel = input("Entrez un numéro de téléphone: ")
    tel = "+33775741552"
    tel_info = recuperer_infos(tel)
    afficher_infos(tel_info)

if __name__ == "__main__":
    main()
