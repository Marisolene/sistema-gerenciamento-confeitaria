
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from decimal import Decimal, InvalidOperation

from app.extensions import db
from app.models import Cliente, Pedido


main = Blueprint("main", __name__)


# Página inicial: consulta os pedidos
@main.route("/")
def index():
    pedidos = Pedido.query.order_by(Pedido.data_entrega.asc()).all()

    return render_template("index.html", pedidos=pedidos)


# Cadastro e consulta de clientes
@main.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        observacoes = request.form.get("observacoes", "").strip()

        if not nome or not telefone:
            flash("Nome e telefone são obrigatórios.", "erro")
            return redirect(url_for("main.clientes"))

        novo_cliente = Cliente(
            nome=nome,
            telefone=telefone,
            observacoes=observacoes or None
        )

        db.session.add(novo_cliente)
        db.session.commit()

        flash("Cliente cadastrado com sucesso!", "sucesso")
        return redirect(url_for("main.clientes"))

    lista_clientes = Cliente.query.order_by(Cliente.nome.asc()).all()

    return render_template(
        "clientes.html",
        clientes=lista_clientes
    )


# Cadastro e consulta de pedidos
@main.route("/pedidos", methods=["GET", "POST"])
def pedidos():
    lista_clientes = Cliente.query.order_by(Cliente.nome.asc()).all()

    if request.method == "POST":
        try:
            id_cliente = int(request.form.get("id_cliente", ""))
            quantidade = int(request.form.get("quantidade", ""))
            valor_total = Decimal(
                request.form.get("valor_total", "").replace(",", ".")
            )

            data_pedido = datetime.strptime(
                request.form.get("data_pedido", ""),
                "%Y-%m-%d"
            ).date()

            data_entrega = datetime.strptime(
                request.form.get("data_entrega", ""),
                "%Y-%m-%d"
            ).date()

            produto = request.form.get("produto", "").strip()

            if not produto:
                raise ValueError("Informe o produto.")

            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")

            if valor_total < 0:
                raise ValueError("O valor não pode ser negativo.")

            if data_entrega < data_pedido:
                raise ValueError(
                    "A entrega não pode ser anterior ao pedido."
                )

            cliente = db.session.get(Cliente, id_cliente)

            if cliente is None:
                raise ValueError("Selecione um cliente válido.")

            novo_pedido = Pedido(
                id_cliente=id_cliente,
                produto=produto,
                quantidade=quantidade,
                valor_total=valor_total,
                data_pedido=data_pedido,
                data_entrega=data_entrega,
                status="Pendente"
            )

            db.session.add(novo_pedido)
            db.session.commit()

            flash("Pedido cadastrado com sucesso!", "sucesso")
            return redirect(url_for("main.pedidos"))

        except (ValueError, InvalidOperation):
            db.session.rollback()
            flash("Confira os dados informados no pedido.", "erro")

    lista_pedidos = Pedido.query.order_by(
        Pedido.data_entrega.asc()
    ).all()

    return render_template(
        "pedidos.html",
        pedidos=lista_pedidos,
        clientes=lista_clientes
    )


# Atualização do status de um pedido
@main.route("/pedidos/<int:id_pedido>/status", methods=["POST"])
def atualizar_status(id_pedido):
    pedido = db.session.get(Pedido, id_pedido)

    status_permitidos = [
        "Pendente",
        "Em preparo",
        "Pronto",
        "Concluído"
    ]

    novo_status = request.form.get("status", "")

    if pedido is None:
        flash("Pedido não encontrado.", "erro")

    elif novo_status not in status_permitidos:
        flash("Status inválido.", "erro")

    else:
        pedido.status = novo_status
        db.session.commit()
        flash("Status atualizado com sucesso!", "sucesso")

    return redirect(url_for("main.pedidos"))
