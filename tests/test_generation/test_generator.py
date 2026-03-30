"""Tests for KiloCodeGenerator orchestrator.

Covers T049: User Story 5 - Test generator orchestration.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from riseon_agents.models.agent import PermissionLevel, PrimaryAgent, Subagent
from riseon_agents.models.generation import FileStatus, GenerationLevel, GenerationResult
from riseon_agents.models.rule import Rule
from riseon_agents.models.skill import Skill
from riseon_agents.generation.generator import KiloCodeGenerator


class TestKiloCodeGenerator:
    """T049: Tests for generator orchestrator."""

    def test_generator_exists(self):
        """KiloCodeGenerator can be instantiated."""
        generator = KiloCodeGenerator()
        assert generator is not None

    def test_generate_requires_selection(self, tmp_path):
        """Generation requires at least one selected agent."""
        generator = KiloCodeGenerator()
        result = generator.generate([], GenerationLevel.LOCAL, tmp_path)

        # Should have errors
        assert result.error_count > 0

    def test_generate_local_target(self, tmp_path):
        """Generate to Local target creates .kilo/ directory."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        # Mock the individual generators to avoid dependencies
        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        assert result.error_count == 0

    def test_generate_creates_directories(self, tmp_path):
        """Generation creates necessary directories."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        # Check .kilo directory was created
        kilo_dir = tmp_path / ".kilo"
        assert kilo_dir.exists()

    def test_result_contains_file_list(self, tmp_path):
        """Generation result contains list of generated files."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        # Create a mock file
        mock_file = MagicMock()
        mock_file.path = tmp_path / "custom_modes.yaml"
        mock_file.status = FileStatus.CREATED

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[mock_file])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        assert len(result.files) > 0

    def test_error_handling(self, tmp_path):
        """Handle errors during generation gracefully."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        with patch.object(generator.modes_gen, "generate") as mock_modes:
            mock_modes.side_effect = Exception("Generation failed")

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        assert result.error_count > 0
        assert "Generation failed" in "; ".join([f.error_message for f in result.error_files if f.error_message])

    def test_overwrite_existing_files(self, tmp_path):
        """Overwrite existing files when requested."""
        # Create an existing file
        kilo_dir = tmp_path / ".kilo"
        kilo_dir.mkdir()
        existing_file = kilo_dir / "custom_modes.yaml"
        existing_file.write_text("old content")

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        # Create a mock file
        mock_file = MagicMock()
        mock_file.path = existing_file
        mock_file.status = FileStatus.UPDATED
        mock_file.content = "new content"

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[mock_file])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path, overwrite=True)

        assert result.error_count == 0

    def test_collects_all_agent_children(self, tmp_path):
        """Generator collects subagents, rules, and skills from agents."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR",
            permissions={},
        )

        rule = Rule(
            name="code-style",
            content="# Code Style",
            is_shared=True,
        )

        skill = Skill(
            name="my-skill",
            description="My skill",
            content="# Skill",
            source_path=tmp_path / "my-skill" / "SKILL.md",
        )

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[subagent],
            rules=[rule],
            skills=[skill],
        )

        generator = KiloCodeGenerator()

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

            # Verify that all generators were called
            mock_modes.assert_called_once()
            mock_subagents.assert_called_once()
            mock_rules.assert_called_once()
            mock_skills.assert_called_once()
