"""Main generator orchestrator.

Implements T054: User Story 5 - Create KiloCodeGenerator orchestrator.
"""

from pathlib import Path

from riseon_agents.models.agent import PrimaryAgent
from riseon_agents.models.generation import (
    FileStatus,
    GeneratedFile,
    GenerationLevel,
    GenerationResult,
    GenerationTarget,
)
from riseon_agents.generation.modes import ModesGenerator
from riseon_agents.generation.subagents import SubagentsGenerator
from riseon_agents.generation.rules import RulesGenerator
from riseon_agents.generation.skills import SkillsGenerator


class KiloCodeGenerator:
    """Main orchestrator for generating Kilo Code configuration files.

    Coordinates the generation of all configuration files:
    - custom_modes.yaml (Primary Agents)
    - .kilo/agents/*.md (Subagents)
    - .kilo/rules/*.md (Shared rules)
    - .kilo/rules-{mode}/*.md (Mode-specific rules)
    - .kilocode/skills/{skill}/SKILL.md (Skills)
    """

    def __init__(self) -> None:
        """Initialize the generator with sub-generators."""
        self.modes_gen = ModesGenerator()
        self.subagents_gen = SubagentsGenerator()
        self.rules_gen = RulesGenerator()
        self.skills_gen = SkillsGenerator()

    def generate(
        self,
        agents: list[PrimaryAgent],
        level: GenerationLevel,
        base_dir: Path,
        overwrite: bool = False,
    ) -> GenerationResult:
        """Generate all configuration files for the selected agents.

        Args:
            agents: List of selected PrimaryAgent objects.
            level: Generation level (LOCAL or GLOBAL).
            base_dir: Base directory for generation (project root for LOCAL).
            overwrite: Whether to overwrite existing files.

        Returns:
            GenerationResult with all generated files and status.
        """
        result = GenerationResult()

        if not agents:
            result.add_file(
                path=base_dir / "custom_modes.yaml",
                status=FileStatus.ERROR,
                error_message="No agents selected for generation. Please select at least one agent.",
            )
            return result

        try:
            # Determine target directories
            if level == GenerationLevel.LOCAL:
                kilo_dir = base_dir / ".kilo"
                kilocode_dir = base_dir / ".kilocode"
            else:  # GLOBAL
                # Use ~/.kilocode/ for global
                kilo_dir = Path.home() / ".kilocode"
                kilocode_dir = kilo_dir

            # Create directories
            kilo_dir.mkdir(parents=True, exist_ok=True)
            kilocode_dir.mkdir(parents=True, exist_ok=True)

            # Generate custom_modes.yaml
            try:
                modes_result = self.modes_gen.generate(agents, kilo_dir)
                result.files.extend(modes_result.files)
            except Exception as e:
                result.add_file(
                    path=kilo_dir / "custom_modes.yaml",
                    status=FileStatus.ERROR,
                    error_message=f"Modes generation failed: {e}",
                )

            # Collect all subagents, rules, and skills from selected agents
            all_subagents = []
            all_rules = []
            all_skills = []

            for agent in agents:
                all_subagents.extend(agent.subagents)
                all_rules.extend(agent.rules)
                all_skills.extend(agent.skills)

            # Generate subagent files
            if all_subagents:
                try:
                    subagents_result = self.subagents_gen.generate(all_subagents, kilo_dir)
                    result.files.extend(subagents_result.files)
                except Exception as e:
                    result.add_file(
                        path=kilo_dir / "agents",
                        status=FileStatus.ERROR,
                        error_message=f"Subagents generation failed: {e}",
                    )

            # Generate rule files
            if all_rules:
                try:
                    rules_result = self.rules_gen.generate(all_rules, kilo_dir)
                    result.files.extend(rules_result.files)
                except Exception as e:
                    result.add_file(
                        path=kilo_dir / "rules",
                        status=FileStatus.ERROR,
                        error_message=f"Rules generation failed: {e}",
                    )

            # Generate skill files
            if all_skills:
                try:
                    skills_result = self.skills_gen.generate(all_skills, kilocode_dir)
                    result.files.extend(skills_result.files)
                except Exception as e:
                    result.add_file(
                        path=kilocode_dir / "skills",
                        status=FileStatus.ERROR,
                        error_message=f"Skills generation failed: {e}",
                    )

            return result

        except Exception as e:
            result.add_file(
                path=base_dir / "generation",
                status=FileStatus.ERROR,
                error_message=f"Generation failed: {e}",
            )
            return result

        try:
            # Determine target directories
            if level == GenerationLevel.LOCAL:
                kilo_dir = base_dir / ".kilo"
                kilocode_dir = base_dir / ".kilocode"
            else:  # GLOBAL
                # Use ~/.kilocode/ for global
                kilo_dir = Path.home() / ".kilocode"
                kilocode_dir = kilo_dir

            # Create directories
            kilo_dir.mkdir(parents=True, exist_ok=True)
            kilocode_dir.mkdir(parents=True, exist_ok=True)

            all_files = []
            errors = []

            # Generate custom_modes.yaml
            try:
                modes_result = self.modes_gen.generate(agents, kilo_dir)
                if modes_result.success:
                    all_files.extend(modes_result.files)
                else:
                    errors.append(modes_result.error_message or "Modes generation failed")
            except Exception as e:
                errors.append(f"Modes generation failed: {e}")

            # Collect all subagents, rules, and skills from selected agents
            all_subagents = []
            all_rules = []
            all_skills = []

            for agent in agents:
                all_subagents.extend(agent.subagents)
                all_rules.extend(agent.rules)
                all_skills.extend(agent.skills)

            # Generate subagent files
            if all_subagents:
                try:
                    subagents_result = self.subagents_gen.generate(all_subagents, kilo_dir)
                    if subagents_result.success:
                        all_files.extend(subagents_result.files)
                    else:
                        errors.append(
                            subagents_result.error_message or "Subagents generation failed"
                        )
                except Exception as e:
                    errors.append(f"Subagents generation failed: {e}")

            # Generate rule files
            if all_rules:
                try:
                    rules_result = self.rules_gen.generate(all_rules, kilo_dir)
                    if rules_result.success:
                        all_files.extend(rules_result.files)
                    else:
                        errors.append(rules_result.error_message or "Rules generation failed")
                except Exception as e:
                    errors.append(f"Rules generation failed: {e}")

            # Generate skill files
            if all_skills:
                try:
                    skills_result = self.skills_gen.generate(all_skills, kilocode_dir)
                    if skills_result.success:
                        all_files.extend(skills_result.files)
                    else:
                        errors.append(skills_result.error_message or "Skills generation failed")
                except Exception as e:
                    errors.append(f"Skills generation failed: {e}")

            # Check if we generated anything
            if not all_files:
                return GenerationResult(
                    success=False,
                    files=[],
                    error_message="No files were generated. " + "; ".join(errors) if errors else "",
                )

            # Return result
            return GenerationResult(
                success=len(errors) == 0,
                files=all_files,
                error_message="; ".join(errors) if errors else None,
            )

        except Exception as e:
            return GenerationResult(
                success=False,
                files=[],
                error_message=f"Generation failed: {e}",
            )

    def check_existing_files(
        self,
        agents: list[PrimaryAgent],
        level: GenerationLevel,
        base_dir: Path,
    ) -> list[Path]:
        """Check for existing files that would be overwritten.

        Args:
            agents: List of selected PrimaryAgent objects.
            level: Generation level.
            base_dir: Base directory.

        Returns:
            List of existing file paths.
        """
        existing = []

        # Determine target directories
        if level == GenerationLevel.LOCAL:
            kilo_dir = base_dir / ".kilo"
        else:
            kilo_dir = Path.home() / ".kilocode"

        # Check custom_modes.yaml
        modes_file = kilo_dir / "custom_modes.yaml"
        if modes_file.exists():
            existing.append(modes_file)

        # Check agent files
        for agent in agents:
            # Subagent files
            for subagent in agent.subagents:
                subagent_file = kilo_dir / "agents" / f"{subagent.slug}.md"
                if subagent_file.exists():
                    existing.append(subagent_file)

            # Rule files
            for rule in agent.rules:
                if rule.is_shared:
                    rule_file = kilo_dir / "rules" / f"{rule.filename}"
                else:
                    mode_slug = rule.mode_slug or "default"
                    rule_file = kilo_dir / f"rules-{mode_slug}" / f"{rule.filename}"
                if rule_file.exists():
                    existing.append(rule_file)

            # Skill files
            for skill in agent.skills:
                if level == GenerationLevel.LOCAL:
                    skill_file = base_dir / ".kilocode" / "skills" / skill.name / "SKILL.md"
                else:
                    skill_file = Path.home() / ".kilocode" / "skills" / skill.name / "SKILL.md"
                if skill_file.exists():
                    existing.append(skill_file)

        return existing
