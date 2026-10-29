from dataclasses import dataclass, field
from datetime import date

@dataclass
class Task:
    title: str
    priority: int = 3
    due: date | None = None
    tags: list[str] = field(default_factory=list)
    done: bool = False

    def overdue(self) -> bool:
        return not self.done and self.due is not None and self.due < date.today()

t = Task("Renew SSL certificate", priority=1, due=date(2026, 11, 1), tags=["ops"])
print(t)
