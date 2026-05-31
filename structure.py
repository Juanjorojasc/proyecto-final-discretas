"""
Author:Oscar Vargas Pabon
"""
import abc
class VirtualPoliticalSAT(abc.ABC):
	@abc.abstractmethod
	def __init__(self,seats:list[int],policies:list[list[int]]):
		pass
	@abc.abstractmethod
	def solve_stability(self,percentage:float)->list[int]:
		pass
	@abc.abstractmethod
	def generate_dnf(self)->str:
		pass