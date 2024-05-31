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
        # Get CSRF token on session start
        response = self.client.get("/blog/")
        self.csrf_token = response.cookies['csrftoken']

    @task(1)
    def basic_blog_post_list(self):
        self.client.post("/blog/blog-post-list/",
                         data={"page": 1}, headers={"X-CSRFToken": self.csrf_token})

    @task(2)
    def next_page_blog_post_list(self):
        self.client.post("/blog/blog-post-list/",
                         data={"page": 2}, headers={"X-CSRFToken": self.csrf_token})

    @task(3)
    def search_blog_posts(self):
        search_term = Faker().word()
        print(search_term)
        self.client.post("/blog/blog-post-list/", data={
                         "page": 1, "search_query": search_term}, headers={"X-CSRFToken": self.csrf_token})

    @task(4)
    def next_page_search_blog_posts(self):
        search_term = Faker().word()
        print(search_term)
        self.client.post("/blog/blog-post-list/", data={
                         "page": 2, "search_query": search_term}, headers={"X-CSRFToken": self.csrf_token})
