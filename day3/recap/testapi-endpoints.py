import requests

endpoint_url = "http://localhost:8000"

def check_api_stats():
    print("[ * ] Checking API Status...")
    r = requests.get(endpoint_url)
    print(r.text)
    print(f"Status Code {r.status_code}")
    print()

def create_task(name, description):
    print(f"[ * ] Creating task {name} with description {description}")
    r = requests.post(f"{endpoint_url}/tasks", json={
            "name": name,
            "description": description
        }
    )
    print(r.text)
    print()

def get_tasks():
    print("[ * ] List of tasks:")
    r = requests.get(f"{endpoint_url}/tasks")
    print(r.text)
    print()

def get_task_by_id(task_id: int):
    print(f"[ * ] Getting task with id {task_id}...")
    r = requests.get(f"{endpoint_url}/tasks/{task_id}")
    print(r.text)
    print()

def mark_task_status(task_id, status):
    print(f"[ * ] Marking task {task_id} with status {status}...")
    r = requests.put(f"{endpoint_url}/tasks/{task_id}?status={status}")
    print(r.text)
    print()

def remove_task(task_id):
    print(f"[ * ] Removing task with id {task_id}...")
    r = requests.delete(f"{endpoint_url}/tasks/{task_id}")
    print(r.text)
    print()

def create_tasks(tasks):
    for task_name in tasks:
        task_description = tasks[task_name]
        create_task(task_name, task_description)

tasks = {
    "Bed Time": "Go to bed at 8 pm",
    "Wake Up": "Get up at 6 am",
    "Breakfast": "Make breakfast and get to work!"
}

check_api_stats()
create_tasks(tasks)
get_tasks()
get_task_by_id(3)
mark_task_status(1, True)
get_tasks()
get_task_by_id(1)
mark_task_status(2, True)
mark_task_status(3, True)
get_tasks()
remove_task(3)
remove_task(3)
get_tasks()
remove_task(2)
remove_task(2)
get_tasks()
remove_task(1)
remove_task(1)
get_tasks()
