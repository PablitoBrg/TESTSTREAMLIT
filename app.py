import streamlit as st #interface
import pandas as pd
import requests
from bs4 import BeautifulSoup #Traitement des données
import re #Expression régulière de recherche
import folium
from streamlit_folium import folium_static
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from folium.plugins import HeatMap
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Coworking",
    page_icon="🏢",
    layout="wide"
)
# Afficher les informations sur l'application
st.sidebar.image("https://mycowork.fr/wp-content/uploads/2018/03/Logo-commun-horizontal-1200-600.png")




st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background-color: #fff3f3;
                color: black;
                border-right: 2px solid #eee;
            }
        </style>
        """, unsafe_allow_html=True)
# Titre et description
st.title("🏢Coworking Parisien")
st.markdown("""
Cette application affiche les espaces de coworking situés à Paris.
Les données sont extraites du site [leportagesalarial.com](https://www.leportagesalarial.com/coworking/).
""")


# Fonction pour extraire le code postal d'une adresse
def extract_postal_code(address):
    if not address:
        return None

    # Recherche d'un code postal français (5 chiffres) avec un REGEX
    match = re.search(r'\b(75|91|92|93|94|77|78)\d{3}\b', address)
    if match:
        return match.group(0)[:2]  # Retourne les 2 premiers chiffres
    return None


# Fonction pour géocoder une adresse
@st.cache_data
def geocode_address(address):
    if not address:
        return None, None

    geolocator = Nominatim(user_agent="coworking_app")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        return None, None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None


# Fonction pour scraper les données
# Utilisation du décorateur @st.cache_data pour sauvegarder les résultats de la fonction
@st.cache_data
def scrape_coworking_data():
    st.info("Extraction des données en cours... Cela peut prendre quelques minutes.")
    # On crée l'ensemble de nos tableaux pour stocker les éléments scrapés.
    all_urls = []
    all_coworking_data = []
    # Récupération de l'url
    website_response = requests.get("https://www.leportagesalarial.com/coworking/")
    if website_response.status_code == 200:
        html_content = website_response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Trouver la balise <h3> qui contient le texte spécifique
        h3_element = soup.find('h3', string=lambda text: text and "Coworking Paris – Île de France :" in text)

        # Si l'élément h3 est trouvé, chercher le <ul> suivant
        if h3_element:
            target_ul = h3_element.find_next('ul')

            # Extraire les URLs des éléments <li> dans target_ul
            if target_ul:
                for list_item in target_ul.find_all('li'):
                    link_element = list_item.find('a')
                    if link_element and link_element.get('href'):
                        all_urls.append(link_element.get('href'))

    # Visiter chaque URL et extraire les données
    for url in all_urls:
        page_response = requests.get(url)

        if page_response.status_code == 200:
            coworking_data = {}  # Dictionnaire pour les données de l'URL actuelle

            page_content = page_response.text
            soup = BeautifulSoup(page_content, 'html.parser')

            # Extraire le nom de l'espace de coworking
            h2_element = soup.find('h2', string=lambda text: text and "Contacter" in text)
            if h2_element:
                coworking_space_name = h2_element.text.replace("Contacter", "").strip()
                coworking_data['nom'] = coworking_space_name

                # Trouver le <ul> qui suit le h2
                contact_ul = h2_element.find_next('ul')

                if contact_ul:
                    for list_item in contact_ul.find_all('li'):
                        text = list_item.text
                        link_element = list_item.find('a')

                        # Extraire et stocker les données en fonction des mots-clés
                        if "Adresse :" in text:
                            coworking_data['adresse'] = text.replace("Adresse :", "").strip()
                        elif "Téléphone :" in text:
                            coworking_data['téléphone'] = text.replace("Téléphone :", "").strip()
                        elif "Accès :" in text:
                            coworking_data['acces'] = text.replace("Accès :", "").strip()
                        elif "Site :" in text and link_element:
                            coworking_data['site'] = link_element.get('href')
                        elif "Mail :" in text and link_element:
                            coworking_data['mail'] = link_element.get('href')

            # Ajouter l'URL à l'objet de données
            coworking_data['url'] = url

            # Ajouter le dictionnaire à la liste seulement s'il contient des données
            if coworking_data and 'nom' in coworking_data:
                all_coworking_data.append(coworking_data)

            # Pause pour éviter de surcharger le serveur
            time.sleep(0.5)

    return all_coworking_data


# Fonction principale
def main():
    # Bouton pour déclencher le scraping
    if st.button("Extraire les données des espaces de coworking"):
        coworking_data = scrape_coworking_data()

        # Convertir en DataFrame
        df = pd.DataFrame(coworking_data)

        # Vérifier si des données ont été trouvées
        if df.empty:
            st.warning("Aucun espace de coworking trouvé. Veuillez vérifier la structure du site web.")
            return

        # Ajouter une colonne pour le code postal
        df['code_postal'] = df['adresse'].apply(extract_postal_code)

        # Filtrer les espaces en Île-de-France
        idf_codes = ['75', '91', '92', '93', '94', '77', '78']
        df_idf = df[df['code_postal'].isin(idf_codes)]

        if df_idf.empty:
            st.warning("Aucun espace de coworking trouvé en Île-de-France.")
            return

        # Afficher le nombre d'espaces trouvés
        st.success(f"{len(df_idf)} espaces de coworking trouvés en Île-de-France.")

        # Ajouter les coordonnées géographiques
        coordinates = []
        for address in df_idf['adresse']:
            lat, lon = geocode_address(address)
            coordinates.append((lat, lon))

        df_idf['latitude'], df_idf['longitude'] = zip(*coordinates)

        # Supprimer les lignes sans coordonnées valides
        df_idf = df_idf.dropna(subset=['latitude', 'longitude'])
        # Champ texte
        search_term = st.sidebar.text_input("Recherche")

        # Bouton
        if st.sidebar.button("Lancer la recherche"):
            filtered_df = df_idf[df_idf.apply(lambda row: search_term.lower() in str(row['nom']).lower()
                                                  or search_term.lower() in str(row['code_postal']).lower()
                                                  or search_term.lower() in str(row['ville']).lower(), axis=1)]
        else:
            filtered_df = df_idf
        # Afficher les données
        st.subheader("Liste des espaces de coworking")
        st.dataframe(df_idf[['nom', 'adresse', 'téléphone', 'site', 'code_postal']])

        # Créer la carte
        st.subheader("Carte des espaces de coworking")

        m = folium.Map(location=[48.8566, 2.3522], zoom_start=11, tiles='CartoDB dark_matter')  # Centré sur Paris

        # Ajouter les marqueurs
        for idx, row in df_idf.iterrows():
            if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                popup_text = f"""
                <b>{row['nom']}</b><br>
                Adresse: {row['adresse']}<br>
                """

                if 'téléphone' in row and pd.notna(row['téléphone']):
                    popup_text += f"Téléphone: {row['téléphone']}<br>"

                if 'site' in row and pd.notna(row['site']):
                    popup_text += f"<a href='{row['site']}' target='_blank'>Site web</a><br>"

                if 'url' in row:
                    popup_text += f"<a href='{row['url']}' target='_blank'>Plus d'infos</a>"

                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_text, max_width=300),
                    tooltip=row['nom'],
                    icon=folium.Icon(color='blue', icon='building', prefix='fa')
                ).add_to(m)

        # Afficher la carte
        left, center, right = st.columns([1, 4, 1])
        with center:
            folium_static(m)

        st.subheader("Carte thermique des espaces de coworking")

        heatmap = folium.Map(location=[48.8566, 2.3522], zoom_start=11, tiles='CartoDB dark_matter')
        HeatMap(data=df_idf[['latitude', 'longitude']].dropna().values.tolist()).add_to(heatmap)
        left, center, right = st.columns([1, 4, 1])
        with center:
            folium_static(heatmap)

        st.subheader("📊 Analyse des Espaces")

        # Création de la colonne 'zone'
        df_idf['zone'] = df_idf['code_postal'].apply(lambda x: "Paris (75)" if x == '75' else "Campagne")

        # Comptage des occurrences
        zone_counts = df_idf['zone'].value_counts()

        # Préparation des données pour Plotly
        labels = zone_counts.index.tolist()
        values = zone_counts.values.tolist()
        colors = ['#ff2c2c', '#878787']

        # Création du camembert Plotly
        fig = go.Figure(data=[go.Pie(
            title="Répartition des coworkings Paris / Campagne",
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo='percent+label',
            hole=0,  # camembert plein, pas de donut
        )])

        # Fond transparent
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',  # transparent
            paper_bgcolor='rgba(0,0,0,0)',  # transparent
        )

        df_idf['has_website'] = df_idf['site'].notnull()

        # Comptage
        counts = df_idf['has_website'].value_counts()
        labels = ['Avec site web', 'Sans site web']
        values = [counts.get(True, 0), counts.get(False, 0)]

        # Couleurs personnalisées
        colors = ['#00BFC2', '#FF8C42']

        # Création du graphique
        fig2 = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            marker=dict(colors=colors),
            textinfo='percent+label',
            hoverinfo='label+percent+value'
        )])

        # Apparence propre
        fig2.update_layout(
            title="Répartition des coworkings avec/sans site web",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black')
        )

        # Créer deux colonnes, on place le graphique dans la première (la moitié gauche)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig, use_container_width=True)

        #
        with col2:
            st.plotly_chart(fig2, use_container_width=False)


# Exécuter l'application
if __name__ == "__main__":
    main()



