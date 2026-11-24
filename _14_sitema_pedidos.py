# ==========================================
# A. GESTIÓN DE PRODUCTOS
# ==========================================
class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def mostrar_info(self):
        print(f"[{self.codigo}] {self.nombre} - {self.precio:.2f}€ (Stock: {self.stock})")

    def actualizar_stock(self, cantidad):
        # Cantidad puede ser positiva (reponer) o negativa (vender)
        self.stock += cantidad


# ==========================================
# C. APLICACIÓN DE DESCUENTOS (Polimorfismo)
# ==========================================
class Descuento:
    def aplicar(self, importe):
        return importe


class SinDescuento(Descuento):
    pass  # Usa el método del padre sin cambios


class DescuentoPorcentual(Descuento):
    def __init__(self, porcentaje):
        self.porcentaje = porcentaje

    def aplicar(self, importe):
        descuento = importe * (self.porcentaje / 100)
        return max(0, importe - descuento)


class DescuentoFijo(Descuento):
    def __init__(self, cantidad_fija):
        self.cantidad_fija = cantidad_fija

    def aplicar(self, importe):
        return max(0, importe - self.cantidad_fija)


# ==========================================
# D. FORMAS DE PAGO (Polimorfismo)
# ==========================================
class MetodoPago:
    def pagar(self, importe):
        raise NotImplementedError("Este método debe implementarse en las subclases")


class TarjetaCredito(MetodoPago):
    def pagar(self, importe):
        total_con_comision = importe * 1.01  # +1% comisión
        return f"Pago de {total_con_comision:.2f}€ realizado con Tarjeta (incluye 1% comisión)."


class PayPal(MetodoPago):
    def pagar(self, importe):
        total_con_comision = importe * 1.02  # +2% comisión
        return f"Pago de {total_con_comision:.2f}€ realizado con PayPal (incluye 2% comisión)."


class Transferencia(MetodoPago):
    def pagar(self, importe):
        return f"Pago de {importe:.2f}€ realizado por Transferencia (sin comisión)."


# ==========================================
# B. GESTIÓN DE PEDIDOS (Composición)
# ==========================================
class LineaPedido:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.lineas = []
        self.estado = "pendiente"
        self.descuento = SinDescuento()  # Por defecto no tiene descuento

    def agregar_producto(self, producto, cantidad):
        if producto.stock >= cantidad:
            linea = LineaPedido(producto, cantidad)
            self.lineas.append(linea)
            producto.actualizar_stock(-cantidad)
            print(f"Añadido: {cantidad}x {producto.nombre}")
        else:
            print(f"Error: Stock insuficiente para {producto.nombre} (Disponible: {producto.stock})")

    def eliminar_producto(self, codigo_producto):
        for linea in self.lineas:
            if linea.producto.codigo == codigo_producto:
                linea.producto.actualizar_stock(linea.cantidad)  # Devuelve el stock
                self.lineas.remove(linea)
                print(f"Eliminado: {linea.producto.nombre} del pedido.")
                return
        print("Producto no encontrado en el pedido.")

    def aplicar_descuento(self, descuento):
        self.descuento = descuento

    def calcular_total(self):
        subtotal = sum(linea.calcular_subtotal() for linea in self.lineas)
        return self.descuento.aplicar(subtotal)

    def mostrar_pedido(self):
        print("\n" + "=" * 40)
        print(f"PEDIDO #{self.numero} | Cliente: {self.cliente} | Estado: {self.estado.upper()}")
        print("-" * 40)
        for linea in self.lineas:
            print(f"- {linea.producto.nombre} (x{linea.cantidad}): {linea.calcular_subtotal():.2f}€")
        print("-" * 40)
        print(f"TOTAL FINAL (con descuento): {self.calcular_total():.2f}€")
        print("=" * 40 + "\n")

    def procesar_pago(self, metodo_pago):
        if not self.lineas:
            print("El pedido está vacío, no se puede pagar.")
            return
        total = self.calcular_total()
        resultado = metodo_pago.pagar(total)
        self.estado = "pagado"
        print(resultado)


# ==========================================
# PRUEBA DEL PROGRAMA (Objetos)
# ==========================================
if __name__ == "__main__":
    # 1. Crear productos
    p1 = Producto("P01", "Teclado Mecánico", 80.0, 10)
    p2 = Producto("P02", "Ratón Inalámbrico", 40.0, 15)
    p3 = Producto("P03", "Monitor 24''", 150.0, 5)

    # 2. Crear un pedido
    pedido1 = Pedido(1001, "Ana García")

    # 3. Añadir y eliminar productos
    pedido1.agregar_producto(p1, 1)
    pedido1.agregar_producto(p2, 2)
    pedido1.agregar_producto(p3, 1)
    pedido1.eliminar_producto("P02")  # Quitamos el ratón

    # 4. Aplicar un descuento (10% de descuento)
    pedido1.aplicar_descuento(DescuentoPorcentual(10))

    # 5. Mostrar contenido del pedido
    pedido1.mostrar_pedido()

    # 6. Pagar el pedido con PayPal
    pago = PayPal()
    pedido1.procesar_pago(pago)
    print(f"Nuevo estado del pedido: {pedido1.estado}")
