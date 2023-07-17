import sqlite3
import json
from models import Employee

EMPLOYEES = [
    {
        "id": 1,
        "name": "Madi Peper",
    },
    {
        "id": 2,
        "name": "Mary Maloney",
    },
    {
        "id": 3,
        "name": "Megan Duckett",
    },
]

def get_all_employees():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name
        FROM employee e
        """)

        employees = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'])
            employees.append(employee.__dict__)

    return employees

def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        employee = Employee(data['id'], data['name'])

        return employee.__dict__

def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee

def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            new_employee["id"] = id
            EMPLOYEES[index] = new_employee
            break
