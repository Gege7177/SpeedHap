import sys, string
from group import *
from candidates import *

class SNP_Matrix:
    def __init__ (self, nameFile=None, M=None):
        if nameFile is None and M is None:
            print "Initialization error"
            sys.exit ()
        if nameFile is not None and M is not None:
            print "Initialization error"
            sys.exit ()
        if nameFile is not None:
            self.M = self.__load_from_file (nameFile)
        else:
            self.M = M
        self.origM = [m for m in self.M]
        self.T = self.__stranspose ()
        self.coverage,  self.mean_frag_size = self.__evaluateCoverageAndFragSize ()
        print "Ceverage", self.coverage, "Mean fragment size", self.mean_frag_size
        
    def __load_from_file (self, nameFile):
        """la funzione legge un file di testo e inserisce
        ciascuna riga in un vettore di stringhe
        Si assume che il numero di colonne sia uguale per tutte le righe """
        try:
            f = open (nameFile)
        except:
            print "File not found"
            sys.exit ()
        v = [riga[:-1] for riga in f]
        f.close ()
        return v

    def __stranspose (self):
        """ data una matrice(vettore di stringhe) costruisce la matrice trasposta
        Si assume che il numero di colonne sia uguale per tutte le
        righe """
        ncol = len(self.M[0])
        transpose = ['' for j in range (ncol)]
        for snp in self.M:
            transpose = [transpose[j]+ snp[j] for j in range(ncol)]
            """la matrice in realta' e' un vettore di stringhe
            la trasposta viene ottenuta costruendo le righe in modo incrementale
            La riga i della matrice di input viene usata per costruire simultaneamente
            la colonne i di tutte le righe della matrice di output"""
        return transpose
   
    def __evaluateCoverageAndFragSize (self):
        tot = 0
        for t in self.T:
            for i in range (len (t)):
                if t[i] != "-":
                    tot += 1
        coverage = (tot / len (self.T)) / 2  # / 2  coverage for the single haplotype
        FragSize = float (tot) / (len (self.M))
        return coverage, FragSize
    
    def groupsBuild (self):
        """Costruisce il vettore dei Gruppi"""
        groups = []
        for i in range(len(self.T)):
            if len(self.T[i]) != 0 :
                g = group (self.T[i])
                groups.append (g)
        self.groups = groups

        for i in range (len (self.groups)):
            #print i
            errors = self.groups[i].cleanSet (self.coverage)
            #errors, tobecorr, chcorr = self.groups[i].cleanSet (self.coverage)
            #if chcorr != "-":
            #    chcorr = self.origM[chcorr][i]
            #    for e in tobecorr:
            #        if self.coverage > 2:
            #            self.origM[e] = self.origM[e][:i] + chcorr + self.origM[e][i+1:]
            #        self.M[e] = self.M[e][:i] + chcorr + self.M[e][i+1:]
            for e in errors:
                # This line is for test
                #self.M[e] = self.M[e][:i] + string.upper (self.M[e][i]) + self.M[e][i+1:]
                self.M[e] = self.M[e][:i] + "-" + self.M[e][i+1:]
                
    def buildComparMatrix (self):
        """ dato un vettore di gruppi,
        costruisce la matrice dei confronti tra gruppi
        la matrice restituita e' una  matrice triangolare M,
        dove l'elemento M[ij]= alla matrice quadrata data dal confronto
        tra i gruppi i,j  """
        length = len(self.groups)
        mCompares = [[None for i in range(j)] for j in range(length)]
        for i in range (length) :
            #for j in range (i):   # XXX - Without sampling
            for j in range (max (0, i - 100), i):   # XXX - With sampling
                mCompares[i][j] = self.groups[i].getComparMatrix(self.groups[j])
        self.mCompares = mCompares




    def outputHaplotype2 (self, rows):
        """costruisce l'haplotype a partire dalla matrice di input iniziale
        Ogni carattere dell'haplotype e' scelto sulla base del carattere, in quella posizione,
        maggiormente presente tra le righe del sottoinsieme ricevuto in input. """
        
        length = len (self.origM[0])  # Length of the haplotype
       
        candidate = [[0,0,0,0] for i in range (length)]
        haplotype = ""
       
        for j in range (length):
            for row in rows:  # Is the index of the row of self.origM
                if self.origM[row][j] == "a":
                    candidate[j][0] += 1
                elif  self.origM[row][j] == "c":
                    candidate[j][1] += 1
                elif  self.origM[row][j] == "g":
                    candidate[j][2] += 1
                elif  self.origM[row][j] == "t":
                    candidate[j][3] += 1

            maxval = candidate[j][0]
            character = "a"
            if candidate[j][1] > maxval:
                maxval = candidate[j][1]
                character = "c"
            if candidate[j][2] > maxval:
                maxval = candidate[j][2]
                character = "g"
            if candidate[j][3] > maxval:
                maxval = candidate[j][3]
                character = "t"
            if maxval == 0:
                character = "-"
                # If unsure of the character return -
            haplotype += character    
        return haplotype
 


    def outputHaplotype (self, rows, final=False):
        """costruisce l'haplotype a partire dalla matrice di input corretta
        Ogni carattere dell'haplotype e' scelto sulla base del carattere, in quella posizione,
        maggiormente presente tra le righe del sottoinsieme ricevuto in input. """
        
        length = len (self.M[0])  # Length of the haplotype
       
        candidate = [[0,0,0,0] for i in range (length)]
        haplotype = ""
       
        for j in range (length):
            if not final:
                if self.groups[j].getSetsSize () == 1 and len (self.groups[j].sets[0]) > 0:
                    for s in self.groups[j].sets[0]:
                        break
                    haplotype += self.M[s][j]
                    continue
            for row in rows:  # Is the index of the row of self.M
                if self.M[row][j] == "a":
                    candidate[j][0] += 1
                elif  self.M[row][j] == "c":
                    candidate[j][1] += 1
                elif  self.M[row][j] == "g":
                    candidate[j][2] += 1
                elif  self.M[row][j] == "t":
                    candidate[j][3] += 1
 
            maxval = candidate[j][0]
            character = "a"
            if candidate[j][1] > maxval:
                maxval = candidate[j][1]
                character = "c"
            if candidate[j][2] > maxval:
                maxval = candidate[j][2]
                character = "g"
            if candidate[j][3] > maxval:
                maxval = candidate[j][3]
                character = "t"
            if maxval == 0:
                character = "-"
            # If unsure of the character return -
            haplotype += character
            
        return haplotype


    def labelGroup (self,alphaset, betaset, correctErrors):
        """ data una partizione iniziale delle righe restituisce, se possibile, una partizione piu ampia
        ottenuta confrontando il superGruppo costruito a partire dalla partizione iniziale con 
        tutti i gruppi non ancora etichettati. se il parametro correctErrors= True,
        gli errori riscontrati vengono corretti sia nei gruppi che nella matrice di input"""
        
        isChanged = False
        alpha = [0 for i in range (len (self.M))]
        beta = [0 for i in range (len (self.M))]
        alpha_err = set ()
        beta_err = set ()
        superGroup = group (alphaset, betaset)
        vCompares = self.buildVectorSuperGVSGroups ( superGroup )
        for i in range  (len(self.groups)):
            #print i, self.groups[i].labeled
            if( not self.groups[i].labeled and vCompares[i] != None  ):
              
                if correctErrors == True:
                    """prima corregge il gruppo e poi prova ad etichettarlo """
                    rowA, rowB, indA, indB = self.groups[i].markGroup (vCompares[i], superGroup)
                    characterA = self.M[indA][i]
                    characterB = self.M[indB][i]
                    for e in rowA :
                        self.M[e] = self.M[e][:i] + characterB  + self.M[e][i+1:]
                    for e in rowB :
                        self.M[e] = self.M[e][:i] + characterA  + self.M[e][i+1:]
                            
                    mcompares = self.groups[i].getComparMatrix (superGroup)
                    #print mcompares
                    a,b = self.groups[i].labelingGroup ( mcompares, superGroup, False)
                elif correctErrors == False:
                    a,b = self.groups[i].labelingGroup ( vCompares[i] , superGroup, False)
                else:
                    errA, errB = self.groups[i].detectErrorInGroup (vCompares[i], superGroup)
                    mcompares = self.groups[i].getComparMatrix (superGroup)
                    a,b = self.groups[i].labelingGroup ( mcompares , superGroup, False)
                    for e in errA:
                        alpha_err.add (e)
                    for e in errB:
                        beta_err.add (e)
                for x in a:
                    alpha[x] += 1
                for x in  b:
                    beta[x] += 1

        for err in alpha_err:
            alphaset.discard (err)
        for err in beta_err:
            betaset.discard (err)

        for i in range (len(self.M)):
            if alpha[i] > beta[i]:
                if(not i in betaset):
                    alphaset.add(i)
                    isChanged = True

            if alpha[i] < beta[i] :
                if(not i in alphaset):
                    betaset.add (i)
                    isChanged = True

        return isChanged, vCompares







    def buildVectorSuperGVSGroups (self, superGroup):
        """Costruisce un vettore di matrici di confronto ottenute dal confronto tra il gruppo ricevuto in input
        con tutti gli altri gruppi"""
        
        vCompares = [None  for i in range (len(self.groups))]
        for i in range  (len(self.groups)):
            vCompares[i] = superGroup.getComparMatrix(self.groups[i])
            if vCompares[i] is not None:
                # If there are no intersections this matrix is not neaded
                if vCompares[i][0][0] == 0 and vCompares[i][0][1] == 0 and \
                       vCompares[i][1][0] == 0 and vCompares[i][1][1] == 0:
                    vCompares[i] = None
        return vCompares



   
        """PRIMO STEP- INIZIO: Suddivisione delle righe in una prima partizione"""
  
    def  reconstruction_Step1_buildPartition (self):
        """ data una lista di candidati (coppie di gruppi) divide i gruppi in due liste
        L'intersezione delle liste e' vuota, la loro unione restituisce un sottoinsieme dell'insieme dei Gruppi"""
        # The vector with the number of conflicts for the group
        conflictCols = [self.groups[i].totCollision for i in range (len (self.groups))]
        print conflictCols
        print
        conflictColsW = [self.groups[i].weightCollision for i in range (len (self.groups))]
        print conflictColsW
        print
        #conflictCols = conflictColsW  # XXX  - Weights
        c = candidates (self.mCompares, conflictCols, self.coverage, self.mean_frag_size)
        candList = c.sortCandidates ()

        alpha = [0 for i in range (len (self.M))]
        beta = [0 for i in range (len (self.M))]
        m = self.mCompares
        if len (self.groups) == 0:
            return [] ,[]
        g = self.groups
        if candList is None:
            return None, None
        
        c = candList[0]

        g[ c[0] ].alpha = 0
        g[ c[0] ].beta = 1
        g[ c[0] ].labeled = True
        
        for x in g[c[0]].sets [ g[ c[0] ].alpha ]:
            alpha[x] += 1
        for x in  g [c[0]].sets [ g[ c[0] ].beta ]:
            beta[x] += 1
        for c in candList:
            #print c, self.mCompares[c[0]][c[1]]
            if g[c[0]].labeled:
                a,b = g[c[1]].labelingGroup(self.mCompares[c[0]][c[1]], g[c[0]])
            else:
                a,b= g[c[0]].labelingGroup(self.mCompares[c[0]][c[1]], g[c[1]])
            for x in a:
                alpha[x] += 1
            for x in  b:
                beta[x] += 1
        alphaset = []
        betaset = []
        for i in range (len (self.M)):
            if alpha[i] > beta[i]:
                alphaset.append (i)
            if alpha[i] < beta[i]:
                betaset.append (i)

        #print alphaset
        #print betaset
        #sys.exit ()
        return alphaset, betaset

    """PRIMO STEP- FINE: Suddivisione delle righe in una prima partizione"""




    """SECONDO STEP - INIZIO : Data una partizione iniziale faccio un primo tentativo per estenderla:
    controllo i gruppi e verifico se il gruppo e' affetto da errori,
    verifico cioe'se il rapporto tra l'insieme con cardinalita' max e quello con cardinalita' min supera la Soglia"""

    def reconstruction_step2 (self, alphaset, betaset):
        """ data una partizione iniziale delle righe restituisce, se possibile, una partizione piu ampia
        ottenuta
        controllando i gruppi ed eliminando eventuali errori se l'insieme piu' piccolo del gruppo ha taglia<soglia
        costruisce un superGruppo a partire dalla partizione iniziale e
        lo incrementa man mano che riesce a correggere e ad etichettare i rimanenti gruppi """
        vCompares = []
        soglia = self.getSoglia_forStep2 ()
        self.step2_checkGroups (soglia)
        isChanged = True
        while  isChanged :
            while  isChanged :
                isChanged, vCompares = self.labelGroup (alphaset, betaset, False)
            # allow correct errors in 2x2 matrices
            isChanged, vCompares = self.labelGroup (alphaset, betaset, True)
        return alphaset, betaset, vCompares





    def getSoglia_forStep2 (self):
        """Funzione usata per determinare i gruppi in cui si sono avuti errori nell'input
        Calcola la soglia ,per ragioni di prudenza e' posta pari alla meta
        del valor medio (<1) dei rapporti tra le cardinalita degli insiemi di un gruppo"""
        rapporti = 0.0
        tot = 0.0
        for i in range (len (self.groups)):
            if self.groups[i].labeled and self.groups[i].getSetsSize () == 2:
                rapporti +=  self.groups[i].getRapporto()
                tot += 1
        return (float (rapporti) / float (tot)) / 2.0




    def step2_checkGroups (self, soglia):
        """Funzione usata nella seconda fase della  ricostruzione dell'aplotipo
        Controlla i gruppi eliminando eventuali errori. Se la taglia dell'insieme piu piccolo del gruppo
        e minore della soglia, e probabile che il gruppo sia affetto da errori e che
        la colonna in origine presentasse un solo carattere"""
        for i in range (len (self.groups)):
            if not self.groups[i].labeled and self.groups[i].getSetsSize () == 2:
                #print i
                #errors, tobecorr, chcorr = self.groups[i].cleanSet (self.coverage, soglia)
                errors = self.groups[i].cleanSet (self.coverage, soglia)
                #if chcorr != "-":
                #    chcorr = self.origM[chcorr][i]
                #    for e in tobecorr:
                #        if self.coverage > 2:
                #            self.origM[e] = self.origM[e][:i] + chcorr + self.origM[e][i+1:]
                #        self.M[e] = self.M[e][:i] + chcorr + self.M[e][i+1:]
                for e in errors:
                    self.M[e] = self.M[e][:i] + "-" + self.M[e][i+1:]

    """SECONDO STEP- FINE"""



    
    """TERZO STEP - INIZIO: ulteriore estenzione della partizione"""
                
    def reconstruction_step3 (self, alphaset, betaset, vCompares):
        cand_as_super = self.__choose_supergroup_forStep3 (alphaset, betaset, vCompares)
        # Notthing to do in step 3
        if cand_as_super == -1:
            return None, None
        self.groups[cand_as_super].labeled = True  # The supergroup was labeled in a certain sense
        alpha = set (self.groups[cand_as_super].sets[0])
        beta = set (self.groups[cand_as_super].sets[1])
        isChanged = True
        while  isChanged :
            while  isChanged :
                isChanged, vCompares = self.labelGroup (alpha, beta, None)
        return alpha, beta


    def __choose_supergroup_forStep3 (self, alphaset, betaset, vCompares):
        maxval = 0
        cand_as_super = -1
        for i in range (len (self.groups)):
            if not (self.groups[i].labeled) and len (self.groups[i].sets) == 2 :
                if  vCompares[i] is not None:
                    val = vCompares[i][0][0] + vCompares[i][0][1] + vCompares[i][1][0] + vCompares[i][1][1]
                    if val > maxval:
                        maxval = val
                        cand_as_super = i
        return cand_as_super

        
        """TERZO STEP- FINE"""



        """FUNZIONI ADOTTATE SOLO PER IL TEST"""
          
    def test_filippo2 (self, alphaset, betaset):
        alpha= self.outputHaplotype (alphaset)
        beta = self.outputHaplotype (betaset)
    
        rowsL = [None for i in range ( len (self.M))]
        for i in alphaset:
            rowsL[i] = 0
        for i in betaset:
             rowsL[i] = 0
        for i in range (len (self.M)):
            if rowsL[i] == None:
                hdistA, covA =  self.getHDistAndCov (self.M[i], alpha )
                hdistB, covB =  self.getHDistAndCov (self.M[i], beta )
                print i, self.M[i]
                print "Confr. con Alpha", "dist =", hdistA, "cop =", covA
                print   "Confr. con Beta","dist =", hdistB,"cop =", covB


   
        
        
            
                    
            
                
    def getHDistAndCov (self, string1, string2):
        """ date due stringhe calcola
        - la distanza di Hamming
        - la copertura, cioe quanto si sovrappongono"""
        
        if (len (string1) != len (string2)):
            print "Initialization error", len (string1), "!=", len (string2)
            sys.exit ()
            
        hDist = 0
        cov = 0
        for i in range (len (string1)) :
            if string1 [i] != "-" and string2 [i] != "-":
                cov += 1
                if string1 [i] != string2 [i]:
                    hDist += 1
        return hDist, cov


        



    def __compFn (self, a, b):
        if a[0] - b[0] != 0:
            return a[0] - b[0]
        return b[1] - a[1]




    def getVectorDistAndCov (self, newAlphaSet, newBetaSet, haplotypeA, haplotypeB):
        distAndCovA = [[None, None, i] for i in range (len (self.M) )]
        distAndCovB = [[None, None, i] for i in range (len (self.M) )]
        for i in range(len (self.M)) :
            distAndCovA [i][0], distAndCovA [i][1] =  self.getHDistAndCov ( haplotypeA, self.M[i])
            distAndCovB [i][0], distAndCovB [i][1] =  self.getHDistAndCov ( haplotypeB, self.M[i])      
            distAndCovA.sort (self.__compFn)
        distAndCovB.sort (self.__compFn)
        return distAndCovA, distAndCovB
