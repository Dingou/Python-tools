from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        self.client.post("/login", {"username":"leo.feng@ylly.com", "password":"2528548fs123"})

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def js1(self):
        self.client.get("/static/web/js/analytics-event-tracking.js")

    @task(1)
    def js2(self):
        self.client.get("/static/web/rs-plugin/js/extensions/revolution.extension.navigation.min.js")

    @task(1)
    def jpg1(self):
        self.client.get("/media/uploads/1.29-%E5%8A%A0%E5%8B%92%E6%AF%94%E4%B8%93%E9%A2%98_154924.jpg")

    @task(1)
    def jpg2(self):
        self.client.get("/media/uploads/3.31-%E5%8A%A0%E5%8B%92%E6%AF%94_425473.jpg")

    @task(1)
    def css1(self):
        self.client.get("/static/webpack/basePage.04923578cb5624160d2f.css")

    @task(1)
    def css2(self):
        self.client.get("/static/webpack/common.04923578cb5624160d2f.css")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000