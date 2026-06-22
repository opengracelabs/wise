"""HTTP and inline clients for RC1 platform service integration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Protocol

import httpx

from wise_reference.rc1_agents import (
    propose_discovery_record,
    propose_graph_entity,
    propose_metadata,
    propose_preservation,
    propose_quality_review,
)


class RC1AgentClient(Protocol):
    def discover(self, stable_id: str) -> dict[str, Any]: ...
    def preserve(self, stable_id: str, *, discovery_record_id: str) -> dict[str, Any]: ...
    def model_metadata(self, stable_id: str, *, preserved_object_ark: str) -> dict[str, Any]: ...
    def place_graph(self, stable_id: str, *, entity_assertion_id: str) -> dict[str, Any]: ...
    def review_quality(self, stable_id: str, *, graph_entity_uri: str) -> dict[str, Any]: ...


@dataclass
class ServiceUrls:
    discovery: str
    preservation: str
    metadata: str
    knowledge_graph: str

    @classmethod
    def from_env(cls) -> ServiceUrls:
        return cls(
            discovery=os.environ.get("DISCOVERY_SERVICE_URL", "http://localhost:8001"),
            preservation=os.environ.get("PRESERVATION_SERVICE_URL", "http://localhost:8003"),
            metadata=os.environ.get("METADATA_SERVICE_URL", "http://localhost:8002"),
            knowledge_graph=os.environ.get(
                "KNOWLEDGE_GRAPH_SERVICE_URL", "http://localhost:8004"
            ),
        )


class InlineRC1AgentClient:
    """Direct integration — used in tests and when WISE_ORCHESTRATION_INLINE=1."""

    def __init__(self, session=None) -> None:
        self._session = session

    def discover(self, stable_id: str) -> dict[str, Any]:
        return propose_discovery_record(stable_id, self._session)

    def preserve(self, stable_id: str, *, discovery_record_id: str) -> dict[str, Any]:
        return propose_preservation(
            stable_id, discovery_record_id=discovery_record_id, session=self._session
        )

    def model_metadata(self, stable_id: str, *, preserved_object_ark: str) -> dict[str, Any]:
        return propose_metadata(
            stable_id, preserved_object_ark=preserved_object_ark, session=self._session
        )

    def place_graph(self, stable_id: str, *, entity_assertion_id: str) -> dict[str, Any]:
        return propose_graph_entity(
            stable_id, entity_assertion_id=entity_assertion_id, session=self._session
        )

    def review_quality(self, stable_id: str, *, graph_entity_uri: str) -> dict[str, Any]:
        return propose_quality_review(
            stable_id, graph_entity_uri=graph_entity_uri, session=self._session
        )


class HttpRC1AgentClient:
    """HTTP client calling platform service RC1 propose endpoints."""

    def __init__(self, urls: ServiceUrls | None = None, timeout: float = 30.0) -> None:
        self._urls = urls or ServiceUrls.from_env()
        self._timeout = timeout

    def discover(self, stable_id: str) -> dict[str, Any]:
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(
                f"{self._urls.discovery}/v1/rc1/discovery/propose",
                json={"stable_id": stable_id},
            )
            response.raise_for_status()
            return response.json()

    def preserve(self, stable_id: str, *, discovery_record_id: str) -> dict[str, Any]:
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(
                f"{self._urls.preservation}/v1/rc1/preservation/propose",
                json={
                    "stable_id": stable_id,
                    "discovery_record_id": discovery_record_id,
                },
            )
            response.raise_for_status()
            return response.json()

    def model_metadata(self, stable_id: str, *, preserved_object_ark: str) -> dict[str, Any]:
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(
                f"{self._urls.metadata}/v1/rc1/metadata/propose",
                json={
                    "stable_id": stable_id,
                    "preserved_object_ark": preserved_object_ark,
                },
            )
            response.raise_for_status()
            return response.json()

    def place_graph(self, stable_id: str, *, entity_assertion_id: str) -> dict[str, Any]:
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(
                f"{self._urls.knowledge_graph}/v1/rc1/graph/propose",
                json={
                    "stable_id": stable_id,
                    "entity_assertion_id": entity_assertion_id,
                },
            )
            response.raise_for_status()
            return response.json()

    def review_quality(self, stable_id: str, *, graph_entity_uri: str) -> dict[str, Any]:
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(
                f"{self._urls.metadata}/v1/rc1/quality/propose",
                json={
                    "stable_id": stable_id,
                    "graph_entity_uri": graph_entity_uri,
                },
            )
            response.raise_for_status()
            return response.json()


def get_rc1_client(session=None) -> RC1AgentClient:
    if os.environ.get("WISE_ORCHESTRATION_INLINE", "").lower() in {"1", "true", "yes"}:
        return InlineRC1AgentClient(session=session)
    return HttpRC1AgentClient()
