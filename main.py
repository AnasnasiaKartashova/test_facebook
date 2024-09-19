from aiohttp import web
from src.handlers.message_handlers import verify_webhook, handle_webhook, handle_request


app = web.Application()
app.router.add_get("/webhook", verify_webhook)
app.router.add_post("/webhook", handle_webhook)
app.router.add_post("/send-message", handle_request)


if __name__ == "__main__":
    web.run_app(app, port=8080)
