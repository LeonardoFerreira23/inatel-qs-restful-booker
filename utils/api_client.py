import os

import requests

BASE_URL = os.getenv("BOOKER_BASE_URL", "https://restful-booker.herokuapp.com")
TIMEOUT = int(os.getenv("BOOKER_TIMEOUT", "15"))


class BookerClient:
    def __init__(self, base_url=BASE_URL, token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _url(self, path):
        return f"{self.base_url}{path}"

    def _headers(self, auth=False):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if auth and self.token:
            headers["Cookie"] = f"token={self.token}"
        return headers

    def ping(self):
        return requests.get(self._url("/ping"), timeout=TIMEOUT)

    def create_token(self, username, password):
        return requests.post(
            self._url("/auth"),
            json={"username": username, "password": password},
            headers=self._headers(),
            timeout=TIMEOUT,
        )

    def get_booking_ids(self, params=None):
        return requests.get(self._url("/booking"), params=params, timeout=TIMEOUT)

    def get_booking(self, booking_id):
        return requests.get(
            self._url(f"/booking/{booking_id}"),
            headers=self._headers(),
            timeout=TIMEOUT,
        )

    def create_booking(self, payload):
        return requests.post(
            self._url("/booking"),
            json=payload,
            headers=self._headers(),
            timeout=TIMEOUT,
        )

    def update_booking(self, booking_id, payload, auth=True):
        return requests.put(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            headers=self._headers(auth=auth),
            timeout=TIMEOUT,
        )

    def partial_update_booking(self, booking_id, payload, auth=True):
        return requests.patch(
            self._url(f"/booking/{booking_id}"),
            json=payload,
            headers=self._headers(auth=auth),
            timeout=TIMEOUT,
        )

    def delete_booking(self, booking_id, auth=True):
        return requests.delete(
            self._url(f"/booking/{booking_id}"),
            headers=self._headers(auth=auth),
            timeout=TIMEOUT,
        )
