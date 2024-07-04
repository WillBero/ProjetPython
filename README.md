# Doodle avec Python / Flask

## Docker-compose pour build le projet.

Il suffit de télécharger le projet entier et de lancer le docker compose à la racine du projet.
- _Docker-compose up -d_

## Kubernetes pour build le projet.

### Télécharger Chocolatey ( Admin )
- _@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"_

### Télécharger KubeCTL ( Admin )
- _curl -LO https://dl.k8s.io/release/v1.30.0/bin/windows/amd64/kubectl.exe_

### Ajouter dans le fichier Host: _127.0.0.1 web.local_
- _C:\Windows\System32\drivers\etc\hosts_


### Télécharger Minikube
- _choco install minikube_
- _minikube start_

### A la racine du projet dans un CMD
- _kubectl apply -f ._
- _minikube tunnel_
- _Se rendre sur http://web.local_

##
###_Contributeurs principaux_

- _Killian Douillet_
- _Berhault William_
