from aiohttp import web
from config.project_settings import settings
from src.services.error_service import ErrorService
from src.services.messenger_service import MessengerService


fb_client = MessengerService(settings.ACCESS_TOKEN)


async def handle_request(request) -> web.Response:
    """Handles a request to send a message using the Facebook client"""
    try:
        data = await request.json()
        recipient_id = data.get("recipient_id")
        message_text = data.get("message_text")
        response = await fb_client.send_message(recipient_id, message_text)
        return web.json_response({"status": "success", "response": response})

    except Exception as e:
        return ErrorService.handle_error(e)


async def handle_webhook(request) -> web.Response:
    """
    Handles incoming webhook data from a source,
    processes messaging events, and logs sender ID and message text
    """
    try:
        data = await request.json()
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                message_text = messaging_event["message"]["text"]
                print(sender_id, message_text)

        return web.json_response({"status": "success"})

    except Exception as e:
        return ErrorService.handle_error(e)


async def verify_webhook(request) -> web.Response:
    """
    Verifies the webhook by comparing the provided token
    with the expected verification token
    """
    token = request.query.get("hub.verify_token")
    challenge = request.query.get("hub.challenge")

    if token == settings.VERIFY_TOKEN:
        return web.Response(text=challenge)
    else:
        return web.Response(text="Invalid token", status=403)
