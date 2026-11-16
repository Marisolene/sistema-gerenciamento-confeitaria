def test_pagina_clientes_carrega(client):
    resposta = client.get("/clientes")
    assert resposta.status_code == 200
    assert b"Cadastro de clientes" in resposta.data


def test_cadastra_cliente(client):
    resposta = client.post(
        "/clientes",
        data={
            "nome": "Maria da Silva",
            "telefone": "11999999999",
            "observacoes": "Cliente de teste",
        },
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    assert "Maria da Silva".encode() in resposta.data
    assert "Cliente cadastrado com sucesso".encode() in resposta.data
