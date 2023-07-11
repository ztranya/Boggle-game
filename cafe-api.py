## cafi-api.py
## Rim El Harras, Ranya Ouzaouit
## 30 avril 2023
## Ce programme est une API simple en Python permettant d'envoyer des requêtes aux cafés étudiants de l'UdeM

#GET /api/menu/items
#GET /api/menu/{categorie}/items
#GET /api/menu/items/{identifiant}
#POST /api/commandes [items]

#GET /api/commandes
#GET /api/commandes/{identifiant}
#PUT /api/menu/items/{identifiant} [disponible=valeur]

import json
from datetime import datetime


def depart() :
    global matricule
    matricule = input('Quel est votre matricule? ')
    mdp = input('Quel est votre mot de passe? ')
    if connection(matricule, mdp) != None :
        demande_requete()
    else : depart()
def connection(matricule, mdp):
    global tentatives
    tentatives = None

    with open("comptes.csv", 'r') as file:
        found = False
        for line in file:
            columns = line.strip().split('|')
            if matricule in columns[0]:

                ## vérifier que la matricule entrée est la matricule complète
                matricule_complete = columns[0]
                if int(matricule_complete) == int(matricule):
                    found = True

                    if mdp in columns[3]:
                        ## vérifier que le mot de passe entré est le mot de passe complet
                        if len(mdp) + 2 == len(columns[3]):
                            actif = '1'
                            if actif in columns[6]:
                                print(f"Bienvenue,{columns[2]}!")

                                # verifier si staff ou public :----------------------------------------------------------

                                if "staff" in columns[5] or "admin" in columns[5]:
                                    tentatives = "staff"

                                elif "public" in columns[5] :
                                    tentatives = "public"

                                break
                            else:
                                print(
                                    'Ce compte n\'est plus actif. Veuillez contacter les administrateurs pour modifier le statut du compte')
                                tentatives = "Inactif"

                        else:
                            found = False
                    else:
                        found = False
                        break
                else:
                    found = False
        if not found:
            print(
                "Erreur, la matricule ou le mot de passe sont erronés... merci de rentrer les informations à nouveau : ")

    return (tentatives)
def commande_n_autorise () :
    print("Vous n'êtes pas autorisé à effectuer cette commande...")
    fin()
def demande_requete () :
    requete = input("Quelle est votre demande : ")
    traitement_requete(requete)
def traitement_requete (requete) :
    reponse = None

    if requete == "GET /api/menu/items" :
        reponse = impression_menu()

    elif requete.startswith("GET /api/menu/") and requete.endswith("/items"):
        choix = (requete[14:len(requete) - 6])
        reponse = impression_categorie(choix)

    elif requete[0:20] == "GET /api/menu/items/" :
        chosen_item = requete[20:len(requete)]
        reponse = information_item(chosen_item)

    elif requete.startswith("POST /api/commandes ") :
            nouvelle_commande = requete[20:len(requete)]
            reponse = ajout_commande(nouvelle_commande)

#commande staff---------------------------------------------------------------------------------------------------------
    elif requete == "GET /api/commandes" :
        if tentatives != "staff" :
            commande_n_autorise()
        affichage_commande ()
    elif  requete[0:19] == "GET /api/commandes/" :
        if tentatives != "staff" :
            commande_n_autorise()
        commande = requete[19:len(requete)]
        reponse = information_commande(commande)

    elif requete[0:20] == "PUT /api/menu/items/" :
        if tentatives != "staff" :
            commande_n_autorise()
        ## Isoler item :------------------------------------------------------------------------------------------------
        # (point de repaire "s" de "items") et (point de repaire "d" de "disponible")
        position_s = requete.index("s")
        position_d = requete.index("d")
        id_item = (requete[position_s + 2: position_d - 1])

        ## Isoler disponibilité voulu :---------------------------------------------------------------------------------
        # (point de repere "=")
        position_egale = requete.index("=")
        disponibilite = (requete[position_egale + 1: len(requete)])

        if disponibilite != "0" and disponibilite != "1":
            print("Erreur... choix de disponibilité doit être égale à 0 ou 1")
            fin()

        else : disponibilite = bool(int(disponibilite))
        # --------------------------------------------------------------------------------------------------------------
        reponse = modification_disponibilite(id_item, disponibilite)


    if reponse != None :
        fin()
