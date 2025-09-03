import reflex as rx

config = rx.Config(
    app_name="ring_status",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)