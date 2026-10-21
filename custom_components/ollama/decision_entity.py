"""System One decision entity for the Ollama integration.

Decision subentries create an AI Task entity backed by an Ollama System One model
(https://docs.ollama.com/capabilities/decision). It does not generate data, so it
is not offered to ``ai_task.generate_data``; it answers ``ollama.decide`` calls.
"""

import base64
from collections.abc import Mapping
import logging
from pathlib import Path
from typing import Any

import httpx

from homeassistant.components import ai_task, conversation
from homeassistant.const import CONF_MODEL
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
import ollama

from .const import CONF_KEEP_ALIVE, DEFAULT_DECISION_KEEP_ALIVE, DOMAIN, KEEP_ALIVE_FOREVER
from .entity import OllamaBaseLLMEntity

_LOGGER = logging.getLogger(__name__)

SYSTEMONE_PATH = "/v1/systemone"
SUPPORTED_IMAGE_TYPES = ("image/png", "image/jpeg", "image/webp")


def _read_image(path: Path) -> str:
    """Read an image file and return it base64 encoded."""
    return base64.b64encode(path.read_bytes()).decode()


class OllamaDecisionEntity(
    ai_task.AITaskEntity,
    OllamaBaseLLMEntity,
):
    """Ollama System One decision entity."""

    _attr_supported_features = ai_task.AITaskEntityFeature(0)

    async def async_decide(
        self,
        state: str | Mapping[str, Any] | list[Any],
        questions: Mapping[str, Mapping[str, Any]],
        attachments: list[conversation.Attachment] | None = None,
    ) -> dict[str, Any]:
        """Answer typed questions about a state with the System One model."""
        settings = {**self.entry.data, **self.subentry.data}
        keep_alive_seconds = int(settings.get(CONF_KEEP_ALIVE, DEFAULT_DECISION_KEEP_ALIVE))

        payload: dict[str, Any] = {
            "model": settings[CONF_MODEL],
            "state": state,
            "questions": questions,
            # -1 must be sent as a number; other values as a duration string.
            "keep_alive": keep_alive_seconds if keep_alive_seconds == KEEP_ALIVE_FOREVER else f"{keep_alive_seconds}s",
        }

        if attachments:
            for attachment in attachments:
                if attachment.mime_type not in SUPPORTED_IMAGE_TYPES:
                    raise ServiceValidationError(
                        translation_domain=DOMAIN,
                        translation_key="unsupported_decision_attachment_type",
                        translation_placeholders={"mime_type": attachment.mime_type},
                    )
            payload["images"] = [
                await self.hass.async_add_executor_job(_read_image, attachment.path) for attachment in attachments
            ]

        try:
            # The ollama library Home Assistant ships has no System One support, so post
            # through the client's raw request helper to keep its auth and error handling.
            response = await self.entry.runtime_data._request_raw(  # noqa: SLF001
                "POST",
                SYSTEMONE_PATH,
                json=payload,
            )
        except (ollama.ResponseError, ollama.RequestError, ConnectionError, httpx.HTTPError) as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="decision_failed",
                translation_placeholders={"error": str(err)},
            ) from err

        result: dict[str, Any] = response.json()
        _LOGGER.debug("System One response: %s", result)
        return result
