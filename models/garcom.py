# Módulo: garcom.py
# Representa um garçom do restaurante (Agregação com Restaurante)

class Garcom:
    """Classe que representa um garçom. Agregada ao Restaurante."""

    def __init__(self, id_garcom: int, nome: str, matricula: str):
        # Atributos encapsulados
        self.__id_garcom = id_garcom
        self.__nome = nome
        self.__matricula = matricula

    # Getters
    def get_id_garcom(self) -> int:
        return self.__id_garcom

    def get_nome(self) -> str:
        return self.__nome

    def get_matricula(self) -> str:
        return self.__matricula

    def __str__(self) -> str:
        # Representação legível do garçom
        return f"[{self.__id_garcom}] {self.__nome} (Matrícula: {self.__matricula})"

