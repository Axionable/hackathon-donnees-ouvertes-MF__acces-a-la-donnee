# Climate Accessibility
**Réutilisation créée pour le Hachkathon Données Ouvertes Météo-France.**

Outil d’aide à la collecte, la transformation et la manipulation de données climatiques.
### Problématique et proposition de valeur
Centraliser le téléchargement et la manipulation de données issues des différents fournisseurs et de formats différents.
### Solution
Projet Python contenant les différentes routines ETL, suivi d’un prototype Streamlit pour des fins de démonstration. La solution est composée de 3 grandes fonctionnalités :
- **DOWNLOADER** :
    - Création d’un catalogue des données
    - Téléchargement des différentes sources de données
    - Application de filtres : indicateurs/variables, temporels, spatiaux
- **TRANSFORMER** :
    - Fusionner les différentes sources des données : projections DRIAS et modèle SIM
    - Réaliser le changement d’échelle : passer du maillage SAFRAN au découpage communal
- **EXPORTER** :
    - (à faire) Sauvegarder la donnée, dans les formats disponibles : tabulaire (CSV, Excel), GRIB et netCDF
    - (à faire) Mettre à jour une base des données : postgreSQL (nécessaire pour de systèmes SIG)
### Impact envisagé
Cette solution est pensée pour des équipes de Data Scientists et Data Analysts voulant travailler sur des données climatiques. Cet outil permettrait d’optimiser la préparation des environnements de travail.

### Architecture
L'architecture actuelle de l'API n'est pas spécialement optimisée pour des fins de démonstration. Une architecture réelle Cloud permettrait de gérer le backend de manière asynchrone (event-driven architecture), afin de garder une interface web réactive. Voici un exemple d'architecture qui pourrait être mise en place avec Google Cloud Platform:

![Architecture](assets/Proposition%20archi%20Cloud.jpg)

### Membres de l’équipe et leurs compétences
- Samirath BORO NGOBI, Data Engineer
- Chani KABLA, Data Engineer
- Anthony UZAN, Senior Data Engineer
- Gaël CHARLES, Senior Data Engineer
- Xavier COLLIGNON, FullStack Data Engineer
- José SANCHEZ, Senior Manager MLE