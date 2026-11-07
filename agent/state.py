
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"


class ActionType(Enum):
    CALL_TOOL = "call_tool"
    FINISH = "finish"


@dataclass
class AgentAction:
    action_type: ActionType
    tool_name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    success: bool
    output: Any = None
    error: str | None = None


@dataclass
class AgentState:
    task: str
    status: AgentStatus = AgentStatus.IDLE
    step_count: int = 0
    max_steps: int = 10
    history: list[dict[str, Any]] = field(default_factory=list)
