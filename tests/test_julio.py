import pytest


def test_tc003_criar_reserva_com_dados_validos(
    client_autenticado,
    payloads
):
    payload = payloads["valido"]

    resposta = client_autenticado.create_booking(payload)

    assert resposta.status_code == 200

    corpo = resposta.json()

    assert "bookingid" in corpo
    assert isinstance(corpo["bookingid"], int)

    assert "booking" in corpo
    assert corpo["booking"] == payload

    client_autenticado.delete_booking(corpo["bookingid"])


def test_tc004_consultar_reserva_existente(
    client,
    booking_criado
):
    booking_id = booking_criado["bookingid"]
    booking_esperado = booking_criado["booking"]

    resposta = client.get_booking(booking_id)

    assert resposta.status_code == 200
    assert resposta.json() == booking_esperado


@pytest.mark.negativo
def test_tc013_consultar_com_identificador_invalido(client):
    resposta = client.get_booking("abc")

    assert resposta.status_code not in range(200, 300)


@pytest.mark.negativo
def test_tc014_criar_reserva_com_dados_incompletos(
    client,
    payloads
):
    payload = payloads["incompleto"]

    resposta = client.create_booking(payload)

    assert resposta.status_code not in range(200, 300)


@pytest.mark.negativo
def test_tc015_criar_reserva_com_tipos_inadequados(
    client,
    payloads
):
    payload = payloads["tipos_incorretos"]

    resposta = client.create_booking(payload)

    assert resposta.status_code not in range(200, 300)