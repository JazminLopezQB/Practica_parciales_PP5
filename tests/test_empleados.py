import pytest
from Practica_parciales_PP5 import *

# --- Fixtures Generales ---

@pytest.fixture
def dias(): # Fixture para cargar las horas que trabajan los empleados por mes
    dias = []
    for i in range(0, 30):
        dias.append(8)
    return dias

@pytest.fixture
def mi_planta():
    return Planta()

@pytest.fixture
def empleado_contratado():
    return Empleado("Pepe", "Argento", 33888999, Contratado(8, 1000))

@pytest.fixture
def empleado_de_planta():
    return Empleado("Juana", "Maria", 34535645, EmpleadoDePlanta(NivelOperativo()))

@pytest.fixture
def mi_planta_llena(mi_planta, empleado_contratado, empleado_de_planta, dias):
    # Agregar empleados
    mi_planta.contratar_empleado(empleado_contratado)
    mi_planta.contratar_empleado(empleado_de_planta)

    # Llenar los vectores de horas diarias de cada empleado
    mi_planta.empleados[0].dias = dias
    mi_planta.empleados[1].dias = dias

    return mi_planta

# --- Tests para clase Empleado ---

@pytest.mark.parametrize("nombre, apellido, dni, contratacion", [
    ("Pepe", "Argento", 33888999, Contratado(8, 1000)),
    ("Juana", "Maria", 34535645, EmpleadoDePlanta(NivelOperativo())),
    ])
def test_agregar_empleado(nombre, apellido, dni, contratacion):
    mi_empleado = Empleado(nombre, apellido, dni, contratacion)

    assert mi_empleado.nombre == nombre
    assert mi_empleado.apellido == apellido
    assert mi_empleado.dni == dni
    assert mi_empleado.contratacion == contratacion

def test_horas_minimas_negativas():
    with pytest.raises(ValueError):
        Contratado(-8, 1000)

def test_costo_hora_negativo():
    with pytest.raises(ValueError):
        Contratado(8, -1000)

def test_nivel_invalido():
    with pytest.raises(TypeError):
        EmpleadoDePlanta("No es un nivel")

def test_contratacion_invalida():
    with pytest.raises(TypeError):
        Empleado("Random", "Random", 33888999, "No es una contratacion")

@pytest.mark.parametrize("nombre, apellido, dni, contratacion, saldo_esperado", [
    ("Pepe", "Argento", 33888999, Contratado(8, 1000), 240000),
    ("Juana", "Maria", 34535645, EmpleadoDePlanta(NivelOperativo()), 280000),
    ])

def test_calcular_saldo(nombre, apellido, dni, contratacion, saldo_esperado, dias):
    mi_empleado = Empleado(nombre, apellido, dni, contratacion)
    mi_empleado.dias = dias
    assert (mi_empleado.sueldo() == saldo_esperado), f"El saldo es: {mi_empleado.sueldo()}"

"""
Por diseño tanto efectivizar como precarizar no deberían tener forma de
alterar los datos de un Empleado, pero a los test se les agregó una
comprobación de la inmutabilidad del vector dias para demostrarlo.
"""

@pytest.mark.parametrize("nivel", [
    (NivelOperativo()),
    (NivelTecnico()),
    (NivelEspecialista())
    ])

def test_efectivizar(empleado_contratado, nivel):
    dias_previos = empleado_contratado.dias
    empleado_contratado.efectivizar(nivel)

    assert isinstance(empleado_contratado.contratacion, EmpleadoDePlanta)
    assert isinstance(empleado_contratado.contratacion.nivel, type(nivel))
    assert (empleado_contratado.dias == dias_previos) 

def test_precarizar(empleado_de_planta):
    dias_previos = empleado_de_planta.dias
    empleado_de_planta.precarizar(8, 1000)
    
    assert isinstance(empleado_de_planta.contratacion, Contratado)
    assert (empleado_de_planta.dias == dias_previos)

# --- Caso de Prueba Puntual de la Consigna ---

def test_caso_de_prueba():
    empleado_pepe = Empleado("Pepe", "Argento", 33888999, Contratado(8, 1000))
    
    assert empleado_pepe.nombre == "Pepe"
    assert empleado_pepe.apellido == "Argento"
    assert empleado_pepe.dni == 33888999
    assert empleado_pepe.contratacion.tipo == "Contratado"

    empleado_pepe.efectivizar(NivelOperativo())

    # En esta parte también se demuestra que efectivizar no afecta los datos del empleado
    assert empleado_pepe.nombre == "Pepe"
    assert empleado_pepe.apellido == "Argento"
    assert empleado_pepe.dni == 33888999
    assert empleado_pepe.contratacion.tipo == "Empleado de planta"

# --- Tests para clase Planta ---

def test_contratar_empleados(mi_planta, empleado_contratado, empleado_de_planta):
    mi_planta.contratar_empleado(empleado_contratado)
    mi_planta.contratar_empleado(empleado_de_planta)

    assert empleado_contratado in mi_planta.empleados
    assert empleado_de_planta in mi_planta.empleados

def test_despedir_empleados(mi_planta_llena, empleado_contratado, empleado_de_planta):
    mi_planta_llena.despedir_empleado(empleado_contratado)
    mi_planta_llena.despedir_empleado(empleado_de_planta)

    assert empleado_contratado not in mi_planta_llena.empleados
    assert empleado_de_planta not in mi_planta_llena.empleados

    with pytest.raises(ValueError): # Asegurarse de que no se puede despedir a un empleado que no está en la planta
        mi_planta_llena.despedir_empleado(empleado_contratado)

def test_despedir_empleados_dato_invalido(mi_planta_llena):
    with pytest.raises(TypeError): # Asegurarse de que no se pueden despedir elementos que no son empleados
        mi_planta_llena.despedir_empleado("No es un empleado")

def test_calcular_total_a_pagar(mi_planta_llena):
    total = mi_planta_llena.total_sueldos_a_pagar()
    assert (total == ((240000) + (280000)))

def test_optimizar_sueldos(mi_planta_llena):
    mi_planta_llena.optimizar_sueldos(8, 1000)
    assert (mi_planta_llena.total_sueldos_a_pagar() == 240000 * 2)

def test_mejor_sueldo(mi_planta_llena):
    mejor = mi_planta_llena.mejor_sueldo()
    assert (mejor == 280000)

def test_mejor_sueldo_sin_empleados(mi_planta):
    with pytest.raises(ValueError):
        mejor = mi_planta.mejor_sueldo()