def menu () :

    with open('menu.json') as json_file:
        data = json.load(json_file)
    items = []
    for category in ["boisson"]:
        items += data[category]["boisson_chaude"]["cafe"]["items"]
        items += data[category]["boisson_chaude"]["the"]["items"]
        items += data[category]["boisson_chaude"]["chocolat"]["items"]
        items += data[category]["boisson_froide"]["items"]
    for category in ["sandwich"]:
        items += data[category]["regulier"]["items"]
        items += data[category]["wrap"]["items"]
    for category in ["fruit"]:
        items += data[category]["items"]
    for category in ["viennoiserie"]:
        items += data[category]["pain"]["items"]
        items += data[category]["chausson"]["items"]
        items += data[category]["croissant"]["items"]
    for category in ["muffin"]:
        items += data[category]["items"]

    return items

## roles publiques
def impression_menu () :
    print("Voici la liste des items du menu : ")
    for i, item in enumerate(menu ()):
        menu_a_print = f" {i + 1}- {item['nom']}"
        print(menu_a_print)

    return menu
def impression_categorie(choix) :

    categorie_imprimer = False

    premier_item = 0
    dernier_item = 0

    ## categorie
    if choix == "boisson":
        premier_item = 1
        dernier_item = 13

    elif choix == "sandwich":
        premier_item = 14
        dernier_item = 19

    elif choix == "fruit":
        premier_item = 20
        dernier_item = 25

    elif choix == "viennoiserie":
        premier_item = 26
        dernier_item = 34

    elif choix == "muffin":
        premier_item = 35
        dernier_item = 40

    # sous_categorie :

    elif choix == "boisson_chaude":
        premier_item = 1
        dernier_item = 9

    elif choix == "boisson_froide":
        premier_item = 10
        dernier_item = 13
    elif choix == "regulier":
        premier_item = 14
        dernier_item = 17
    elif choix == "wrap":
        premier_item = 18
        dernier_item = 19
    elif choix == "pain":
        premier_item = 26
        dernier_item = 28
    elif choix == "chausson":
        premier_item = 29
        dernier_item = 30
    elif choix == "croissant":
        premier_item = 31
        dernier_item = 34

    ## sous-sous-categorie :

    elif choix == "cafe":
        premier_item = 1
        dernier_item = 5
    elif choix == "the":
        premier_item = 6
        dernier_item = 7
    elif choix == "chocolat":
        premier_item = 8
        dernier_item = 9

    ## impression des items des categories
    chosen_item = premier_item

    while chosen_item in range(premier_item, dernier_item + 1):

        # Cherche l'Item dans la liste d'item
        found_item = None
        for i, item in enumerate(menu()):
            if (i + 1) == chosen_item:
                found_item = item
                break

        # Imprime le résultat
        if found_item:
            print({found_item['id']}, found_item['nom'])
            categorie_imprimer =  True
        else:
            print("Désolé.. cet item n'a pas été trouvé...")
            fin()

        chosen_item += 1
    return (categorie_imprimer)
def information_item (chosen_item) :

    # Cherche l'Item dans la liste d'item
    found_item = None
    for i, item in enumerate(menu ()):
        if str(i + 1) == chosen_item:
            found_item = item
            break

    # Imprime le résultat

    if found_item:
        information = (f"Les informations de cet item sont : Id {found_item['id']} , {found_item['nom']} , "
              f"le prix est de {found_item['prix']} , la disponibilité -- {found_item['disponible']}")

        print(information)
    else:
        print("Désolé... Cet item n'a pas été trouvé..")
        information = ""

    return information
