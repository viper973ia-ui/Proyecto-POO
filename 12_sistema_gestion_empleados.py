# Ejercicio: Sistema de gestión de empleados 
# 1. Enunciado 
# Una empresa necesita desarrollar una pequeña aplicación para gestionar diferentes tipos 
# de empleados. 
# Todos los empleados tienen una serie de características comunes, pero el cálculo de su 
# salario depende del tipo de empleado. 
# Debes implementar las siguientes clases: 
# Clase Empleado (superclase) 
# Atributos: 
#  nombre: nombre del empleado. 
#  edad: edad. 
#  salario_base: salario base mensual. 
# Métodos: 
#  mostrar_informacion(): muestra los datos del empleado. 
#  calcular_salario(): devuelve el salario base. 
# Clase Desarrollador (hereda de Empleado) 
# Atributos adicionales: 
#  lenguaje: lenguaje de programación que utiliza. 
#  horas_extra: número de horas extraordinarias realizadas durante el mes. 
# Métodos: 
#  Sobrescribir calcular_salario(): devuelve el salario base más 25 € por cada 
# hora extra. 
#  Sobrescribir mostrar_informacion(): muestra también el lenguaje de 
# programación y las horas extra. 
# Clase Gerente (hereda de Empleado) 
# Atributos adicionales: 
#  departamento: departamento que dirige. 
#  bonus: cantidad adicional que recibe mensualmente. 
# Métodos: 
#  Sobrescribir calcular_salario(): devuelve el salario base más el bonus. 
#  Sobrescribir mostrar_informacion(): muestra también el departamento y el 
# bonus. 
# 2. Programa principal 
# En el programa principal debes realizar las siguientes operaciones: 
# 1. Crear dos objetos de tipo Desarrollador. 
# 2. Crear dos objetos de tipo Gerente. 
# 3. Guardar los cuatro objetos en una única lista. 
# 4. Recorrer la lista mostrando la información de cada empleado. 
# 5. Mostrar el salario calculado de cada empleado. 
# 6. Calcular y mostrar el importe total de las nóminas de la empresa. 

class Empleado:
    def __init__ (self,nombre,edad,salario_base):
        self.nombre=nombre
        self.edad=edad
        self.salario_base=salario_base
    
    def mostrar_informacion(self):
        print (f"Nombre {self.nombre}")
        print (f"Edad: {self.edad}")
        print (f"Salario base: {self.salario_base}")
        
    def calcular_salario(self):
        return self.salario_base
    
class Desarrollador(Empleado):
    def __init__(self,nombre, edad, salario_base, lenguaje,horas_extra):
        super().__init__(nombre,edad,salario_base)
        self.lenguaje=lenguaje
        self.horas_extra=horas_extra

    def calcular_salario(self, pago_hora_extra=20):
        return super().calcular_salario() + (self.horas_extra * pago_hora_extra)
    
    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"  Lenguaje: {self.lenguaje}, horas extra: {self.horas_extra}")
        
class Gerente(Empleado):
    def __init__(self, nombre, edad, salario_base, departamento, bonus):
        super().__init__(nombre, edad, salario_base)
        self.departamento = departamento 
        self.bonus = bonus

    def calcular_salario(self):
        return super().calcular_salario() + self.bonus

    def mostrar_informacion(self):
        super().mostrar_informacion()
        print(f"  Departamento: {self.departamento}, bonus: {self.bonus} €")

# 1. Dos desarrolladores
dev1 = Desarrollador("Lucía", 28, 2200, "Python", 12)
dev2 = Desarrollador("Javier", 34, 2500, "Java", 8)

# 2. Dos gerentes
ger1 = Gerente("Carmen", 45, 3500, "Ventas", 800)
ger2 = Gerente("Andrés", 50, 3800, "IT", 650)

# 3. Lista con los cuatro
empleados = [dev1, dev2, ger1, ger2]

# 4. Información de cada empleado
for e in empleados:
    e.mostrar_informacion()

print("************************************************")

# 5. Salario de cada empleado
for e in empleados:
    print(f"{e.nombre}: {e.calcular_salario()} €")

print("************************************************")

# 6. Total de nóminas
total = 0
for e in empleados:
    total += e.calcular_salario()
print("Total nóminas:", total, "€")

print("************************************************")
print("************************************************")