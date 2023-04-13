import random
import sqlite3
nom = ""
prenom = ""
joueur_id = 0
nom_entreprise = ""
entreprise_id = 0

conn = sqlite3.connect("jeu.db")
cursor = conn.cursor()


def RandomEmploye():
    noms = ['Dubois', 'Martin', 'Durand', 'Lefebvre', 'Moreau', 'Fournier', 'Girard', 'Barbier', 'Fontaine', 'Rousseau', 'Chevalier', 'Lemaire', 'Perrin', 'André', 'Roussel',
            'Moulin', 'Garnier', 'Simon', 'Marchand', 'Dupont', 'Leroy', 'Lecomte', 'Renard', 'Fabre', 'Mercier', 'Gauthier', 'Clement', 'Aubert', 'Dumont', 'Brun', 'Blanchard']

    prenoms = ['Jean', 'Pierre', 'Paul', 'Jacques', 'François', 'Antoine', 'Nicolas', 'Michel', 'David', 'Patrick', 'Alexandre', 'Vincent', 'Maxime', 'Thomas', 'Julien',
               'Christophe', 'Luc', 'Laurent', 'Julie', 'Sophie', 'Marie', 'Caroline', 'Isabelle', 'Nathalie', 'Catherine', 'Hélène', 'Emilie', 'Alice', 'Camille', 'Elodie']

    """Fonction qui renvoie une liste de 5 employés aléatoires"""
    personnes = []
    for i in range(5):
        nom = random.choice(noms)
        prenom = random.choice(prenoms)
        salaire_brut = random.randint(1710, 3500)
        productivite = round(random.uniform(0.5, 1.5), 2)
        personnes.append({'nom': nom, 'prenom': prenom,
                          'salaire_brut': salaire_brut, 'productivite': productivite})
    return personnes


def Setup():
    CreerTable()
    AjoutEquipementType()
    AjoutMatierePremiereType()


def CreerTable():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS joueurs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT
        )
        """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS entreprises(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            capital INTEGER,
            responsable_id INTEGER,
            FOREIGN KEY(responsable_id) REFERENCES joueurs(id)
            )
        """)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            salaire_brut INTEGER,
            productivite FLOAT,
            entreprise_id INTEGER,
            FOREIGN KEY(entreprise_id) REFERENCES entreprises(id)
            )
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipement_type(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prix INTEGER
        )
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipement(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipement_type_id INTEGER,
        entreprise_id INTEGER,
        FOREIGN KEY(equipement_type_id) REFERENCES equipement_type(id),
        FOREIGN KEY(entreprise_id) REFERENCES entreprises(id)
        )
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matiere_premiere_type(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        prix INTEGER,
        unit TEXT
        )
        """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matiere_premiere(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matiere_premiere_type_id INTEGER,
        entreprise_id INTEGER,
        quantite INTEGER,
        FOREIGN KEY(matiere_premiere_type_id) REFERENCES matiere_premiere_type(id),
        FOREIGN KEY(entreprise_id) REFERENCES entreprises(id)
        )
        """)

    conn.commit()


def AjoutEquipementTypeBase(nom, prix):
    cursor.execute(
        """
        INSERT INTO equipement_type(nom, prix)
        VALUES(?, ?)
        """, (nom, prix))
    conn.commit()


def AjoutEquipementType():
    # Verifie si la table equipement_type est vide
    cursor.execute(
        """
        SELECT * FROM equipement_type
        """
    )
    if cursor.fetchone() is None:
        AjoutEquipementTypeBase("Chaise", 25)
        AjoutEquipementTypeBase("Table", 175)
        AjoutEquipementTypeBase("Machine à thé", 300)
        AjoutEquipementTypeBase("Machine à sceller", 800)


def AjoutMatierePremiereTypeBase(nom, prix, unité):
    cursor.execute(
        """
        INSERT INTO matiere_premiere_type(nom, prix,unit)
        VALUES(?, ?, ?)
        """, (nom, prix, unité))
    conn.commit()


