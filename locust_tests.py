from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def home_page(self):
        self.client.get("/base/home/")  # Relative path

    @task(2)
    def ui_elements_page(self):
        self.client.get("/base/ui-elements/")  # Relative path

    # ... other tasks
