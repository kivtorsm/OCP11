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


def test_should_raise_index_error():
    email = 'false@adress.com'
    with pytest.raises(IndexError):
        #raise IndexError
        club = server.get_club_by_email(email)


class MockCompetition:
    @staticmethod
    def get_info():
        return


@pytest.fixture
def club():
    club = {
        "name": "Club Mock",
        "email": "Email Mock",
        "points": "5"
    }
    return club


@pytest.fixture
def competition():
    competition = {
        "name": "Competition Mock",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "25"
    }
    return competition

@pytest.fixture
def competitions(competition):
    competitions = [competition]
    return competitions


@pytest.fixture
def clubs(club):
    clubs = [club]
    return clubs


def test_should_check_max_input(mocker, client, club, competition, clubs, competitions):
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'competitions', competitions)
    print(club)
    print(clubs)

    response = client.get(f'/book/{competition["name"]}/{club["name"]}')
    response_soup = BeautifulSoup(response.data.decode(), 'html.parser')
    input_field = response_soup.find("input", {"name": "places"})
    input_max_places = input_field.attrs["max"]
    print(input_max_places)
    expected_result = 5

    assert int(input_max_places) == expected_result


def test_should_validate_point_substraction(mocker, client, club, competition, clubs, competitions):

    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'competitions', competitions)
    response = client.post('/purchasePlaces', data={
        "places": "5",
        "competition": competition["name"],
        "club": club["name"],
    })
    print(response.data.decode())
    expected_result = 0
    assert int(club["points"]) == expected_result
