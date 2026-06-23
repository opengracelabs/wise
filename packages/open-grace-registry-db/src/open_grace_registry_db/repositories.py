"""Repository pattern for governed registry entries."""

from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from open_grace_registry_db.base import GovernedMixin

T = TypeVar("T", bound=BaseModel)
M = TypeVar("M")


def _governed_from_record(record: BaseModel, row: GovernedMixin) -> None:
    row.lifecycle_stage = record.lifecycle_stage.value if hasattr(record.lifecycle_stage, "value") else str(record.lifecycle_stage)
    row.created_at = record.created_at
    row.updated_at = record.updated_at
    row.steward_actor = record.steward_actor
    row.reference_models = list(record.reference_models)
    row.payload = record.model_dump(mode="json")


def _record_from_payload(model: type[T], payload: dict) -> T:
    return model.model_validate(payload)


class GovernedRepository(Generic[T, M]):
    """CRUD repository wrapping a SQLAlchemy model and pydantic record type."""

    def __init__(
        self,
        session: Session,
        model: type[M],
        record_model: type[T],
        id_field: str,
    ) -> None:
        self._session = session
        self._model = model
        self._record_model = record_model
        self._id_field = id_field

    def _get_id(self, record: T) -> str:
        return getattr(record, self._id_field)

    def list(self) -> list[T]:
        rows = self._session.scalars(select(self._model)).all()
        return [_record_from_payload(self._record_model, row.payload) for row in rows]

    def get(self, entry_id: str) -> T | None:
        row = self._session.get(self._model, entry_id)
        if row is None:
            return None
        return _record_from_payload(self._record_model, row.payload)

    def upsert(self, record: T) -> T:
        entry_id = self._get_id(record)
        row = self._session.get(self._model, entry_id)
        if row is None:
            row = self._model(**{self._id_field: entry_id})
            self._session.add(row)
        _governed_from_record(record, row)
        self._session.flush()
        return record

    def delete(self, entry_id: str) -> bool:
        row = self._session.get(self._model, entry_id)
        if row is None:
            return False
        self._session.delete(row)
        return True

    def clear(self) -> None:
        self._session.execute(delete(self._model))


class BindingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list(self) -> list[dict[str, str]]:
        from open_grace_registry_db.models import AgentCapabilityBinding

        rows = self._session.scalars(select(AgentCapabilityBinding)).all()
        return [
            {"agent_id": row.agent_id, "capability_class_id": row.capability_class_id}
            for row in rows
        ]

    def replace_all(self, bindings: list[dict[str, str]]) -> int:
        from open_grace_registry_db.models import AgentCapabilityBinding

        self._session.execute(delete(AgentCapabilityBinding))
        for binding in bindings:
            self._session.add(
                AgentCapabilityBinding(
                    agent_id=binding["agent_id"],
                    capability_class_id=binding["capability_class_id"],
                )
            )
        return len(bindings)


class KnowledgeRepository:
  """Knowledge entries with type discriminator."""

  KNOWLEDGE_TYPES = (
      "entity",
      "species",
      "place",
      "heritage",
      "collection",
      "media",
      "knowledge_graph",
  )

  def __init__(self, session: Session) -> None:
      from open_grace_knowledge.schemas import (
          CollectionRegistryRecord,
          EntityRegistryRecord,
          HeritageRegistryRecord,
          KnowledgeGraphRegistryRecord,
          MediaRegistryRecord,
          PlaceRegistryRecord,
          SpeciesRegistryRecord,
      )
      from open_grace_registry_db.models import KnowledgeEntry

      self._session = session
      self._model = KnowledgeEntry
      self._type_map = {
          "entity": (EntityRegistryRecord, "entity_id"),
          "species": (SpeciesRegistryRecord, "species_id"),
          "place": (PlaceRegistryRecord, "place_id"),
          "heritage": (HeritageRegistryRecord, "heritage_id"),
          "collection": (CollectionRegistryRecord, "collection_id"),
          "media": (MediaRegistryRecord, "media_id"),
          "knowledge_graph": (KnowledgeGraphRegistryRecord, "graph_id"),
      }

  def list(self, knowledge_type: str | None = None) -> list[BaseModel]:
      stmt = select(self._model)
      if knowledge_type:
          stmt = stmt.where(self._model.knowledge_type == knowledge_type)
      rows = self._session.scalars(stmt).all()
      results: list[BaseModel] = []
      for row in rows:
          model, _ = self._type_map[row.knowledge_type]
          results.append(model.model_validate(row.payload))
      return results

  def upsert(self, knowledge_type: str, record: BaseModel) -> BaseModel:
      model, id_field = self._type_map[knowledge_type]
      entry_id = getattr(record, id_field)
      row = self._session.get(self._model, entry_id)
      if row is None:
          row = self._model(entry_id=entry_id, knowledge_type=knowledge_type)
          self._session.add(row)
      row.knowledge_type = knowledge_type
      row.lifecycle_stage = record.lifecycle_stage.value if hasattr(record.lifecycle_stage, "value") else str(record.lifecycle_stage)
      row.created_at = record.created_at
      row.updated_at = record.updated_at
      row.steward_actor = record.steward_actor
      row.reference_models = list(record.reference_models)
      row.payload = record.model_dump(mode="json")
      self._session.flush()
      return record

  def clear(self) -> None:
      self._session.execute(delete(self._model))


class ExecutionRepository:
    def __init__(self, session: Session) -> None:
        from open_grace_registry_db.models import ExecutionEntry
        from open_grace_runtime.schemas import ExecutionRecord

        self._session = session
        self._model = ExecutionEntry
        self._record_model = ExecutionRecord

    def list(self) -> list:
        rows = self._session.scalars(select(self._model)).all()
        return [self._record_model.model_validate(row.payload) for row in rows]

    def get(self, run_id: str):
        row = self._session.get(self._model, run_id)
        if row is None:
            return None
        return self._record_model.model_validate(row.payload)

    def upsert(self, record) -> object:
        row = self._session.get(self._model, record.run_id)
        if row is None:
            row = self._model(
                run_id=record.run_id,
                agent_id=record.agent_id,
                status=record.status.value if hasattr(record.status, "value") else str(record.status),
            )
            self._session.add(row)
        row.agent_id = record.agent_id
        row.status = record.status.value if hasattr(record.status, "value") else str(record.status)
        row.payload = record.model_dump(mode="json")
        self._session.flush()
        return record
