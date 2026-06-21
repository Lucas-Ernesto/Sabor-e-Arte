# Módulo: restaurante.py
# Contém listas de garçons (Agregação) e pedidos

from .garcom import Garcom
from .pedido import Pedido

class Restaurante:
    """Classe central do sistema. Agrega Garçons e gerencia Pedidos."""

    def __init__(self, nome: str, cnpj: str):
        # Atributos encapsulados
        self.__nome = nome
        self.__cnpj = cnpj
        self.__garcons: list[Garcom] = []   # Agregação: garçons existem fora da classe
        self.__pedidos: list[Pedido] = []   # Composição: pedidos pertencem ao restaurante

    # Getters
    def get_nome(self) -> str:
        return self.__nome

    def get_garcons(self) -> list:
        return self.__garcons

    def get_pedidos(self) -> list:
        return self.__pedidos

    # Adicionar garçom ao restaurante
    def adicionar_garcom(self, garcom: Garcom):
        self.__garcons.append(garcom)

    # Adicionar pedido ao restaurante
    def adicionar_pedido(self, pedido: Pedido):
        self.__pedidos.append(pedido)

    # Buscar garçom por ID
    def buscar_garcom_por_id(self, id_garcom: int):
        for garcom in self.__garcons:
            if garcom.get_id_garcom() == id_garcom:
                return garcom
        return None

    def __str__(self) -> str:
        # Representação legível do restaurante
        return f"Restaurante: {self.__nome} | CNPJ: {self.__cnpj}"

