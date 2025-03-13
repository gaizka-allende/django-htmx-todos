from datetime import datetime, timedelta
from playwright.sync_api import expect
from django.template.loader import get_template

def test_add_todo(page):
    def handle_todos_route(route):
        if route.request.method == 'GET':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True  }) 
            )
        elif route.request.method == 'POST':
            route.fulfill(
                status=200,
                content_type='text/html',
                body=get_template('index.html').render({'screen': True, 'uncompletedTodos': [], 'completedTodos': []}) 
            )
        else:
            route.fallback()
            return
    page.route("**/todos", handle_todos_route)
    
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
    page.get_by_test_id("add-todo").press_sequentially("buy milk")
    page.get_by_role("button", name="add").click()
    
    expect(page.get_by_role("button", name="delete")).to_be_visible()

def test_delete_todo(page):
    def handle_todos_route(route):
        if route.request.method != 'GET':
            route.fallback()
            return

        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('index.html').render({'screen': True, 'uncompletedTodos': [
            {
                'title': 'buy milk',
                'id': '5d686f21-8775-42c6-ae9a-2cd88bdfb6d2',
                'completed': 0,
                'created_modified': datetime.now()
            }
            ], 'completedTodos': []}) 
        )
    page.route("**/todos", handle_todos_route)
    
    def handle_todo_delete_route(route):
        if route.request.method != 'DELETE':
            route.fallback()
            return
            
        route.fulfill(
            status=200,
            content_type='application/text',
            body='<div></div>'
        )
    page.route("**/todo/*", handle_todo_delete_route)
    
    page.goto("http://localhost:3000/todos")
    page.wait_for_selector("text=Todo")
    page.get_by_role("button", name="delete").click()
    
    expect(page.get_by_role("button", name="delete")).not_to_be_visible()

def test_complete_todo(page):
    def handle_todos_route(route):
        if route.request.method != 'GET':
            route.fallback()
            return
            
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('index.html').render({'screen': True, 'uncompletedTodos': [
            {
                'title': 'buy milk',
                'id': '5d686f21-8775-42c6-ae9a-2cd88bdfb6d2',
                'completed': 0,
                'created_modified': datetime.now()
            }
            ], 'completedTodos': []}) 
        )
    page.route("**/todos", handle_todos_route)
    
    def handle_todo_patch_route(route):
        if route.request.method != 'PATCH':
            route.fallback()
            return
            
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('index.html').render({
                'screen': True, 
                'uncompletedTodos': [], 
                'completedTodos': [{
                    'title': 'buy milk',
                    'id': '5d686f21-8775-42c6-ae9a-2cd88bdfb6d2',
                    'completed': 1,
                    'created_modified': datetime.now()
                }]
            })
        )

    page.route("**/todo/*", handle_todo_patch_route)
    
    page.goto("http://localhost:3000/todos")

    page.wait_for_selector("text=Todo")
    
    page.get_by_role("checkbox").click()
    
    expect(page.get_by_text("Completed (1)")).to_be_visible(timeout=5000)
    
    page.get_by_test_id("show-completed").click()
    
    expect(page.get_by_role("checkbox")).to_be_checked()

def test_edit_todo(page):
    todo_id = '5d686f21-8775-42c6-ae9a-2cd88bdfb6d2'
    
    def handle_todos_route(route):
        if route.request.method != 'GET':
            route.fallback()
            return
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('index.html').render({'screen': True, 'uncompletedTodos': [
            {
                'title': 'buy milk',
                'id': todo_id,
                'completed': 0,
                'created_modified': datetime.now()
            }
            ], 'completedTodos': []}) 
        )
    page.route("**/todos", handle_todos_route)
    
    def handle_todo_put_route(route):
        if route.request.method != 'PUT':
            route.fallback()
            return
            
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('index.html').render({'screen': True, 'uncompletedTodos': [
            {
                'title': 'buy chocolate',
                'id': todo_id,
                'completed': 0,
                'created_modified': datetime.now()
            }
            ], 'completedTodos': []}) 
        )
    page.route("**/todo/*", handle_todo_put_route)
    
    page.goto("http://localhost:3000/todos")
    page.wait_for_selector("text=Todo")

    expect(page.locator(f'[name="textbox_{todo_id}"]')).to_have_value("buy milk")
    page.locator(f'[name="textbox_{todo_id}"]').fill("buy chocolate")
    expect(page.locator(f'[name="textbox_{todo_id}"]')).to_have_value("buy chocolate")
