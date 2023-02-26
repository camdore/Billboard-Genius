# Projet Billboard-Genius

Ce projet python permet de créer une application dédiée à la musique contenant les données des meilleures chansons au monde, basées sur les ventes numériques et le streaming de plus de 200 pays dans le monde et de montrer  l'évolution des tendences au fil du temps

## Présentation du sujet

Pour cela nous avons récuperé par le biasis du scraping les donnée contenus dans deux sites web : 

1) Billbord : nous permet de récupérer le classement hebdomadaire des 200 meilleurs chansons d'artistes du classement global 200. Dans le classement du Billboard global 200 les données récupés sont le nom de l'artiste, le titre et des informations liés le rang de la chanson tel que le rang occupé dans semaine actuelle, le meilleur rang atteint et le nombre de semaines que le titre a passé dans le classement.

2) Genius : nous permet de récupérer des données plus spécifiques telles que les genres musicaux, le producteurs, Les dstributeurs et les écrivains du text

Pour une meilleure visualisation des données récuperés le scraping est effectué sur une durée de 5 mois.(Il est important de noter que à cause d'une durée d'attente de environ 2h pour effetuer le scraping dans ça totalité il à été pensé judicieux de stocker les données du mois d'octobre 2022 jusqu'au mois de février 2023 dans un fichier csv).

Une fois l’application lancée vous aurez accès au données de plus de 4000 chanson. Vous pourrez visualiser des données intéressantes concernant l'évolution des tendences au cours du temps ainsi que les genres et distrubuters les plus dominants dans la musique.

### Sources de nos données

Billboard global 200 :  [Billboard.com](https://www.billboard.com/charts/billboard-global-200/).

Genius : [Genius.com](https://genius.com/).

## User Guide 

Ci-dessous les instructions et les précautions nécessaires pour faire tourner l’application dans de bonnes conditions.

### Prérequis 

Vous devez d’abord vous assurer d’avoir la dernière version de Python installée sur votre machine. 
Si ce n’est pas le cas vous pouvez suivre les instructions d'installation [ici](https://www.python.org/downloads/).

Vous devez vous assurer aussi d'avoir Docker installé sur votre machine. Si ce n'est pas le cas vous pouvez le téléchargé [ici](https://www.docker.com/products/docker-desktop/)


### Installation 

Assurez-vous d'abord de posséder Git afin de pouvoir cloner le projet à l'aide de la commande suivante à l'aide de Git Bash 

Pour installer l’application effectuer l’instruction suivante : 

    git clone https://github.com/camdore/Billboard-Genius

Placez vous d'abord dans le repertoire approprié avec la commande suivante : 

    cd /path /Billboard-Genius

Puis, entrez la commande suivante pour construire les conteneurs avec Docker. Il faut également avoir assez d'espace sur votre disque dur (environ 1.5Go). En faisant cela, les installations nécessaires pour les différents packages utilisés seront effectués automatiquement.

    docker-compose up -d

Nous avons maintenant 3 conteneurs qui se lancent. A la fin de leur build, nous avons une adresse locale qui est :

    http://127.0.0.1:5000/

Veuillez copier coller cette url dans votre navigateur préféré pour pouvoir accéder à notre application Web.

## Developper Guide 

### Arbre du projet

    Billboard-Genius/ 

    |-- assets
        |--positions_basket.jpg
        
    |-- scrap
    |-- csv_geoloc.csv 
    |-- functions.py
    |-- main.py 
    |-- README.md 

### Fonctions des différents fichiers 

requirement.txt contient les instructions pour installer les librairies nécessaires.

csv_geoloc.csv contient les données pour les saisons 2003 à 2017 de Lebron James.

functions.py contient les fonctions essentiellement utilisées pour le nettoyage de la dataframe.

main.py contient tout le code permettant d'éxecuter et lancer l'app.

Le répertoire assets contient l'image positions_basket.jpg utilisée dans le README.md de ce projet. 

### Copyright

Je déclare sur l’honneur que le code fourni a été produit par moi/nous même, à l’exception des lignes ci dessous.

## L'application web 

Dans l'application Web, vous pouvez recherchez grâce à la barre de recherche et au filtrer à disposition des informations detaillé liés aux artistes, les tistres des chansons, le genres, les distributeurs et les producteurs.(Il faut cependant reinsegner le nom exact pour la recherche)



### Conclusion 

La visualisation graphique de la donnée permet de faire ressortir des nombreuses tendences interessantes des préférences du grand public. Parmi celle-ci on peut voir comment l'arrivé du noel influence lurdement les abitudes des auditeurs



## Auteurs 

Camille Doré, Thomas Ekué Amouzouglo et Adam Lafkih