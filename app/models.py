from app.extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.Text, nullable=True)

    pedidos = db.relationship(
        "Pedido",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Cliente {self.nome}>"


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id_cliente"),
        nullable=False
    )
    produto = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    data_pedido = db.Column(db.Date, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pendente"
    )

    cliente = db.relationship(
        "Cliente",
        back_populates="pedidos"
    )

    __table_args__ = (
        db.CheckConstraint(
            "quantidade > 0",
            name="check_quantidade_positiva"
        ),
        db.CheckConstraint(
            "valor_total >= 0",
            name="check_valor_nao_negativo"
        ),
        db.CheckConstraint(
            "data_entrega >= data_pedido",
            name="check_data_entrega"
        ),
        db.CheckConstraint(
            "status IN ('Pendente', 'Em preparo', 'Pronto', 'Concluído')",
            name="check_status_pedido"
        ),
    )

    def __repr__(self):
        return f"<Pedido {self.id_pedido} - {self.produto}>"
