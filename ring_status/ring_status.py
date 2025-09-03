import reflex as rx
from rxconfig import config
from .views import header, track_status

"""
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )
"""
"""
def index() -> rx.Component:
    return rx.vstack(
        header.header(),
        track_status.track_status(),
        align="stretch"
        )
"""
def index() -> rx.Component:
    return rx.fragment(
        header.header(),
        rx.box(
            track_status.track_status(),
            class_name="max-w-4xl mx-auto p-6 space-y-8"
        )
        )        

app = rx.App()
app.add_page(index)
