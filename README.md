# Projet Billboard-Genius

Ce projet python permet de créer une application dédiée à la musique contenant les données des meilleures chansons au monde, basées sur les ventes numériques et le streaming de plus de 200 pays dans le monde et de montrer  l'évolution des tendences au fil du temps

 les informations liés aux artistes apparu dans le classement du global 200 (https://www.billboard.com/charts/billboard-global-200/)

## Présentation du sujet

Pour cela nous avons récuperé par le biasis du scraping les donnée contenus dans deux sites web : 

1) Billbord : nous permet de récupérer le classement hebdomadaire des 200 meilleurs chansons d'artistes du classement global 200. Dans le classement du Billboard global 200 les données récupés sont le nom de l'artiste, le titre et des informations liés le rang de la chanson tel que le rang occupé dans semaine actuelle, le meilleur rang atteint et le nombre de semaines que le titre a passé dans le classement.

2) Genius : nous permet de récupérer des données plus spécifiques telles que les genres musicaux, le producteurs, Les dstributeurs et les écrivains du text

Pour une meilleure visualisation des données récuperés le scraping est effectué sur une durée de 5 mois 

Une fois l’application lancée vous aurez accès au données de plus de 4000 chanson. Vous pourrez visualiser des données intéressantes concernant l'évolution des tendences au cours du temps ainsi que les genres et distrubuters les plus dominants dans la musique.

### Sources de nos données

Billboard global 200 :  [Billboard.com](https://www.billboard.com/charts/billboard-global-200/).

Genius : [Genius.com](https://genius.com/).

## User Guide 

Ci-dessous les instructions et les précautions nécessaires pour faire tourner l’application dans de bonnes conditions.

### Prérequis 

Vous devez d’abord vous assurer d’avoir la dernière version de Python installée sur votre machine. 
Si ce n’est pas le cas vous pouvez suivre les instructions d'installation [ici](https://www.python.org/downloads/).

### Installation 

Pour installer l’application effectuer l’instruction suivante : 

    git clone https://github.com/camdore/Billboard-Genius

Placez vous d'abord dans le repertoire approprié avec la commande suivante : 

    cd /path /Billboard-Genius

Pour éviter tout bug d'abord effectuer la commande suivante : 

    pip list --format=freeze > requirements.txt 

Pour s’assurer que toutes les librairies suivantes soient installées sur votre machine exécuter la commande suivante : 
   
    python -m pip install -r requirements.txt 

### Utilisation
Pour lancer l’application sur Windows taper l’instruction suivante depuis le terminal : 

    python main.py 

Pour lancer l’application sur Linux/MacOS taper l’instruction suivante depuis le terminal : 

    python3 main.py 

L’application Dashboard tourne sur n'importe quel navigateur à l’adresse suivante : http://127.0.0.1:8050/

L'utilisateur peut cocher les différentes cases et filtres à disposition. Il peut également passer la souris sur les graphiques pour avoir des informations numériques sur les graphiques.

## Developper Guide 

### Arbre du projet

    projet-python/ 

    |-- assets
        |--positions_basket.jpg
        
    |-- requirements.txt 
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

    def ellipse_arc(x_center=0, y_center=0, a=1, b =1, start_angle=0, end_angle=2*np.pi, N=100, closed= False):
    """
        Permet de faire des arcs de cercle équivalents à ceux proposés en SVG 

        Args : 
            x_center : la coordonée x du centre de l'arc de cercle \n
            y_center : la coordonée y du centre de l'arc de cercle \n
            a : point du début de l'arc de cercle \n
            b : point de fin de l'arc de cerlce \n
            start_angle : angle du début de l'arc de cercle \n
            end_angle : angle de la fin de l'arc de cercle \n
            N = nombre d'échantillons pour linspace \n
            closed : fermer ou non l'arc de cercle (bool) 

        Returns: 
            path : le chemin correspondant au l'arc de cercle en SVG (Scalable Vector Graphics)
            
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a*np.cos(t)
        y = y_center + b*np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'

    return path

La fonction `ellipse_arc` vient du site suivant : https://community.plotly.com/t/arc-shape-with-path/7205/5 .

Dans la fonction `add_shape()`, le paramètre path n'accepte pas les arcs de cercle (A) (doc officielle).

## Rapport d'analyse

### Présentaion

Ce projet à pour but de visualiser des données sur les types de tirs effectués lors de la saison 2017-2016. Il à également pour but d'observer l'évolution du jeu en NBA sur les 10 dernières années à travers les données d'un des meilleurs joueur de l'histoire de la NBA : Lebron James.

### La saison 2017-2018

![Positions des joueurs sur un terrain de basket](projet-python/assets/positions_basket.jpg)

Sur le premier graphique nous découvrons que les 10 meilleurs joueurs marquent en général beaucoup plus de paniers à 2 points que de paniers 3 points. Seul James Harden à un nombre de 3 points plus élevé que les 2 points. La proportion de lancer francs est très petite ce qui est normale puisque ces tirs sont accordés après une faute, et non marqués dans le jeu.

Sur le 2e graphique nous voyons que le type de points marqués dépend de la position des joueurs. Ainsi nous observons que les paniers à 3 points sont marqués en majorité par les Shooting Guard (SG) et les Point Guard(PG). Ce qui est logique puisqu'ils sont placés au bord de la ligne des 3 points. Pour les paniers à 2 points ils sont inscrits en majorité par les Center (C) qui sont placés au abord du panier. Les lancers francs ne sont pas influencés par la postion et dépendent uniquement de l'adresse du joueurs qui les tire.

Sur le 3e graphique nous voyons que l'efficicaté des tirs ne change pas malgré l'âge contre ce que l'on auraot pu penser, tout comme le nombre de paniers tentés. Nous remarquons cependant une anomalie pour les joueurs de 39 ans. Cela est expliqué par le fait qu'il n'y en a qu'un seul donc la moyenne est faussée.

### Carrière de Lebron James

La principal évolution à lieu sur le fait que la zone Mid-Range est délaissée au fil des années. Lebron James marque de plus en plus derrière la ligne des 3 points malgré sa position de Power Forward ou Small Forward qui est proche du panier. Bien sur il garde quand même une concentration importante de tirs dans les zones proches du panier. Cela est confirmé par le graphique en dessous avec le nombre de 3 point qui fini par dépasser le nombre de tirs dans la Mid-Range.

### Conclusion 

Nous voyons que la manière de jouer à évoluer au cours des années en NBA. Le rôle de chacun malgré des positions similaires a changer entre 2003 et 2018.

## Auteurs 

Camille Doré et Thomas Ekué Amouzouglo