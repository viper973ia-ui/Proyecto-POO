# Crea una clase calculadora, con las siguientes características:

# - Dos atributos donde se guardaran los números con
#   los que se van a operar.

# - Tendrá los siguientes métodos:
#       - Sumar() - devuelve suma.
#       - Restar() - devuelve la resta del mayor menos el menor.
#       - Multiplicar() - devuelve la multiplicación.
#       - Dividir() - devuelve la división del mayor menos el menor.

class Calculadora:
    operando_1=0
    operando_2=0
    
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
        return max(self.operando_1,self.operando_2)/min(self.operando_1,self.operando_2) 
