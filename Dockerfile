# Utilise l'image Python 3.11 officielle comme base
FROM python:3.11


# Définissez le répertoire de travail à l'intérieur du conteneur
WORKDIR /app
RUN  pip install --upgrade pip
RUN pip install selenium bs4 pandas webdriver_manager pipenv
RUN pipenv install --skip-lock

# Copiez le code du programme dans le conteneur
COPY . /app


CMD ["python", "test_ekue.py" ]
#CMD ["/bin/bash"]