def AjoutMatierePremiereType():
    # Verifie si la table matiere_premiere_type est vide
    cursor.execute(
        """
        SELECT * FROM matiere_premiere_type
        """
    )
    if cursor.fetchone() is None:
        AjoutMatierePremiereTypeBase("Thé en vrac", 10, "kg")
        AjoutMatierePremiereTypeBase("Lait", 0.7, "L")
        AjoutMatierePremiereTypeBase("Gobelets en plastique", 0.05, "unité")
        AjoutMatierePremiereTypeBase("Pailles en plastique", 0.02, "unité")
        AjoutMatierePremiereTypeBase(
            "Cuillères à thé en plastique", 0.01, "unité")


def AjouterJoueurBase():
    """Ajout d'un joueur dans la base de données"""
    cursor.execute(
        """
        INSERT INTO joueurs(nom, prenom)
        VALUES(?, ?)
        """, (nom, prenom))
    """Récupération de l'id du joueur"""
    joueur_id = cursor.lastrowid
    conn.commit()
    return joueur_id


def AjouterEntrepriseBase():
    """Ajout d'une entreprise dans la base de données"""
    cursor.execute(
        """
        INSERT INTO entreprises(nom, capital, responsable_id)
        VALUES(?, ?, ?)
        """, (nom_entreprise, 50_000, joueur_id))
    entreprise_id = cursor.lastrowid
    conn.commit()
    return entreprise_id


def Inscription():
    global nom, prenom, joueur_id, nom_entreprise, entreprise_id
    """Inscription d'un joueur"""
    print("Pour votre inscription, veuillez remplir le formulaire ci-dessous")
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    nom_entreprise = input("Nom de l'entreprise : ")
    """Ajout dans la base de données"""
    joueur_id = AjouterJoueurBase()
    entreprise_id = AjouterEntrepriseBase()
    print("Merci pour votre inscription, vous êtes maintenant inscrit au jeu")


def SelectMenu(text, possibilities):
    """Fonction qui permet de choisir un menu parmis plusieurs possibilités"""
    while True:
        choix = input(text)
        if choix in possibilities:
            return choix
        else:
            print("Veuillez choisir un choix valide")


def MenuPrincipal():
    print("""
        Vos possibilités ce tour-ci sont les suivantes :
        0. Continuer
        1. Gestions des employés
        2. Gestions des équipements
        3. Gestions des matières premières
        4. Afficher mon solde
        """
          )
    choix = SelectMenu("Votre choix : ", ["0", "1", "2", "3", "4"])
    if choix == "0":
        print("Vous avez choisi de continuer")
        return
    if choix == "1":
        return GestionEmployes()
    if choix == "2":
        return GestionEquipements()
    if choix == "3":
        return GestionMatierePremiere()
    if choix == "4":
        return AfficherMonSolde()


def GestionEmployes():
    print("""
        Vos possibilités ce tour-ci sont les suivantes :
        0. Quitter la gestion des employés
        1. Liste des employés
        2. Embaucher un employé
        3. Licencier un employé
        """
          )
    choix = SelectMenu("Votre choix : ", ["0", "1", "2", "3"])
    if choix == "0":
        MenuPrincipal()
        return
    if choix == "1":
        ListeEmployes()
        return
    if choix == "2":
        EmbaucherEmploye()
        return
    if choix == "3":
        LicenciementEmploye()
        return


def EmbaucherEmploye():
    print("Voici la liste des employés que vous pouvez embaucher, ( numéro, nom, prenom, salaire(BRUT), productivité):")
    embauchable = RandomEmploye()
    for i in range(len(embauchable)):
        print(i+1, embauchable[i]["nom"], embauchable[i]["prenom"],
              embauchable[i]["salaire_brut"], embauchable[i]["productivite"])
    print("Vous pouvez embaucher un employé en tapant son numéro")
    print("Vous pouvez aussi quitter en tapant 0")
    choix = SelectMenu("Votre choix : ", ["0", "1", "2", "3", "4", "5"])
    if choix == "0":
        GestionEmployes()
        return
    EmbaucherEmployeBase(embauchable[int(choix)-1])
    print("Bravo, vous avez embauché un nouvel employé")
    GestionEmployes()


