# Bubble Tea

## Présentation

Ce programme est une simulation de gestion d'une entreprise de Bubble Tea. Le but du joueur est de faire croître son entreprise en gérant les ressources (matières premières, équipements, employés, etc.) et en maximisant les bénéfices.

## Fonctionnalités

- Gestion des employés : embauche, licenciement, paiement des salaires
- Gestion des équipements : achat, vente
- Gestion des matières premières : achat, utilisation
- Calcul des bénéfices mensuels
- Paiement du loyer mensuel

## Base de données

Le programme utilise une base de données SQLite pour stocker les informations de l'entreprise, des employés, des équipements, des matières premières et des types d'équipements/matériaux.

![Image de conception de la base de données](https://cdn.discordapp.com/attachments/1029731031630233601/1096123709128978542/image.png)

<details>
  <summary>Conception de la base de données</summary>

- La première table est "entreprises" qui contient des informations sur les différentes entreprises. Cette table stocke les identifiants d'entreprise, les noms, les prénoms et les capitaux.

- La deuxième table est "employes" qui stocke les informations sur les employés de chaque entreprise. Cette table stocke les identifiants d'employés, les noms, les prénoms, les salaires, les niveaux de productivité et les identifiants d'entreprise.

- La troisième table est "equipement_type" qui stocke les différents types d'équipement que les entreprises peuvent acheter. Cette table stocke les identifiants d'équipement, les noms, les prix et les unités.

- La quatrième table est "equipement" qui contient les équipements possédés par chaque entreprise. Cette table stocke les identifiants d'équipement, les identifiants de type d'équipement et les identifiants d'entreprise.

- La cinquième table est "matiere_premiere_type" qui stocke les différents types de matières premières que les entreprises peuvent acheter. Cette table stocke les identifiants de matière première, les noms, les prix et les unités.

- La sixième table est "matiere_premiere" qui contient les matières premières possédées par chaque entreprise. Cette table stocke les identifiants de matière première, les identifiants de type de matière première, les identifiants d'entreprise et les quantités.

- Enfin, il y a la septième table qui est "matiere_premiere_utilise" qui contient des informations sur les matières premières nécessaires à la production de Bubble Tea, leur quantité nécessaire et l'identifiant de l'entreprise.

Ces différentes tables permettent de stocker les informations nécessaires pour la gestion de l'entreprise de Bubble Tea, tels que le capital, les employés, les équipements et les matières premières.

</details>

## Utilisation

Pour lancer le jeu il faut ouvrir **jeu.py** dans un interpréteur Python. Une fois le jeu lancé, le joueur doit créer une entreprise, puis peut commencer à gérer son entreprise en choisissant parmi les options de menu.

## Exemple en jeu

- Création d'entreprise
  ![Image de l'inscription](https://cdn.discordapp.com/attachments/1029731031630233601/1096117284474474600/image.png)

- Gestion d'employés
  ![Image de gestion des employe](https://cdn.discordapp.com/attachments/1029731031630233601/1096118049414844569/image.png)

  - Embauche

  ![Image de gestion des employe](https://cdn.discordapp.com/attachments/1029731031630233601/1096118262816850091/image.png)

  - Licenciment
    ![Image de gestion des employe](https://cdn.discordapp.com/attachments/1029731031630233601/1096118496896765952/image.png)

- Fin de tour
  ![Image de fin de tour](https://cdn.discordapp.com/attachments/1029731031630233601/1096118994106323024/image.png)

### Créé par Juliette SOL et Clotilde Oliver
