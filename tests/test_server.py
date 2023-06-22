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


@pytest.fixture
def club(request):
    clubs = [{
        "name": "Club Mock",
        "email": "Email Mock",
        "points": "5"
    },
    {
        "name": "Club Mock",
        "email": "Email Mock",
        "points": "13"
    }
    ]
    return clubs[request.param]


@pytest.fixture
def club2():
    club = {
        "name": "Club Mock",
        "email": "Email Mock",
        "points": "13"
    }
    return club


@pytest.fixture
@pytest.mark.parametrize("club", [0, 1], indirect=True)
def clubs(club):
    clubs = [club]
    return clubs


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


@pytest.mark.parametrize("club", [0, 1], indirect=True)
def test_should_check_max_input(mocker, client, club, competition, clubs, competitions):
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'competitions', competitions)
    print(club)
    print(clubs)

    response = client.get(f'/book/{competition["name"]}/{club["name"]}')
    response_soup = BeautifulSoup(response.data.decode(), 'html.parser')
    input_field = response_soup.find("input", {"name": "places"})
    print(input_field)
    input_max_places = input_field.attrs["max"]
    print(input_max_places)
    expected_result = min(12, int(club['points']))

    assert int(input_max_places) == expected_result


@pytest.mark.parametrize("club", [0], indirect=True)
def test_should_validate_point_and_places_substraction(mocker, client, club, competition, clubs, competitions):

    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'competitions', competitions)
    response = client.post('/purchasePlaces', data={
        "places": "5",
        "competition": competition["name"],
        "club": club["name"],
    })
    print(response.data.decode())
    expected_result_points = 0
    expected_result_places = 20
    assert int(club["points"]) == expected_result_points
    assert int(competition["numberOfPlaces"]) == expected_result_places
