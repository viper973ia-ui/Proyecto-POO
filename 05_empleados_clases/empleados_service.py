import csv
import os

class Empleado:
    def __init__(self, nombre, edad, salario, departamento):
        self.nombre = nombre
        self.edad = edad
        self.salario = salario
        self.departamento = departamento

class Gestor_Empleados:
    def __init__(self, dir):
        self.dir = dir
        if not os.path.exists(self.dir):
            with open(self.dir, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(["nombre", "edad", "salario", "departamento"])

    def _leer_filas(self):
        """Método interno que lee el CSV por posición y detecta si usa coma o punto y coma."""
        with open(self.dir, "r", encoding="utf-8") as f:
            muestra = f.read(1024)
            f.seek(0)
            separador = ";" if ";" in muestra else ","
            lector = csv.reader(f, delimiter=separador)
            
            filas = []
            for fila in lector:
                # Ignoramos filas vacías o la fila de cabecera (donde la edad no es un número)
                if len(fila) >= 4 and fila[1].strip().isdigit():
                    filas.append(fila)
            return filas

    def alta_empleado(self, empleado):
        with open(self.dir, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([empleado.nombre, empleado.edad, empleado.salario, empleado.departamento])

    def buscar_empleado(self, nombre):
        for e in self._leer_filas():
            if e[0].strip().lower() == nombre.strip().lower():
                return Empleado(e[0].strip(), int(e[1]), float(e[2]), e[3].strip())
        return None

    def departamentos(self):
        return sorted(list({e[3].strip() for e in self._leer_filas() if e[3].strip()}))

    def empleados_departamento(self, departamento):
        return [
            Empleado(e[0].strip(), int(e[1]), float(e[2]), e[3].strip())
            for e in self._leer_filas() if e[3].strip() == departamento
        ]

    def empleados_por_salarios(self, sal_min, sal_max):
        return [
            Empleado(e[0].strip(), int(e[1]), float(e[2]), e[3].strip())
            for e in self._leer_filas() if sal_min <= float(e[2]) <= sal_max
        ]

