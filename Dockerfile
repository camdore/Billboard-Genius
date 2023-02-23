# Utilise l'image Python 3.11 officielle comme base
FROM python:3.11


# Définissez le répertoire de travail à l'intérieur du conteneur
WORKDIR /app
<<<<<<< HEAD
=======

#Ouvre et installe les différents loigiciels requis
>>>>>>> 139b30b5715d9cf778db9014e95f4cb60de80a15
RUN  pip install --upgrade pip
RUN pip install selenium bs4 pandas webdriver_manager pipenv
RUN pipenv install --skip-lock

# Copiez le code du programme dans le conteneur
COPY . /app

<<<<<<< HEAD

=======
#Lance le programme souhaité
>>>>>>> 139b30b5715d9cf778db9014e95f4cb60de80a15
CMD ["python", "test_ekue.py" ]
#CMD ["/bin/bash"]