def EmbaucherEmployeBase(employe):
    """Ajout d'un employé dans la base de données"""
    cursor.execute(
        """
        INSERT INTO employes( nom, prenom, salaire_brut, productivite, entreprise_id)
        VALUES(?, ?, ?, ?, ?)
        """, (employe["nom"], employe["prenom"], employe["salaire_brut"], employe["productivite"], entreprise_id))
    conn.commit()


def ListeEmployesBase():
    cursor.execute(
        """
        SELECT * FROM employes
        WHERE entreprise_id = ?
        """, (entreprise_id,))
    employes = cursor.fetchall()
    return employes


def ListeEmployes():
    employes = ListeEmployesBase()
    if (len(employes) == 0):
        print("Vous n'avez pas encore d'employés")
        input("Appuyez sur entrée pour continuer")
        GestionEmployes()
        return
    print("Voici la liste des employés de votre entreprise (numéro, nom, prenom, salaire(BRUT), productivité):")
    for (id, nom, prenom, salaire, productivite, entreprise_id) in employes:
        print(nom, prenom, salaire, productivite)
    input("Appuyez sur entrée pour continuer")
    GestionEmployes()


def LicenciementEmploye():
    print("Voici la liste des employés que vous pouvez licencier, (nom, prenom, salaire(BRUT), productivité):")
    employes = ListeEmployesBase()
    possibilites = ["0"]
    for (id, nom, prenom, salaire, productivite, entreprise_id) in employes:
        print(id, nom, prenom, salaire, productivite)
        possibilites.append(str(id))
    print("Vous pouvez licencier un employé en tapant son numéro")
    print("Vous pouvez aussi quitter en tapant 0")
    choix = SelectMenu("Votre choix : ", possibilites)
    if choix == "0":
        GestionEmployes()
        return
    LicencierEmployeBase(choix)
    print("Vous avez licencié un employé")
    input("Appuyez sur entrée pour continuer")
    GestionEmployes()


def LicencierEmployeBase(employe_id):
    """Suppression d'un employé dans la base de données"""
    cursor.execute(
        """
        DELETE FROM employes
        WHERE id = ?
        """, (employe_id,))
    conn.commit()


def GestionEquipements():
    print("""
        Vos possibilités ce tour-ci sont les suivantes :
        0. Quitter la gestion des équipements
        1. Liste des équipements
        2. Acheter un équipement
        3. Vendre un équipement
        """
          )
    choix = SelectMenu("Votre choix : ", ["0", "1", "2", "3"])
    if choix == "0":
        MenuPrincipal()
        return
    if choix == "1":
        ListeEquipements()
        return
    if choix == "2":
        AcheterEquipement()
        return
    if choix == "3":
        VendreEquipement()
        return


def EquipementAchetable():
    """Fonction qui permet de récupérer la liste des équipements achetables"""
    cursor.execute(
        """
        SELECT * FROM equipement_type
        """)
    equipements = cursor.fetchall()
    return equipements


def AcheterEquipement():
    print("Voici la liste des équipements que vous pouvez acheter, (nom, prix, productivité):")
    equipements = EquipementAchetable()
    possibilites = ["0"]
    for (id, nom, prix) in equipements:
        print(id, nom, prix)
        possibilites.append(str(id))
    print("Vous pouvez acheter un équipement en tapant son numéro")
    print("Vous pouvez aussi quitter en tapant 0")
    choix = SelectMenu("Votre choix : ", possibilites)
    if choix == "0":
        GestionEquipements()
        return

    equipement = equipements[int(choix)-1]
    if (Capital() < equipement[2]):
        print("Vous n'avez pas assez d'argent pour acheter cet équipement")
        input("Appuyez sur entrée pour continuer")
        GestionEquipements()
        return
    AcheterEquipementBase(equipement)
    print("Vous avez acheté un nouvel équipement")
    input("Appuyez sur entrée pour continuer")
    GestionEquipements()


