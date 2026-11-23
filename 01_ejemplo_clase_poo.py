class Rectangulo:
    Alto=0
    Ancho=0
    
    def area (self):
        return self.alto * self.ancho
    
    def perimetro (self):
        return 2 * (self.alto + self.ancho)
    
    def aumentar(self,valor):
        self.alto+=valor
        self.ancho+=valor
    
    def dibujar (self):
        for a in range(0,self.alto):
            for b in range(0,self.ancho):
                print("*",end=" ")
            print()
    print()
#ejemplo de uso

r1=Rectangulo()
r2=Rectangulo()
r1.alto=5
r1.ancho=10
r2.alto=6
r2.ancho=3
print(f"Area del primer rectángulo: {r1.area()}")
print(f"Perímetro del segundo rectángulo: {r2.perimetro()}")

r1.dibujar()
r2.dibujar()