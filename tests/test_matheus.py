def test_tc005_atualizacao_completa_da_reserva(client,client_autenticado,booking_criado):
    """TC-005 | Atualização completa de uma reserva utilizando PUT."""

    booking_id = booking_criado["bookingid"]

    payload_atualizado = {
        "firstname": "Matheus",
        "lastname": "Reis",
        "totalprice": 500,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05",
        },
        "additionalneeds": "Cafe da tarde"
    }

    resposta = client_autenticado.update_booking(
        booking_id,
        payload_atualizado
    )

    assert resposta.status_code == 200

    resposta_consulta = client.get_booking(booking_id)

    assert resposta_consulta.status_code == 200
    assert resposta_consulta.json() == payload_atualizado

def test_tc006_atualizacao_parcial_da_reserva(client,client_autenticado,booking_criado,payloads):
    """TC-006 | Atualização parcial da reserva utilizando PATCH."""

    booking_id = booking_criado["bookingid"]

    payload_atualizado = {
        "firstname": "Matheus",
    }

    resposta = client_autenticado.partial_update_booking(
        booking_id,
        payload_atualizado
    )

    assert resposta.status_code == 200

    resposta_consulta = client.get_booking(booking_id)

    assert resposta_consulta.status_code == 200

    reserva_atualizada = resposta_consulta.json()

    assert reserva_atualizada["firstname"] == "Matheus"
    assert reserva_atualizada["lastname"] == payloads["valido"]["lastname"]
    assert reserva_atualizada["totalprice"] == payloads["valido"]["totalprice"]
    assert reserva_atualizada["depositpaid"] == payloads["valido"]["depositpaid"]
    assert reserva_atualizada["bookingdates"] == payloads["valido"]["bookingdates"]
    assert reserva_atualizada["additionalneeds"] == payloads["valido"]["additionalneeds"]

def test_tc016_atualizacao_completa_sem_autenticacao(client,client_autenticado,booking_criado,payloads):
    """TC-016 | Atualização completa de uma reserva sem autenticação."""

    booking_id = booking_criado["bookingid"]

    payload_atualizado = {
        "firstname": "Matheus",
        "lastname": "Reis",
        "totalprice": 500,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05",
        },
        "additionalneeds": "Cafe da tarde"
    }

    resposta = client_autenticado.update_booking(
        booking_id,
        payload_atualizado,
        auth=False
    )

    assert resposta.status_code == 403

    resposta_consulta = client.get_booking(booking_id)

    assert resposta_consulta.status_code == 200
    assert resposta_consulta.json() == payloads["valido"]

def test_tc017_atualizacao_parcial_sem_autenticacao(client,client_autenticado,booking_criado,payloads):
    """TC-017 | Atualização parcial de uma reserva sem autenticação."""

    booking_id = booking_criado["bookingid"]

    payload_atualizado = {
        "firstname": "Matheus",
    }

    resposta = client_autenticado.partial_update_booking(
        booking_id,
        payload_atualizado,
        auth=False
    )

    assert resposta.status_code == 403

    resposta_consulta = client.get_booking(booking_id)

    assert resposta_consulta.status_code == 200
    assert resposta_consulta.json() == payloads["valido"]

def test_tc019_atualizacao_de_reserva_inexistente(client_autenticado,id_inexistente):
    """TC-019 | Atualização de uma reserva com ID inexistente."""

    payload_atualizado = {
        "firstname": "Matheus",
        "lastname": "Reis",
        "totalprice": 500,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2026-12-01",
            "checkout": "2026-12-05",
        },
        "additionalneeds": "Cafe da tarde"
    }

    resposta = client_autenticado.update_booking(
        id_inexistente,
        payload_atualizado
    )

    assert resposta.status_code == 405