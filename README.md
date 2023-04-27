# ocfp9_Metro_Quentin
ocfp9 - Développez une application Web en utilisant Django

## LIRE AVEC ATTENTION ET EN ENTIER AVANT DE TENTER QUOI QUE CE SOIT:
Application Web de Ticket/critique sur des livres, avec fonctionnalité de Flux et d'abonnements, utilisant Django

## Prérequis, installation, déploiement:
- Pour télécharger la dernière version, cliquer ci-dessus: Code -> Download ZIP
- apres avoir téléchargé et extraire le ZIP dans un nouveau dossier
- assurer d'avoir une version à jour de 'python'
- Ouvrir un terminal de commandes et placez-vous dans le dossier du projet
- lancer l'environnement virtuel `.\env\Scripts\activate`
- lancer la commande `pip install -r requirements.txt` afin d'installer les packages nécessaire
- puis la commande `python .\LITReview\manage.py runserver` pour lancer le serveur.
- vous pouvez désormais accéder au site par son URL.

## Page accessible sans connexion:
- la page de connexion, permettant de se connecter au site ou de se rediriger vers la page d'inscription.
- la page d'inscription, permettant de créer un compte d'utilisateur.


## Page accessible uniquement en étant connecté:
- la page `Flux` , qui est la page d'accueil après connexion, permet d'afficher tous les tickets et critiques de nous ou des utilisateurs que l'on suit
  -  permet également créer un ticket seul ou un ticket avec sa critique associé.
- la page `Posts` qui affiche tous les tickets et critiques que l'utilisateur a postés. Permet également de les modifier ou supprimer.
- la page `Abonnements` permet de gérer ses abonnements
  - elle contient un chaps de texte pour suivre un utilisateur.
  - la liste des utilisateurs ainsi qu'un bouton permettant de cesser de le suivre.
  - la liste des utilisateurs qui nous suivent.
- La barre de menu contient un bouton `Se déconnecter` afin de se déconnecter et d'être redirigé vers la page de connexion.