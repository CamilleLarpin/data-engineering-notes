# Notes — sql-crud

## Optimzing BQ usage
Store: almost free
Load/ Extract/ Copy data: free
Processing: 5$/B

Set up quotas: at project level or user level

Limit columns queried

Partitioning

CREATE OR REPLACE ne fonctionne que dans une même region

Structure: regroupement de nbre de colonnes

Array: reduire stockage


## Table VS View ##

Table: octet de sauvergarde >> utilisation pour plugguer à un dashboard qui demande d’executer la donnée frequement

View: octet de transformation >> utilisation possible dans pipeline de donnée pour étape interfmediaire OU comme proxi de secu car ne donne pas accès directement à la donnée


## CRUD ##
