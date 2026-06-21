from controllers.restaurant_controller import RestaurantController
from models import Garcom, Produto, Pedido


class RestaurantView:
    def __init__(self, controller: RestaurantController):
        self.controller = controller

    def display_menu(self) -> None:
        print("""
============================================
   SISTEMA SABOR & ARTE - RESTAURANTE
============================================
  1. Cadastrar Garçom
  2. Cadastrar Produto
  3. Abrir Pedido (com produtos)
  4. Listar Garçons
  5. Listar Pedidos
  6. Sair
============================================""")

    def cadastrar_garcom(self) -> None:
        print("\n === CADASTRAR GARÇOM === ")
        nome = input("Nome do garçom: ").strip()
        matricula = input("Matrícula: ").strip()
        if not nome or not matricula:
            print("ERRO: Nome e matrícula são obrigatórios.")
            return

        garcom = self.controller.add_garcom(nome, matricula)
        if garcom is None:
            print("ERRO: Matrícula já cadastrada.")
        else:
            print(f"Garçom cadastrado com sucesso: {garcom}")

    def cadastrar_produto(self) -> Produto | None:
        print("\n === CADASTRAR PRODUTO === ")
        try:
            nome = input("Nome do produto: ").strip()

            if not nome:
                print("ERRO: Nome é obrigatório.")
                return None

            # Verificar duplicidade ANTES de pedir preço e categoria
            produto_existente = self.controller.get_produto_by_nome(nome)
            if produto_existente:
                print(f"AVISO: O produto '{nome}' já está cadastrado no cardápio.")
                return produto_existente

            preco_str = input("Preço (ex: 29.90): ").strip()
            categoria = input("Categoria (ex: Prato, Bebida, Sobremesa): ").strip()

            if not categoria:
                print("ERRO: Categoria é obrigatória.")
                return None

            try:
                preco = float(preco_str)
                if preco < 0:
                    raise ValueError
            except ValueError:
                print("ERRO: Preço inválido.")
                return None

            produto = self.controller.add_produto(nome, preco, categoria)
            print(f"Produto '{nome}' cadastrado com sucesso!")
            return produto

        except Exception as e:
            print(f"ERRO inesperado ao cadastrar produto: {str(e)}")
            return None

    def _selecionar_ou_criar_produto(self) -> Produto | None:
        """Permite selecionar um produto existente ou criar um novo."""
        print("\n === SELECIONAR PRODUTO === ")
        produtos = self.controller.list_produtos()

        if not produtos:
            print("Nenhum produto cadastrado. Vou criar um novo.")
            return self.cadastrar_produto()

        print("\n === PRODUTOS DISPONÍVEIS === ")
        for produto in produtos:
            print(f"{produto}")

        print("\nOpções:")
        print("1. Selecionar um produto existente")
        print("2. Criar novo produto")

        opcao = input("Escolha uma opção (1 ou 2): ").strip()

        if opcao == "1":
            try:
                id_selecionado = int(input("ID do produto: ").strip())
                produto = self.controller.get_produto_by_id(id_selecionado)
                if produto:
                    return produto
                else:
                    print("ERRO: Produto não encontrado.")
                    return None
            except ValueError:
                print("ERRO: ID inválido.")
                return None

        elif opcao == "2":
            return self.cadastrar_produto()

        else:
            print("ERRO: Opção inválida.")
            return None

    def abrir_pedido(self) -> None:
        """Fluxo de abertura de pedido: mesa -> garçom -> produtos com validação."""
        print("\n === ABRIR PEDIDO === ")
        
        try:
            # Etapa 1: Selecionar número da mesa
            try:
                numero_mesa = int(input("Número da mesa: ").strip())
                if numero_mesa <= 0:
                    print("ERRO: Número da mesa deve ser positivo.")
                    return
            except ValueError:
                print("ERRO: Insira um número válido para a mesa.")
                return

            # Etapa 2: Selecionar garçom
            garcons = self.controller.list_garcons()
            if not garcons:
                print("ERRO: Nenhum garçom cadastrado ainda.")
                return

            print("\n === GARÇONS DISPONÍVEIS === ")
            for garcom in garcons:
                print(f"{garcom}")

            try:
                id_garcom = int(input("\nID do garçom responsável: ").strip())
            except ValueError:
                print("ERRO: ID do garçom inválido.")
                return

            # Validar se o ID informado está na lista exibida
            garcom_ids = [g.get_id_garcom() for g in garcons]
            if id_garcom not in garcom_ids:
                print(f"ERRO: Garçom com ID {id_garcom} não encontrado. Escolha um ID da lista acima.")
                return

            # Etapa 3: Validar e criar pedido com verificação de mesa ocupada
            pedido, mensagem = self.controller.abrir_pedido_com_validacao(numero_mesa, id_garcom)
            
            if pedido is None:
                print(mensagem)  # Exibe mensagem de erro
                return
            
            # Pedido foi criado com sucesso
            print(f"\n{mensagem}")

            # Etapa 4: Adicionar produtos ao pedido
            while True:
                continuar = input("\nAdicionar produto ao pedido? (s/n): ").strip().lower()
                if continuar != "s":
                    break

                produto = self._selecionar_ou_criar_produto()
                if produto:
                    try:
                        sucesso = self.controller.add_produto_to_pedido(pedido, produto)
                        if sucesso:
                            pedido.adicionar_produto(produto)
                            print(f"Produto adicionado: {produto.get_nome()}")
                        else:
                            print("ERRO: Não foi possível adicionar o produto ao pedido.")
                    except Exception as e:
                        print(f"ERRO ao adicionar produto ao pedido: {str(e)}")

            print(f"\n{pedido}")
        
        except Exception as e:
            print(f"ERRO inesperado ao abrir pedido: {str(e)}")

    def mostrar_garcons(self) -> None:
        print("\n === GARÇONS CADASTRADOS === ")
        garcons = self.controller.list_garcons()
        if not garcons:
            print("Nenhum garçom cadastrado ainda.")
            return

        for garcom in garcons:
            print(f"{garcom}")

    def mostrar_pedidos(self) -> None:
        print("\n === PEDIDOS CADASTRADOS === ")
        pedidos = self.controller.listar_pedidos_completos()
        if not pedidos:
            print("Nenhum pedido cadastrado ainda.")
            return

        for pedido in pedidos:
            print(f"\n  Pedido #{pedido['id_pedido']} | Mesa {pedido['numero_mesa']} | Garçom: {pedido['garcom']} | Status: {pedido['status']}")
            
            if pedido['produtos']:
                print("  Produtos:")
                for produto in pedido['produtos']:
                    print(f"    - {produto.get_nome()}: R$ {produto.get_preco():.2f}")
            else:
                print("  Produtos: nenhum")
            
            print(f"  Total do Pedido: R$ {pedido['total']:.2f}")
