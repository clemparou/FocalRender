Arnold focal preview pour maya2016

Le programme contient 2 fichiers :

depthShader2.py : C'est le plug-in, il faut le mettre dans ...\maya2016\bin\plug-ins\
pas besoin de le charger à la main, le script s'en charge, il ne faut pas modifier son nom !
Son rôle est de créer un surface shader avec l'information depth.

focal_script.py : C'est le script il peut être copier dans le script editor ou saved to shelf.
Son role est de créer une instance du shader, de la configurer en fonction des paramètres de la caméra sélectionnée
et de l'appliquer aux objets de type geometry de la scene.

Utilisation : 

Méthode 1 : 
- on selectionne la caméra sur laquelle on veut la preview
- on execute le script
- on ouvre la render view 
- on choisit le maya software renderer
- on lance un rendu d'une frame avec la camera qu'on a selectionnée plus tôt

Cette méthode marche mais le gain de temps par rapport a un rendu arnold est minime, je recommande la 2e

Méthode 2 : 
- on règle le viewport rendrerer sur "Legacy Default Viewport" 
- on active les textures dans le viewport
- on choisit la caméra, dont on veut la preview, comme caméra du viewport
- on selectionne la caméra dont on veut la preview
- on execute le script

le shader apparaît dans le viewport instantanement, le gain de temps par rapport au rendu arnold est maximal.

