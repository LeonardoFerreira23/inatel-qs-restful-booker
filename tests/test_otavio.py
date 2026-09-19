import pytest


def test_tc007_reserva_criada_e_consultavel_por_id(client, booking_criado, payloads):
    """TC-007 | Reserva criada via POST persiste e GET /booking/{id} retorna os mesmos dados."""
    booking_id = booking_criado["bookingid"]

    resposta = client.get_booking(booking_id)

    assert resposta.status_code == 200
    assert resposta.json() == payloads["valido"]


def test_tc008_reserva_criada_aparece_na_listagem(client, booking_criado, payloads):
    """TC-008 | Reserva criada aparece em GET /booking ao filtrar por nome e sobrenome."""
    booking_id = booking_criado["bookingid"]
    filtros = {
        "firstname": payloads["valido"]["firstname"],
        "lastname": payloads["valido"]["lastname"],
    }

    resposta = client.get_booking_ids(params=filtros)
    ids = [item["bookingid"] for item in resposta.json()]

    assert resposta.status_code == 200
    assert booking_id in ids


def test_tc009_exclusao_com_token_valido(client_autenticado, booking_criado):
    """TC-009 | DELETE /booking/{id} com token válido retorna 201 e a reserva deixa de existir."""
    booking_id = booking_criado["bookingid"]

    resposta_exclusao = client_autenticado.delete_booking(booking_id)
    resposta_consulta = client_autenticado.get_booking(booking_id)

    assert resposta_exclusao.status_code == 201
    assert resposta_consulta.status_code == 404


@pytest.mark.auth
@pytest.mark.negativo
def test_tc018_exclusao_sem_autenticacao(client_autenticado, booking_criado):
    """TC-018 | DELETE /booking/{id} sem token retorna 403 e a reserva é preservada."""
    booking_id = booking_criado["bookingid"]

    resposta_exclusao = client_autenticado.delete_booking(booking_id, auth=False)
    resposta_consulta = client_autenticado.get_booking(booking_id)

    assert resposta_exclusao.status_code == 403
    assert resposta_consulta.status_code == 200


@pytest.mark.negativo
def test_tc020_exclusao_de_reserva_inexistente(client_autenticado, id_inexistente):
    """TC-020 | DELETE /booking/{id} com ID inexistente é rejeitado com 405.

    O esperado numa API REST seria 404, mas a Restful Booker responde 405
    (defeito registrado no README). O teste valida o comportamento real.
    """
    resposta = client_autenticado.delete_booking(id_inexistente)

    assert resposta.status_code == 405
