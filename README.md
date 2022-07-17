# Fifteen exercice technique par Alix MACHARD

## Environnement technique

Les librairies utiles au bon fonctionnement du code sont dans le fichier requirements.txt
Afin d'éviter les problèmes liés à l'utilisation de bases de données en local, on utilise ici une base de données
en ligne, postgreSQL.
L'API a été testée à l'aide de l'outil postman pour plus de facilité étant donné l'absence de partie "front"

## Fonctionnement

L'API fonctionne en exécutant le fichier bike_api.py. 
Le fichier prepare_data.py permet la création des tables dans la base de données ainsi que la génération
aléatoire d'un jeu de données (ici 1000 vélos et 50 stations).
Le fichier schemas.py contient les classes demandées dans la première partie du sujet (Bike et Station) ainsi
que deux autres classes qui ont servies à la mise en place de l'API. Il y a également quelques exemples d'utilisation
des modèles qui ont permis de tester les classes dans un premier temps.
Enfin le fichier postgresql_funcs.py contients toutes les fonctions permettant la gestion CRUD demandées dans la deuxième partie du sujet.

## Observations, limites et perspectives

### Base de données

Pour ce qui est de la construction des tables dans la base de données, peut-être aurait-il pu être intéressant de fonctionner différement en ce qui concerne le lien entre vélos et stations. En effet, ces dernières contiennent chacune une liste de vélos qui leur est associée. Peut-être les stations auraient-elles pu être gérées directement depuis la table des vélos en ajoutant un attribut à celle-ci permettant ainsi de simplifier la base de données.

Dans un second temps on peut évoquer la partie historique (demandée en 3ème partie). L'idée ici a été de créer deux historiques (pour les vélos d'un côté et les stations de l'autre). Ces historiques contiennent différents champs tels que un "maintenance_state_old" et un "maintenance_state_new" et ainsi pour chacun des attributs. Il y aurait sans doute une façon plus optimisée de procéder, peut-être en combinant les deux tables dans un premier temps et en ne conservant que les champs nécéssaires selon les cas.

### API

En ce qui concerne l'API, pour chacune de fonctionnalités de celle-ci, des cas d'utilisations particuliers ont été traités (exemple d'un numéro de série qui n'existe pas renvoyant un message erreur à l'utilisateur), certains peuvent être approfondis. 

De même, les problèmes de types qui ont pu être posés entre un objet style dataframe et une réponse json, les conversions pourraient être faites différemment et à d'autres niveaux permettant ainsi une amélioration des performances (notamment en cas de jeu de données important).

De plus et pour la partie historique, le traitement des min date et max date mériteraient d'être différents notamment en cas d'absence de min date, et retournant ainsi les informations uniquement à partir de la date max.
Il eut également peut-être été intéressant d'ajouter des fonctions permettant des retourner l'historique selon d'autres critères que les dates (par exemple, le type d'opération effectuée, le numéro de série etc...). De même que l'ajout de fonction permettant de retrouver les vélos et stations non pas uniquement avec leur numéro de série mais également selon les autres critères.

Les fonctions seraient à optimiser sur différents critères afin d'obtenir de meilleures performances.

### Sécurité

Autre point non inclu dans le sujet, la sécurité. En effet il y aurait beaucoup de choses à ajouter à sujet, un système d'authentification (inscription et connexion à l'aide d'un mot de passe hashé) permettant d'intéragir avec l'API, peut-être différents degrés d'accès (de l'admin ayant tous les droits à un utilisateur plus restreint). En ce qui concerne la partie suppression, l'utilisation d'un système d'authentification à deux facteurs permettrait de sécuriser plus encore.
Garder une trace des évênements et des statistiques de connexions peut aussi aider à sécuriser le système.
L'utilisation de jetons CSRF permettent également de gagner en sécurité et sont supportés par Flask (requête json/Ajax)