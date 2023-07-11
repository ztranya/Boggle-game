
#Se connecter
#Tant que l'utilisateur entre des données erronées, il peut faire des tentatives de connexion,
tentatives=True
while tentatives:
  matricule = input('Quel est votre matricule? ')
  mdp = input('Quel est votre mot de passe? ')
  with open("./desktop/caféAPI/comptes.csv", 'r') as file:
    found = False
    for line in file:
        columns = line.strip().split('|')
        if matricule in columns[0]:
            found = True
            if mdp in columns[3]:
                actif='1'
                if actif in columns[6]:
                  print(f"Bienvenue,{columns[2]}!")
                  tentatives=False
                  break
                else:
                    print('Ce compte n\'est plus actif. Veuillez contacter les administrateurs pour modifier le statut du compte')
            else:
                print("Erreur, le mot de passe est incorrect.")
                break
    if not found:
        print("Erreur, le matricule est incorrect.")

#Formuler une requête



