from playwright.sync_api import expect
from django.template.loader import get_template

def test_successful_login(page):
    def handle_login_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('login.html').render({}) 
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True}) 
            )
        else:
            route.fallback()
            return

    page.route("**/login", handle_login_route)
    
    page.goto("http://localhost:3000/login")
    expect(page).to_have_title("Login")

    page.get_by_label("username", exact=False).press_sequentially("success_login")
    page.get_by_label("password", exact=False).press_sequentially("success_password")
    page.get_by_role("button", name="login", exact=False).click()

    expect(page).to_have_title("Todos", timeout=10000)
    page.wait_for_selector("text=Todos")

def test_unsuccessful_login(page):
    def handle_login_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('login.html').render({}) 
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=401,
                content_type='text/html',
                body='Invalid username or password'
            )
        else:
            route.fallback()
            return
    page.route("**/login", handle_login_route)

    page.goto("http://localhost:3000/login")
    expect(page).to_have_title("Login")

    page.get_by_label("username", exact=False).press_sequentially("failed_login")
    page.get_by_label("password", exact=False).press_sequentially("failed_password")
    page.get_by_role("button", name="login", exact=False).click()
    page.wait_for_selector("text=Invalid username or password")


def test_successful_login_second_attempt(page):
    def handle_login_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('login.html').render({}) 
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=401,
                content_type='text/html',
                body='Invalid username or password'
            )
        else:
            route.fallback()
            return
    page.route("**/login", handle_login_route)


    page.goto("http://localhost:8000/login")
    expect(page).to_have_title("Login")
    
    page.get_by_label("username", exact=False).press_sequentially("failed_login")
    page.get_by_label("password", exact=False).press_sequentially("failed_password")
    page.get_by_role("button", name="login", exact=False).click()
    page.wait_for_selector("text=Invalid username or password")

    def handle_login_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('login.html').render({}) 
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True}) 
            )
        else:
            route.fallback()
            return
    page.route("**/login", handle_login_route)   

    page.get_by_label("username", exact=False).clear()
    page.get_by_label("username", exact=False).press_sequentially("success_login")
    
    page.get_by_label("password", exact=False).clear()
    page.get_by_label("password", exact=False).press_sequentially("success_password")
    
    page.get_by_role("button", name="login", exact=False).click()
    
    page.wait_for_selector("text=Todos")

def test_ensure_button_and_input_are_disabled_when_submitting(page):
    def handle_login_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('login.html').render({}) 
            )
        elif route.request.method == 'POST':
            page.wait_for_timeout(1000)  # 1 second delay
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True}) 
            )
        else:
            route.fallback()
            return
    page.route("**/login", handle_login_route)   

    page.goto("http://localhost:8000/login")
    expect(page).to_have_title("Login")

    page.get_by_label("username", exact=False).press_sequentially("success_login")
    page.get_by_label("password", exact=False).press_sequentially("success_password")
    
    expect(page.get_by_role("button", name="login", exact=False)).to_be_enabled()
    page.get_by_role("button", name="login", exact=False).click()
    
    expect(page.get_by_role("button", name="login", exact=False)).to_be_disabled()
    
    page.wait_for_selector("text=Todo")

def test_login_error(page):
    def handle_login_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('login.html').render({'screen': True})
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=404,
                content_type='text/html',
                body='Invalid username or password'
            )
    page.route("**/login", handle_login_route)
    
    page.goto("http://localhost:3000/login")
    
    # Try to login with invalid credentials
    page.get_by_label("Username").fill("wronguser")
    page.get_by_label("Password").fill("wrongpass")
    page.get_by_role("button", name="Login").click()
    
    expect(page.get_by_text("Invalid username or password")).to_be_visible()
