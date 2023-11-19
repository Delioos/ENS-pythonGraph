import numpy as np
import graphviz as gv
import os


class Sommet:
    def __init__(self, nom):
        self.nom = nom

    def __str__(self):
        return "{}".format(self.nom)


class Arc:
    def __init__(self, depart, arrive, poids):
        self.depart = depart
        self.arrive = arrive
        self.poids = poids

    def __str__(self):
        return "(départ:{}, arrivé:{}, poids:{})".format(self.depart, self.arrive, self.poids)

    def __repr__(self):
        return "Arc: " + self.__str__()


class Graphe:

    def __init__(self):
        self.nom = "unamed"
        self.sommets = []
        self.arcs = []
        self.tab = np.zeros((len(self.sommets), len(self.sommets)))

    def __str__(self):
        return "{},{}".format(self.sommets, self.arcs)

    def __repr__(self):
        return "Graphe: " + self.__str__()

    def initialiser_depuis_un_tuple(self, donnees):
        nom_graphe, sommets, arcs = donnees
        self.nom = nom_graphe
        self.sommets = [Sommet(s) for s in sommets]
        self.arcs = [Arc(d[0], d[1], d[2]) for d in arcs]
        # initialisation du tableau
        # construction du tableau de distance
        n = len(self.sommets)
        TableauResultats = np.array([['-' for i in range(n + 1)] for j in range(n + 1)], dtype=np.dtype('U100'))

        # on initialise le poids des arcs à

        TableauResultats[0, 1:] = [str(s) for s in self.sommets]
        TableauResultats[1:, 0] = [str(s) for s in self.sommets]

        for arc in self.arcs:
            # recherche de l'indice du sommet de depart
            # on parcourt les matrices numpy avec des indices
            indice_depart = np.where(TableauResultats[0, 1:] == str(arc.depart))[0][0] + 1
            # recherche de l'indice du sommet d'arrivee
            indice_arrivee = np.where(TableauResultats[1:, 0] == str(arc.arrive))[0][0] + 1

            # maj de la valeur dans le tableau
            TableauResultats[indice_depart][indice_arrivee] = arc.poids

        self.tab = TableauResultats

    # fonction permettant de recuperer les voisins d'un sommet en regardant les arcs de notre graphe
    def voisins(self, sommet):
        voisins = []
        for arc in self.arcs:
            if arc.depart == sommet.nom:
                voisins.append(arc.arrive)
        return voisins

    def poids(self, a, b):
        # on retrouve l'arc qui relie a et b
        for arc in self.arcs:
            if arc.depart == a and arc.arrive == b:
                return arc.poids

    # retourne le plus long des plus courts chemins
    def distances_dijkstra(self, sommet_debut):
        # Sommets déjà explorés dont on connait la distance minimale
        sommet_explores = []
        # map des distances minimales connues des Sommets à sommet_debut
        distances = []

        # on initialise la map de predesseceur
        predesseceur = []

        for s in self.sommets:
            distances.append([s.nom, float('inf')])
            predesseceur.append([s.nom, None])

        # on cherche le sommet de depart dans la liste des sommets a explorer pour le mettre a 0
        for i, s in enumerate(distances):
            if s[0] == sommet_debut.nom:
                distances[i] = [s[0], 0]
                break

        # tant qu'il existe un sommet non explore
        while len(sommet_explores) < len(self.sommets):
            # on prends le sommet le plus proche de notre sommet de depart
            # on copie la liste des distances
            distances_copie = distances.copy()
            # on retire les sommets deja explores
            for s in sommet_explores:
                for i, d in enumerate(distances_copie):
                    if d[0] == s:
                        distances_copie.pop(i)
                        break
            # on trie la liste des distances
            distances_copie.sort(key=key_sort)
            # on recupere le sommet le plus proche
            sommet_plus_proche = distances_copie[0][0]
            # on ajoute le sommet le plus proche dans la liste des sommets explores
            sommet_explores.append(sommet_plus_proche)

            # on met a jour les distances
            # on recupere les voisins du sommet le plus proche
            voisins = self.voisins(Sommet(sommet_plus_proche))
            # on met a jour les distances
            # on recupere la liste de voisin qui ne sont pas encore explores
            voisins_non_explores = []
            for v in voisins:
                if v not in sommet_explores:
                    voisins_non_explores.append(v)

            # pour chaque voisin non explore
            for v in voisins_non_explores:
                # si la distance entre le sommet de depart et le voisin est plus grande que la distance entre le
                # sommet de depart et le sommet le plus proche + la distance entre le sommet le plus proche et le voisin
                poids = self.poids(sommet_plus_proche, v)
                # on recupere l'indice du voisin dans la liste des distances
                for i, d in enumerate(distances):
                    if d[0] == v:
                        indice_voisin = i
                        break
                # pareil pour le sommet le plus proche
                for i, d in enumerate(distances):
                    if d[0] == sommet_plus_proche:
                        indice_sommet_plus_proche = i
                        break

                # print("sommet plus proche : {} voisin : {} poids : {}".format(sommet_plus_proche, v, poids))
                d = distances[indice_voisin][1]
                d2 = distances[indice_sommet_plus_proche][1] + poids
                # print("distance entre {} et {} : {}".format(sommet_debut.nom, v, d))
                # print("distance entre {} et {} : {}".format(sommet_debut.nom, sommet_plus_proche, d2))

                # print("distances : {}".format(distances))
                # print("-----------")
                if distances[indice_voisin][1] > distances[indice_sommet_plus_proche][1] + poids:
                    # on met a jour la distance entre le sommet de depart et le voisin
                    distances[indice_voisin][1] = distances[indice_sommet_plus_proche][1] + poids
                    # on met a jour le predesseceur du voisin
                    # on recupere l'indice du voisin dans la liste des predesseceurs
                    for i, d in enumerate(predesseceur):
                        if d[0] == v:
                            indice_voisin = i
                            break

                    predesseceur[indice_voisin][1] = sommet_plus_proche

        # on retrouve le plus long des plus courts chemins
        # on recupere la distance la plus grande
        distance_max = 0
        sommet_plus_loin = None
        distances_filtrees = []
        for d in distances:
            if d[1] != float('inf'):
                distances_filtrees.append(d)

        for d in distances_filtrees:
            if d[1] > distance_max:
                distance_max = d[1]
                sommet_plus_loin = d[0]

        # on retrouve le chemin le plus long en faisant du backtracking
        chemin = []
        while sommet_plus_loin != sommet_debut.nom and sommet_plus_loin is not None:
            chemin.append(sommet_plus_loin)
            for d in predesseceur:
                if d[0] == sommet_plus_loin:
                    sommet_plus_loin = d[1]
                    break
        chemin.append(sommet_debut.nom)
        chemin.reverse()

        return distance_max, chemin, distances

    def html_chemin(self, chemin):
        html = "<ul>"
        for i in range(0, len(chemin) - 1):
            c = chemin[i]
            c2 = chemin[i + 1]
            html += "<li> Origine : {}, Extremite : {}, Poids : {}</li>".format(c, c2 ,
                                                                                self.poids(c,c2 ))
        html += "</ul>"
        return html

    def html_tableau_distances(self, tableau_distances):
        html = "<table>"
        for i, l in enumerate(tableau_distances):
            html += "<tr>"
            for j, c in enumerate(l):
                html += "<td>{}</td>".format(c)
            html += "</tr>"
        html += "</table>"
        return html



    def graphviz_chemin(self, chemin):
        # retirer pour reutiliser en "standalone"
        return ""
        # on trace une premiere fois le graphe full black
        g = gv.Digraph(format='png')
        for s in self.sommets:
            g.node(s.nom)
        for a in self.arcs:
            g.edge(a.depart, a.arrive, label=str(a.poids))

        # puis on rajooute le chemin en rouge
        for i in range(0, len(chemin) - 1):
            c = chemin[i]
            c2 = chemin[i + 1]
            g.edge(c, c2, color="red")
        # on enregistre le graphe
        g.render('graphviz_raw.gv', view=False)
        # on retourne le code html
        return "<img src='graphviz_raw.gv.png' alt='graph' />"

    def html_render(self, tableau_distances, chemin_max, distance_max):
        # on genere le fichier html si il n'existe pas
        if os.path.exists("index.html"):
            os.remove("index.html")

        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>TP-Graphes</title>
