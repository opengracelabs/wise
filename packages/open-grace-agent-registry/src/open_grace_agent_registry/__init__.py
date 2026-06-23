"""Open Grace Agent, Capability, and Model registries."""

from open_grace_agent_registry.agent_registry import AgentRegistry
from open_grace_agent_registry.capability_registry import CapabilityRegistry
from open_grace_agent_registry.model_registry import ModelRegistry
from open_grace_agent_registry.nature_culture import (
    NatureCultureAgentRecord,
    NatureCultureAgentRegistry,
    register_nature_culture_agents,
)

__version__ = "1.0.0"

__all__ = [
    "AgentRegistry",
    "CapabilityRegistry",
    "ModelRegistry",
    "NatureCultureAgentRecord",
    "NatureCultureAgentRegistry",
    "register_nature_culture_agents",
]
