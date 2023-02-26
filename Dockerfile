# Utilise l'image Python 3.11 officielle comme base
FROM python:3.11


# On lance des commandes directement dans le conteneur
# Ici pour créer des dossiers
RUN mkdir /home/dev/ && mkdir /home/dev/code/

# On place le répertoire de travail du conteneur
WORKDIR /home/dev/code/

# On copie l'ensemble des fichiers directement dans le dossier de travail du conteneur
COPY . .
COPY requirements.txt /
RUN pip install -r /requirements.txt
# On install les dépendances via pipenv
RUN  pip install --upgrade pip &&  pip install pipenv && pipenv install --skip-lock

CMD ["python", "flask_app.py" ]
#CMD ["/bin/bash"]