</head>
<body>
    <h1>TP-Graphes</h1>
    <h2>Graphe etudie: {}</h2>
    {}<img src="graphviz.svg" alt="graph" />
    <p>Plus long des plus courts chemins est represente en rouge</p>
    <h2>Plus long des plus courts chemins entre {} et {} : distance de {}</h2>    
    <p> arcs contenus dans le chemin : </p>
    <p>{}</p>
   
    <h2>Distances minimales entre les sommets</h2>
    {}
</body>
<style>
    table, th, td {{
        border: 1px solid black;
        border-collapse: collapse;
    }}
</html>""".format(self.nom, self.graphviz_chemin(chemin_max), chemin_max[0], chemin_max[-1],
                  distance_max, self.html_chemin(chemin_max), self.html_tableau_distances(tableau_distances))

        with open('index.html', 'w') as fichier_html:
            # Écrire la chaîne dans le fichier
            fichier_html.write(html)

    def generer_rapport_texte(self):
        print("Contenu du graphe '{}' :".format(self.nom))
        print("- {} sommets : {}".format(len(self.sommets), ', '.join([str(s) for s in self.sommets])))
        print("- {} arcs : {}".format(len(self.arcs), ', '.join([str(arc) for arc in self.arcs])))

        print("Tableau de distance initialisé :")
        print(self.tab)
        tableau_distances = self.tab.copy()
        distance_max = 0
        for i in range(0, len(self.sommets)):
            s = self.sommets[i]
            distance, chemin, distances = self.distances_dijkstra(s)
            # on rempli le tableau de distance
            for d in distances:
                for j in range(0, len(self.sommets)):
                    if tableau_distances[0][j + 1] == d[0]:
                        tableau_distances[i + 1][j + 1] = d[1]
                        break

            if distance > distance_max:
                distance_max = distance
                chemin_max = chemin
                distances_max = distances
                sommet_depart = s

        print("Tableau de distance après l'algorithme de Dijkstra :")
        print(tableau_distances)

        print("Plus long des plus courts chemins :")
        print("- Entre {} et {} : distance de {}".format(sommet_depart, chemin_max[-1], distance_max))
        print("- {}".format(' -> '.join([str(s) for s in chemin_max])))

        self.html_render(tableau_distances, chemin_max, distance_max)


def key_sort(item):
    return item[1]


if __name__ == "__main__":
    # Si ce script est appellé directement, alors la suite est exécutée ; si il est
    # appellé comme un module depuis un autre script la suite n'est pas exécutée
    # Instantiation de l'objet 'g' à partir de la classe 'Graphe'
    g = Graphe()

    donnees = ("Graphe1", ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
               [('A', 'A', 2), ('A', 'B', 5), ('A', 'C', 8), ('B', 'C', 6),
                ('B', 'D', 8), ('B', 'E', 6), ('C', 'B', 2), ('C', 'D', 1),
                ('C', 'E', 2), ('D', 'E', 3), ('D', 'F', 1), ('E', 'A', 5),
                ('E', 'D', 1), ('E', 'G', 5), ('F', 'D', 4), ('F', 'E', 1),
                ('F', 'G', 3), ('F', 'H', 6), ('E', 'I', 3), ('G', 'H', 2),
                ('H', 'B', 6), ('H', 'B', 7), ('I', 'J', 4), ('J', 'I', 5)])

    g.initialiser_depuis_un_tuple(donnees)
    g.generer_rapport_texte()
