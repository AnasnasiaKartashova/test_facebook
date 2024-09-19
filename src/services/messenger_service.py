import aiohttp
from pydantic import BaseModel
from config.project_settings import settings
from src.schemas.message_payload import MessagePayload


class MessengerService:
    def __init__(self, access_token: str):
        self.base_url = settings.BASE_URL
        self.access_token = access_token

    async def send_message(self, recipient_id: str, message_text: str) -> dict:
        """Send text message to specified recipient id"""
        payload = MessagePayload(
            recipient={"id": recipient_id}, message={"text": message_text}
        )
        return await self.make_request(payload)

    async def make_request(self, payload: BaseModel) -> dict:
        """Sends an asynchronous POST request with the specified payload to a given URL"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                params={"access_token": self.access_token},
                json=payload.dict(),
            ) as response:
                response_text = await response.text()
                if response.status != 200:
                    raise Exception(
                        f"Failed to send message: {response.status}, Response: {response_text}"
                    )
                return await response.json()
