from playwright.sync_api import expect

def test_successful_login(page):
    page.goto("http://localhost:8000")
    expect(page).to_have_title("Login")
    
    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="text/html",
            body='<div id="screen"><h1>Todos</h1></div>'
        )
    page.route("**/login", handle_route)

    page.get_by_label("username", exact=False).press_sequentially("success_login")
    page.get_by_label("password", exact=False).press_sequentially("success_password")
    page.get_by_role("button", name="login", exact=False).click()

    expect(page).to_have_title("Todos", timeout=10000)
    page.wait_for_selector("text=Todos")

def test_unsuccessful_login(page):

    page.goto("http://localhost:8000/")
    expect(page).to_have_title("Login")
    
    def handle_route(route):
        route.fulfill(
            status=401,
            content_type="text/html",
            body='Invalid username or password'
        )
    page.route("**/login", handle_route)

    page.get_by_label("username", exact=False).press_sequentially("failed_login")
    page.get_by_label("password", exact=False).press_sequentially("failed_password")
    page.get_by_role("button", name="login", exact=False).click()
    page.wait_for_selector("text=Invalid username or password")

def test_successful_login_second_attempt(page):

    page.goto("http://localhost:8000/")
    expect(page).to_have_title("Login")

    def handle_route(route):
        route.fulfill(
            status=401,
            content_type="text/html",
            body='Invalid username or password'
        )
    page.route("**/login", handle_route)
    
    page.get_by_label("username", exact=False).press_sequentially("failed_login")
    
    page.get_by_label("password", exact=False).press_sequentially("failed_password")
    
    page.get_by_role("button", name="login", exact=False).click()
    
    page.wait_for_selector("text=Invalid username or password")

    def handle_route(route):
        route.fulfill(
            status=200,
            content_type="text/html",
            body='<div id="screen"><h1>Todos</h1></div>'
        )
    page.route("**/login", handle_route)

    page.get_by_label("username", exact=False).clear()
    page.get_by_label("username", exact=False).press_sequentially("success_login")
    
    page.get_by_label("password", exact=False).clear()
    page.get_by_label("password", exact=False).press_sequentially("success_password")
    
    page.get_by_role("button", name="login", exact=False).click()
    
    page.wait_for_selector("text=Todos")

def test_ensure_button_and_input_are_disabled_when_submitting(page):

    page.goto("http://localhost:8000/")
    expect(page).to_have_title("Login")

    def handle_route(route):
        # Add delay to simulate network latency
        page.wait_for_timeout(1000)  # 1 second delay
        route.fulfill(
            status=200,
            content_type="text/html",
            body='<div id="screen"><h1>Todos</h1></div>'
        )
    page.route("**/login", handle_route)

    page.get_by_label("username", exact=False).press_sequentially("success_login")
    page.get_by_label("password", exact=False).press_sequentially("success_password")
    
    expect(page.get_by_role("button", name="login", exact=False)).to_be_enabled()
    page.get_by_role("button", name="login", exact=False).click()
    
    expect(page.get_by_role("button", name="login", exact=False)).to_be_disabled()
    
    page.wait_for_selector("text=Todo")
