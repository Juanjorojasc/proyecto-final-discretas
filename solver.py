"""
Author: [JUAN JOSE ROJAS CANENCIO ]

"""
 
import structure          # Importamos la clase abstracta que debemos implementar
from itertools import product  # Para generar todas las combinaciones posibles
 
 
class PoliticalSAT(structure.VirtualPoliticalSAT):
    """
    Clase principal del solucionador.
    Hereda de VirtualPoliticalSAT e implementa sus métodos abstractos.
    """
 
    def __init__(self, seats: list[int], policies: list[list[int]]):
        """
        Constructor: guarda los datos del problema.
 
        seats    -> lista con los escaños de cada partido. Ej: [19, 8, 16]
        policies -> matriz n x p donde policies[i][j] es la postura del
                    partido i sobre la política j. Valores: -1, 0, +1
        """
        self.seats = seats          # Escaños de cada partido
        self.policies = policies    # Matriz de posturas
 
    def solve_stability(self, percentage: float) -> list[int]:
        """
        Busca una asignación de políticas que forme un gobierno estable.
 
        Una asignación es "estable" si los partidos que la apoyan completamente
        suman al menos (percentage * total_escaños) escaños.
 
        Retorna la lista de decisiones [d_1, d_2, ..., d_p] donde cada d_j es +1 o -1.
        Si no existe ninguna asignación válida, retorna todo ceros.
        """
 
        n = len(self.seats)           # Número de partidos
        p = len(self.policies[0])     # Número de políticas
        total_seats = sum(self.seats)  # Total de escaños en el parlamento
        threshold = total_seats * percentage  # Mínimo de escaños necesarios
 
        # Guardamos la última decisión probada para usarla en generate_dnf()
        self.last_decision = [0] * p
 
        # Iteramos sobre todas las posibles combinaciones de decisiones
        # product([-1, 1], repeat=p) genera: (-1,-1,...,-1), (-1,-1,...,1), ..., (1,1,...,1)
        for decision in product([-1, 1], repeat=p):
 
            government_seats = 0  # Escaños que apoyan esta decisión
 
            # Revisamos cada partido para ver si apoya la decisión completa
            for i in range(n):
                party_agrees = True  # Asumimos que el partido está de acuerdo
 
                for j in range(p):
                    postura = self.policies[i][j]   # Postura del partido i en política j
                    dec = decision[j]                # Decisión tomada para política j
 
                    # El partido se opone si tiene postura definida y NO coincide con la decisión
                    if postura != 0 and postura != dec:
                        party_agrees = False
                        break  # No hace falta seguir revisando políticas
 
                # Si el partido apoya todas las decisiones, sumamos sus escaños
                if party_agrees:
                    government_seats += self.seats[i]
 
            # Si los escaños que apoyan esta decisión alcanzan el umbral, la retornamos
            if government_seats >= threshold - 1e-12:
                # Guardamos la decisión para generate_dnf()
                self.last_decision = list(decision)
                return list(decision)
 
        # Si ninguna combinación funcionó, retornamos todo ceros (imposible)
        self.last_decision = [0] * p
        return [0] * p
 
    def generate_dnf(self) -> str:
        """
        Genera la Forma Normal Disyuntiva (DNF) del problema.
 
        La DNF expresa las condiciones que hacen que un partido apoye la decisión.
        Cada partido genera una cláusula (conjunción) con sus restricciones.
        Las cláusulas de todos los partidos se unen con OR (disyunción).
 
        Formato de salida:
          (x1 ^ !x2 ^ x3) | (!x1 ^ x4) | ...
 
        Donde:
          - x_j  significa "la política j se aprueba (+1)"
          - !x_j significa "la política j se rechaza (-1)"
          - políticas con postura 0 (neutral) no aparecen en la cláusula del partido
        """
 
        n = len(self.seats)
        p = len(self.policies[0])
 
        clauses = []  # Lista de cláusulas, una por cada partido
 
        for i in range(n):
            literals = []  # Literales de la cláusula del partido i
 
            for j in range(p):
                postura = self.policies[i][j]
 
                if postura == 1:
                    # El partido apoya la política j: necesita que x_j = +1
                    literals.append(f"x{j+1}")
 
                elif postura == -1:
                    # El partido rechaza la política j: necesita que x_j = -1
                    literals.append(f"!x{j+1}")
 
                # Si postura == 0: el partido es neutral, no agrega restricción
 
            # Si el partido no tiene ninguna restricción (todo ceros), acepta cualquier decisión
            if len(literals) == 0:
                clauses.append("T")   # T = siempre verdadero (tautología)
            else:
                # Unimos los literales con AND (^) dentro de la cláusula
                clauses.append("(" + " ^ ".join(literals) + ")")
 
        # Unimos todas las cláusulas con OR (|)
        return " | ".join(clauses)
