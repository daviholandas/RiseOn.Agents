"""Generation models for RiseOn.Agents.

Defines the data structures for configuration file generation including
target paths, file status tracking, and generation results.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class GenerationLevel(Enum):
    """Where to generate configuration files."""

    LOCAL = "local"  # Project: ./.kilo/
    GLOBAL = "global"  # User: ~/.kilocode/


class FileStatus(Enum):
    """Status of a generated file."""

    CREATED = "created"
    UPDATED = "updated"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class GenerationTarget:
    """Target configuration for generation.

    Resolves paths based on generation level (Local vs Global).
    """

    level: GenerationLevel
    base_path: Path  # Resolved absolute path (project root or home)

    @property
    def kilo_dir(self) -> Path:
        """Path to .kilo directory."""
        if self.level == GenerationLevel.LOCAL:
            return self.base_path / ".kilo"
        return self.base_path  # Global uses ~/.kilocode directly

    @property
    def kilocode_dir(self) -> Path:
        """Path to .kilocode directory (for skills)."""
        if self.level == GenerationLevel.LOCAL:
            return self.base_path / ".kilocode"
        return self.base_path  # Global uses ~/.kilocode directly

    @property
    def modes_file(self) -> Path:
        """Path to custom_modes.yaml."""
        return self.kilo_dir / "custom_modes.yaml"

    @property
    def agents_dir(self) -> Path:
        """Path to agents directory."""
        return self.kilo_dir / "agents"

    @property
    def rules_dir(self) -> Path:
        """Path to shared rules directory."""
        return self.kilo_dir / "rules"

    def rules_mode_dir(self, mode_slug: str) -> Path:
        """Path to mode-specific rules directory."""
        return self.kilo_dir / f"rules-{mode_slug}"

    @property
    def skills_dir(self) -> Path:
        """Path to skills directory."""
        return self.kilocode_dir / "skills"

    @classmethod
    def local(cls, project_root: Path) -> "GenerationTarget":
        """Create a local generation target."""
        return cls(level=GenerationLevel.LOCAL, base_path=project_root.resolve())

    @classmethod
    def global_(cls) -> "GenerationTarget":
        """Create a global generation target."""
        return cls(level=GenerationLevel.GLOBAL, base_path=Path.home() / ".kilocode")

    def ensure_directories(self) -> None:
        """Create all necessary directories for generation."""
        self.kilo_dir.mkdir(parents=True, exist_ok=True)
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.rules_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class GeneratedFile:
    """Result of generating a single file."""

    path: Path
    status: FileStatus
    error_message: str | None = None
    existed_before: bool = False

    @property
    def is_success(self) -> bool:
        """Check if the file was generated successfully."""
        return self.status in (FileStatus.CREATED, FileStatus.UPDATED)

    @property
    def is_error(self) -> bool:
        """Check if there was an error generating this file."""
        return self.status == FileStatus.ERROR


@dataclass
class GenerationResult:
    """Complete result of a generation operation."""

    files: list[GeneratedFile] = field(default_factory=list)
    target: GenerationTarget | None = None
    interrupted: bool = False

    def add_file(
        self,
        path: Path,
        status: FileStatus,
        error_message: str | None = None,
        existed_before: bool = False,
    ) -> GeneratedFile:
        """Add a file result to the generation."""
        file_result = GeneratedFile(
            path=path,
            status=status,
            error_message=error_message,
            existed_before=existed_before,
        )
        self.files.append(file_result)
        return file_result

    @property
    def created_count(self) -> int:
        """Count of newly created files."""
        return sum(1 for f in self.files if f.status == FileStatus.CREATED)

    @property
    def updated_count(self) -> int:
        """Count of updated files."""
        return sum(1 for f in self.files if f.status == FileStatus.UPDATED)

    @property
    def skipped_count(self) -> int:
        """Count of skipped files."""
        return sum(1 for f in self.files if f.status == FileStatus.SKIPPED)

    @property
    def error_count(self) -> int:
        """Count of files with errors."""
        return sum(1 for f in self.files if f.status == FileStatus.ERROR)

    @property
    def total_count(self) -> int:
        """Total count of files processed."""
        return len(self.files)

    @property
    def success_count(self) -> int:
        """Count of successfully generated files."""
        return self.created_count + self.updated_count

    @property
    def success(self) -> bool:
        """Check if generation completed without errors."""
        return self.error_count == 0 and not self.interrupted

    @property
    def error_files(self) -> list[GeneratedFile]:
        """Get list of files that had errors."""
        return [f for f in self.files if f.status == FileStatus.ERROR]

    def get_summary(self) -> str:
        """Get a human-readable summary of the generation result."""
        lines = []
        if self.interrupted:
            lines.append("Generation Interrupted")
        else:
            lines.append("Generation Complete" if self.success else "Generation Failed")

        lines.append("")
        lines.append(f"Created: {self.created_count} files")
        lines.append(f"Updated: {self.updated_count} files")
        lines.append(f"Skipped: {self.skipped_count} files")

        if self.error_count > 0:
            lines.append(f"Errors: {self.error_count} files")

        if self.target:
            level_str = "Local" if self.target.level == GenerationLevel.LOCAL else "Global"
            lines.append("")
            lines.append(f"Target: {level_str} ({self.target.base_path})")

        return "\n".join(lines)
