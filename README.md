# traceline

Traceline est un petit programme qui permet de récupérer des informations sur un numéro de téléphone, telles que le fuseau horaire, l'opérateur et la région associés. Le programme affiche aussi la localisation sur une carte. 

*Remarque* : Le programme ne récupère que les informations sur le premier opérateur du téléphone. Si l'opérateur du numéro de téléphone a été changé, le programme ne l'affichera pas.

## Installation

1. Clone ce dépôt GitHub :

    ```
    git clone https://github.com/nicolasmarra/traceline.git
    ```

2. Installe les dépendances:

    ```
    pip install -r requirements.txt
    ```
3. Crée un fichier d'environnement .env et ajoute ta clé API de Folium :

    ```
    API_KEY_FOLIUM=your_api_key_here
    ```

## Utilisation

Exécute le programme en utilisant la commande suivante :

```
python3 traceline.py <numéro_de_téléphone> <nom_du_fichier_carte>
```
