# Utiliser Ubuntu 22.04 comme base
FROM ubuntu:22.04

# Définition des variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV TZ=Indian/Reunion

# Mise à jour et installation des dépendances nécessaires
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        curl \
        tzdata \
        python3 \
        python3-pip \
        nano \
        gcc \
        cron \
        build-essential \
        supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définition du fuseau horaire
RUN ln -fs /usr/share/zoneinfo/Indian/Reunion /etc/localtime

# Définition du répertoire de travail
WORKDIR /app

# Copie des fichiers dans le conteneur
ADD . /app/

# Installation des dépendances Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Copie du fichier Supervisord.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exposition des ports
EXPOSE 8888 9999

# Démarrer Supervisord pour gérer plusieurs processus
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
