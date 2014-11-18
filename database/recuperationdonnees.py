import sqlalchemy
import random
from database.Basedonnees_initiation import table_morceaux, connection as conn
from creationfichier.fichier import writeM3U, writeXSPF, writePLS

#Définition d'une variable regroupant un ensemble d'arguments
argument_cli = ['titrePlaylist','artistePlaylist','albumPlaylist','genrePlaylist']

#Définition de la playlist
musiquePL =[]

#Fonction permettant de récupérer des données dans la BDD par rapport aux besoins de l'utilisateur
def recupererDonnees(args):
    for attribut in argument_cli:
        if getattr(args, attribut) is not None:
            for argument in getattr(args, attribut):
                if (attribut == 'titrePlaylist'):
                    RecuperationDonnees = sqlalchemy.select([table_morceaux]).where(table_morceaux.c.titre == argument[0])
                if (attribut == 'artistePlaylist'):
                    RecuperationDonnees = sqlalchemy.select([table_morceaux]).where(table_morceaux.c.artiste == argument[0])
                if (attribut == 'albumPlaylist'):
                    RecuperationDonnees = sqlalchemy.select([table_morceaux]).where(table_morceaux.c.album == argument[0])
                if (attribut== 'genrePlaylist'):
                    RecuperationDonnees = sqlalchemy.select([table_morceaux]).where(table_morceaux.c.genre == argument[0])

                # Connection à la base de données suivi de l'execution de la requète
                recuperation = conn.execute(RecuperationDonnees)
                #Insere les données récuperées dans un list
                recuperation = list(recuperation)
                #Melange la musique dans la list
                random.shuffle(recuperation)
                
                
                argument.insert(2,[])
                i=0   #Initialisation de la valeur à 0
                duree = 0 #Initialisation de la valeur à 0
                
                for champBDD in recuperation: #Pour chaque musique recuperer dans la liste, on vérifie la durée afin de correspondre au mieux au demande de l'utilisateur
                    duree += champBDD[5]  #Correspond au champ durée dans la BDD
                    if(duree < argument[1]*60): #Si durée inf. à durée demandé par utilisateur + conversion en minutes
                        argument[2].insert(i, champBDD)
                        i += 1
                    else:
                        duree -= champBDD[5] #Correspond au champ durée dans la BDD
                          

#Génération de la liste de playlist
def generationPlaylist(args):
    i = 0
    for attribut in argument_cli:
        if getattr(args, attribut) is not None:
            for argument in getattr(args, attribut):
                for musique in argument[2]: # Pour chaque musique dans la playlist on insére le titre, l'artiste, l'album, le format et le chemin 
                    musiquePL.insert(i, [musique[0], musique[2], musique[1], musique[5], musique[8]])
                    i += 1
    random.shuffle(musiquePL) #On mélange les musiques aléatoirement
        
def Playlist(args):
    duree = 0 #initialisation à 0
    for musique in musiquePL: #Pour chaque musique dans la playlist selon un genre précis
        duree += musique[3]
        
    if(duree < args.dureePlaylist*60): #Si la duree de la musique est inférieur à la durée totale demandée par l'utilisateur on effectue la requête permettant d'aller chercher des musiques alétoirement dans la base correspondant au genre
        select_morceaux = sqlalchemy.select([table_morceaux])
        resultat = conn.execute(select_morceaux)
        resultat = list(resultat)
        random.shuffle(resultat)
    
    i=len(musiquePL)
    for musique in resultat:
        duree += musique[5] #
        if(duree < args.dureePlaylist*60):
            musiquePL.insert(i, [musique[0], musique[2], musique[1], musique[5], musique[8]])
            i += 1
        else:
            duree -= musique[5]
    
def EcritureFichier(args, musiquePL):
    if(args.formatPlaylist == 'm3u'):
        writeM3U(args, musiquePL)
    if(args.formatPlaylist == 'xspf'):
        writeXSPF(args, musiquePL)
    if(args.formatPlaylist == 'pls'):
        writePLS(args, musiquePL)

