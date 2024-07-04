# Doodle avec Python / Flask

## Docker-compose pour build le projet.

Il suffit de télécharger le projet entier et de lancer le docker compose à la racine du projet.
- Docker-compose up -d

## Kubernetes pour build le projet.

### Télécharger Chocolatey ( Admin )
- @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

### Télécharger KubeCTL ( Admin )
- curl -LO https://dl.k8s.io/release/v1.30.0/bin/windows/amd64/kubectl.exe

### Ajouter dans le fichier Host 127.0.0.1 web.local
- C:\Windows\System32\drivers\etc\hosts


### Télécharger Minikube
- choco install minikube
- minikube start

### A la racine du projet dans un CMD
- kubectl apply -f .
- minikube tunnel
- Se rendre sur http://web.local

## _Contributeurs principaux_

- _Killian Douillet_
- _Berhault William_
