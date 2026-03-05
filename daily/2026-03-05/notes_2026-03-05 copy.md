# GCP services

## App Engine
Permet d'héberger et déployer une application alors qu'on donne uniquement le code.
Il :
- déploie
- héberge
- conteneurise
- autoscale si nécessaire
- versionne
Il prend en charge la volumétrie - i.e. couche d'observabilité.

## Streamlit
Permet d'écrire le code d'une application.

## Cloud Run
Pour déployer sur Cloud Run on a besoin d'un conteneur Docker.
Pricing as use.

## Gestion des accès sur GCP
- On gère les accès par utilisateur
- Par ressource (tables, etc.)
- Niveau sur ces ressources - read, write, admin

**Rôles :** reader + editor + owner

**Mécanisme :** user account + service account + TOCHECK

SSO permet d'authentifier.