###

class candidates:
    def __init__ (self, mCompares, conflictCols, covrg, meanFragSize):
        self.mCompares = mCompares
        # len (mCompares) is also the number of column of M aka the number of groups
        self.totGroups = len (mCompares)
        self.candidates = self.__getCandidate (mCompares, conflictCols, covrg, meanFragSize)


    def __get_threshold (self, mCompares, conflictCols, covrg, meanFragSize):
        mean = [0,0,0]
        mean[0] = self.__get_threshold_oring_lore (mCompares, conflictCols, covrg, meanFragSize)
        mean[1] = self.__get_threshold_hi_cvrg (mCompares, conflictCols, covrg, meanFragSize)
        mean[2] = self.__get_threshold_exp  (mCompares, conflictCols, covrg, meanFragSize)
        return mean[0] 
        
    def __get_threshold_oring_lore (self, mCompares, conflictCols, covrg, meanFragSize):
        mean = 0.0
        tot = len (conflictCols)
        for c in conflictCols:
            mean += c
        if tot == 0 or mean == 0:
            mean = 1.1  # XXX - Fake number to make conflictCols[i] < mean true
        else:
            mean /= tot
        print "Loredana Used mean", mean, tot
        return mean

    def __get_threshold_hi_cvrg (self, mCompares, conflictCols, covrg, meanFragSize):
        mean = 0.0
        tot = len (conflictCols)
        for c in conflictCols:
            mean += c
            # XXX - Include in the mean also the columns with just one element
            if covrg < 5:
                if c == 0:
                    tot -= 1
        if tot == 0 or mean == 0:
            mean = 1.1  # XXX - Fake number to make conflictCols[i] < mean true
        else:
            mean /= tot
        print "Mean", mean, tot
        mean = min (meanFragSize / 2, mean)
        print "meanFragSize used mean", mean
        return mean
    
    def __get_threshold_exp (self, mCompares, conflictCols, covrg, meanFragSize):
        mean = 0.0
        tot = len (conflictCols)
        for c in conflictCols:
            mean += c
            # XXX - Include in the mean also the columns with just one element
            if c == 0:
                tot -= 1
        if tot == 0 or mean == 0:
            mean = 1.1  # XXX - Fake number to make conflictCols[i] < mean true
        else:
            mean /= tot
        var = 0.0
        for c in conflictCols:
            if c != 0:
                var += (c - mean)**2
        if tot == 0:
            var = 0
        else:
            var /= tot
            var = var**.5
        print "Media", mean, "Varianza", var
        if mean - var <= 1:
            return 1.1
        return mean - var

    def __getCandidate (self, mCompares, conflictCols, covrg, meanFragSize, thresVal=None):
        if thresVal is None:
            mean = self.__get_threshold (mCompares, conflictCols, covrg, meanFragSize)
        else:
            mean = thresVal
        for i in range (len (conflictCols)):
            if conflictCols[i] < mean:
                conflictCols[i] = True
            else:
                conflictCols[i] = False
        # Build the candidate list
        candidate = []
        for i in range (len (mCompares)):
            for j in range(i):
                m =  mCompares [i][j]
                if m is not None:
                    #if (m[0][0]+m[1][1] != 0 or m[0][1]+m[1][0] != 0):
                    if (m[0][0]+m[1][1] != 0 and m[0][1]+m[1][0] == 0) or \
                       (m[0][0]+m[1][1] == 0 and m[0][1]+m[1][0] != 0):
                        # Only a full diagonal matrix for candidates
                        if m[0][0] + m[0][1] == 0 or m[1][0] + m[1][1] == 0:
                            continue
                        # The number of conflicts in both groups is under the mean
                        if conflictCols[i] == True and \
                           conflictCols[j] == True:
                            candidate.append( (i,j) )

        if len (candidate) == 0:
            return self.__getCandidate (mCompares, conflictCols, covrg, meanFragSize, mean + 1)
        return candidate

    def __getCandidate2 (self, mCompares):
        candidate = []
        candWMismatch = []
        for i in range(len (mCompares)):
            for j in range(i):
                m =  mCompares [i][j]
                if m is not None:
                    if (m[0][0]+m[1][1] != 0 and m[0][1]+m[1][0] != 0):
                        candWMismatch.append( (i,j) )
                    elif (m[0][0]+m[1][1] != 0 or m[0][1]+m[1][0] != 0):
                        candidate.append( (i,j) )
        #candidate.extend(candWMismatch)
        #print "candidati =", candidate
        return candidate


       
    def __compCand (self, a, b):
        """ funzione adottata per il confronto tra candidati"""
        if a[0] - b[0] != 0:
            return a[0] - b[0]
        return a[1] - b[1]
 
    def __createV (self):
        """crea la struttura di appoggio per effettuare la visita dei candidati """
        self.candidates.sort (self.__compCand)
        V = [None for i in range (self.totGroups + 1)]
        V[self.totGroups] = len(self.candidates)
        for i in range (len (self.candidates)):
            # The first element of the couple in candidate vector
            j = self.candidates[i][0]
            if V[j] == None:
                V[j] = i
        for j in range (self.totGroups, 0, -1):
            if V[j-1] == None:
                V[j-1] = V[j]
        return V
      
    def sortCandidates (self):
        # Sort candidates and create a vector used for visit
        candidate_list = []
        V = self.__createV ()
        # Visited is False if never used, True if visitable, None is completely used 
        visited = [False for i in range (self.totGroups)]
        while not self.__isComplete ():
            visited, candidates = self. __sortCandidates (visited, V)
            candidate_list.append (candidates)
        maxval = len (candidate_list[0])
        maxind = 0
        for i in range (len (candidate_list)):
            print "Size of candidate set", len (candidate_list[i])
            if len (candidate_list[i]) > maxval:
                maxval = len (candidate_list[i])
                maxind = i
        return candidate_list[maxind]
     
    def __isComplete (self):
        for v in self.candidates:
            if v is not None:
                return False 
        return True
    
    def __sortCandidates (self, visited, V):
        """Ordina i candidati in modo che almeno un elemento della coppia sia gia' stato visitato
        cosi' da poter etichettare l'altro per confronto con quello gia' visitato """
        sortedCandidates = []
        otherToVisit = True  # Initialization
        i = 0
        while self.candidates[i] is None:
            i += 1
        startset = self.candidates[i][0] # the first element not none in the candidates list
        # Build the list of candidates
        while otherToVisit == True: # Other elements can be added to list
            visited[startset] = None
            for i in range (V[startset], V[startset + 1]):
                # If it is None we already added it
                if self.candidates[i] is None:
                    continue
                sortedCandidates.append (self.candidates[i])
                # If I can visit some other group of couple
                if visited[self.candidates[i][1]] == False:
                    visited[self.candidates[i][1]] = True
                self.candidates[i] = None  # Remove the couple, but do not shrink the vector
            # now try to add couple whose second element can be added
            for i in range (len (visited) - 1): # XXX - Not last element
                if visited[i] is not None:
                    for j in range (V[i], V[i + 1]):
                        if self.candidates[j] is not None:
                            # The couple can be inserted due the second element is visited
                            if visited[self.candidates[j][1]] != False:
                                sortedCandidates.append (self.candidates[j])
                                # Note that try to mark the first element of the couple
                                if visited[self.candidates[j][0]] == False:
                                    visited[self.candidates[j][0]] = True
                                # Remove the couple, but do not shrink the vector
                                self.candidates[j] = None  
            # Search the new elem among first elements
            otherToVisit = False 
            for i in range (len (visited)):
                if visited[i] == True:
                    startset = i
                    otherToVisit = True
                    break
        return visited, sortedCandidates
