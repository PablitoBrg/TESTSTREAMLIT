# 🧾 Documentation – `app.py`

Ce document décrit le fonctionnement du fichier `app.py`, qui constitue le cœur de l'application Streamlit de visualisation des espaces de coworking en Île-de-France.

---

## 📌 Objectif

Ce script Streamlit permet de :

* Collecter, nettoyer et enrichir les données des espaces de coworking.
* Afficher les données sous forme de carte interactive (Folium) et de visualisations (Plotly, matplotlib).
* Proposer une interface utilisateur simple pour explorer, trier et filtrer les espaces.

---

## 🗂️ Structure Générale

Le fichier `app.py` est composé des blocs suivants :

### 1. **Importation des bibliothèques**

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
...
```

Bibliothèques utilisées pour :

* Manipulation de données (`pandas`)
* Visualisation (`plotly`, `folium`, `matplotlib`)
* Interface (`streamlit`, `streamlit_folium`)

---

### 2. **Chargement ou scraping des données**

Deux options :

* Soit les données sont chargées depuis un fichier CSV local ou un cache.
* Soit le script scrape les données depuis le site source si elles ne sont pas encore présentes.

```python
@st.cache_data
def get_data():
    ...
    return df
```

---

### 3. **Traitement des données**

* Nettoyage des colonnes.
* Classification par zone (`Paris (75)` vs. campagne).
* Enrichissement : présence de site web, coordonnées GPS.

---

### 4. **Interface Utilisateur avec Streamlit**

#### Sidebar (latérale)

* Barre de recherche (par nom, code postal ou ville)
* Options d’affichage

#### Corps principal

* Affichage de la **carte Folium**
* Affichage de **graphiques** (camemberts, bar charts, etc.)
* Affichage d’un **DataFrame filtré**
* Téléchargement CSV

---

### 5. **Visualisations interactives**

* **Camembert Plotly** pour visualiser la répartition Paris / campagne.
* **Graphique Plotly** pour la proportion de sites avec ou sans site web.
* **Carte Folium** personnalisée : couleur de fond, icônes, centré automatiquement.

---

## 🖼️ Exemples de composants visuels

```python
# Pie chart avec Plotly
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
st.plotly_chart(fig, use_container_width=True)
```

```python
# Carte Folium
m = folium.Map(location=[lat, lon], zoom_start=12, tiles='cartodbpositron')
for row in df_filtered.itertuples():
    folium.Marker(...).add_to(m)
st_folium(m, width=700, height=500)
```

---

## 📤 Fonctions utiles

### 🔍 Recherche

```python
search = st.text_input("Rechercher un espace...")
df_filtered = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
```

### 📊 Téléchargement CSV

```python
csv = df_filtered.to_csv(index=False)
st.download_button(label="Télécharger les données", data=csv, file_name='coworking.csv')
```

---

## ✅ À Personnaliser / Étendre

* Ajouter un bouton de mise à jour automatique des données.
* Intégrer un tri avancé (par prix, surface, équipements).
* Ajouter des filtres multi-critères (zone, ville, type d'espace).
* Améliorer le design avec `st.markdown()` et `st.columns()`.

---

## 🧪 Exemple de lancement local

```bash
streamlit run app.py
```
