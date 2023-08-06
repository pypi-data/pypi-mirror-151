# Odoo Addons Installer
Le but de cette lib est de trouver et d'installer si voulut un dossier contenant des addons Odoo

## ADDONS_GIT
Represent un addons pth ce trouvant sur un repos git distant. Ce repos peut être public ou privé.
S'il est privé uniquement le clone via login mot de passe est supporté

### BRANCH
Permet de préciser une branche ou un tag git a pull en particulier. Par defaut `master` sera utilisé

### CLONE_PATH
Permet de spécifier un chemin ou placer le clone du repos distant.
Ce chemin peut être relatif, càd commencer par un `.` ou par `~` si l'on veut utiliser le path de l'utilisateur éxecutant `addons_installer`

### PULL_OPTIONS
Permet de spécifier d'autres options lors du `git clone`. Par default `--depth#1 --quiet --single-branch` sont utilisé.

### HTTPS_LOGIN et HTTPS_PASSWORD
Permet de spécifier le login et le mot de passe lors du `git clone` si le repo est privé et qu'il necessite une authentification.
Si les 2 sont renseigné alors `PROTOCOLE` passera à `https` automatiquement

### PROTOCOLE
Permet de préciser le protocole de clone à utiliser. peut prendre comme valeur `public` ou `https`. Par defaut c'est `public` ou `https` si `HTTPS_LOGIN` et `HTTPS_PASSWORD` sont rensignées.

### SERVER
Permet de préciser le serveur git lors du `git clone`.

#### ADDONS_SUBDIR_GIT d'ADDONS_GIT
Permet de préciser un sous repertoire du repo `git` à inclure dans les `addons_path` d'Odoo.

## ADDONS_LOCAL
Represente un addons path ce trouvant deja sur la machine host où est executé `addons_installer`

### BASE_PATH
Permet de préciser un path de qui sera ajouté au `ADDONS_LOCAL`. il peut être relatif s'il commence par `.` ou par `~`.

#### ADDONS_SUBDIR_LOCAL d'ADDONS_LOCAL
Permet de préciser un sous repertoire du path d'`ADDONS_LOCAL` à inclure dans les `addons_path` d'Odoo.


