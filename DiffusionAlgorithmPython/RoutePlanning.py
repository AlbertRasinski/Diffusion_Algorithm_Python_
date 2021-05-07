import numpy as np

class RoutePlanning:
    """
    Klasa imlementująca algorytm dyfuzyjny służacy do znajdowania drogi do celu

    ...

    Attributes
    ----------
    __basicMap : np.array([])
        mapa zawierająca informację o położeniu robota, celu oraz przeszkód
    __waveMap : np.array([])
        mapa zawierająca informację o położeniu robota, celu, przeszkód oraz mocy fali
    __robotX : int
        położenie x robota
    __robotY : int
        położenie y robota
    __goalX : int
        położenie x celu podróży
    __goalY : int
        położenie y celu robota
    __maxPower : int
        wartość maksymalna mocy fali
    __route : []


    Methods
    -------
    __findPlaceInMap(valueToFind)
        znajduje położenie danego pola na mapie
    __findMaxPower()
        znajduje maksymalną moc fali
    __waveDiffusion()
        fala jest dyfuzjowana aż do momentu, gdy możliwe jest wyznaczenie drogi pomiędzy robotem, a celem lub gdy nie można dalej rozszerzać fali
    __findRoute()
        znajduje drogę pomiędzy robotem, a celem
    loadMapFromFile(path)
        wczytuje mapę z oodanego pliku
    getMapSize()
        zwraca rozmiar mapy
    getValueOfMap(i,j)
        zwraca wartość pola o podanym położeniu
    getMaxPower()
        zwraca maksymalną wartość mocy fali
    getRoute()
        zwraca tor ruchu wyznaczonej drogi pomiędzy robotem, a celem
    """

    def __init__(self):
        self.__basicMap = np.array([])
        self.__waveMap = np.array([])
        self.__robotX = 0
        self.__robotY = 0
        self.__goalX = 0
        self.__goalY = 0
        self.__maxPower = 0
        self.__route = []

    def __findPlaceInMap(self, valueToFind):
        """Zwraca położenie pola, dla podanej wartości pola

        Parameters
        ----------
        valueToFind : int
            Wartość, której położenie jest poszukiwane

        Returns
        -------
        int
            położenie x pola
        int
            położenie y pola
        """
        for i in range(len(self.__basicMap)):
            for j in range(len(self.__basicMap[i])):
                if (self.__basicMap[i][j] == valueToFind):
                    return i, j

    def __findMaxPower(self):
        """Zwraca maksyamalną moc fali

        Returns
        -------
        int
            moc maksymalna fali
        """
        max = 0
        for i in self.__basicMap:
            max += len(i)
        self.__basicMap[self.__goalX][self.__goalY] = max
        return max

    def __waveDiffusion(self):
        """fala jest dyfuzjowana aż do momentu, gdy możliwe jest wyznaczenie drogi pomiędzy robotem, a celem lub gdy nie można dalej rozszerzać fali

        Returns
        -------
        numpy.array
            nowa mapa
        """
        newList = [x[:] for x in self.__basicMap]
        listOfLatestWave = []
        listOfLatestWave.append((self.__goalX, self.__goalY))
        powerOfWave = self.__maxPower - 1
        while True:
            if len(listOfLatestWave) == 0:
                break
            newTmpWave = []
            for i in listOfLatestWave:
                if i[0] - 1 >= 0 and i[1] - 1 >= 0 and newList[i[0] - 1][i[1]] != 0 and newList[i[0]][i[1] - 1] != 0 and newList[i[0] - 1][i[1] - 1] is None:
                    newList[i[0] - 1][i[1] - 1] = powerOfWave
                    newTmpWave.append((i[0] - 1, i[1] - 1))
                if i[0] - 1 >= 0 and newList[i[0] - 1][i[1]] is None:
                    newList[i[0] - 1][i[1]] = powerOfWave
                    newTmpWave.append((i[0] - 1, i[1]))
                if (i[0] - 1 >= 0 and i[1] + 1 < len(newList[i[0] - 1]) and newList[i[0] - 1][i[1]] != 0 and newList[i[0]][i[1] + 1] != 0 and newList[i[0] - 1][i[1] + 1] is None):
                    newList[i[0] - 1][i[1] + 1] = powerOfWave
                    newTmpWave.append((i[0] - 1, i[1] + 1))
                if i[0] >= 0 and i[1] - 1 >= 0 and newList[i[0]][i[1] - 1] is None:
                    newList[i[0]][i[1] - 1] = powerOfWave
                    newTmpWave.append((i[0], i[1] - 1))
                if i[0] >= 0 and i[1] + 1 < len(newList[i[0] - 1]) and newList[i[0]][i[1] + 1] is None:
                    newList[i[0]][i[1] + 1] = powerOfWave
                    newTmpWave.append((i[0], i[1] + 1))
                if (i[0] + 1 < len(newList) and i[1] - 1 >= 0 and newList[i[0] + 1][i[1]] != 0 and newList[i[0]][i[1] - 1] != 0 and newList[i[0] + 1][i[1] - 1] is None):
                    newList[i[0] + 1][i[1] - 1] = powerOfWave
                    newTmpWave.append((i[0] + 1, i[1] - 1))
                if i[0] + 1 < len(newList) and i[1] >= 0 and newList[i[0] + 1][i[1]] is None:
                    newList[i[0] + 1][i[1]] = powerOfWave
                    newTmpWave.append((i[0] + 1, i[1]))
                if (i[0] + 1 < len(newList) and i[1] + 1 < len(newList[i[0] + 1]) and newList[i[0] + 1][i[1]] != 0 and newList[i[0]][i[1] + 1] != 0 and newList[i[0] + 1][i[1] + 1] is None):
                    newList[i[0] + 1][i[1] + 1] = powerOfWave
                    newTmpWave.append((i[0] + 1, i[1] + 1))

                listOfLatestWave = [x[:] for x in newTmpWave]

            if (self.__robotX - 1 >= 0 and self.__robotY - 1 >= 0 and newList[self.__robotX - 1][self.__robotY - 1] != 0 and newList[self.__robotX - 1][self.__robotY - 1] is not None):
                break
            if (self.__robotX - 1 >= 0 and newList[self.__robotX - 1][self.__robotY] is not None and newList[self.__robotX - 1][self.__robotY] != 0):
                break
            if (self.__robotX - 1 >= 0 and self.__robotY + 1 < len(newList[self.__robotX - 1]) and newList[self.__robotX - 1][self.__robotY + 1] is not None and newList[self.__robotX - 1][self.__robotY + 1] != 0):
                break
            if (self.__robotX >= 0 and self.__robotY - 1 >= 0 and newList[self.__robotX][self.__robotY - 1] is not None and newList[self.__robotX][self.__robotY - 1] != 0):
                break
            if (self.__robotX >= 0 and self.__robotY + 1 < len(newList[self.__robotX - 1]) and newList[self.__robotX][self.__robotY + 1] is not None and newList[self.__robotX][self.__robotY + 1] != 0):
                break
            if (self.__robotX + 1 < len(newList) and self.__robotY - 1 >= 0 and newList[self.__robotX + 1][self.__robotY - 1] is not None and newList[self.__robotX + 1][self.__robotY - 1] != 0):
                break
            if (self.__robotX + 1 < len(newList) and self.__robotY >= 0 and newList[self.__robotX + 1][self.__robotY] is not None and newList[self.__robotX + 1][self.__robotY] != 0):
                break
            if (self.__robotX + 1 < len(newList) and self.__robotY + 1 < len(newList[self.__robotX + 1]) and newList[self.__robotX + 1][self.__robotY + 1] is not None and newList[self.__robotX + 1][self.__robotY + 1] != 0):
                break

            powerOfWave -= 1
        return np.array(newList)

    def __findRoute(self):
        """znajduje drogę pomiędzy robotem, a celem

        Parameters
        ----------
        valueToFind : int
            Wartość, której położenie jest poszukiwane

        Returns
        -------
        list
            wyznaczona ścieżka
        """
        listOfPositionRoute = []
        positionX = self.__robotX
        positionY = self.__robotY
        currentPower = 0

        listOfPositionRoute.append((self.__robotX, self.__robotY))

        while True:
            if (self.__waveMap[positionX][positionY] == self.__maxPower):
                return listOfPositionRoute
            elif (positionX - 1 >= 0 and self.__waveMap[positionX - 1][positionY] is not None and self.__waveMap[positionX - 1][positionY] > currentPower):
                positionX -= 1
            elif (positionX + 1 < len(self.__waveMap) and self.__waveMap[positionX + 1][positionY] is not None and self.__waveMap[positionX + 1][positionY] > currentPower):
                positionX += 1
            elif (positionY - 1 >= 0 and self.__waveMap[positionX][positionY - 1] is not None and self.__waveMap[positionX][positionY - 1] > currentPower):
                positionY -= 1
            elif (positionY + 1 < len(self.__waveMap[positionX]) and self.__waveMap[positionX][positionY + 1] is not None and self.__waveMap[positionX][positionY + 1] > currentPower):
                positionY += 1
            elif (positionX - 1 >= 0 and positionY - 1 >= 0 and self.__waveMap[positionX - 1][positionY - 1] is not None and self.__waveMap[positionX - 1][positionY - 1] > currentPower):
                positionX -= 1
                positionY -= 1
            elif (positionX - 1 >= 0 and positionY + 1 < len(self.__waveMap[positionX]) and self.__waveMap[positionX - 1][positionY + 1] is not None and self.__waveMap[positionX - 1][positionY + 1] > currentPower):
                positionX -= 1
                positionY += 1
            elif (positionX + 1 < len(self.__waveMap) and positionY - 1 >= 0 and self.__waveMap[positionX + 1][positionY - 1] is not None and self.__waveMap[positionX + 1][positionY - 1] > currentPower):
                positionX += 1
                positionY -= 1
            elif (positionX + 1 < len(self.__waveMap) and positionY + 1 < len(self.__waveMap[positionX]) and self.__waveMap[positionX + 1][positionY + 1] is not None and self.__waveMap[positionX + 1][positionY + 1] > currentPower):
                positionX += 1
                positionY += 1
            else:
                break

            listOfPositionRoute.append((positionX, positionY))
            currentPower = self.__waveMap[positionX][positionY]



    def loadMapFromFile(self, path):
        """znajduje drogę pomiędzy robotem, a celem

        Returns
        -------
        Exception
            zwraca błąd gdy wystąpi lub None gdy nie
        """
        fileStream = open(path)
        toNpArray = []
        counterLine = 0

        try:
            robotInMap = False
            goalInMap = False

            for line in fileStream:
                toNpArray.append(line.split())
                for i in range(len(toNpArray[counterLine])):
                    if toNpArray[counterLine][i] == "None":
                        toNpArray[counterLine][i] = None
                    elif toNpArray[counterLine][i] == "0":
                        toNpArray[counterLine][i] = 0
                    elif toNpArray[counterLine][i] == "-2":
                        if (goalInMap):
                            raise Exception("Mapa posiada więcej niż jeden cel")
                        goalInMap = True
                        toNpArray[counterLine][i] = -2
                    elif toNpArray[counterLine][i] == "-1":
                        if (robotInMap):
                            raise Exception("Mapa posiada więcej niż jednego robota")
                        robotInMap = True
                        toNpArray[counterLine][i] = -1
                    else:
                        raise Exception("Plik posiada błędne dane")
                if 'str' in line:
                    break;
                counterLine += 1

            if (not goalInMap):
                raise Exception("Nie ma celu w mapie")
            if (not robotInMap):
                raise Exception("Nie ma robota w mapie")

            for i in range(len(toNpArray) - 1):
                if (len(toNpArray[i]) != len(toNpArray[i + 1])):
                    raise Exception("Plik nie posiada prostokątnej mapy")

            self.__basicMap = np.array(toNpArray)
            self.__robotX, self.__robotY = self.__findPlaceInMap(-1)
            self.__goalX, self.__goalY = self.__findPlaceInMap(-2)
            self.__maxPower = self.__findMaxPower()
            self.__waveMap = self.__waveDiffusion()
            self.__route = self.__findRoute()
            return None
        except Exception as e:
            return e

    def getMapSize(self):
        """zwraca rozmiar mapy

        Returns
        -------
        (int, int)
            rozmiar mapy
        """
        return self.__basicMap.shape

    def getValueOfMap(self, i, j):
        """zwraca wartość pola dla podanych współrzędnych

        Parameters
        ----------
        i : int
            położenie pierwszej współrzędnej
        j : int
            położenie drugiej współrzędnej

        Returns
        -------
        int
            wartość pola mapy
        """
        return self.__waveMap[i][j]

    def getMaxPower(self):
        """zwraca maksymalną moc fali

        Returns
        -------
        int
            maksymalna moc fali
        """
        return self.__maxPower

    def getRoute(self):
        """zwraca drogę, jaką ma się poruszać robot

        Returns
        -------
        list
            lista zawierająca kolejne kroki w trasie robota
        """
        return self.__route;