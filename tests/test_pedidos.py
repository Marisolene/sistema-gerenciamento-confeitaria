from datetime import date
from app.extensions import db
from app.models import Cliente, Pedido


def criar_cliente(app):
    with app.app_context():
        cliente = Cliente(nome="Ana", telefone="11988887777")
        db.session.add(cliente)
        db.session.commit()
        return cliente.id_cliente


def test_cadastra_pedido(client, app):
    id_cliente = criar_cliente(app)
    resposta = client.post(
        "/pedidos",
        data={
            "id_cliente": str(id_cliente),
            "produto": "Bolo de chocolate",
            "quantidade": "1",
            "valor_total": "85,50",
            "data_pedido": date.today().isoformat(),
            "data_entrega": date.today().isoformat(),
        },
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    assert "Bolo de chocolate".encode() in resposta.data


def test_atualiza_status(client, app):
    with app.app_context():
        cliente = Cliente(nome="Ana", telefone="11988887777")
        db.session.add(cliente)
        db.session.flush()
        pedido = Pedido(
            id_cliente=cliente.id_cliente,
            produto="Torta",
            quantidade=1,
            valor_total=50,
            data_pedido=date.today(),
            data_entrega=date.today(),
            status="Pendente",
        )
        db.session.add(pedido)
        db.session.commit()
        pedido_id = pedido.id_pedido

    resposta = client.post(
        f"/pedidos/{pedido_id}/status",
        data={"status": "Em preparo"},
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    assert "Em preparo".encode() in resposta.data
