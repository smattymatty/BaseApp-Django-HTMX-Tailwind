from locust import HttpUser, task, between
from faker import Faker


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def home_page(self):
        self.client.get("/base/home/")  # Relative path

    @task(2)
    def ui_elements_page(self):
        self.client.get("/base/ui-elements/")  # Relative path

    # ... other tasks


class BlogUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.get("/blog/")
        if response.status_code == 200:
            self.csrf_token = response.cookies.get('csrftoken')
        else:
            self.csrf_token = None

    @task(1)
    def basic_blog_post_list(self):
        if self.csrf_token:
            response = self.client.post("/blog/blog-post-list/",
                                        data={"page": 1},
                                        headers={"X-CSRFToken": self.csrf_token})
            if response.status_code != 200:
                print(
                    f"Failed POST /blog/blog-post-list/: {response.status_code} - {response.text}")

    @task(2)
    def next_page_blog_post_list(self):
        if self.csrf_token:
            response = self.client.post("/blog/blog-post-list/",
                                        data={"page": 2},
                                        headers={"X-CSRFToken": self.csrf_token})
            if response.status_code != 200:
                print(
                    f"Failed POST /blog/blog-post-list/: {response.status_code} - {response.text}")

    @task(3)
    def search_blog_posts(self):
        if self.csrf_token:
            search_term = Faker().word()
            response = self.client.post("/blog/blog-post-list/",
                                        data={"page": 1,
                                              "search_query": search_term},
                                        headers={"X-CSRFToken": self.csrf_token})
            if response.status_code != 200:
                print(
                    f"Failed POST /blog/blog-post-list/: {response.status_code} - {response.text}")

    @task(4)
    def next_page_search_blog_posts(self):
        if self.csrf_token:
            search_term = Faker().word()
            response = self.client.post("/blog/blog-post-list/",
                                        data={"page": 2,
                                              "search_query": search_term},
                                        headers={"X-CSRFToken": self.csrf_token})
            if response.status_code != 200:
                print(
                    f"Failed POST /blog/blog-post-list/: {response.status_code} - {response.text}")
