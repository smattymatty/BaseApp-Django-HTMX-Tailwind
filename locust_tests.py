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


class BlogUser(HttpUser):
    wait_time = between(1, 5)  # Simulate user think time

    @task(1)
    def basic_blog_post_list(self):
        # Get the first page (default)
        self.client.post("/blog/blog-post-list/", data={"page": 1})

    @task(2)
    def next_page_blog_post_list(self):
        # Get a subsequent page
        self.client.post("/blog/blog-post-list/", data={"page": 2})

    @task(3)
    def search_blog_posts(self):
        search_term = "western"  # Or generate random search terms
        self.client.post("/blog/blog-post-list/",
                         data={"page": 1, "search_query": search_term})

    @task(4)
    def search_blog_posts_with_pagination(self):
        search_term = "black"  # Or generate random search terms
        self.client.post("/blog/blog-post-list/",
                         data={"page": 2, "search_query": search_term})