def ajout_commande (nouvelle_commande) :
    ## Trouver les fois comme repères
    x = "x"
    apparence_x = [index for index, character in enumerate(nouvelle_commande) if character == x]
    # -----------------------------------------------------------------------------------------------------------------------
    ## Trouver les depart, espaces, fin comme repères

    espace = " "
    apparence_espace = [index for index, character in enumerate(nouvelle_commande) if character == espace]
    apparence_espace.insert(0, -1)
    apparence_espace.append(len(nouvelle_commande))

    # -----------------------------------------------------------------------------------------------------------------------
    ## Liste des items demandés

    zero = 0
    list_id_choisi = []
    while zero in range(len(apparence_x)):
        id_choisi = nouvelle_commande[apparence_espace[zero] + 1: apparence_x[zero]]
        list_id_choisi.append(id_choisi)
        zero += 1

    ##imprimer chaque nombre de fois par commande:----------------------------------------------------------
    zero = 0
    list_nombre_fois = []
    while zero in range(len(apparence_x)):
        nbr_fois = nouvelle_commande[apparence_x[zero] + 1: apparence_espace[zero + 1]]
        list_nombre_fois.append(nbr_fois)
        zero += 1

    # nombre de commandes deja présentes
    with open("commandes.csv") as file:
        list_nbr_commande = 0
        for line in file:
            columns = line.strip().split('|')
            list_nbr_commande += 1

    # formation ligne de commande :
    # -----------------------------------------------------------------------------------------------------------------------
    column_1 = list_nbr_commande + 1
    # -----------------------------------------------------------------------------------------------------------------------
    column_2 = matricule
    # -----------------------------------------------------------------------------------------------------------------------
    column_3 = ""
    zero = 0

    while zero in range(len(list_nombre_fois)):

        if (list_nombre_fois[zero]).isdigit() == False :
            print("Choix invalide...")
            fin()

        else :
            formulation_commande = (f"{list_id_choisi[zero]}x{list_nombre_fois[zero]}, ")
            column_3 += (formulation_commande)
            zero += 1

    column_3 = (column_3[:-2])
    column_3 += " "
    # ------------------------------------------------------------------------------------------------------------------
    column_4 = datetime.today().strftime('%Y-%m-%d')
    # ------------------------------------------------------------------------------------------------------------------
    #calcul du prix :
    # transformer liste de id en liste de prix :------------------------------------------------------------------------
    zero = 0
    liste_prix = []

    while zero < len(list_id_choisi):
        found_item = 0
        chosen_item = list_id_choisi[zero]
        for i, item in enumerate(menu()):
            if str(i + 1) == chosen_item:
                liste_prix.append(item['prix'])
                found_item += 1

        if found_item == 0 :
            print("Item invalide...")
            fin()


        zero += 1
    # calcul prix total :-----------------------------------------------------------------------------------------------
    prix_total = 0
    zero = 0
    while zero < len(liste_prix) :
        prix = float(liste_prix[zero]) * float(list_nombre_fois[zero])
        prix_total += prix
        zero += 1
    column_5 = prix_total

    # ------------------------------------------------------------------------------------------------------------------
    creation_ligne = (f"\n{column_1}  | {column_2} | {column_3}| {column_4} | {column_5}  ")
    print("La commande à été rajouté à notre dossier de commandes")

    # ------------------------------------------------------------------------------------------------------------------
    # ajout au fichier commandes.csv :
    with open('commandes.csv', 'a') as fd:
        fd.write(creation_ligne)

    return (creation_ligne)

## roles staff
def affichage_commande () :
    # ---ouverture fichier des commande : ---------------------------------------------------------------------------
    with open("commandes.csv") as file:
        for line in file:
            columns = line.strip().split('|')
            print('| ' + columns[0] + '|' + columns[3] + '|' + columns[4])

    fin()
def information_commande(commande) :
    # ---ouverture fichier des commande : ------------------------------------------------------------------------------

    demande = False

    with open("commandes.csv") as file:

        nbr_lignes = 0
        nbr_ligne_non_trouve = 0
        for line in file:
            columns = line.strip().split('|')
            nbr_lignes += 1

            if commande in columns[0]:

                # ---Impression id des items :--------------------------------------------------------------------------
                print(" id : ", columns[0])

                # ---Impression nom items et nombre de fois :-----------------------------------------------------------
                choix = columns[2]

                ## création d'une list incluant point de départ, point final, virgules:---------------------------------
                virgule = [i for i, x in enumerate(choix) if x == ","]
                virgule.insert(0, -1)
                virgule.append(len(choix))

                # création d'une list incluant les multiplication:------------------------------------------------------
                fois = [i for i, x in enumerate(choix) if x == "x"]

                ##imprimer chaque items par commande:-------------------------------------------------------------------
                zero = 0
                list_id_choisi = []
                while zero in range(len(fois)):
                    id_choisi = choix[virgule[zero] + 2: fois[zero]]
                    list_id_choisi.append(id_choisi)
                    zero += 1

                # transformer liste de id a liste de nom :--------------------------------------------------------------

                zero = 0
                liste_nom_choisi = []

                while zero < len(list_id_choisi):
                    chosen_item = list_id_choisi[zero]
                    for i, item in enumerate(menu ()):
                        if str(i + 1) == chosen_item:
                            liste_nom_choisi.append(item['nom'])

                    zero += 1

                ##imprimer chaque nombre de fois par commande:----------------------------------------------------------
                zero = 0
                list_nombre_fois = []
                while zero in range(len(fois)):
                    choix_choisi = choix[fois[zero] + 1: virgule[zero + 1]]
                    list_nombre_fois.append(choix_choisi)
                    zero += 1

                # impression list item et leur nombre de fois:----------------------------------------------------------
                zero = 0
                print(" liste item :")
                while zero in range(len(list_nombre_fois)):
                    print("              -", list_nombre_fois[zero], "fois", liste_nom_choisi[zero])
                    zero += 1

                # ---Impression la date et total de l'achat :-----------------------------------------------------------
                print(
                    " date : ", columns[3], '\n',
                    "total : ", columns[4], "$", '\n',
                )
                demande = True

            else :
                nbr_ligne_non_trouve += 1


    if nbr_ligne_non_trouve == nbr_lignes :
        print("Choix invalide...")

    return demande
