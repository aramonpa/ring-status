import reflex as rx

def track_status() -> rx.Component:
    return rx.center(
            rx.text("Track open"),
            class_name="flex justify-center transition transform hover:scale-105"
        )
        