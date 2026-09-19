from solucion import *

if __name__ == "__main__":
    mi_empleado = Empleado("Juana", "Maria", 34535645, EmpleadoDePlanta(NivelOperativo()))
    dias = []
    for i in range(0, 30):
        dias.append(8)
    mi_empleado.dias = dias
    mi_empleado.mostrar_datos()