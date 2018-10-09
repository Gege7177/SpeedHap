
class bioStats:
    def __init__ (self, matrix):
        self.M = matrix

        
    def __collectStatsHalfMarix (self, rows):
        d = {}
        length = len (self.M[0])  # Length of the haplotype
        for row in rows:
            for j in range (1, length - 1):  # Tutte le triplette di centro j e raggio 1
                t = self.M[row][j - 1] + self.M[row][j] + self.M[row][j + 1]
                if self.M[row][j - 1] != "-" and self.M[row][j] != "-" \
                   and self.M[row][j + 1] != "-":
                    if d.has_key (t):
                        d[t] += 1
                    else:
                        d[t] = 1
        return d

    def __lettersInStatus (self, status):
        alphabet = ["a","c","g","t"]
        m = max (status)
        letter = []
        for i in range (len (alphabet)):
            if status[i] == m:
                letter.append (alphabet[i])
        return letter
        

    def __getQueries (self, string, stats, side, status=None):
        if status is not None:
            letter = self.__lettersInStatus (status)
        else:
            letter = ["a","c","g","t"]
        query = []
        if side == "left":
            for i in range (len (letter)):
                if len (string) == 3:  
                    query.append ([letter[i] + string[1:], letter[i]])
                else: # len (string) == 4:
                    query.append ([letter[i] + string[2:], letter[i]])
                    query.append ([string[0] + letter[i] + string[2], letter[i]])

        if side == "right":
            for i in range (len (letter)):
                query.append ([string[:2] + letter[i], letter[i]])
                if len (string) == 4:  
                    query.append ([string[1] + letter[i] + string[3], letter[i]])
                    
        if side == "center":
            for i in range (len (letter)):
                if len (string) == 3:
                    query.append ([string[0] + letter[i] + string[2], letter[i]])
                else:
                    query.append ([letter[i] + string[3:], letter[i]])
                    query.append ([string[:2] + letter[i], letter[i]])
                    query.append ([string[1] + letter[i] + string[3], letter[i]])
        return query
    
    def __charQuery (self, string, stats, side, status=None):
        score = []
        query = self.__getQueries (string, stats, side, status)
        for q in query:
            if stats.has_key (q[0]):
                score.append ([stats[q[0]], q[1]])
        if len (score) == 0:  # No statistics found
            if status is not None:
                m = max (status)
                if status[0] == m:
                    return "a"
                if status[1] == m:
                    return "c"
                if status[2] == m:
                    return "g"
                if status[3] == m:
                    return "t"
            else:
                return "-"  # No idea return a gap
        score.sort ()
        score.reverse ()
        return score[0][1]


    def __consensusMatrix (self, rows, length):
        candidate = [[0,0,0,0] for i in range (length)]
        for j in range (length):
            for row in rows:  # Is the index of the row of self.M
                if self.M[row][j] == "a":
                    candidate[j][0] += 1
                elif  self.M[row][j] == "c":
                    candidate[j][1] += 1
                elif  self.M[row][j] == "g":
                    candidate[j][2] += 1
                elif  self.M[row][j] == "t":
                    candidate[j][3] += 1
        return candidate
    
    def outputHaplotypeStatistical (self, rows):
        stats = self.__collectStatsHalfMarix (rows)
        # La versione che usa la statistica per ricostruire un haplotype for TCBB
        length = len (self.M[0])  # Length of the haplotype
        haplotype = ""
        candidate = self.__consensusMatrix (rows, length)


        for j in range (length):
            candCol = [[candidate[j][0], "a"], [candidate[j][1], "c"], [candidate[j][2], "g"], \
                       [candidate[j][3], "t"]]
            candCol.sort ()
            candCol.reverse ()
            if candCol[0][0] == 0:
                character = "-"
                # If unsure of the character return -
            elif candCol[0][0] == candCol[1][0]:
                character = "*"
            else:
                character = candCol[0][1]
                # Verify if there is a conflict
            haplotype += character

        # Adjust haplotype conflicts
        for j in range (length):
            if haplotype[j] == "*":
                if j == 0:
                    c = self.__charQuery (haplotype[0:3], stats, "left", candidate[j])
                elif j == length - 1:
                    c = self.__charQuery (haplotype[-3:], stats, "right", candidate[j])
                else:
                    c = self.__charQuery (haplotype[j-1:j+2], stats, "center", candidate[j])
                haplotype = haplotype[:j] + c + haplotype[j+1:]
        return haplotype


    def outputHaplotypeStatistical2 (self, rows):
        stats = self.__collectStatsHalfMarix (rows)
        # La versione che usa la statistica per ricostruire un haplotype for TCBB
        length = len (self.M[0])  # Length of the haplotype
        haplotype = ""
        candidate = self.__consensusMatrix (rows, length)

        
        for j in range (length):
            candCol = [[candidate[j][0], "a"], [candidate[j][1], "c"], [candidate[j][2], "g"], \
                       [candidate[j][3], "t"]]
            candCol.sort ()
            candCol.reverse ()
            if candCol[0][0] == 0:
                character = "-"
                # If unsure of the character return -
            elif candCol[0][0] == candCol[1][0]:
                character = "*"
            else:
                character = candCol[0][1]
                # Verify if there is a conflict
            haplotype += character
        # Adjust haplotype conflicts
        for j in range (length):
            if haplotype[j] == "*":
                if j == 0:  # the first character of the string
                    c = self.__charQuery (haplotype[0:3], stats, "left", candidate[j])
                elif j == 1: # the second character of the string
                    c = self.__charQuery (haplotype[0:4], stats, "left", candidate[j])
                elif j == length - 1: # the last character of the string
                    c = self.__charQuery (haplotype[-3:], stats, "right", candidate[j])
                elif j == length - 2: # the next to last character of the string
                    c = self.__charQuery (haplotype[-4:], stats, "right", candidate[j])
                else:  # an intermediate character
                    c = self.__charQuery (haplotype[j-2:j+3], stats, "center", candidate[j])
                haplotype = haplotype[:j] + c + haplotype[j+1:]
        return haplotype
