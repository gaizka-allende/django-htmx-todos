from datetime import datetime
from playwright.sync_api import expect
from django.template.loader import get_template

def test_select_suggestion(page):
    def handle_todos_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True}) 
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
            body=get_template('todo.html').render({
                'todo': {
                    'title': 'buy milk', 
                    'id': '5d686f21-8775-42c6-ae9a-2cd88bdfb6d2', 
                    'completed': 0, 
                    'created_modified': datetime.now()
                }
            })
        )
    page.route("**/todo", handle_todo_route)
    
    page.goto("http://localhost:3000/todos")
    
    # Type "buy" in the input field
    page.get_by_test_id("add-todo").press_sequentially("buy")
    
    # Wait for and verify suggestions
    expect(page.locator("li", has_text="Buy coffee")).to_be_visible()
    expect(page.locator("li", has_text="Buy milk")).to_be_visible()
    
    # Click on suggestion containing "Buy milk"
    page.locator("li", has_text="Buy milk").click()
    
    # Verify the input field was populated
    expect(page.get_by_test_id("add-todo")).to_have_value("Buy milk")
    
    # Submit the todo
    page.get_by_test_id("add-todo").press("Enter")
    
    # Verify the todo was added to the list
    expect(page.get_by_test_id("todo-item-input")).to_have_value("buy milk")

def test_suggestions_hide_on_click_outside(page):
    def handle_todos_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True}) 
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
    expect(suggestions).not_to_be_visible()

    


