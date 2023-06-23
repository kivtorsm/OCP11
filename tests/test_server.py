import pytest
import datetime

from bs4 import BeautifulSoup

import server


class TestShowSummary:
    @pytest.mark.parametrize("email", ['admin@irontemple.com', 'false@adress.com'])
    def test_should_status_code_200_and_error_message_if_unknown_email(self, client, email):
        response = client.post('/showSummary', data={
            'email': email
        })
        expected_value = 200
        assert response.status_code == expected_value
        if email == 'false@adress.com':
            assert 'The email address provided does not exist' in response.data.decode()


def test_should_raise_index_error():
    email = 'false@adress.com'
    with pytest.raises(IndexError):
        club = server.get_club_by_email(email)


@pytest.fixture
def club(request):
    clubs = [{
        "name": "Club Mock",
        "email": "Email Mock",
        "points": "5"
    }, {
        "name": "Club Mock",
        "email": "Email Mock",
        "points": "13"
    }
    ]
    return clubs[request.param]


@pytest.fixture
@pytest.mark.parametrize("club", [0, 1], indirect=['club'])
def clubs(club):
    clubs = [club]
    return clubs


@pytest.fixture
def competition(request):
    competitions = [{
        "name": "Competition Mock",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "25"
    }, {
        "name": "Competition Mock",
        "date": "2024-10-22 13:30:00",
        "numberOfPlaces": "24"
    }]
    return competitions[request.param]


@pytest.fixture
@pytest.mark.parametrize("competition", [0, 1], indirect=['competition'])
def competitions(competition):
    competitions = [competition]
    return competitions


@pytest.mark.parametrize("club, competition", [(0, 0)], indirect=['club', 'competition'])
def test_should_validate_point_and_places_substraction(mocker, client, club, competition, clubs, competitions):
    mocker.patch.object(server, 'clubs', clubs)
    mocker.patch.object(server, 'competitions', competitions)
    response = client.post('/purchasePlaces', data={
        "places": "5",
        "competition": competition["name"],
        "club": club["name"],
    })
    expected_result_points = 0
    expected_result_places = 20
    assert int(club["points"]) == expected_result_points
    assert int(competition["numberOfPlaces"]) == expected_result_places


class TestBook():
    @pytest.mark.parametrize("club,competition", [(0, 1), (1, 1)], indirect=['club', 'competition'])
    def test_should_check_max_input(self, mocker, client, club, competition, clubs, competitions):
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        print(club)
        print(clubs)

        response = client.get(f'/book/{competition["name"]}/{club["name"]}')
        response_soup = BeautifulSoup(response.data.decode(), 'html.parser')
        print(response_soup)
        input_field = response_soup.find("input", {"name": "places"})
        print(input_field)
        input_max_places = input_field.attrs["max"]
        print(input_max_places)
        expected_result = min(12, int(club['points']))

        assert int(input_max_places) == expected_result

    @pytest.mark.parametrize(
        "club, competition, expected",
        [(0, 0, "You can&#39;t book events in the past"),
         (0, 1, "Perfect. Go on.")],
        indirect=['club', 'competition'])
    def test_booking_events_should_show_message_and_status_code_200(
            self, client, mocker, club, competition, clubs, competitions, expected):
        """
        Tests an error is shown if trying to book an event in the past.
        """
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')
        assert expected in response.data.decode('unicode_escape')
        assert response.status_code == 200


