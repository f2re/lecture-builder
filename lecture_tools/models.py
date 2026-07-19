from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

Severity = Literal["error", "warning", "info"]


@dataclass(slots=True)
class Finding:
    code: str
    message: str
    severity: Severity = "error"
    path: str | None = None
    location: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ValidationResult:
    name: str
    findings: list[Finding] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)

    @property
    def errors(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [item for item in self.findings if item.severity == "warning"]

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(
        self,
        code: str,
        message: str,
        *,
        severity: Severity = "error",
        path: str | Path | None = None,
        location: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.findings.append(
            Finding(
                code=code,
                message=message,
                severity=severity,
                path=str(path) if path is not None else None,
                location=location,
                details=details or {},
            )
        )

    def extend(self, other: "ValidationResult") -> None:
        self.findings.extend(other.findings)
        self.metrics.update(other.metrics)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "findings": len(self.findings),
            },
            "metrics": self.metrics,
            "findings": [item.to_dict() for item in self.findings],
        }
