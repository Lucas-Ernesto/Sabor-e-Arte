import sqlite3
from models import Restaurante, Garcom, Pedido, Produto

class RestaurantController:
    def __init__(self, database_path: str = "banco.db"):
        self.database_path = database_path
        self.connection = self._connect_db()
        self._create_tables()
        self.restaurante = Restaurante("Sabor & Arte", "12.345.678/0001-99")

    def _connect_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path)
        return conn

    def _create_tables(self) -> None:
        cursor = self.connection.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS garcom (
                id_garcom   INTEGER PRIMARY KEY AUTOINCREMENT,
                nome        TEXT NOT NULL,
                matricula   TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS produto (
                id_produto  INTEGER PRIMARY KEY AUTOINCREMENT,
                nome        TEXT NOT NULL,
                preco       REAL NOT NULL,
                categoria   TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS pedido (
                id_pedido   INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_mesa INTEGER NOT NULL,
                id_garcom   INTEGER NOT NULL,
                status      TEXT NOT NULL DEFAULT 'aberto',
                FOREIGN KEY (id_garcom) REFERENCES garcom(id_garcom)
            );

            CREATE TABLE IF NOT EXISTS pedido_produto (
                id_pedido   INTEGER NOT NULL,
                id_produto  INTEGER NOT NULL,
                FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
                FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
            );
        """)
        self.connection.commit()

    def add_garcom(self, nome: str, matricula: str) -> Garcom | None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO garcom (nome, matricula) VALUES (?, ?)",
                (nome, matricula),
            )
            self.connection.commit()
            id_gerado = cursor.lastrowid
            garcom = Garcom(id_gerado, nome, matricula)
            self.restaurante.adicionar_garcom(garcom)
            return garcom
        except sqlite3.IntegrityError:
            return None

    def get_produto_by_nome(self, nome: str) -> Produto | None:
        """Busca um produto pelo nome no banco de dados."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_produto, nome, preco, categoria FROM produto WHERE nome = ?", (nome,))
        row = cursor.fetchone()
        return Produto(row[0], row[1], row[2], row[3]) if row else None

    def get_ou_criar_produto(self, nome: str, preco: float, categoria: str) -> Produto:
        """Verifica se produto existe por nome. Se existir, retorna-o. Se não, cria um novo."""
        produto_existente = self.get_produto_by_nome(nome)
        if produto_existente:
            return produto_existente
        # Produto não existe, insere novo
        return self.add_produto(nome, preco, categoria)

    def add_produto(self, nome: str, preco: float, categoria: str) -> Produto:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO produto (nome, preco, categoria) VALUES (?, ?, ?)",
            (nome, preco, categoria),
        )
        self.connection.commit()
        id_gerado = cursor.lastrowid
        produto = Produto(id_gerado, nome, preco, categoria)
        return produto

    def add_pedido(self, numero_mesa: int, id_garcom: int) -> Pedido:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO pedido (numero_mesa, id_garcom, status) VALUES (?, ?, 'aberto')",
            (numero_mesa, id_garcom),
        )
        self.connection.commit()
        id_pedido = cursor.lastrowid
        pedido = Pedido(id_pedido, numero_mesa, id_garcom)
        self.restaurante.adicionar_pedido(pedido)
        return pedido

    def add_produto_to_pedido(self, pedido: Pedido, produto: Produto) -> bool:
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO pedido_produto (id_pedido, id_produto) VALUES (?, ?)",
                (pedido.get_id_pedido(), produto.get_id_produto()),
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"ERRO ao vincular produto ao pedido: {e}")
            return False

    def list_garcons(self) -> list[Garcom]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_garcom, nome, matricula FROM garcom")
        rows = cursor.fetchall()
        return [Garcom(row[0], row[1], row[2]) for row in rows]

    def list_pedidos(self) -> list[tuple[int, int, str, str]]:
        cursor = self.connection.cursor()
        cursor.execute(
            """
                SELECT p.id_pedido, p.numero_mesa, g.nome, p.status
                FROM pedido p
                JOIN garcom g ON p.id_garcom = g.id_garcom
            """
        )
        return cursor.fetchall()

    def list_produtos(self) -> list[Produto]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_produto, nome, preco, categoria FROM produto")
        rows = cursor.fetchall()
        return [Produto(row[0], row[1], row[2], row[3]) for row in rows]

    def get_garcom_by_id(self, id_garcom: int) -> Garcom | None:
        """Busca um garçom pelo ID no banco de dados."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_garcom, nome, matricula FROM garcom WHERE id_garcom = ?", (id_garcom,))
        row = cursor.fetchone()
        return Garcom(row[0], row[1], row[2]) if row else None

    def get_produto_by_id(self, id_produto: int) -> Produto | None:
        """Busca um produto pelo ID no banco de dados."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id_produto, nome, preco, categoria FROM produto WHERE id_produto = ?", (id_produto,))
        row = cursor.fetchone()
        return Produto(row[0], row[1], row[2], row[3]) if row else None

    def get_pedido_detalhado(self, id_pedido: int) -> dict | None:
        """Retorna um pedido com seus produtos associados."""
        cursor = self.connection.cursor()
        
        # Buscar informações do pedido
        cursor.execute(
            """
            SELECT p.id_pedido, p.numero_mesa, g.nome, p.status, p.id_garcom
            FROM pedido p
            JOIN garcom g ON p.id_garcom = g.id_garcom
            WHERE p.id_pedido = ?
            """,
            (id_pedido,)
        )
        pedido_row = cursor.fetchone()
        if not pedido_row:
            return None
        
        # Buscar produtos do pedido
        cursor.execute(
            """
            SELECT pr.id_produto, pr.nome, pr.preco, pr.categoria
            FROM produto pr
            JOIN pedido_produto pp ON pr.id_produto = pp.id_produto
            WHERE pp.id_pedido = ?
            """,
            (id_pedido,)
        )
        produtos_rows = cursor.fetchall()
        produtos = [Produto(row[0], row[1], row[2], row[3]) for row in produtos_rows]
        
        # Calcular total
        total = sum(p.get_preco() for p in produtos)
        
        return {
            'id_pedido': pedido_row[0],
            'numero_mesa': pedido_row[1],
            'garcom': pedido_row[2],
            'status': pedido_row[3],
            'id_garcom': pedido_row[4],
            'produtos': produtos,
            'total': total
        }

    def listar_pedidos_completos(self) -> list[dict]:
        """Lista todos os pedidos com seus produtos em duas queries fixas (sem N+1)."""
        cursor = self.connection.cursor()

        # Query 1: buscar todos os pedidos
        cursor.execute(
            """
            SELECT p.id_pedido, p.numero_mesa, g.nome, p.status, p.id_garcom
            FROM pedido p
            JOIN garcom g ON p.id_garcom = g.id_garcom
            """
        )
        pedidos_rows = cursor.fetchall()

        if not pedidos_rows:
            return []

        # Query 2: buscar todos os produtos de todos os pedidos de uma vez
        cursor.execute(
            """
            SELECT pp.id_pedido, pr.id_produto, pr.nome, pr.preco, pr.categoria
            FROM pedido_produto pp
            JOIN produto pr ON pr.id_produto = pp.id_produto
            """
        )
        produtos_rows = cursor.fetchall()

        # Agrupar produtos por id_pedido em memória
        produtos_por_pedido: dict[int, list[Produto]] = {}
        for row in produtos_rows:
            id_pedido = row[0]
            produto = Produto(row[1], row[2], row[3], row[4])
            produtos_por_pedido.setdefault(id_pedido, []).append(produto)

        # Montar lista final
        pedidos_completos = []
        for pedido_row in pedidos_rows:
            id_pedido = pedido_row[0]
            produtos = produtos_por_pedido.get(id_pedido, [])
            total = sum(p.get_preco() for p in produtos)
            pedidos_completos.append({
                'id_pedido': id_pedido,
                'numero_mesa': pedido_row[1],
                'garcom': pedido_row[2],
                'status': pedido_row[3],
                'id_garcom': pedido_row[4],
                'produtos': produtos,
                'total': total
            })

        return pedidos_completos

    def is_mesa_ocupada(self, numero_mesa: int) -> bool:
        """Verifica se a mesa possui um pedido aberto (ativo)."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM pedido WHERE numero_mesa = ? AND status = 'aberto'",
                (numero_mesa,)
            )
            count = cursor.fetchone()[0]
            return count > 0
        except sqlite3.Error as e:
            print(f"ERRO ao verificar disponibilidade da mesa: {e}")
            return False

    def adicionar_produto_com_feedback(self, nome: str, preco: float, categoria: str) -> tuple[Produto | None, str, bool]:
        """Adiciona produto com feedback. Retorna (Produto, mensagem, é_novo)."""
        try:
            # Verificar se o produto já existe
            produto_existente = self.get_produto_by_nome(nome)
            if produto_existente:
                mensagem = f"O produto '{nome}' já está cadastrado no cardápio."
                return (produto_existente, mensagem, False)
            
            # Produto não existe, insere novo
            produto = self.add_produto(nome, preco, categoria)
            mensagem = f"Produto '{nome}' cadastrado com sucesso!"
            return (produto, mensagem, True)
        
        except sqlite3.Error as e:
            mensagem = f"ERRO ao cadastrar produto: {str(e)}"
            return (None, mensagem, False)

    def abrir_pedido_com_validacao(self, numero_mesa: int, id_garcom: int) -> tuple[Pedido | None, str]:
        """Abre pedido com validação de mesa ocupada. Retorna (Pedido, mensagem)."""
        try:
            # Verificar se a mesa está ocupada
            if self.is_mesa_ocupada(numero_mesa):
                mensagem = f"Atenção: A mesa {numero_mesa} já está ocupada. Por favor, escolha outra."
                return (None, mensagem)
            
            # Verificar se garçom existe
            garcom = self.get_garcom_by_id(id_garcom)
            if not garcom:
                mensagem = f"ERRO: Garçom com ID {id_garcom} não encontrado."
                return (None, mensagem)
            
            # Mesa está disponível, cria o pedido
            pedido = self.add_pedido(numero_mesa, id_garcom)
            mensagem = f"Pedido aberto para {garcom} - Mesa {numero_mesa}"
            return (pedido, mensagem)
        
        except sqlite3.Error as e:
            mensagem = f"ERRO ao abrir pedido: {str(e)}"
            return (None, mensagem)

    def close(self) -> None:
        self.connection.close()

