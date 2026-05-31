# Proyecto Final — Matemáticas Discretas 2026-1
**Pontificia Universidad Javeriana**  
**Autor:** [Tu nombre]

---

## ¿Qué hace el proyecto?

Implementa un solucionador llamado **PoliticalSAT** que modela la formación de gobiernos de coalición en un parlamento.

Dado un conjunto de partidos con escaños y posturas sobre políticas (+1 a favor, -1 en contra, 0 neutral), el programa encuentra una asignación de políticas tal que los partidos que la apoyen completen al menos un porcentaje mínimo de los escaños totales.

---

## Archivos

| Archivo | Descripción |
|---|---|
| `solver.py` | Solución principal — clase `PoliticalSAT` |
| `main.py` | Interfaz del programa (provisto por el profesor) |
| `structure.py` | Clase abstracta base (provista por el profesor) |
| `cases/` | Casos de prueba de entrada y salida esperada |

---

## Algoritmo

Se usa **fuerza bruta**: se prueban todas las combinaciones posibles de decisiones (2^p combinaciones, donde p es el número de políticas). Para cada combinación se cuenta cuántos escaños la apoyan. En cuanto se encuentra una que alcanza el mínimo requerido, se retorna.

Un partido apoya la decisión si para cada política su postura es **neutral (0)** o **coincide exactamente** con la decisión tomada.

---

## Cómo correr las pruebas

```bash
python main.py "-read_case=cases\in_01.txt" "-print_cmp=stdout"
python main.py "-read_case=cases\in_02.txt" "-print_cmp=stdout"
python main.py "-read_case=cases\in_03.txt" "-print_cmp=stdout"
python main.py "-read_case=cases\in_04.txt" "-print_cmp=stdout"
python main.py "-read_case=cases\in_05.txt" "-print_cmp=stdout"
```

---

## Resultados

Todos los casos de prueba pasan correctamente.
