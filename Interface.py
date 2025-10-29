import flet as ft
from flet import TextField, Checkbox, ElevatedButton, Text, Row, Column
from flet import ControlEvent
import asyncio
from Email_Bot import sendmail
import random
import threading
from Save import *

def main(page: ft.Page) -> None:
    page.title = 'Shared Locker'
    page.add(
        ft.Row(
            controls = [ft.Text("Welcome to The Shared Locker", size = 30, weight = "bold")],
            alignment = ft.MainAxisAlignment.CENTER
        )
    )
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # Fixed typo
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False

    # Setup UI Elements for login
    text_username: TextField = TextField(label='Email:', text_align=ft.TextAlign.LEFT, width=300)
    button_submit: ElevatedButton = ElevatedButton(text='Sign in', width=100)
    #For After putting items in
    done_button: ElevatedButton = ElevatedButton(text='Sign out', width=300, disabled=False)
    item_name_field = TextField(label='Item Name:', width=250)
    item_quantity_field = TextField(label='Quantity:', width=250, keyboard_type=ft.KeyboardType.NUMBER)
    items_list = Column(spacing=10)
    email_token = TextField(label='Token', text_align=ft.TextAlign.CENTER, width=300)
    
    


    def validate(e: ControlEvent) -> None:
        if all([text_username.value]):
            button_submit.disabled = False
        else:
            button_submit.disabled = True
        page.update()

    

    def submit(e: ControlEvent) -> None:
        #This is how we'll get the email
        #for the email sender 
        #Make an email sending function
        user_email = text_username.value

        #sends the email!        
        # Clear the login screen
        page.clean()
        loading_text = Text("Sending verification code...", size=20)
        loading_ring = ft.ProgressRing()

        page.add(
            ft.Container(
                content=Column(
                    [loading_ring, loading_text],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        )
        page.update()

        #send the email
        token = sendmail(user_email)

        # Clear loading screen show token screen
        page.clean()
        
        #Intiialize token screen
        token_title = Text("Input email.", size=30, weight=ft.FontWeight.BOLD)
        token_instruction = Text(f"A verification code has been sent to {user_email}", size=14, text_align=ft.TextAlign.CENTER)
        token_input = TextField(label='Enter Token', text_align=ft.TextAlign.CENTER, width=300, keyboard_type=ft.KeyboardType.NUMBER)
        token_error = Text("", color=ft.Colors.RED_400, size=14)
        verify_button = ElevatedButton(text='Verify', width=200, disabled=True)

        def validate_input(e:ControlEvent) -> None:
            verify_button.disabled = not bool(token_input.value)
            page.update()

        def verify_token(e: ControlEvent) -> None:

            entered_token = token_input.value

            if entered_token == token:
                show_inv(user_email)
            else:
                token_error.value = "Invalid Token. Try again."
                token_input.value = ""
                page.update()

        token_input.on_change = validate_input
        verify_button.on_click = verify_token

        token_box = ft.Container(
            content=Column(
                [
                    token_title,
                    ft.Divider(height=20),
                    token_instruction,
                    ft.Divider(height=20),
                    token_input,
                    token_error,
                    verify_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            padding=40,
            alignment=ft.alignment.center

        )
        page.add(token_box)
        page.update()
            
       
        
        # Input fields for adding items
        def show_inv(user_email: str) -> None:

            page.clean()
                
            error_text = Text("", color = ft.Colors.RED_400, size = 30)
            page.add(error_text)


            #Add items to inventory
            def add_item(e: ControlEvent) -> None:
                ItemCheck = item_name_field.value.replace(" ", "").lower() 
                QuantCheck = item_quantity_field.value.replace(" ", "")
                
                    
                if item_name_field.value and item_quantity_field.value:

                    if not (ItemCheck.isalpha() and QuantCheck.isdigit()):
                        error_text.value = "Please enter a valid name and quantity, no symbols!"
                        error_text.update()
                        page.update()
                        return 
                    
                    error_text.value = ""
                    page.update()

                    new_item = Row(
                        controls=[
                            Text(f"{item_name_field.value} - Qty: {item_quantity_field.value}", size=16),
                            ElevatedButton(
                                text="Remove",
                                on_click=lambda e: remove_item(new_item),
                                bgcolor=ft.Colors.RED_400,
                                color=ft.Colors.WHITE
                            )
                        ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                    items_list.controls.append(new_item)
                    
                    # Clear the input fields
                    item_name_field.value = ""
                    item_quantity_field.value = ""
                    # Save Inventory
                    save_inventory(items_list)
                    page.update()
                else:
                    error_text.value = "Please enter a vaild name and quantity"
                    error_text.update()
                    page.update()
                
            
            #Removes items from the list
            def remove_item(item_row):
                items_list.controls.remove(item_row)
                save_inventory(items_list)
                page.update()
                
            add_button = ElevatedButton(
                text='Add Item',
                width=250,
                on_click=add_item
            )
            
            # Create the inventory UI
            inv_title = Text(
                "Inventory",
                size=30,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.LEFT,
            )
            
            welcome_text = Text(
                value=f'Welcome {text_username.value[:3]}!',
                size=20,
                weight=ft.FontWeight.W_500
            )
            
            main_container = ft.Container(

                content=Column(

                    [
                        welcome_text,
                        ft.Divider(height=20),
                        inv_title,
                        ft.Divider(),
                        item_name_field,
                        item_quantity_field,
                        add_button,
                        ft.Divider(height=20),
                        Text("Your Items:", size=18, weight=ft.FontWeight.BOLD),
                        items_list,
                        done_button,

                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO\
                ),

                expand=False,
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.TRANSPARENT,
                width=350
            )
            
            page.add(main_container)
            page.update()

    def remove_item_by_text(item_text: str) -> None:
        for row in items_list.controls:
            if isinstance(row, ft.Row):
                for control in row.controls:
                    if isinstance(control, ft.Text) and control.value == item_text:
                        items_list.controls.remove(row)
                        save_inventory(items_list)
                        page.update()
                        return

    def show_login(e: None):
        #The show login function
        #Shows the inventory and log in buttons
        items_list.controls.clear()
        for item_text in load_inventory():
            item_row = ft.Row(
                controls=[
                    ft.Text(item_text, size=16),
                    ft.ElevatedButton(
                        text="Remove",
                        on_click=lambda e, r=item_text: remove_item_by_text(r),
                        bgcolor=ft.Colors.RED_400,
                        color=ft.Colors.WHITE 
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            items_list.controls.append(item_row)

        Inventory_Col = Column(
            controls=[
                Text("Current Inventory", size=30, weight=ft.FontWeight.W_500),
                ft.Divider(),
                items_list
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            width=200,
        )
        Login_Col = Column(
            controls=[
                text_username,
                button_submit,

            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=400
        )
        page.add(
            Row(
                controls=[
                    ft.Container(content=Inventory_Col, expand=True),
                    ft.Container(Login_Col, expand=True)
                    ]
            )
        )

        

    
    async def Done(e: ControlEvent) -> None:
        #Clear the page
        page.clean()
        def btn(e):
            Done(e)
        #Thanking message

        thank_you = Text(
            value='Thank you for your contribution!',
            size=20,
            weight=ft.FontWeight.W_500
        )


        Thank_You_Image = ft.Image(
            src='BulldogSalute.png.png',
            width=350,
            height=350
            )
        inv_col = ft.Column(
            controls=[
                items_list.controls
            ]
        )
        #The actual picture
        thanking_col = ft.Container(
            content=Column(
                [
                    thank_you,
                    ft.Divider(),
                    Thank_You_Image,
                    ft.Divider(),

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20

        )
        #Code to center the pictures
        centered = ft.Container(
            content=thanking_col,
            alignment=ft.alignment.center,
            expand=True
        )
        page.add(centered)
        page.update()
        await asyncio.sleep(6)
        page.clean()
        show_login(e)
        page.update()
       
   
        
    






    text_username.on_change = validate
    button_submit.on_click = submit
    done_button.on_click = Done

    # Render login UI Elements
    show_login(None)
if __name__ == '__main__':
    ft.app(target=main)

#GPT made the remove and add item functionalities. Did just about everything else.