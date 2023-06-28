from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", {"email": "admin@irontemple.com"})

    @task
    def book(self):
        club = "Iron Temple"
        competition = "Fall Classic2"
        self.client.get(f"/book/{competition}/{club}")

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", {"competition": "Fall Classic2", "club": "Iron Temple", "places": "5"})

    @task
    def logout(self):
        self.client.get("/logout")
