# 🏢 Coworking Parisien – Visualisation des Espaces en Île-de-France

**TESTSTREAMLIT** est une application Streamlit interactive permettant de visualiser les espaces de coworking situés à Paris et en Île-de-France. Les données sont extraites du site [leportagesalarial.com](https://www.leportagesalarial.com/coworking/), puis enrichies avec des informations géographiques et affichées sur une carte interactive.

---

## ✨ Fonctionnalités

* 🔍 **Extraction automatique des données** depuis le site source.
* 📍 **Géocodage des adresses** pour obtenir les coordonnées GPS.
* 🗺️ **Affichage des espaces sur une carte interactive** avec Folium.
* 📊 **Visualisation des données** sous forme de tableaux et de graphiques.
* 📥 **Téléchargement des données** au format CSV.
* 🎛️ **Filtres interactifs** dans la barre latérale pour affiner les résultats.

---

## 🛠️ Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/PablitoBrg/TESTSTREAMLIT.git
   cd TESTSTREAMLIT
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé) :**

   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application :**

   ```bash
   streamlit run app.py
   ```

---

## 🧾 Dépendances principales

* [Streamlit](https://streamlit.io/) – Création d'interfaces web interactives.
* [Pandas](https://pandas.pydata.org/) – Manipulation et analyse de données.
* [Requests](https://docs.python-requests.org/) – Requêtes HTTP.
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) – Analyse de documents HTML.
* [Folium](https://python-visualization.github.io/folium/) – Cartographie interactive.
* [Geopy](https://geopy.readthedocs.io/) – Géocodage d'adresses.

---

## 📊 Aperçu des Visualisations

L'application propose plusieurs visualisations pour mieux comprendre la répartition des espaces de coworking :

* **Carte interactive** des espaces de coworking en Île-de-France.
* **Diagramme en secteurs** comparant les espaces situés à Paris et en dehors.
* **Statistiques** sur la disponibilité des sites web des espaces.

---

## 📁 Structure du Projet

```
TESTSTREAMLIT/
├── app.py               # Script principal de l'application Streamlit
├── requirements.txt     # Liste des dépendances Python
└── README.md            # Ce fichier
```

---

## 📌 À propos

Ce projet a été réalisé dans le cadre d'un cours pour apprendre à développer des applications web interactives en Python. Il démontre l'utilisation de Streamlit pour créer des interfaces utilisateur conviviales, ainsi que l'intégration de diverses bibliothèques pour le traitement et la visualisation des données.

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.

---

N'hésite pas à personnaliser ce `README.md` en fonction des spécificités de ton projet et des informations que tu souhaites mettre en avant.
