# **P10 SOFTDESK**

Projet "Créez une API sécurisée RESTful en utilisant Django REST" d' OPENCLASSROOMS - formation développeur Python.

### **Le contexte du projet**:
SoftDesk, une société d'édition de logiciels de développement et de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B. 

### **Le projet**:
Créer une API sécurisée REST avec DJANGO REST-FRAMEWORK permettant :

1. L'authentification des utilisateurs (inscription et connexion) à l'aide de JWT.

2. Les opérations CRUD sur les projets, contributeurs/utilisateurs, les problèmes, les commentaires.

3. La gestion des permissions et autorisations de l'utilisateur connecté sur les vues et opérations.

4. la sécurisation des accès et données suivant l'OWASP.


## **Documentation**:

La documentation de l'API est accessible à l'adresse : https://documenter.getpostman.com/view/23145404/2s935pq3eS

Vous y trouverez la définition de chaque endpoint avec les données à fournir et les réponses attendues.

<br>

## **Pré-requis**

Vous pouvez accéder à l'API en :

* clonant le projet à l'aide de votre terminal en tapant la commande :
<br> 

```

    https://github.com/EmmanuelD79/OpenClassrooms_Projet_10_SoftDesk.git


```

* créer un environnement virtuel à l'aide de votre terminal en tapant la commande:

```

    python -m venv env

```

* puis l'activer :
  * sur windows :

    ```

        .\env\scripts\activate

    ```

  * sur mac et linux :

    ```

        source env/bin/activate

    ```

<br>

## **Installation**

Pour utiliser ce projet, il est nécessaire d'installer les modules du fichier requirements.txt.

Pour installer automatiquement ces modules, dans votre terminal, vous devez aller dans le dossier du projet et ensuite taper la commande suivante :
```

pip install -r requirements.txt

```

ou le faire manuellement en consultant le fichier requirements.txt en tapant sur votre terminal la commande :

```

cat requirements.txt

```

puis les installer un par un avec la commande :

```

pip install <nom du paquage>

```
<br>

## **Démarrage**

Pour démarrer le projet, vous devez aller dans le répertoire du projet et taper sur votre terminal la commande:

```

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```


L'application web est disponible en local à l'adresse:  http://localhost:8000/api/

Afin d'utiliser l'API, vous devez d'abord vous inscrire en tant qu'utilisateur à l'aide de l'endpoint :
```
http://localhost:8000/api/signup/

```
puis vous connecter et récupérer les tokens sur l'endpoint :
```
http://localhost:8000/api/login/

```
