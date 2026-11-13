from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class Node:
    label: str
    children: List['Node'] = field(default_factory=list)
    value: Any = None
    production: Optional[str] = None
    attribute: Optional[str] = None

    def add_child(self, child: 'Node') -> None:
        self.children.append(child)

    def __str__(self):
        return f"{self.label}:{self.value}"
