import numpy as np
donnees=('GrapheDeTest', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
         [('A', 'A', 2), ('A', 'B', 5), ('A', 'C', 8), ('B', 'C', 6),
          ('B', 'D', 8), ('B', 'E', 6), ('C', 'B', 2), ('C', 'D', 1),
          ('C', 'E', 2), ('D', 'E', 3), ('D', 'F', 1), ('E', 'A', 5),
          ('E', 'D', 1), ('E', 'G', 5), ('F', 'D', 4), ('F', 'E', 1),
          ('F', 'G', 3), ('F', 'H', 6), ('E', 'I', 3), ('G', 'H', 2),
          ('H', 'B', 6), ('H', 'B', 7), ('I', 'J', 4), ('J', 'I', 5)])

class Graphe():
    def __init__(self,Nom,Sommets,Arcs):
        self.nom=Nom
        self.Sommets=Sommets
        self.Arcs=Arcs
    def __str__(self):
        return("{},{}".format(self.Sommets,self.Arcs))
    def __repr__(self):
        return "Graphe : "+self.__str__()
    
    def PlusCourtChemin(self,A): #A objet Sommet de départ
        P=[] # Sommets déjà explorés dont on connait la distance minimale
        D={} # Distance minimale connue des Sommets à A
        for s in self.Sommets:
            D[s]=float('inf')
        D[A]=0
        while len(P)<len(self.Sommets):
            Ls=list(D.items())
            Ls.sort(key=cletri)
            while Ls[0][0] in P:
                Ls.pop(0)
            Sc=Ls[0][0] # Sommet courant
            P.append(Sc)
            for (Sv,poids) in [(arc.arrive,arc.poids) for arc in Sc.ArcsSortants if arc.arrive not in P]: #on explore les sommets voisins de Sc
                if D[Sv]>D[Sc]+poids:
                    D[Sv]=D[Sc]+poids
        
        Ls=list(D.keys()) #liste des sommets "atteints"
        ListeDistances=[(s.nom,D[s]) for s in Ls]
        return ListeDistances
    
    def generer_rapport_texte(self):
        print("Contenu du graphe '{}' :".format(self.nom))
        print("- {} sommets : {}".format(len(self.Sommets),', '.join([s.nom for s in self.Sommets])))
        print("- {} arcs : {}".format(len(self.Arcs),', '.join(['({},{},{})'.format(arc.depart.nom,arc.arrive.nom,arc.poids) for arc in self.Arcs])))
        
        n=len(donnees[1])
        TableauResultats=np.array([['' for i in range(n+1)] for j in range(n+1)],dtype=np.dtype('U100'))
        TableauResultats[0,1:]=donnees[1]
        TableauResultats[1:,0]=donnees[1]
        for i,l in enumerate(donnees[1]):
            L=Graphe1.PlusCourtChemin(Sommets[l])
            for e in L:
                j=donnees[1].index(e[0])
                TableauResultats[i+1,j+1]=str(e[1])

        print('\nTableau des distances:')
        print(TableauResultats)

        print("Plus long des plus courts chemins :")
        print("- Entre {} et {} : distance de {}")
        print (" - {}")
        

class Sommet():
    def __init__(self,nom):
        self.nom=nom
        self.ArcsSortants=[]
    def __str__(self):
        return("{}".format(self.nom))
    def __repr__(self):
        return "Sommet : "+self.__str__()

class Arc():
    def __init__(self,depart,arrive,poids): #départ et arrivé objets Sommet
        self.depart=depart
        self.arrive=arrive
        self.poids=poids
    def __str__(self):
        return("(départ:{}, arrivé:{}, poids:{})".format(self.depart,self.arrive,self.poids))
    def __repr__(self):
        return "Arc : "+self.__str__()

def cletri(x):
    return x[1]
def cletri2(x):
    return x[0]

Sommets={i:Sommet(i) for i in donnees[1]}
Arcs=[]
for i in donnees[2]:
    Arcs.append(Arc(Sommets[i[0]],Sommets[i[1]],i[2]))
    Sommets[i[0]].ArcsSortants.append(Arcs[-1])
print(len(Arcs))    
Graphe1=Graphe("GrapheDeTest",list(Sommets.values()),Arcs)


Graphe1.generer_rapport_texte()




"""n=len(donnees[1])
TableauResultats=np.array([['' for i in range(n+1)] for j in range(n+1)],dtype=np.dtype('U100'))
TableauResultats[0,1:]=donnees[1]
TableauResultats[1:,0]=donnees[1]
for i,l in enumerate(donnees[1]):
    L=Graphe1.PlusCourtChemin(Sommets[l])
    for e in L:
        j=donnees[1].index(e[0])
        TableauResultats[i+1,j+1]=str(e[1])


print('Tableau des distances:')
print(TableauResultats)"""
