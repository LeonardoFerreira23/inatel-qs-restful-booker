def test_tc001_autenticacao_com_credenciais_validas(client):
    """TC-001 | POST /auth com credenciais válidas retorna token."""
    resposta = client.create_token("admin", "password123")
    corpo = resposta.json()

    assert resposta.status_code == 200
    assert "token" in corpo


def test_tc002_listagem_de_reservas(client):
    """TC-002 | GET /booking retorna lista de identificadores."""
    resposta = client.get_booking_ids()
    corpo = resposta.json()

    assert resposta.status_code == 200
    assert isinstance(corpo, list)
    assert len(corpo) > 0
    assert "bookingid" in corpo[0]


def test_tc010_fluxo_completo_de_reserva(client_autenticado, payloads):
    """TC-010 | Fluxo completo: criação → consulta → exclusão → confirmação."""
    resposta_criacao = client_autenticado.create_booking(payloads["valido"])
    assert resposta_criacao.status_code == 200

    booking_id = resposta_criacao.json()["bookingid"]

    resposta_consulta = client_autenticado.get_booking(booking_id)
    assert resposta_consulta.status_code == 200

    resposta_exclusao = client_autenticado.delete_booking(booking_id)
    assert resposta_exclusao.status_code == 201

    resposta_pos_exclusao = client_autenticado.get_booking(booking_id)
    assert resposta_pos_exclusao.status_code == 404


def test_tc011_autenticacao_com_credenciais_invalidas(client):
    """TC-011 | POST /auth com senha incorreta não retorna token."""
    resposta = client.create_token("admin", "senha_errada")
    corpo = resposta.json()

    assert "token" not in corpo


def test_tc012_consulta_de_reserva_inexistente(client):
    """TC-012 | GET /booking/{id} com ID inexistente retorna 404."""
    resposta = client.get_booking(999999)

    assert resposta.status_code == 404
