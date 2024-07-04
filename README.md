# Doodle avec Python / Flask

## Docker-compose pour build le projet.

Il suffit de télécharger le projet entier et de lancer le docker compose à la racine du projet.
_Docker-compose up -d_

- Killian Douillet / Berhault William 


## Kubernetes pour build le projet.

### Télécharger Chocolatey ( Admin )
- @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

### Télécharger KubeCTL ( Admin )
- curl -LO https://dl.k8s.io/release/v1.30.0/bin/windows/amd64/kubectl.exe

### Télécharger Minikube
- choco install minikube
- minikube start

### A la racine du projet dans un CMD
- kubectl apply -f .
- minikube tunnel
- Se rendre sur http://web.local

