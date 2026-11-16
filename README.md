# Sistema de Gerenciamento de Pedidos para Confeitarias

MVP acadêmico desenvolvido para apoiar pequenas confeiteiras na organização de clientes e encomendas, reunindo em um só lugar informações que hoje podem ficar dispersas entre conversas e anotações.

## Funcionalidades implementadas

- Cadastro de clientes com nome, telefone e observações.
- Cadastro de pedidos vinculados a um cliente.
- Consulta de pedidos ordenados pela data de entrega.
- Atualização do status: Pendente, Em preparo, Pronto e Concluído.
- Painel inicial com resumo dos pedidos.

## Tecnologias

- Python 3.12
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- SQLite
- HTML5 e CSS3
- pytest e GitHub Actions

## Estrutura

```text
app/
  __init__.py
  extensions.py
  models.py
  routes.py
  templates/
    base.html
    index.html
    clientes.html
    pedidos.html
  static/
    css/style.css
tests/
  conftest.py
  test_clientes.py
  test_pedidos.py
.github/workflows/tests.yml
config.py
requirements.txt
run.py
```

## Executar localmente

Requer Python 3.12 instalado.

1. Clone ou baixe este repositório.
2. Abra a pasta do projeto no VS Code.
3. Crie e ative um ambiente virtual:

   **Windows (PowerShell):**
   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Instale as dependências:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Inicie a aplicação:

   ```powershell
   python run.py
   ```

6. Abra no navegador o endereço mostrado no terminal (normalmente http://127.0.0.1:5000).

O banco SQLite é criado automaticamente na primeira execução.

## Executar os testes

No terminal do VS Code:

```powershell
python -m pytest -q
```

Os testes também são executados automaticamente pelo GitHub Actions em pushes para a branch principal/de desenvolvimento e em Pull Requests para `main`.

## Configurações

A aplicação aceita `SECRET_KEY` e `DATABASE_URL` por variáveis de ambiente. Para uso fora do ambiente local, configure uma chave secreta forte e HTTPS no servidor. O valor de chave de desenvolvimento definido em `config.py` não deve ser usado em produção.

## Escopo do MVP

Este MVP contempla o fluxo básico de clientes e pedidos. Integração com WhatsApp, estoque, financeiro avançado, múltiplos itens por pedido e envio automático de mensagens não fazem parte desta versão.

## Validação em campo

As validações de usabilidade com a confeiteira parceira devem ser realizadas e documentadas pela equipe do projeto. Não são considerados resultados de validação até que as sessões reais sejam executadas e registradas.