def EquipementBase():
    """Fonction qui permet de récupérer la liste des équipements de l'entreprise"""
    cursor.execute(
        """
        SELECT * FROM equipement AS e1
        JOIN equipement_type AS et ON e1.equipement_type_id = et.id
        WHERE e1.entreprise_id = ?
        """, (entreprise_id,))
    equipements = cursor.fetchall()
    return equipements


def ListeEquipements():
    equipements = EquipementBase()
    if (len(equipements) == 0):
        print("Vous n'avez pas encore d'équipements")
        input("Appuyez sur entrée pour continuer")
        GestionEquipements()
        return
    print("Voici la liste des équipements de votre entreprise (nom, prix):")
    for (id, equipement_type_id, entreprise_id, id, nom, prix) in equipements:
        print(nom, prix,)
    input("Appuyez sur entrée pour continuer")
    GestionEquipements()


def VendreEquipement():
    print("Voici la liste des équipements que vous pouvez vendre, ( numero, nom, prix):")
    equipements = EquipementBase()
    possibilites = ["0"]
    for (id, equipement_type_id, entreprise_id, type_id, nom, prix) in equipements:
        print(id, nom, prix/2, "€")
        possibilites.append(str(id))
    print("Vous pouvez vendre un équipement en tapant son numéro")
    print("Vous pouvez aussi quitter en tapant 0")
    choix = SelectMenu("Votre choix : ", possibilites)
    if choix == "0":
        GestionEquipements()
        return
    VendreEquipementBase(choix)
    print("Vous avez vendu un équipement")
    input("Appuyez sur entrée pour continuer")
    GestionEquipements()


def VendreEquipementBase(equipement_id):
    """Suppression d'un équipement dans la base de données"""
    equipement = cursor.execute(
        """
        SELECT * FROM equipement AS e1
        JOIN equipement_type AS et ON e1.equipement_type_id = et.id
        WHERE e1.id = ?
        """, (equipement_id,)).fetchone()

    cursor.execute(
        """
        DELETE FROM equipement
        WHERE id = ?
        """, (equipement_id,))
    cursor.execute(
        """
        UPDATE entreprises
        SET capital = capital + ?/2
        WHERE id = ?
        """, (equipement[5], entreprise_id))
    conn.commit()


def AcheterEquipementBase(equipement):
    """Ajout d'un équipement dans la base de données"""
    cursor.execute(
        """
        INSERT INTO equipement( equipement_type_id, entreprise_id)
        VALUES(?, ?)
        """, (equipement[0], entreprise_id))
    cursor.execute(
        """
        UPDATE entreprises
        SET capital = capital - ?
        WHERE id = ?
        """, (equipement[2], entreprise_id))
    conn.commit()


def GestionMatierePremiere():
    print("""
        Vos possibilités ce tour-ci sont les suivantes :
        0. Quitter la gestion des matières premières
        1. Liste des matières premières
        2. Acheter une matière première

        """
          )
    choix = SelectMenu("Votre choix : ", ["0", "1", "2"])
    if choix == "0":
        MenuPrincipal()
        return
    if choix == "1":
        ListeMatierePremiere()
        return
    if choix == "2":
        AcheterMatierePremiere()
        return


def AfficherMonSolde():
    print("Votre solde est de", Capital(), "€")
    input("Appuyez sur entrée pour continuer")
    MenuPrincipal()
    return


def MatierePremiereBase():
    """Fonction qui permet de récupérer la liste des matières premières de l'entreprise"""
    cursor.execute(
        """
        SELECT * FROM matiere_premiere AS mp
        JOIN matiere_premiere_type AS mpt ON mp.matiere_premiere_type_id = mpt.id
        WHERE mp.entreprise_id = ?
        """, (entreprise_id,))
    matieres = cursor.fetchall()
    return matieres


