# Correction Exercice CI/CD

Flask: framework de développement web:
utilisation de templates - variabiliser en Python. Peut être utilisé pour mettre un front pour un utilisateur.

Github action à implémenter: on ne la fait pas from scratch.
Les 3 clés indispensables pour définir:
- trigger
- machines
- jobs

pytest: fonction qui permet de vérifier et de visualiser que pour chaque fonction et chaque classe on a des tests.

# Docker

Nous permet de déployer une application.
Standard pour la mise en production de code.

Permettre de lancer une application sereinement, sans dépendance des OS.

**Image**: recette pour construire l'application
De quoi a-t-on besoin pour faire tourner l'app sur machine virtuelle:
- Python
- dépendances
- code source
- OS
- variables d'environnement (permet d'aller taper dans le service externe)
- serveur

Comme ces étapes sont déterministes >> Docker propose de lister ces étapes = Images

**Container**: image prête à tourner ou image qui tourne TOCHECK

**Daemon**: command docker

**Client**: permet d'interagir avec le Daemon

**Registry**: public ou privé

Docker est aussi une solution d'optimisation:
si on fait tourner des images sur Docker elles sont isolées les unes des autres et partagent les mêmes ressources.

**Avantages Docker**:
- Vitesse de déploiement
- Portabilité - hyper simple de partager l'image
- Isolation

Le Dockerfile est la liste de recette.

Quand on a qu'une seule image dans le projet on met l'image à la racine du repo.

Artifact Registry sur Google

L'application doit être idempotente: donc doit être capable d'oublier pour fonctionner.