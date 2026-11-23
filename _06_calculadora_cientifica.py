import _03calculadora as cal
class Cientifica(cal.Calculadora):
    def sumatorio(self):
        suma=0
        for n in range(self.operando_1,self.operando_2+1):
            suma+=n
        return suma 