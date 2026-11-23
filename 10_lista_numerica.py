# Crear una subclase de list para el almacenamiento de números con las
# siguientes características:
# incluirá los métodos:
# sum(). Devuelve la suma de los números almacenados
# mean(). Devuelve la media de los números almacenados
# Además de estos métodos, elconstructor recibirá un parámetro
# booleano que, en caso de ser true
# impedirá que repite números


class Lista_Numerica(list):
    def __init__(self, iterable=None, sin_repetidos=False):
        super().__init__()
        self.sin_repetidos = sin_repetidos
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def sum(self):
        return sum(self)

    def mean(self):
        if len(self) == 0:
            return 0
        return self.sum() / len(self)

    def append(self, item):
        if self.sin_repetidos and item in self:
            return
        super().append(item)   

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def insert(self, index, item):
        if self.sin_repetidos and item in self:
            return
        super().insert(index, item)