def modification_disponibilite(id_item, disponibilite):

    modification_faite = False
    # verifier disponilité type  == bool :
    if type(disponibilite) != bool :
        modification_faite = False
        print("Choix de disponibilité invalide...")

    else :
        with open("menu.json", "rb") as f:
            data = json.load(f)
        # Définit tous les items du menu
        items = []
        for category in ["boisson"]:
            items += data[category]["boisson_chaude"]["cafe"]["items"]
            items += data[category]["boisson_chaude"]["the"]["items"]
            items += data[category]["boisson_chaude"]["chocolat"]["items"]
            items += data[category]["boisson_froide"]["items"]
        for category in ["sandwich"]:
            items += data[category]["regulier"]["items"]
            items += data[category]["wrap"]["items"]
        for category in ["fruit"]:
            items += data[category]["items"]
        for category in ["viennoiserie"]:
            items += data[category]["pain"]["items"]
            items += data[category]["chausson"]["items"]
            items += data[category]["croissant"]["items"]
        for category in ["muffin"]:
            items += data[category]["items"]

        # Modification disponibilité
        chosen_item = str(id_item)

        found_item = 0
        for i, items in enumerate(items):
            if str(i + 1) == chosen_item:
                items['disponible'] = disponibilite
                found_item += 1
                modification_faite = True
                print("La disponibilité du produit à bien été modifié dans le document menu.csv...")

        if found_item == 0 :
            print("Choix d'item invalide...")
            modification_faite = False

        with open("menu.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    return (modification_faite)

def fin() :
    choix = input("Avez-vous une autre demande? (oui, non) : ")

    if choix == "oui" :
        demande_requete()

    elif choix == "non" :
        print("Déconnection en cours... Au revoir!")
        depart()

    else :
        fin()
        print(input("Entrée invalide.. entrez oui ou non : "))
def test():
    def test_connection():

        # 1 Matricule et mdp existant ( connexion réussie)

        matricule = '20130405'
        mdp='yaPass_01'
        assert connection (matricule, mdp) == "public" or connection (matricule, mdp) == "staff"

        # 2 Matricule et mdp existant mais compte non actif

        matricule = '20088891'
        mdp='lfPass_06'
        assert connection (matricule, mdp) == "Inactif"

        # 3 Matricule non existant et/ou le mdp non existant

        matricule = '83729837'
        mdp='lfPas82791872'
        assert connection (matricule, mdp) == None

    #test_connection()

    def test_impression_categorie():

        # Vérification pour une catégorie (1er niveau)
        choix='boisson'
        assert impression_categorie(choix) == True

        # Vérification pour une sous-atégorie (2eme niveau)
        choix='chausson'
        assert impression_categorie(choix) == True

        # Vérification pour une sous-sous-catégorie (dernier niveau)
        choix='chocolat'
        assert impression_categorie(choix) == True

        # Vérification pour une catégorie qui n'est pas valide par l'utilisateur
        choix='smoothie'
        assert impression_categorie(choix) == False

    #test_impression_categorie()

    def test_modification_disponibilite() :
        # Verifier Bonne dispo - Bon item

        id_item = 4
        disponibilite = True
        assert modification_disponibilite(id_item, disponibilite) == True

        # Verifier Bonne dispo - Mauvais item

        id_item = 30129
        disponibilite = False
        assert modification_disponibilite(id_item, disponibilite) == False

        # Verifier mauvaise dispo - Bon item
        id_item = 8
        disponibilite = "coucou"
        assert modification_disponibilite(id_item, disponibilite) == False

        # Verifier utilisation notation 0 - 1 vs True False pour dispo ne marche pas

            # 0 == False

        id_item = 10
        disponibilite_chiffre= 0
        disponibilite_bool = False
        assert modification_disponibilite(id_item, disponibilite_chiffre) != modification_disponibilite(id_item, disponibilite_bool)

            # 1 == True

        id_item = 28
        disponibilite_chiffre= 1
        disponibilite_bool = True
        assert modification_disponibilite(id_item, disponibilite_chiffre) != modification_disponibilite(id_item, disponibilite_bool)

    test_modification_disponibilite()


depart()
#test()