def ListeMatierePremiere():
    print("Voici la liste des matières premières que vous possédez (nom, quantité):")
    matieres = MatierePremiereBase()
    if (len(matieres) == 0):
        print("Vous n'avez pas encore de matières premières")
        input("Appuyez sur entrée pour continuer")
        GestionMatierePremiere()
        return
    for (id, matiere_premiere_type_id, entreprise_id, quantite, premiere_type_id, nom, prix, unit) in matieres:
        print("-", nom, quantite, unit)
    input("Appuyez sur entrée pour continuer")
    GestionMatierePremiere()


def MatierePremiereTypeBase():
    """Fonction qui permet de récupérer la liste des matières premières de l'entreprise"""
    cursor.execute(
        """
        SELECT * FROM matiere_premiere_type
        """)
    matieres = cursor.fetchall()
    return matieres


def AcheterMatierePremiereBase(matiere_premiere_type_id, quantite_achat):
    """Ajout d'une matière première dans la base de données"""
    matiere = cursor.execute(
        """
        SELECT * FROM matiere_premiere_type
        WHERE id = ?
        """, (matiere_premiere_type_id,)).fetchone()
    cursor.execute(
        """
        INSERT INTO matiere_premiere( matiere_premiere_type_id, entreprise_id, quantite)
        VALUES(?, ?,?)
        """, (matiere_premiere_type_id, entreprise_id, quantite_achat))
    cursor.execute(
        """
        UPDATE entreprises
        SET capital = capital - ?
        WHERE id = ?
        """, (matiere[2]*quantite_achat, entreprise_id))
    conn.commit()


def AcheterMatierePremiere():
    print("Voici la liste des matières premières que vous pouvez acheter, ( numero, nom, prix, quantité):")
    matieres = MatierePremiereTypeBase()
    possibilites = ["0"]
    for (id, nom, prix, quantite) in matieres:
        print(id, nom, prix, "€/", quantite,)
        possibilites.append(str(id))
    print("Vous pouvez acheter une matière première en tapant son numéro")
    print("Vous pouvez aussi quitter en tapant 0")
    choix = SelectMenu("Votre choix : ", possibilites)
    if choix == "0":
        GestionMatierePremiere()
        return
    quantite_achat = 0
    while quantite_achat <= 0:
        try:
            quantite_achat = int(input("Combien voulez-vous en acheter ? "))
        except ValueError:
            print("Vous devez entrer un nombre")

    AcheterMatierePremiereBase(choix, quantite_achat)
    print("Vous avez acheté une matière première")
    input("Appuyez sur entrée pour continuer")
    GestionMatierePremiere()


def paiementSalaire():
    """Fonction qui permet de payer les salaires des employés"""
    employes = ListeEmployesBase()
    for (id, nom, prenom, salaire, productivite, entreprise_id) in employes:
        cursor.execute(
            """
            UPDATE entreprises
            SET capital = capital - ?
            WHERE id = ?
            """, (salaire, entreprise_id))
        conn.commit()


def Benefices():
    """Fonction qui permet de calculer les bénéfices de l'entreprise"""
    equipements = EquipementBase()
    employes = ListeEmployesBase()
    benef = 0
    fait_par_employe = random.randint(50, 200)
    for (id, nom, prenom, salaire, productivite, entreprise_id) in employes:
        if (not MatierePremiereUtilise(fait_par_employe)):
            print("Vous n'avez pas assez de matières premières pour produire plus de Bubble Tea, fermeture de l'entreprise...")
            return benef

        benef = benef + productivite*len(equipements)*fait_par_employe*5.5
    return benef


