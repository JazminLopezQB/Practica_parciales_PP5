# Modelo de Parcial de Paradigmas de Programación 5 del 2024

El modelo de parcial con ñas consignas está incluido en el repositorio.

## Preguntas Teóricas

Responder las siguientes preguntas sin realizar ningún código:
1. ¿Es necesario realizar cambios sobre la lógica inicial del método
`total_sueldos_a_pagar` cuando se agreguen nuevos tipos de empleados? Justificar
conceptualmente.
    - No, todos los empleados independientemente de su tipo reciben un sueldo y aunque dicho sueldo dependa del tipo de empleado no implica calculos en el método contador.
    - Gracias al polimorfismo debería ser posible aplicar la implementación del calculo de saldo correspondiente a cada tipo de empleado sin tocar el codigo de `total_sueldos_a_pagar`.
2. ¿Qué concepto del paradigma orientado a objetos se rompería al utilizar `if` en el método
`optimizar_sueldos`? Justificar conceptualmente.
    - Se rompería el polimorfismo al tener que determinar primero el tipo de elemento antes de aplicar la lógica.