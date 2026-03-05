# GCP services

COMPUTE

## App Engine
Permet d'héberger et déployer une application alors qu'on donne uniquement le code.
Il :
- déploie
- héberge
- conteneurise
- autoscale si nécessaire
- versionne
Il prend en charge la volumétrie - i.e. couche d'observabilité.

Compute Engine : déployer les VM

## Cloud Run - ancien Cloud Functions
Pour déployer sur Cloud Run on a besoin d'un conteneur Docker.
Pricing as use.

STORAGE

BigQuery

Cloud Storage

## Streamlit
Permet d'écrire le code d'une application.

## Gestion des accès sur GCP
- On gère les accès par utilisateur
- Par ressource (tables, etc.)
- Niveau sur ces ressources - read, write, admin

**Rôles :** reader + editor + owner

**Mécanisme :** user account + service account + TOCHECK

SSO permet d'authentifier.

Cloud Build permet de faire des actions de CI/CD sur GCP

Kraken : Automatisation de CI/CD

MACHINE LEARNING

Versioning model, stockage des metrics
Besoin de MLflow