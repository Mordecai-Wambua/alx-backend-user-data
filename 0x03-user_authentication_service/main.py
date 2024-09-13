#!/usr/bin/env python3
"""Function to validate the response's expected status code and payload."""
import requests


def register_user(email: str, password: str) -> None:
    """Query for register_user end-point."""
    url = 'http://127.0.0.1:5000/users'
    body = {'email': email, 'password': password}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    response = requests.post(url, data=body)
    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Query for log_in_wrong_password end-point."""
    url = 'http://127.0.0.1:5000/sessions'
    body = {'email': email, 'password': password}
    response = requests.post(url, data=body)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Query for log_in end-point."""
    url = 'http://127.0.0.1:5000/sessions'
    body = {'email': email, 'password': password}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Query for profile_unlogged end-point."""
    url = 'http://127.0.0.1:5000/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Query for profile_logged end-point."""
    url = 'http://127.0.0.1:5000/profile'
    cookie_dict = {'session_id': session_id}
    response = requests.get(url, cookies=cookie_dict)
    assert response.status_code == 200
    assert 'email' in response.json()


def log_out(session_id: str) -> None:
    """Query for log_out end-point."""
    url = 'http://127.0.0.1:5000/sessions'
    cookie_dict = {'session_id': session_id}
    response = requests.delete(url, cookies=cookie_dict)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Query for reset_password_token end-point."""
    url = 'http://127.0.0.1:5000/reset_password'
    body = {'email': email}
    response = requests.post(url, data=body)
    assert response.status_code == 200
    assert response.json()['email'] == email
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Query for update_password end-point."""
    url = 'http://127.0.0.1:5000/reset_password'
    body = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(url, data=body)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
