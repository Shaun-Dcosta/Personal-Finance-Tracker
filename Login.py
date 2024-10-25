import flet as ft
import os
import mysql.connector as mysql

con=mysql.connect(host='localhost',user='root',password='mysql@123',database='pft',port='3306')
cursor=con.cursor()

def main(page: ft.Page):
    page.title = "Login and Signup"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f4f8"
    page.fonts = {
        "Roboto": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "Roboto-Bold": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf"
    }

    def route_change(route):
        page.views.clear()
        if page.route == "/signup":
            page.views.append(
                ft.View(
                    "/signup",
                    [
                        ft.AppBar(title=ft.Text("Sign Up"), bgcolor=ft.colors.BLUE_600),
                        signup_view()
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.BLUE_600),
                        login_view()
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def login_view():
        def login(e):
            if not username.value:
                username.error_text = "Username cannot be empty"
                page.update()
            elif not password.value:
                password.error_text = "Password cannot be empty"
                page.update()
            else:
                page.splash = ft.ProgressBar()
                page.update()
                page.splash = None
                uname=username.value
                pwd=password.value
                pull_user="select*from user"
                cursor.execute(pull_user)
                user_details=cursor.fetchall()
                for i in user_details:
                    if uname==i[1] and pwd==i[2]:
                        page.window.destroy()
                        os.system('python homepage.py')  
                        page.update()                      
                        print("yup")
                        break
                else:
                    dialog = ft.AlertDialog(
                        title=ft.Text("Log In Unsuccessful"),
                        content=ft.Text("Check your credentials"),
                    )
                    page.dialog = dialog
                    dialog.open = True
                    page.update()

        # Logo
        logo = ft.Icon(ft.icons.LOCK_OUTLINE, size=80, color=ft.colors.BLUE_600)

        # Input fields
        username = ft.TextField(
            label="Username",
            border=ft.InputBorder.UNDERLINE,
            width=300,
            text_style=ft.TextStyle(font_family="Roboto"),
        )
        password = ft.TextField(
            label="Password",
            border=ft.InputBorder.UNDERLINE,
            password=True,
            can_reveal_password=True,
            width=300,
            text_style=ft.TextStyle(font_family="Roboto"),
        )

        # Remember me checkbox
        remember_me = ft.Checkbox(label="Remember me", value=False)

        # Forgot password link
        forgot_password = ft.Text(
            "Forgot password?",
            color=ft.colors.BLUE_600,
            weight=ft.FontWeight.BOLD,
            size=12,
        )

        # Login button
        login_button = ft.ElevatedButton(
            content=ft.Text(
                "Login",
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                font_family="Roboto-Bold",
            ),
            style=ft.ButtonStyle(
                color={ft.MaterialState.HOVERED: ft.colors.WHITE},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLUE_600,
                         ft.MaterialState.HOVERED: ft.colors.BLUE_700},
                padding={ft.MaterialState.DEFAULT: 20},
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=8),
                },
                elevation={"pressed": 0, "": 1},
            ),
            on_click=login,
            width=300,
            height=50,
        )

        # Sign up link
        signup_link = ft.TextButton(
            content=ft.Text(
                "Don't have an account? Sign up",
                color=ft.colors.BLUE_600,
                weight=ft.FontWeight.BOLD,
                size=14,
            ),
            on_click=lambda _: page.go("/signup")
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(logo, padding=ft.padding.only(bottom=20)),
                    ft.Text(
                        "Welcome Back",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        font_family="Roboto-Bold",
                    ),
                    ft.Text(
                        "Please enter your credentials to login",
                        size=14,
                        color=ft.colors.GREY_700,
                        font_family="Roboto",
                    ),
                    ft.Container(height=20),
                    username,
                    ft.Container(height=10),
                    password,
                    ft.Container(height=10),
                    ft.Row(
                        [remember_me, forgot_password],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        width=300,
                    ),
                    ft.Container(height=20),
                    login_button,
                    ft.Container(height=10),
                    signup_link,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=400,
            padding=40,
            border_radius=20,
            bgcolor=ft.colors.WHITE,
            animate=ft.animation.Animation(300, ft.AnimationCurve.DECELERATE),
            animate_opacity=300,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

    def signup_view():
        def signup(e):
            if not email.value:
                email.error_text = "Email cannot be empty"
                page.update()
            elif not username.value:
                username.error_text = "Username cannot be empty"
                page.update()
            elif not password.value:
                password.error_text = "Password cannot be empty"
                page.update()
            else:
                page.splash = ft.ProgressBar()
                page.update()
                page.splash = None
                uname=username.value
                pwd=password.value
                em=email.value
                try:
                    signup_query = "INSERT INTO user (username, password, email) VALUES (%s, %s, %s)"
                    values = (uname, pwd, em)    
                    cursor.execute(signup_query, values)
                    cursor.execute('commit')
                    dialog = ft.AlertDialog(
                        title=ft.Text("Sign Up Successful"),
                        content=ft.Text(f"Welcome, {username.value}! You can now login."),
                    )
                    page.dialog = dialog
                    dialog.open = True
                    page.update()
                except:
                    dialog = ft.AlertDialog(
                        title=ft.Text("Sign Up Unsuccessful"),
                        content=ft.Text("Something Went wrong. Check the details entered and try again"),
                    )
                    page.dialog = dialog
                    dialog.open = True
                    page.update()


        # Logo
        logo = ft.Icon(ft.icons.PERSON_ADD, size=80, color=ft.colors.BLUE_600)

        # Input fields
        email = ft.TextField(
            label="Email",
            border=ft.InputBorder.UNDERLINE,
            width=300,
            text_style=ft.TextStyle(font_family="Roboto"),
        )
        username = ft.TextField(
            label="Username",
            border=ft.InputBorder.UNDERLINE,
            width=300,
            text_style=ft.TextStyle(font_family="Roboto"),
        )
        password = ft.TextField(
            label="Password",
            border=ft.InputBorder.UNDERLINE,
            password=True,
            can_reveal_password=True,
            width=300,
            text_style=ft.TextStyle(font_family="Roboto"),
        )

        # Sign up button
        signup_button = ft.ElevatedButton(
            content=ft.Text(
                "Sign Up",
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                font_family="Roboto-Bold",
            ),
            style=ft.ButtonStyle(
                color={ft.MaterialState.HOVERED: ft.colors.WHITE},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLUE_600,
                         ft.MaterialState.HOVERED: ft.colors.BLUE_700},
                padding={ft.MaterialState.DEFAULT: 20},
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=8),
                },
                elevation={"pressed": 0, "": 1},
            ),
            on_click=signup,
            width=300,
            height=50,
        )

        # Login link
        login_link = ft.TextButton(
            content=ft.Text(
                "Already have an account? Login",
                color=ft.colors.BLUE_600,
                weight=ft.FontWeight.BOLD,
                size=14,
            ),
            on_click=lambda _: page.go("/")
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(logo, padding=ft.padding.only(bottom=20)),
                    ft.Text(
                        "Create an Account",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        font_family="Roboto-Bold",
                    ),
                    ft.Text(
                        "Please fill in the details to sign up",
                        size=14,
                        color=ft.colors.GREY_700,
                        font_family="Roboto",
                    ),
                    ft.Container(height=20),
                    email,
                    ft.Container(height=10),
                    username,
                    ft.Container(height=10),
                    password,
                    ft.Container(height=20),
                    signup_button,
                    ft.Container(height=10),
                    login_link,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=400,
            padding=40,
            border_radius=20,
            bgcolor=ft.colors.WHITE,
            animate=ft.animation.Animation(300, ft.AnimationCurve.DECELERATE),
            animate_opacity=300,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            ),
        )

    page.go(page.route)

ft.app(target=main)