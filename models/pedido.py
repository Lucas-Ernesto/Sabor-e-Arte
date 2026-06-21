# Módulo: pedido.py
# Representa um pedido feito por uma mesa (Agrega Produtos)

from .produto import Produto

class Pedido:
    """Classe que representa um pedido. Agrega uma lista de Produtos."""

    def __init__(self, id_pedido: int, numero_mesa: int, id_garcom: int):
        # Atributos encapsulados
        self.__id_pedido = id_pedido
        self.__numero_mesa = numero_mesa
        self.__id_garcom = id_garcom
        self.__produtos: list[Produto] = []  # Agregação: lista de Produtos
        self.__status = "aberto"

    # Getters
    def get_id_pedido(self) -> int:
        return self.__id_pedido

    def get_numero_mesa(self) -> int:
        return self.__numero_mesa

    def get_id_garcom(self) -> int:
        return self.__id_garcom

    def get_status(self) -> str:
        return self.__status

    def get_produtos(self) -> list:
        return self.__produtos

    # Adicionar produto ao pedido (Agregação)
    def adicionar_produto(self, produto: Produto):
        self.__produtos.append(produto)

    # Calcular total do pedido
    def calcular_total(self) -> float:
        return sum(p.get_preco() for p in self.__produtos)

    # Fechar pedido
    def fechar_pedido(self):
        self.__status = "fechado"

    def __str__(self) -> str:
        # Representação legível do pedido
        nomes_produtos = ", ".join(p.get_nome() for p in self.__produtos) if self.__produtos else "nenhum"
        return (f"Pedido [{self.__id_pedido}] | Mesa {self.__numero_mesa} | "
                f"Garçom ID {self.__id_garcom} | Status: {self.__status} | "
                f"Produtos: {nomes_produtos} | Total: R$ {self.calcular_total():.2f}")
