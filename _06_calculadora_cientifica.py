import _03calculadora as cal
class Cientifica(cal.Calculadora):
    def sumatorio(self):
        suma=0
        for n in range(self.operando_1,self.operando_2+1):
            suma+=n
        return suma 
    
    
"""
    class Calculadora:
    def __init__(self,op1,op2):
        self.operando_1=op1
        self.operando_2=op2
    def sumar(self):
        return self.operando_1+self.operando_2
    def restar(self):        
        return max(self.operando_1,self.operando_2)-min(self.operando_1,self.operando_2)
    def multiplicar(self):      
        return self.operando_1*self.operando_2
    def dividir(self):       
        return max(self.operando_1,self.operando_2)/min(self.operando_1,self.operando_2) _summary_
"""