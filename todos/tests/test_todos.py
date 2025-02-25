import os
from datetime import datetime, timedelta
import pytest
from playwright.sync_api import expect
import django
from django.conf import settings
from django.template.loader import get_template

settings.configure(TEMPLATES=[{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['todos/templates'],
}], INSTALLED_APPS=['django.contrib.humanize'])
django.setup()

def test_add_todo(page):
    def handle_todos_route(route):
        if route.request.method != 'GET':
            route.fallback()
            return
        
        route.fulfill(
            status=200,
            content_type='text/html',
            body=get_template('index.html').render({'screen': True}) 
        )
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

#def test_delete_todo(page):
    #def handle_todos_route(route):
        #if route.request.method != 'GET':
            #route.fallback()
            #return
            
        #route.fulfill(
            #status=200,
            #content_type='text/html',
            #body='<div class="todo">buy milk</div>'
        #)
    
    #def handle_todo_delete_route(route):
        #if route.request.method != 'DELETE':
            #route.fallback()
            #return
            
        #route.fulfill(
            #status=200,
            #content_type='application/text',
            #body='<div></div>'
        #)

    #page.route("**/todos", handle_todos_route)
    #page.route("**/todo/*", handle_todo_delete_route)
    
    #page.goto("http://localhost:3000/todos")
    #page.wait_for_selector("text=Todo")
    #page.get_by_role("button", name="delete").click()
    
    #expect(page.get_by_role("button", name="delete")).not_to_be_visible()

#def test_complete_todo(page):
    #def handle_todos_route(route):
        #if route.request.method != 'GET':
            #route.fallback()
            #return
            
        #route.fulfill(
            #status=200,
            #content_type='text/html',
            #body='<div class="todo"><input type="checkbox">buy milk</div>'
        #)
    
    #def handle_todo_patch_route(route):
        #if route.request.method != 'PATCH':
            #route.fallback()
            #return
            
        #route.fulfill(
            #status=200,
            #content_type='application/text',
            #body='<div class="todo completed"><input type="checkbox" checked>buy milk</div>'
        #)

    #page.route("**/todos", handle_todos_route)
    #page.route("**/todo/*", handle_todo_patch_route)
    
    #page.goto("http://localhost:3000/todos")
    #page.wait_for_selector("text=Todo")
    #page.get_by_role("checkbox").click()
    #page.wait_for_selector("text=Completed (1)")
    #page.get_by_test_id("show-completed").click()
    
    #expect(page.get_by_role("checkbox")).to_be_checked()

#def test_edit_todo(page):
    #todo_id = '5d686f21-8775-42c6-ae9a-2cd88bdfb6d2'
    
    #def handle_todos_route(route):
        #if route.request.method != 'GET':
            #route.fallback()
            #return
            
        #route.fulfill(
            #status=200,
            #content_type='text/html',
            #body=f'<div class="todo"><input name="{todo_id}" value="buy milk"></div>'
        #)
    
    #def handle_todo_put_route(route):
        #if route.request.method != 'PUT':
            #route.fallback()
            #return
            
        #route.fulfill(
            #status=200,
            #content_type='application/text',
            #body=todo_id
        #)

    #page.route("**/todos", handle_todos_route)
    #page.route("**/todo/*", handle_todo_put_route)
    
    #page.goto("http://localhost:3000/todos")
    #page.wait_for_selector("text=Todo")
    
    #page.locator(f'[name="{todo_id}"]').fill("buy chocolate")
    #expect(page.locator(f'[name="{todo_id}"]')).to_have_value("buy chocolate") 