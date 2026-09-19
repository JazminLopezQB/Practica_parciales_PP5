
from abc import ABC, abstractmethod

"""
Para gestionar los niveles de los empleados de planta se optó por aplicar Strategy, los niveles
realmente no tienen interacciones entre si y cada uno maneja su propio conjunto de datos.
"""
class Nivel(ABC): # Todas las subclases deben definir si o si las propiedades en común

    @property
    @abstractmethod
    def nombre(self):
        pass

    @property
    @abstractmethod
    def valor_hora(self):
        pass

class NivelOperativo(Nivel):

    @property
    def nombre(self):
        return "Nivel Operativo"

    @property
    def valor_hora(self):
        return 1000

class NivelTecnico(Nivel):

    @property
    def nombre(self):
        return "Nivel Tecnico"

    @property
    def valor_hora(self):
        return 2000

class NivelEspecialista(Nivel):

    @property
    def nombre(self):
        return "Nivel Especialista"

    @property
    def valor_hora(self):
        return 3000

"""
Para gestionar los tipos de contratación se optó por aplicar State, las contrataciones pueden convertirse
a las otras según lo requiera la empresa, son estados internos a los empleados que se transforman con
precarizar o efectivizar.
"""
class Contratacion(ABC):
    
    @property
    @abstractmethod
    def tipo(self):
        pass

    @property
    def empleado(self):
        return self._empleado

    @empleado.setter
    def empleado(self, empleado):
        if not (isinstance(empleado, Empleado)):
            raise TypeError("Solo se pueden asignar contrataciones a los empleados.")
        self._empleado = empleado

    @abstractmethod
    def detalles(self):
        pass
    
    @abstractmethod
    def calcular_sueldo(self, dias):
        pass

    def efectivizar(self, nivel): # Incluir ambos métodos en la Superclase para poder
        pass                      # tratar a las contrataciones indistintamente en los métodos de planta

    def precarizar(self, horas_minimas, costo_hora):
        pass

class Contratado(Contratacion):

    def __init__(self, horas_minimas, costo_hora):
        self._empleado = None
        self.horas_minimas = horas_minimas
        self.costo_hora = costo_hora
    
    @property
    def tipo(self):
        return "Contratado"

    @property
    def horas_minimas(self):
        return self._horas_minimas

    @horas_minimas.setter
    def horas_minimas(self, numero):
        if numero < 0:
            raise ValueError("Un empleado no puede trabajar menos de 0 horas.")
        self._horas_minimas = numero

    @property
    def costo_hora(self):
        return self._costo_hora

    @costo_hora.setter
    def costo_hora(self, numero):
        if numero < 0:
            raise ValueError("No se le puede pagar a un empleado un saldo negativo.")
        self._costo_hora = numero

    def detalles(self):
        print(f"Tipo de Contratacion: {self.tipo}\nHoras Minimas: {self.horas_minimas}\nCosto por Hora: {self.costo_hora}")

    def calcular_sueldo(self, dias):
        saldo = 0
        for d in dias:
            if (d >= self.horas_minimas):
                saldo += (self.horas_minimas * self.costo_hora)
        return saldo
    
    def efectivizar(self, nivel):
        self.empleado.contratacion = EmpleadoDePlanta(nivel)

class EmpleadoDePlanta(Contratacion):

    def __init__(self, nivel):
        self._empleado = None
        self.nivel = nivel
    
    @property
    def tipo(self):
        return "Empleado de planta"

    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, nivel):
        if not (isinstance(nivel, Nivel)):
            raise TypeError("Los empleados de planta deben asignarse a un nivel valido.")
        self._nivel = nivel

    def detalles(self):
        print(f"Tipo de Contratacion: {self.tipo}\nNivel: {self.nivel.nombre}")

    def calcular_sueldo(self, dias):
        horas_mensuales = 0
        for d in dias:
            horas_mensuales += d

        if (horas_mensuales >= 200):
            return ((200 * self.nivel.valor_hora) + ((horas_mensuales - 200) * 2 * self.nivel.valor_hora))
        return 0 # Interpretación personal de la consigna

    def precarizar(self, horas_minimas, costo_hora):
        self.empleado.contratacion = Contratado(horas_minimas, costo_hora)

class Empleado():

    def __init__(self, nombre, apellido, dni, contratacion):
        self.contratacion = contratacion
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni
        self.dias = []

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def apellido(self):
        return self._apellido

    @property
    def dni(self):
        return self._dni

    @property
    def contratacion(self):
        return self._contratacion

    @contratacion.setter
    def contratacion(self, contratacion):
        if not (isinstance(contratacion, Contratacion)):
            raise TypeError("Cada empleado debe recibir una contratacion valida")
        self._contratacion = contratacion
        self._contratacion.empleado = self

    def sueldo(self):
        return self.contratacion.calcular_sueldo(self.dias)

    def mostrar_datos(self): # Función para revisar manualmente que los datos sean correctos
        print(f"Nombre: {self.nombre} {self.apellido}\nDNI: {self.dni}\n")
        print("--- Detalles de Contratacion ---\n")
        self.contratacion.detalles()

    def efectivizar(self, nivel): # Un empleado puede efectivizarse o precarizarse
        self.contratacion.efectivizar(nivel)

    def precarizar(self, horas_minimas, costo_hora):
        self.contratacion.precarizar(horas_minimas, costo_hora)

class Planta():

    def __init__(self):
        self.empleados = []

    def contratar_empleado(self, empleado):
        if not (isinstance(empleado, Empleado)):
            raise TypeError("Solo se pueden contratar empleados validos.\n")
        self.empleados.append(empleado)

    def despedir_empleado(self, empleado):
        if not (isinstance(empleado, Empleado)):
            raise TypeError("Solo se pueden despedir empleados validos.\n")
        if empleado not in self.empleados:
            raise ValueError("No se pueden despedir a empleados que no pertenecen a la planta.\n")
        self.empleados.remove(empleado)

    def total_sueldos_a_pagar(self):
        total = 0
        for e in self.empleados:
            total += e.sueldo()
        return total

    def optimizar_sueldos(self, horas_minimas, costo_hora):
        for e in self.empleados:
            e.precarizar(horas_minimas, costo_hora)
    
    def mejor_sueldo(self):
        if not self.empleados:
            raise ValueError("No hay empleados contratados.\n")
        mejor = self.empleados[0].sueldo()
        for e in self.empleados:
            mejor = max(e.sueldo(), mejor)
        return mejor