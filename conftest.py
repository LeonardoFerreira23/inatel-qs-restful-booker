import json
import os
from pathlib import Path

import pytest

from utils.api_client import BookerClient

DATA_DIR = Path(__file__).parent / "data"

USERNAME = os.getenv("BOOKER_USER", "admin")
PASSWORD = os.getenv("BOOKER_PASS", "password123")


def carregar_dados(nome):
    with open(DATA_DIR / nome, encoding="utf-8") as arquivo:
        return json.load(arquivo)


@pytest.fixture(scope="session")
def payloads():
    return carregar_dados("bookings.json")


@pytest.fixture(scope="session")
def token():
    resposta = BookerClient().create_token(USERNAME, PASSWORD)
    assert resposta.status_code == 200, "Falha ao autenticar no setup da suite"
    return resposta.json()["token"]


@pytest.fixture
def client():
    return BookerClient()


@pytest.fixture
def client_autenticado(token):
    return BookerClient(token=token)


@pytest.fixture
def booking_criado(client_autenticado, payloads):
    resposta = client_autenticado.create_booking(payloads["valido"])
    assert resposta.status_code == 200, "Nao foi possivel criar a reserva de apoio"
    corpo = resposta.json()

    yield corpo

    client_autenticado.delete_booking(corpo["bookingid"])
