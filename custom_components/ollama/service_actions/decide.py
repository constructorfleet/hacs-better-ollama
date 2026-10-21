"""The ollama.decide service action.

Asks a System One decision model typed questions (noul, choice or score) about a
state built from a prompt and/or entity states. See
https://docs.ollama.com/capabilities/decision for the request semantics.
"""

from typing import TYPE_CHECKING, Any, cast

import probatio

from custom_components.ollama.const import DOMAIN
from homeassistant.components.ai_task.task import _resolve_attachments
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv, selector
from homeassistant.helpers.chat_session import async_get_chat_session
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.json import json_dumps
from homeassistant.util.json import json_loads

if TYPE_CHECKING:
    # Imported for typing only: the entity module imports the integration package.
    from custom_components.ollama.decision_entity import OllamaDecisionEntity

SERVICE_DECIDE = "decide"

ATTR_ATTACHMENTS = "attachments"
ATTR_CRITERIA = "criteria"
ATTR_ENTITIES = "entities"
ATTR_INSTRUCTIONS = "instructions"
ATTR_NAME = "name"
ATTR_PROMPT = "prompt"
ATTR_QUESTIONS = "questions"
ATTR_TYPE = "type"

QUESTION_TYPE_CHOICE = "choice"
QUESTION_TYPE_NOUL = "noul"
QUESTION_TYPE_SCORE = "score"

MAX_QUESTIONS = 64
MIN_CHOICES = 2
MIN_SCORE_LEVELS = 2
MAX_SCORE_LEVELS = 10


def _validate_question(question: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize the criteria for a question type."""
    question_type = question[ATTR_TYPE]
    criteria = question.get(ATTR_CRITERIA)

    if question_type == QUESTION_TYPE_CHOICE:
        if not isinstance(criteria, dict) or len(criteria) < MIN_CHOICES:
            raise probatio.Invalid(f"choice questions need at least {MIN_CHOICES} criteria options")
        normalized = {str(key).strip(): None if value is None else str(value) for key, value in criteria.items()}
        if "" in normalized:
            raise probatio.Invalid("choice criteria option names must not be blank")
        question[ATTR_CRITERIA] = normalized
    elif question_type == QUESTION_TYPE_SCORE:
        if not isinstance(criteria, list) or not MIN_SCORE_LEVELS <= len(criteria) <= MAX_SCORE_LEVELS:
            raise probatio.Invalid(
                f"score questions need {MIN_SCORE_LEVELS} to {MAX_SCORE_LEVELS} criteria, ordered lowest to highest"
            )
        question[ATTR_CRITERIA] = [str(level) for level in criteria]
    elif criteria is not None:
        # YAML parses unquoted true/false keys as booleans, so normalize them.
        if not isinstance(criteria, dict):
            raise probatio.Invalid("noul criteria must map 'true' and/or 'false' to descriptions")
        normalized = {str(key).lower(): str(value) for key, value in criteria.items()}
        if not normalized.keys() <= {"true", "false"}:
            raise probatio.Invalid("noul criteria may only describe 'true' and 'false'")
        question[ATTR_CRITERIA] = normalized

    return question


QUESTION_SCHEMA = probatio.All(
    probatio.Schema(
        {
            probatio.Optional(ATTR_NAME): cv.string,
            probatio.Required(ATTR_TYPE): probatio.In([QUESTION_TYPE_NOUL, QUESTION_TYPE_CHOICE, QUESTION_TYPE_SCORE]),
            probatio.Required(ATTR_INSTRUCTIONS): cv.string,
            probatio.Optional(ATTR_CRITERIA): probatio.Any(dict, list),
        }
    ),
    _validate_question,
)

DECIDE_SCHEMA = probatio.All(
    cv.make_entity_service_schema(
        {
            probatio.Optional(ATTR_PROMPT): cv.string,
            probatio.Optional(ATTR_ENTITIES): cv.entity_ids,
            probatio.Required(ATTR_QUESTIONS): probatio.All(
                cv.ensure_list, [QUESTION_SCHEMA], probatio.Length(min=1, max=MAX_QUESTIONS)
            ),
            probatio.Optional(ATTR_ATTACHMENTS): selector.MediaSelector({"accept": ["image/*"], "multiple": True}),
        }
    ),
    cv.has_at_least_one_key(ATTR_PROMPT, ATTR_ENTITIES),
)


def _build_state(hass: HomeAssistant, prompt: str | None, entity_ids: list[str]) -> str | dict[str, Any]:
    """Build the System One state from the prompt and entity states."""
    if not entity_ids:
        assert prompt is not None
        return prompt

    entities: list[dict[str, Any]] = []
    for entity_id in entity_ids:
        if (state := hass.states.get(entity_id)) is None:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="entity_not_found",
                translation_placeholders={"entity_id": entity_id},
            )
        entities.append(
            {
                "entity_id": state.entity_id,
                "name": state.name,
                "state": state.state,
                "attributes": dict(state.attributes),
                "last_changed": state.last_changed.isoformat(),
            }
        )

    decision_state: dict[str, Any] = {"entities": entities}
    if prompt:
        decision_state["context"] = prompt
    # Round-trip through HA's JSON encoder so attributes like datetimes serialize.
    return json_loads(json_dumps(decision_state))  # type: ignore[return-value]


def _build_questions(questions: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Key questions by name, as the System One API expects."""
    named: dict[str, dict[str, Any]] = {}
    for index, question in enumerate(questions, start=1):
        name = question.get(ATTR_NAME) or f"question_{index}"
        if name in named:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="duplicate_question_name",
                translation_placeholders={"name": name},
            )
        named[name] = {key: value for key, value in question.items() if key != ATTR_NAME}
    return named


async def async_handle_decide(entity: Entity, call: ServiceCall) -> ServiceResponse:
    """Handle the ollama.decide service action for one entity."""
    if not hasattr(entity, "async_decide"):
        raise ServiceValidationError(
            translation_domain=DOMAIN,
            translation_key="not_decision_entity",
            translation_placeholders={"entity_id": entity.entity_id},
        )

    hass = call.hass
    state = _build_state(hass, call.data.get(ATTR_PROMPT), call.data.get(ATTR_ENTITIES, []))
    questions = _build_questions(call.data[ATTR_QUESTIONS])

    with async_get_chat_session(hass) as session:
        attachments = await _resolve_attachments(hass, session, call.data.get(ATTR_ATTACHMENTS))
        return await cast("OllamaDecisionEntity", entity).async_decide(state, questions, attachments or None)
