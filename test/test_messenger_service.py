import pytest
from unittest.mock import AsyncMock
from src.services.messenger_service import MessengerService


@pytest.mark.asyncio
async def test_send_message_successful(mocker):
    recipient_id = "1234"
    message_id = "gBEGkYiEB1VXAglK1ZEqA1YKPrU"
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json.return_value = {"messages": [{"id": message_id}]}
    mock_post = mocker.patch("aiohttp.ClientSession.post", return_value=AsyncMock())
    mock_post.return_value.__aenter__.return_value = mock_response

    service = MessengerService(access_token="fake_token")
    result = await service.send_message(recipient_id, "Hello!")
    assert result == {"messages": [{"id": message_id}]}
    mock_post.assert_called_once_with(
        service.base_url,
        params={"access_token": "fake_token"},
        json={"recipient": {"id": recipient_id}, "message": {"text": "Hello!"}},
    )


@pytest.mark.asyncio
async def test_send_message_failed(mocker):
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.text.return_value = '{"error": "Something went wrong"}'
    mock_post = mocker.patch("aiohttp.ClientSession.post", return_value=AsyncMock())
    mock_post.return_value.__aenter__.return_value = mock_response

    service = MessengerService(access_token="fake_token")

    with pytest.raises(Exception) as e:
        await service.send_message("recipient_id", "Hello!")

    assert "Failed to send message" in str(e.value)
    assert "500" in str(e.value)
