from datetime import datetime, timedelta
from playwright.sync_api import expect
import django
from django.conf import settings
from django.template.loader import get_template

settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['todos/templates'],
}], INSTALLED_APPS=['django.contrib.humanize'])
django.setup()

def test_select_suggestion(page):
    def handle_todos_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True, 'uncompletedTodos': [], 'uncompletedTodosCount': 0, 'completedTodos': [], 'completedTodosCount': 0}) 
            )
        else:
            route.fallback()
            return
    page.route("**/todos", handle_todos_route)
    
    def handle_suggestions_route(route):
        if route.request.method != 'GET':
            route.fallback()
            return
            
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('suggestions.html').render({
                'suggestions': [
                    [
                        {'text': ''},
                        {'text': 'Buy', 'highlight': True},
                        {'text': ' coffee'}
                    ],
                    [
                        {'text': ''},
                        {'text': 'Buy', 'highlight': True},
                        {'text': ' milk'}
                    ]
                ]
            })
        )
    page.route("**/suggestions**", handle_suggestions_route)

    def handle_todo_route(route):
        if route.request.method != 'POST':
            route.fallback()
            return
            
        route.fulfill(
            status=200,
            content_type='application/text',
            body=get_template('todo.html').render({'todo': {'title': 'buy milk', 'id': '5d686f21-8775-42c6-ae9a-2cd88bdfb6d2', 'completed': 0, 'created_modified': datetime.now()}})
        )
    page.route("**/todo", handle_todo_route)
    
    page.goto("http://localhost:3000/todos")
    
    # Type "buy" in the input field
    page.get_by_test_id("add-todo").press_sequentially("buy")
    
    # Wait for and verify suggestions
    expect(page.get_by_text("Buy coffee")).to_be_visible()
    expect(page.get_by_text("Buy milk")).to_be_visible()
    
    # Click on "Buy coffee" suggestion
    page.get_by_text("Buy milk").click()
    
    # Verify the input field was populated
    expect(page.get_by_test_id("add-todo")).to_have_value("Buy milk")
    
    # Submit the todo
    page.get_by_test_id("add-todo").press("Enter")
    
    # Verify the todo was added to the list
    todo_item = page.get_by_test_id("todo-item-input").first
    expect(page.get_by_test_id("todo-item-input")).to_have_value("buy milk")

def test_suggestions_hide_on_click_outside(page):
    # Set up the same route handlers as in test_select_suggestion
    def handle_todos_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True, 'uncompletedTodos': [], 'uncompletedTodosCount': 0, 'completedTodos': [], 'completedTodosCount': 0}) 
            )
        else:
            route.fallback()
            return
    page.route("**/todos", handle_todos_route)
    
    def handle_suggestions_route(route):
        if route.request.method != 'GET':
            route.fallback()
            return
            
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('suggestions.html').render({
                'suggestions': [
                    [
                        {'text': ''},
                        {'text': 'Buy', 'highlight': True},
                        {'text': ' coffee'}
                    ]
                ]
            })
        )
    page.route("**/suggestions**", handle_suggestions_route)
    
    page.goto("http://localhost:3000/todos")
    
    # Type "buy" in the input field to trigger suggestions
    page.get_by_test_id("add-todo").press_sequentially("buy")
    
    # Verify suggestions are visible
    suggestions = page.locator("#suggestions")
    expect(suggestions).to_be_visible()
    
    # Click outside the suggestions (clicking the body element)
    page.locator("body").click()
    
    # Verify suggestions are hidden
    expect(suggestions).to_have_class("hidden")

    


