Arnold focal preview pour maya2016

Le programme contient 2 fichiers :

depthShader2.py : C'est le plug-in, il faut le mettre dans ...\maya2016\bin\plug-ins\
pas besoin de le charger � la main, le script s'en charge, il ne faut pas modifier son nom !
Son r�le est de cr�er un surface shader avec l'information depth.

focal_script.py : C'est le script il peut �tre copier dans le script editor ou saved to shelf.
Son role est de cr�er une instance du shader, de la configurer en fonction des param�tres de la cam�ra s�lectionn�e
et de l'appliquer aux objets de type geometry de la scene.

Utilisation : 

M�thode 1 : 
- on selectionne la cam�ra sur laquelle on veut la preview
- on execute le script
- on ouvre la render view 
- on choisit le maya software renderer
- on lance un rendu d'une frame avec la camera qu'on a selectionn�e plus t�t

Cette m�thode marche mais le gain de temps par rapport a un rendu arnold est minime, je recommande la 2e

M�thode 2 : 
- on r�gle le viewport rendrerer sur "Legacy Default Viewport" 
- on active les textures dans le viewport
- on choisit la cam�ra, dont on veut la preview, comme cam�ra du viewport
- on selectionne la cam�ra dont on veut la preview
- on execute le script

le shader appara�t dans le viewport instantanement, le gain de temps par rapport au rendu arnold est maximal.

