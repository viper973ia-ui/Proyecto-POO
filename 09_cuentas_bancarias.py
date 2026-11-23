class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo

    def ingresar(self, cantidad):
        self.saldo += cantidad

    def extraer(self, cantidad):
        self.saldo -= cantidad


class CuentaLimitada(Cuenta):
    def __init__(self, saldo, limite=0):
        super().__init__(saldo)
        self.limite = limite

    def extraer(self, cantidad):
        if self.saldo <= 0:
            print("Operación denegada: el saldo de la cuenta es 0 o negativo.")
            return

        if self.limite == 0 or cantidad <= self.limite:
            super().extraer(cantidad)
        else:
            print(f"La cantidad ({cantidad}) supera el límite. Se extraerá el límite permitido: {self.limite}.")
            super().extraer(self.limite)


class Movimiento:
    def __init__(self, cantidad, tipo):
        self.cantidad = cantidad
        self.tipo = tipo  # "ingreso" o "extracción"

    def __repr__(self):
        return f"Movimiento(tipo='{self.tipo}', cantidad={self.cantidad})"


# --- Nueva clase encapsuladora ---
class HistorialMovimientos:
    def __init__(self):
        # Atributo privado (__movimientos) para evitar modificaciones externas directas
        self.__movimientos = []
        print(type(self.__movimientos))

    def agregar(self, cantidad, tipo):
        nuevo_movimiento = Movimiento(cantidad, tipo)
        self.__movimientos.append(nuevo_movimiento)

    def obtener_ultimos(self, n=5):
        # return self.__movimientos[-n:]
        # Toma los últimos 'n' elementos y los invierte con [::-1]
        return self.__movimientos[-n:][::-1]

    def __repr__(self):
        return str(self.__movimientos)


class CuentaMovimientos(CuentaLimitada):
    def __init__(self, saldo, limite=0):
        super().__init__(saldo, limite)
        # Composición: CuentaMovimientos TIENE UN HistorialMovimientos
        self.historial = HistorialMovimientos()

    def ingresar(self, cantidad):
        super().ingresar(cantidad)
        self.historial.agregar(cantidad, "ingreso")
        print("Prueba ingreso:", self.historial)
        print("*************************************")

    def extraer(self, cantidad):
        saldo_anterior = self.saldo
        super().extraer(cantidad)
        cantidad_real = saldo_anterior - self.saldo
        if cantidad_real > 0:
            self.historial.agregar(cantidad_real, "extracción")
            print("Prueba extracción:", self.historial)
            print("++++++++++++++++++++++++++++++++++++++++++++")

    def ultimos_movimientos(self):
        return self.historial.obtener_ultimos(5)


# --- Ejemplo de uso ---
if __name__ == "__main__":
    cuenta = CuentaMovimientos(1000, limite=300)

    cuenta.ingresar(200)     # Ingresa 200 -> Saldo: 1200
    cuenta.extraer(100)      # Extrae 100 -> Saldo: 1100
    cuenta.extraer(500)      # Supera límite (300), extrae 300 -> Saldo: 800
    cuenta.ingresar(50)      # Ingresa 50 -> Saldo: 850
    cuenta.extraer(250)      # Extrae 250 -> Saldo: 600
    cuenta.ingresar(100)     # Ingresa 100 -> Saldo: 700
    cuenta.extraer(50)       # Extrae 50 -> Saldo: 650

    print("\nSaldo final:", cuenta.saldo)
    print("Últimos 5 movimientos:")
    for mov in cuenta.ultimos_movimientos():
        print(f" - {mov.tipo.capitalize()}: {mov.cantidad} €")
    print("\n---> Valor actual de __name__:", __name__)
