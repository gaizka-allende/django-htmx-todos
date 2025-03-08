from datetime import datetime
from playwright.sync_api import expect
import django
from django.conf import settings
from django.template.loader import get_template
from django.contrib.auth.hashers import make_password

settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['todos/templates'],
}], INSTALLED_APPS=['django.contrib.humanize'])
django.setup()

def test_account_form_display(page):
    def handle_account_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('account.html').render({
                    'screen': True,
                    'username': 'testuser'
                })
            )
        else:
            route.fallback()
    page.route("**/account", handle_account_route)
    
    page.goto("http://localhost:3000/account")
    
    # Verify form elements are present
    expect(page.get_by_text("Account")).to_be_visible()
    expect(page.get_by_label("Username")).to_be_visible()
    expect(page.get_by_label("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Save")).to_be_visible()
    
    # Verify username is pre-filled
    expect(page.get_by_label("Username")).to_have_value("testuser")

def test_account_update_success(page):
    def handle_account_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('account.html').render({
                    'screen': True,
                    'username': 'testuser'
                })
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('account.html').render({
                    'screen': True,
                    'username': 'newuser',
                    'success_message': 'Account updated successfully'
                })
            )
    page.route("**/account", handle_account_route)
    
    page.goto("http://localhost:3000/account")
    
    # Update username and password
    page.get_by_label("Username").fill("newuser")
    page.get_by_label("Password").click()  # Focus to clear dots
    page.get_by_label("Password").fill("newpassword")
    
    # Submit form
    page.get_by_role("button", name="Save").click()
    
    # Verify success message
    expect(page.get_by_text("Account updated successfully")).to_be_visible()
    
    # Verify form is still present with updated username
    expect(page.get_by_label("Username")).to_have_value("newuser")

def test_account_username_exists_error(page):
    def handle_account_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('account.html').render({
                    'screen': True,
                    'username': 'testuser'
                })
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=400,
                content_type='text/plain',
                body='Username already exists'
            )
    page.route("**/account", handle_account_route)
    
    page.goto("http://localhost:3000/account")
    
    # Try to update to existing username
    page.get_by_label("Username").fill("existinguser")
    page.get_by_role("button", name="Save").click()
    
    # Verify error message
    expect(page.get_by_text("Username already exists")).to_be_visible()

def test_password_field_behavior(page):
    def handle_account_route(route):
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('account.html').render({
                'screen': True,
                'username': 'testuser'
            })
        )
    page.route("**/account", handle_account_route)
    
    page.goto("http://localhost:3000/account")
    
    # Click to focus should clear the field
    page.get_by_label("Password").click()
    expect(page.get_by_label("Password")).to_have_value("")
    
    # Blur without typing should restore a non-empty value
    page.get_by_label("Username").click()  # Click away to blur
    expect(page.get_by_label("Password")).not_to_have_value("")
    
    # Type new password
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill("newpassword")
    page.get_by_label("Username").click()  # Click away to blur
    expect(page.get_by_label("Password")).to_have_value("newpassword") 