def MatierePremiereUtilise(quantite_necessaire):
    # Création de la liste des matières premières nécessaires pour la recette
    # Avec:
    #     - 2g de thé pour un Bubble Tea
    #     - 15cl de Lait pour un Bubble Tea
    #     - 1 goblet pour un Bubble Tea
    #     - 1 paille pour un Bubble Tea
    #     - 1 cuillères en plastique pour un Bubble Tea

    necessaire = [
        {
            "matiere_premiere_type_id": 1,
            "quantite_necessaire": quantite_necessaire*0.010

        },
        {
            "matiere_premiere_type_id": 2,
            "quantite_necessaire": quantite_necessaire*0.15
        },
        {
            "matiere_premiere_type_id": 3,
            "quantite_necessaire": quantite_necessaire
        },
        {
            "matiere_premiere_type_id": 4,
            "quantite_necessaire": quantite_necessaire
        },
        {
            "matiere_premiere_type_id": 5,
            "quantite_necessaire": quantite_necessaire
        }
    ]
    for matiere in necessaire:
        if (not AMatierePremiere(matiere["matiere_premiere_type_id"], matiere["quantite_necessaire"])):
            return False
    for matiere in necessaire:
        SupprimeMatierePremiereUtilise(
            matiere["matiere_premiere_type_id"], matiere["quantite_necessaire"])
    return True


def SupprimeMatierePremiereUtilise(matiere_premiere_type_id, quantite_necessaire):
    if (not AMatierePremiere(matiere_premiere_type_id, quantite_necessaire)):
        return False
    cursor.execute(
        """
        UPDATE matiere_premiere
        SET quantite = quantite - ?
        WHERE matiere_premiere_type_id = ? AND entreprise_id = ?
        """, (quantite_necessaire, matiere_premiere_type_id, entreprise_id))
    conn.commit()
    return True


def AMatierePremiere(matiere_premiere_type_id, quantite_necessaire):
    """Fonctions qui permet de savoir s'il y a assez de matières premières pour la production"""
    matiere = cursor.execute(
        """
        SELECT * FROM matiere_premiere
        WHERE matiere_premiere_type_id = ? AND entreprise_id = ?
        """, (matiere_premiere_type_id, entreprise_id)).fetchone()
    if (matiere == None):
        return False
    if matiere[3] >= quantite_necessaire:
        return True
    else:
        return False


def TurnBenefices():
    benef = Benefices()
    cursor.execute(
        """
        UPDATE entreprises
        SET capital = capital + ?
        WHERE id = ?
        """, (benef, entreprise_id))
    conn.commit()


def Capital():
    """Fonction qui permet de récupérer le capital de l'entreprise"""
    cursor.execute(
        """
        SELECT capital FROM entreprises
        WHERE id = ?
        """, (entreprise_id,))
    capital = cursor.fetchone()
    return capital[0]


def PaiementLoyer():
    """Fonction qui permet de payer le loyer"""
    cursor.execute(
        """
        UPDATE entreprises
        SET capital = capital - ?
        WHERE id = ?
        """, (2666, entreprise_id))
    conn.commit()


Setup()
Inscription()
print(
    f"""Bienvenue {nom} {prenom} en tant que responsable de l'entreprise {nom_entreprise}, vous avez un capital {50_000}€ pour commencer.
   Vous êtes au tour 0. Chaque tour est considere comme un mois, le jeu durera 4 ans, soit 48 tours.
   Vous avez déjà un local, dans l'hyper centre de Toulouse, chaque mois vous devez payer 2666€ de loyer.
   Votre but est de faire grossir votre entreprise de Bubble Tea, pour cela vous devez embaucher des employés, acheter des équipements, etc.
   """
)


def Tour(nombre):
    ancien_capital = Capital()
    paiementSalaire()
    after_salaire = Capital()
    TurnBenefices()
    after_benef = Capital()
    PaiementLoyer()
    print(f"Vous êtes au tour {nombre}.")
    print(f"Vous avez payé {ancien_capital - after_salaire}€ de salaires")
    print(
        f"Vous avez fait {after_benef - after_salaire}€ de vente de Bubble Tea")
    print(f"Vous avez payé 2666€ de loyer")
    print(f"Vous avez maintenant {Capital()}€")
    if (Capital() <= 0):
        print("Vous avez fait faillite, l'entreprise est fermée...")
        exit(0)
    input("Appuyez sur entrée pour continuer")


for i in range(48):
    MenuPrincipal()
    Tour(i+1)
