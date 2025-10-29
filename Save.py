import json
import os
import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet import ControlEvent


def save_inventory(items_list):
    with open("inventory.txt", "w") as f:
        for row in items_list.controls:
            if isinstance(row, Row):
                for control in row.controls:
                    if isinstance(control, Text):
                        f.write(control.value + "\n")
                        break  # Only write the first Text per row

def load_inventory():
    try:
        with open("inventory.txt", "r") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
