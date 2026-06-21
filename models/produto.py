# Módulo: produto.py
# Representa um item do cardápio do restaurante

class Produto:
    """Classe que representa um produto do cardápio."""

    def __init__(self, id_produto: int, nome: str, preco: float, categoria: str):
        # Atributos encapsulados com _ (convenção snake_case)
        self.__id_produto = id_produto
        self.__nome = nome
        self.__preco = preco
        self.__categoria = categoria

    # Getters
    def get_id_produto(self) -> int:
        return self.__id_produto

    def get_nome(self) -> str:
        return self.__nome

    def get_preco(self) -> float:
        return self.__preco

    def get_categoria(self) -> str:
        return self.__categoria

    # Setters com validação
    def set_preco(self, novo_preco: float):
        if novo_preco < 0:
            raise ValueError("Preço não pode ser negativo.")
        self.__preco = novo_preco

    def __str__(self) -> str:
        # Representação legível do produto
        return f"[{self.__id_produto}] {self.__nome} - R$ {self.__preco:.2f} ({self.__categoria})"

