# CLASS GROUP

import sys

class group:
    """ il gruppo e' un vettore di insiemi.
    Un insieme appartenente al gruppo Gi contiene tutti gli indici delle righe che,
    in colonna i, presentano lo stesso carattere"""

    def __init__ (self, p1, p2=None):
        if p2 == None:
           self.__buildByMatrics (p1)
        else:
           self.__buildBySets (p1, p2)

    def cleanSetOriginal (self, coverage, threshold=0):
        errors = set ()
        while len (self.sets) > 2:
            # Remove sets with min (length) elements
            i = 0
            while i < len (self.sets):
                if len (self.sets[i]) == m:
                    errors.update (self.sets[i])
                    del self.sets[i]
                else:
                    i += 1
        # Can be len (self.sets) = 1 or 0
        if len (self.sets) == 2:
            if len (self.sets[0]) < len (self.sets[1]):
                min_index = 0
                max_index = 1
            else:
                min_index = 1
                max_index = 0
            if float (len (self.sets[min_index])) / \
                   float (len (self.sets[max_index])) < threshold:
                errors.update (self.sets[min_index])
                self.sets[max_index].update (self.sets[min_index])  # Update set
                del self.sets[min_index]
        # Remove sets with just an element
        i = 0
        while i < len (self.sets):
            if len (self.sets[i]) == 1:
                errors.update (self.sets[i])
                del self.sets[i]
            else:
                i += 1

        # XXX - Ricalcola prop che non si dovrebbe usare piu
        if len(self.sets) == 1:
            self.prop = 1 # value 0 =indefinite, 1 = correct, 2 = incorrect, 3 = dubt
        elif len(self.sets) > 2:
            self.prop = 2
        return errors

        
    def cleanSet (self, coverage, threshold=0):
        errors = set ()
        while len (self.sets) > 2:
            length = [len (s) for s in self.sets]
            #print length
            m = min (length)
            t = 0
            for i in range (len (length)):
                if length[i] == m:
                    t += 1
            #if len (length) - t == 1:
            #    break
            # Remove sets with min (length) elements
            i = 0
            while i < len (self.sets):
                if len (self.sets[i]) == m:
                    errors.update (self.sets[i])
                    del self.sets[i]
                else:
                    i += 1

            #print  [len (s) for s in self.sets]
            #print

        # Can be len (self.sets) = 1 or 0
        if len (self.sets) == 2:
            if len (self.sets[0]) < len (self.sets[1]):
                min_index = 0
                max_index = 1
            else:
                min_index = 1
                max_index = 0
            if float (len (self.sets[min_index])) / \
                   float (len (self.sets[max_index])) < threshold:# or \
                   #len (self.sets[min_index]) == 1:  # XXX - Can not happen if coverage is 2 l
                errors.update (self.sets[min_index])
                self.sets[max_index].update (self.sets[min_index])  # Update set
                del self.sets[min_index]
        # Remove sets with just an element
        #if coverage > 2 or len (self.sets) == 2:
        i = 0
        while i < len (self.sets):
            if len (self.sets[i]) == 1:
                errors.update (self.sets[i])
                del self.sets[i]
            else:
                i += 1

        # XXX - Ricalcola prop che non si dovrebbe usare piu
        if len(self.sets) == 1:
            self.prop = 1 # value 0 =indefinite, 1 = correct, 2 = incorrect, 3 = dubt
        elif len(self.sets) > 2:
            self.prop = 2
        return errors

    def cleanSetTryCorrect (self, coverage, threshold=0):
        errors = set ()
        toBeCorrected = set ()
        charToSet = "-"
        while len (self.sets) > 2:
            length = [len (s) for s in self.sets]
            print length
            m = min (length)
            t = 0
            for i in range (len (length)):
                if length[i] == m:
                    t += 1
            if len (length) - t == 1:
                break
            # Remove sets with min (length) elements
            i = 0
            while i < len (self.sets):
                if len (self.sets[i]) == m:
                    errors.update (self.sets[i])
                    del self.sets[i]
                else:
                    i += 1

            print  [len (s) for s in self.sets]
            print

        # Can be len (self.sets) = 1 or 0
        if len (self.sets) == 2:
            if len (self.sets[0]) < len (self.sets[1]):
                min_index = 0
                max_index = 1
            else:
                min_index = 1
                max_index = 0
            if float (len (self.sets[min_index])) / \
                   float (len (self.sets[max_index])) < threshold or \
                   len (self.sets[min_index]) == 1:  # XXX - Can not happen if coverage is 2 l
                toBeCorrected.update (self.sets[min_index])
                #errors.update (self.sets[min_index])
                for x in self.sets[max_index]:
                    charToSet = x
                    break
                self.sets[max_index].update (self.sets[min_index])  # Update set
                del self.sets[min_index]
        # Remove sets with just an element
        if coverage > 2 or len (self.sets) == 2:
            i = 0
            while i < len (self.sets):
                if len (self.sets[i]) == 1:
                    errors.update (self.sets[i])
                    del self.sets[i]
                else:
                    i += 1

        # XXX - Ricalcola prop che non si dovrebbe usare piu
        if len(self.sets) == 1:
            self.prop = 1 # value 0 =indefinite, 1 = correct, 2 = incorrect, 3 = dubt
        elif len(self.sets) > 2:
            self.prop = 2
        return errors, toBeCorrected, charToSet
        
    def  __buildByMatrics (self,cValue):
        self.sets = [set() for i in ["a","c","g","t"]]
        self.alpha = None
        self.beta = None
        self.prop = 0 # value 0 =indefinite, 1 = correct, 2 = incorrect, 3 = dubt
        self.labeled = False  # Value false = to label, True = labeled
        self.totCollision = 0
        self.weightCollision = 0
        self.ProbErrRows = set ()
        for i in range(len(cValue)):
            if 'a' == cValue[i]:
                self.sets[0].add(i)
            elif 'c' == cValue[i]:
                self.sets[1].add(i)
            elif 'g' == cValue[i]:
                self.sets[2].add(i)
            elif 't' ==cValue[i]:
                self.sets[3].add(i)
        i = 0
        while i < len (self.sets):
            if len (self.sets[i]) == 0:
                del self.sets[i]
            else:
                i += 1
        if len(self.sets) == 1:
            self.prop = 1 # value 0 =indefinite, 1 = correct, 2 = incorrect, 3 = dubt
        elif len(self.sets)> 2:
            self.prop = 2

    def  __buildBySets (self, setA, setB):
        self.sets = [setA, setB]
        self.alpha = 0
        self.beta = 1
        self.prop = 2 # value 0 =indefinite, 1 = correct, 2 = incorrect, 3 = dubt
        self.labeled = True # Value false = to label, True = labeled
        self.totCollision = 0
        self.weightCollision = 0
        self.ProbErrRows = set ()



    def getSetsSize (self):
        return len (self.sets)

    def getSets (self):
        return self.sets

    def getComparMatrix (self, othGroup):
        """ effettua il confronto tra due gruppi
        il risultato del confronto lo usa
        per costruire la matrice dei confronti tra i due gruppi(mcompares(i,j))
        """
        if len (self.sets) != 2 or othGroup.getSetsSize () != 2:
            return None
        m = [[0 for i in range (2)] for j in range (2)]
        for i in range(2):
            for j in range(2):                          
                m[i][j]= len (self.sets[i] & othGroup.sets[j])
        # Look if we have a collision between the two groups
        # XXX - Probably useless
        if  m[0][0] + m[1][1] != 0  and  m[0][1] + m[1][0] != 0:
            othRows = (othGroup.sets[0] | othGroup.sets[1])
            me = (self.sets[0] | self.sets[1])
            self.ProbErrRows = self.ProbErrRows | (me & othRows)
            othGroup.ProbErrRows = othGroup.ProbErrRows | (me & othRows)
            self.totCollision += 1
            othGroup.totCollision += 1
            self.weightCollision += min (m[0][0] + m[1][1], m[0][1] + m[1][0])
            othGroup.weightCollision += min (m[0][0] + m[1][1], m[0][1] + m[1][0])
        return m

        
    def labelingGroup2 (self, m, othGroup):
        if  m[0][0] + m[1][1] != 0:
            self.alpha = othGroup.alpha
            self.beta = othGroup.beta
        else:
            self.alpha =othGroup.beta
            self.beta = othGroup.alpha
        self.labeled = True
        return self.sets[self.alpha], self.sets[self.beta]
    

    def markGroup (self, m, othGroup):
        """ cerca la presenza di eventuali errori nel gruppo.
        Data la matrice di confronto tra il Supergruppo e uno dei gruppi non etichettati
        Vi e' errore se: i valori della diagonale principale sono molto piu'
        grandi di quelli della diagonale secondaria (o viceversa),
        in tal caso rimuovo le righe dal gruppo sbagliato e le inserisco in quello corretto,
        indicando gli indici dei caratteri da usare per correggere l'input"""
        
        rowsA = set()
        rowsB = set()
        if (m[0][0] > m[0][1] + m[1][0]    and     m[1][1] > m[0][1] + m[1][0]) :
            rowsA = othGroup.sets[0] & self.sets[1]
            rowsB = othGroup.sets[1] & self.sets[0]
        if (m[0][1] > m[0][0] + m[1][1]    and     m[1][0] > m[0][0] + m[1][1]) :
            rowsB = othGroup.sets[0] & self.sets[0]
            rowsA = othGroup.sets[1] & self.sets[1]
        self.sets[0] -= rowsB
        self.sets[1] -= rowsA
        for indB in self.sets[0]:
            break
        for indA in self.sets[1]:
            break
        #othGroup.sets[0] -= rowsB
        #othGroup.sets[0] = othGroup.sets[0] | rowsA
        #othGroup.sets[1] -= rowsA
        #othGroup.sets[1] = othGroup.sets[1] | rowsB

        self.sets[0] = self.sets[0] | rowsA
        self.sets[1] =  self.sets[1] | rowsB
        return rowsA, rowsB, indA, indB


    def detectErrorInGroupWeak (self, m, othGroup):
        rowsA = set()
        rowsB = set()
        #Nota nella matrice l'indice di riga corrisponde a other, quello di colonna a self 
        if m[0][0] + m[1][1] > m[0][1] + m[1][0] :
            rowsA = othGroup.sets[0] & self.sets[1]
            rowsB = othGroup.sets[1] & self.sets[0]
            self.sets[0] -= rowsB
            self.sets[1] -= rowsA
        if m[0][0] + m[1][1] < m[0][1] + m[1][0] :
            rowsA = othGroup.sets[0] & self.sets[0]
            rowsB = othGroup.sets[1] & self.sets[1]
            self.sets[0] -= rowsA
            self.sets[1] -= rowsB
        if m[0][0] + m[1][1] == m[0][1] + m[1][0] :
            return False
        return True
        
    def detectErrorInGroup (self, m, othGroup):
        """ cerca la presenza di eventuali errori nel gruppo.
        Data la matrice di confronto tra il Supergruppo e uno dei gruppi non etichettati
        Vi e' errore se: i valori della diagonale principale sono molto piu'
        grandi di quelli della diagonale secondaria (o viceversa),
        in tal caso rimuovo le righe dal gruppo sbagliato e le inserisco in quello corretto,
        indicando gli indici dei caratteri da usare per correggere l'input"""
        
        rowsA = set()
        rowsB = set()
        #Nota nella matrice l'indice di riga corrisponde a other, quello di colonna a self 
        if (m[0][0] > m[0][1] + m[1][0]    and     m[1][1] > m[0][1] + m[1][0]) :
            rowsA = othGroup.sets[0] & self.sets[1]
            rowsB = othGroup.sets[1] & self.sets[0]
            self.sets[0] -= rowsB
            self.sets[1] -= rowsA
        if (m[0][1] > m[0][0] + m[1][1]    and     m[1][0] > m[0][0] + m[1][1]) :
            rowsA = othGroup.sets[0] & self.sets[0]
            rowsB = othGroup.sets[1] & self.sets[1]
            self.sets[0] -= rowsA
            self.sets[1] -= rowsB
        return rowsA, rowsB


    def labelingGroup (self, m, othGroup, weak = True):
        """etichetto il gruppo (self) confrontandolo con un altro gia' etichettato""" 
        if othGroup.labeled: #la condizione e' sempre vera per costruzione
            if (m[0][0]+m[1][1] != 0 and m[0][1]+m[1][0] == 0) and ( weak or (m[0][0] != 0 and m[1][1] != 0) ):
                """la prima parte della condizione corrisponde ad un or escusivo: 
                solo una delle due diagonali della matrice puo essere nulla
                la seconda  serve per verificare una condizione piu stretta,
                che entrambi i membri della diagonale siano diversi da zero,
                questa seconda condizione e verificata solo se il parametro
                passato indica di usare una condizione piu forte"""
                self.alpha = othGroup.alpha
                self.beta = othGroup.beta
            if m[0][0]+m[1][1] == 0 and m[0][1]+m[1][0] != 0 and ( weak or (m[0][1] != 0 and m[1][0] != 0 )):
                self.alpha = othGroup.beta
                self.beta = othGroup.alpha
                
            if ( self.alpha!= None and self.beta!= None):
                self.labeled = True
                return self.sets[self.alpha], self.sets[self.beta]
            else:
                return set(), set()
        else:
            print "Initialization error"
            sys.exit ()




    def getRapporto (self):
        """ calcola il rapporto tra la lunghezza degli insiemi di un gruppo con 2 insiemi (set)
        il valore del rapporto e sempre <1"""
        if self.getSetsSize () != 2:
            return None
        if self.getSetsSize () == 2:
            minval = min (len (self.sets[0]), len (self.sets[1]))
            maxval = max (len (self.sets[0]), len (self.sets[1]))
            return  float (minval) / float (maxval)
  


    
