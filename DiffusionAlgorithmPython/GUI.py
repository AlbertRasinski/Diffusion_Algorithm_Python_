import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox
from RoutePlanning import RoutePlanning


class GUI:
    """
    Klasa imlementująca interfejs graficzny aplikacji

    ...

    Attributes
    ----------
    __step : int
        określa krok wyznaczania drogi poprzez algorytm dyfuzyjny
    __rp : RoutePlanning
        obiekt do rozwiązywania algorytmu dyfuzyjnego
    __window : tkinter.Tk
        okno, w którym jest wysietlane GUI
    __font : tkinter.Font.font
        określa czcionkę
    __canvasMap : tk.Canvas
        płótno do rysowania mapy

    Methods
    -------
    __setWindow()
        ustawienie parametrów okienka
    __setButtonFile()
        ustawienie parametrów przycisku do wczytywania pliku
    __buttonChooseFileOnClick()
        zaimplementowanie funkcjonalności przycisku do wczytywania pliku
    __setButtonNext()
        ustawienie parametrów przycisku służacego do pokazania kolejnego kroku algorytmu dyfuzyjnego
    __buttonNextOnClick()
        zaimplementowanie funkcjonalności przycisku służacego do pokazania kolejnego kroku algorytmu dyfuzyjnego
    __setButtonPrev()
        ustawienie parametrów przycisku służacego do pokazania poprzedniego kroku algorytmu dyfuzyjnego
    __buttonPrevOnClick()
        zaimplementowanie funkcjonalności przycisku służacego do pokazania kolejnego kroku algorytmu dyfuzyjnego
    __setButtonStart()
        ustawienie parametrów przycisku służacego do pokazania pierwszego kroku algorytmu dyfuzyjnego
    __buttonStartOnClick()
        zaimplementowanie funkcjonalności przycisku służacego do pokazania pierwszego kroku algorytmu dyfuzyjnego
    __setButtonEnd()
        ustawienie parametrów przycisku służacego do pokazania ostatniego kroku algorytmu dyfuzyjnego
    __buttonEndOnClick()
        zaimplementowanie funkcjonalności przycisku służacego do pokazania ostatniego kroku algorytmu dyfuzyjnego
    __canvasUpdate()
        modyfikowanie rozmiaru płótna w zależności od wielkości mapy
    __drawMap()
        rysowanie mapy na płótnie
    """

    def __init__(self):
        self.__step = 0
        self.__rp = RoutePlanning()
        self.__window = tk.Tk()
        self.__font = tkFont.Font(family='Helvetica', size=16, weight='bold')
        self.__setWindow()
        self.__setButtonFile()
        self.__setButtonNext()
        self.__setButtonPrev()
        self.__setButtonStart()
        self.__setButtonEnd()
        self.__canvasMap = tk.Canvas(self.__window, height=700, width=700)
        self.__window.mainloop()

    def __setWindow(self):
        """ustawienie parametrów okienka
        """
        self.__window.title("Rasiński Albert - Python - algorytm dyfuzyjny")
        self.__window.wm_attributes("-transparentcolor", 'grey')
        self.__window.geometry("1280x720")
        self.__window.resizable(False, False)
        self.__img = tk.PhotoImage(file="bckgrnd.png")
        label = tk.Label(self.__window, image=self.__img)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def __setButtonFile(self):
        """ustawienie parametrów przycisku do wczytywania pliku
        """
        self.__buttonChooseFile = tk.Button(self.__window, text="WYBIERZ PLIK", font=self.__font,
                                            command=self.__buttonChooseFileOnClick, bg="#454545", fg="white")
        self.__buttonChooseFile.config(height=2, width=15)
        self.__buttonChooseFile.place(x=875, y=100)

    def __buttonChooseFileOnClick(self):
        """zaimplementowanie funkcjonalności przycisku do wczytywania pliku
        """
        self.__window.filename = filedialog.askopenfilename(title="WYBIERZ PLIK", filetypes=(
        ("pliki txt", "*.txt"), ("wszystkie pliki", "*.*")))
        check = self.__rp.loadMapFromFile(self.__window.filename)
        if check is None:
            self.__canvasUpdate()
            if self.__rp.getRoute() is not None:
                self.__step = self.__rp.getMaxPower() - 2 * len(self.__rp.getRoute()) + 3
            else:
                self.__step = self.__rp.getMaxPower()
                tk.messagebox.showwarning("Uwaga", "Brak możliwości wyznaczenia drogi")
            self.__drawMap(self.__step)
            self.__buttonNext['state'] = tk.NORMAL
            self.__buttonPrev['state'] = tk.NORMAL
            self.__buttonStart['state'] = tk.NORMAL
            self.__buttonEnd['state'] = tk.NORMAL
        else:
            tk.messagebox.showerror("Błąd", check)

    def __setButtonNext(self):
        """ustawienie parametrów przycisku służacego do pokazania kolejnego kroku algorytmu dyfuzyjnego
        """
        self.__buttonNext = tk.Button(self.__window, text="+1", font=self.__font, command=self.__buttonNextOnClick,
                                      bg="#454545", fg="white")
        self.__buttonNext.config(height=2, width=5)
        self.__buttonNext.place(x=980, y=200)
        self.__buttonNext['state'] = tk.DISABLED

    def __buttonNextOnClick(self):
        """zaimplementowanie funkcjonalności przycisku służacego do pokazania kolejnego kroku algorytmu dyfuzyjnego
        """
        self.__step -= 1
        self.__drawMap(self.__step)

    def __setButtonPrev(self):
        """ustawienie parametrów przycisku służacego do pokazania poprzedniego kroku algorytmu dyfuzyjnego
        """
        self.__buttonPrev = tk.Button(self.__window, text="-1", font=self.__font, command=self.__buttonPrevOnClick,
                                      bg="#454545", fg="white")
        self.__buttonPrev.config(height=2, width=5)
        self.__buttonPrev.place(x=895, y=200)
        self.__buttonPrev['state'] = tk.DISABLED

    def __buttonPrevOnClick(self):
        """zaimplementowanie funkcjonalności przycisku służacego do pokazania kolejnego kroku algorytmu dyfuzyjnego
        """
        self.__step += 1
        self.__drawMap(self.__step)

    def __setButtonStart(self):
        """ustawienie parametrów przycisku służacego do pokazania pierwszego kroku algorytmu dyfuzyjnego
        """
        self.__buttonStart = tk.Button(self.__window, text="START", font=self.__font, command=self.__buttonStartOnClick,
                                       bg="#454545", fg="white")
        self.__buttonStart.config(height=2, width=7)
        self.__buttonStart.place(x=780, y=200)
        self.__buttonStart['state'] = tk.DISABLED

    def __buttonStartOnClick(self):
        """zaimplementowanie funkcjonalności przycisku służacego do pokazania pierwszego kroku algorytmu dyfuzyjnego
        """
        self.__step = self.__rp.getMaxPower() + 1
        self.__drawMap(self.__step)

    def __setButtonEnd(self):
        """ustawienie parametrów przycisku służacego do pokazania ostatniego kroku algorytmu dyfuzyjnego
        """
        self.__buttonEnd = tk.Button(self.__window, text="KONIEC", font=self.__font, command=self.__buttonEndOnClick,
                                     bg="#454545", fg="white")
        self.__buttonEnd.config(height=2, width=7)
        self.__buttonEnd.place(x=1070, y=200)
        self.__buttonEnd['state'] = tk.DISABLED

    def __buttonEndOnClick(self):
        """zaimplementowanie funkcjonalności przycisku służacego do pokazania ostatniego kroku algorytmu dyfuzyjnego
        """
        self.__step = self.__rp.getMaxPower() - 2 * len(self.__rp.getRoute()) + 3
        self.__drawMap(self.__step)

    def __canvasUpdate(self):
        """modyfikowanie rozmiaru płótna w zależności od wielkości mapy
        """
        self.__canvasMap.delete("all")
        y, x = self.__rp.getMapSize()
        if y > x:
            self.__canvasMap.config(height=700, width=700 / y * x, background="white")
            self.__canvasMap.place(x=(720 - (700 / y * x)) / 2, y=10)
        else:
            self.__canvasMap.config(height=700 / x * y, width=700, background="white")
            self.__canvasMap.place(x=10, y=(720 - (700 / x * y)) / 2)

    def __drawMap(self, minValueToPrint):
        """rysowanie mapy na płótnie
        """
        self.__canvasMap.delete("all")
        y, x = self.__rp.getMapSize()
        max = self.__rp.getMaxPower()
        if y > x:
            sizeSquare = 700 / y
        else:
            sizeSquare = 700 / x
        sizeFont = int(sizeSquare / 3)

        for tmpY in range(y):
            for tmpX in range(x):
                value = self.__rp.getValueOfMap(tmpY, tmpX)
                if value is None:
                    self.__canvasMap.create_rectangle(sizeSquare * tmpX + 3, sizeSquare * tmpY + 3,
                                                      sizeSquare * tmpX + sizeSquare - 3,
                                                      sizeSquare * tmpY + sizeSquare - 3, fill="#b9b9b9", width=3)
                elif value == 0:
                    self.__canvasMap.create_rectangle(sizeSquare * tmpX + 3, sizeSquare * tmpY + 3,
                                                      sizeSquare * tmpX + sizeSquare - 3,
                                                      sizeSquare * tmpY + sizeSquare - 3, fill="#cf2828", width=3)
                elif value == -2 or value == max:
                    self.__canvasMap.create_rectangle(sizeSquare * tmpX + 3, sizeSquare * tmpY + 3,
                                                      sizeSquare * tmpX + sizeSquare - 3,
                                                      sizeSquare * tmpY + sizeSquare - 3, fill="#0756c9", width=3)
                    self.__canvasMap.create_text(sizeSquare * tmpX + sizeSquare / 2, sizeSquare * tmpY + sizeSquare / 2,
                                                 font=("Arial", sizeFont, "bold"), text="G")
                elif value == -1:
                    self.__canvasMap.create_rectangle(sizeSquare * tmpX + 3, sizeSquare * tmpY + 3,
                                                      sizeSquare * tmpX + sizeSquare - 3,
                                                      sizeSquare * tmpY + sizeSquare - 3, fill="#06c206", width=3)
                    self.__canvasMap.create_text(sizeSquare * tmpX + sizeSquare / 2, sizeSquare * tmpY + sizeSquare / 2,
                                                 font=("Arial", sizeFont, "bold"), text="R")
                elif value >= minValueToPrint:
                    self.__canvasMap.create_rectangle(sizeSquare * tmpX + 3, sizeSquare * tmpY + 3,
                                                      sizeSquare * tmpX + sizeSquare - 3,
                                                      sizeSquare * tmpY + sizeSquare - 3, fill="#e3e343", width=3)
                    self.__canvasMap.create_text(sizeSquare * tmpX + sizeSquare / 2, sizeSquare * tmpY + sizeSquare / 2,
                                                 font=("Arial", sizeFont, "bold"), text=str(value))
                else:
                    self.__canvasMap.create_rectangle(sizeSquare * tmpX + 3, sizeSquare * tmpY + 3,
                                                      sizeSquare * tmpX + sizeSquare - 3,
                                                      sizeSquare * tmpY + sizeSquare - 3, fill="#b9b9b9", width=3)

        route = self.__rp.getRoute()

        if self.__rp.getRoute() is not None:
            routeCounterToPrint = max - len(route) + 3 - minValueToPrint

            if routeCounterToPrint == -1 * len(route) + 2:
                self.__step -= 1

            if routeCounterToPrint == len(route) + 1:
                self.__step += 1
                routeCounterToPrint -= 1

            if routeCounterToPrint <= len(route):
                for i in range(routeCounterToPrint - 1):
                    self.__canvasMap.create_line(sizeSquare * (route[i][1] + 0.5), sizeSquare * (route[i][0] + 0.5),
                                                 sizeSquare * (route[i + 1][1] + 0.5),
                                                 sizeSquare * (route[i + 1][0] + 0.5), width=10, fill="#920098")
