"""Service actions for the Ollama integration."""

from custom_components.ollama.const import DOMAIN
from homeassistant.components.ai_task import DOMAIN as AI_TASK_DOMAIN
from homeassistant.core import HomeAssistant, SupportsResponse, callback
from homeassistant.helpers import service

from .decide import DECIDE_SCHEMA, SERVICE_DECIDE, async_handle_decide


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Register the Ollama service actions."""
    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        SERVICE_DECIDE,
        entity_domain=AI_TASK_DOMAIN,
        schema=DECIDE_SCHEMA,
        func=async_handle_decide,
        supports_response=SupportsResponse.ONLY,
    )
