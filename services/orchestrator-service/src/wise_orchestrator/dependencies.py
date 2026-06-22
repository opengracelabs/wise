"""FastAPI dependencies."""

from __future__ import annotations

from wise_orchestrator.rc1_run_service import RC1RunService
from wise_orchestrator.run_service import RunService

_run_service: RunService | None = None
_rc1_run_service: RC1RunService | None = None


def set_run_service(service: RunService) -> None:
    global _run_service
    _run_service = service


def set_rc1_run_service(service: RC1RunService) -> None:
    global _rc1_run_service
    _rc1_run_service = service


def get_run_service() -> RunService:
    if _run_service is None:
        raise RuntimeError("RunService not initialized")
    return _run_service


def get_rc1_run_service() -> RC1RunService:
    if _rc1_run_service is None:
        raise RuntimeError("RC1RunService not initialized")
    return _rc1_run_service


def clear_run_service() -> None:
    global _run_service, _rc1_run_service
    if _run_service is not None:
        _run_service.close()
    _run_service = None
    if _rc1_run_service is not None:
        _rc1_run_service.close()
    _rc1_run_service = None
