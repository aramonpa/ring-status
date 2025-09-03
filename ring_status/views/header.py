import reflex as rx
from pathlib import Path

def header() -> rx.Component:
    return rx.box(
        rx.image(
            src="/neverbeen.png",
            alt="Nordschleife logo",
            width="7%"
            #class_name="w-20 h-20 mb-4 drop-shadow-lg"
        ),
        rx.heading(
            "Nürburgring Nordschleife",
            size="4",
            class_name="font-extrabold tracking-wide drop-shadow-lg"
            ),
        rx.text(
            "Current state of the track",
            class_name="mt-2 text-gray-300 text-lg"
            ),
        class_name="relative bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white p-8 shadow-lg flex flex-col items-center justify-center"
        )