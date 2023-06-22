import sys
import os
import pytest

import server

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


@pytest.mark.parametrize("email", ['admin@irontemple.com', 'false@adress.com'])
def test_should_status_code_200(client, email):
    response = client.post('/showSummary', data={
        'email': email
    })
    expected_value = 200
    assert response.status_code == expected_value


def test_should_show_error(client):
    '''
    Tests an error is shown if email provided is unknown.
    '''
    email = 'false@adress.com'
    response = client.post('/showSummary', data={
        'email': email
    })
    expected_value = 'The email address provided does not exist'
    assert expected_value in response.data.decode()


def test_should_raise_index_error():
    email = 'false@adress.com'
    with pytest.raises(IndexError):
        #raise IndexError
        club = server.get_club_by_email(email)


