import pytest

from bs4 import BeautifulSoup

import server


@pytest.mark.parametrize("email", ['admin@irontemple.com', 'false@adress.com'])
def test_should_status_code_200(client, email):
    response = client.post('/showSummary', data={
        'email': email
    })
    expected_value = 200
    assert response.status_code == expected_value


def test_should_show_error(client):
    """
    Tests an error is shown if email provided is unknown.
    """
    email = 'false@adress.com'
    response = client.post('/showSummary', data={
        'email': email
    })
    expected_value = 'The email address provided does not exist'
    assert expected_value in response.data.decode()


def test_should_raise_index_error(client):
    email = 'false@adress.com'
    with pytest.raises(IndexError):
        client.post('/showSummary', data={
            'email': email
        })


@pytest.mark.xfail(raises=IndexError)
def test_should_raise_index_error2(client):
    email = 'false@adress.com'
    client.post('/showSummary', data={
        'email': email
    })


class MockCompetition:
    @staticmethod
    def get_info():
        return


def test_should_check_max_input(mocker, client):
    club = {
        "name": "Club Mock",
        "email": "Email Mock",
        "points": "5"
    }
    competition = {
        "name": "Competition Mock",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "25"
    }
    mock_clubs = [club]
    mock_competitions = [competition]
    mocker.patch.object(server, 'clubs', mock_clubs)
    mocker.patch.object(server, 'competitions', mock_competitions)

    response = client.get(f'/book/{competition["name"]}/{club["name"]}')
    response_soup = BeautifulSoup(response.data.decode(), 'html.parser')
    input_field = response_soup.find("input", {"name": "places"})
    input_max_places = input_field.attrs["max"]

    expected_result = 5

    assert int(input_max_places) == expected_result
