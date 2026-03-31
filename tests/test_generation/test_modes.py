"""Tests for custom_modes.yaml generation.

Covers T045: User Story 5 - Generate custom_modes.yaml.
"""

import pytest

from riseon_agents.generation.modes import HandoffSectionGenerator, ModesGenerator
from riseon_agents.models.agent import PermissionLevel, PrimaryAgent, Subagent


class TestHandoffSection:
    """T101-T105: Tests for handoff section generation."""

    def test_generate_returns_markdown_table(self):
        """T101: HandoffSectionGenerator.generate() returns Markdown table."""
        subagents = [
            Subagent(
                name="code-reviewer",
                description="Reviews code for quality",
                markdown_body="# Code Reviewer",
                permissions={},
            ),
        ]
        result = HandoffSectionGenerator.generate(["code-reviewer"], subagents)
        assert result is not None
        assert "| Subagent | Description |" in result
        assert "| code-reviewer | Reviews code for quality |" in result
        assert "## Available Subagents for Delegation" in result

    def test_empty_handoffs_returns_none(self):
        """T103: Empty handoffs list returns None."""
        subagents = [
            Subagent(
                name="code-reviewer",
                description="Reviews code for quality",
                markdown_body="# Code Reviewer",
                permissions={},
            ),
        ]
        result = HandoffSectionGenerator.generate([], subagents)
        assert result is None

    def test_invalid_handoff_slug_returns_none(self):
        """T103: Invalid handoff slug returns None."""
        subagents = [
            Subagent(
                name="code-reviewer",
                description="Reviews code for quality",
                markdown_body="# Code Reviewer",
                permissions={},
            ),
        ]
        result = HandoffSectionGenerator.generate(["non-existent"], subagents)
        assert result is None


class TestHandoffSectionIntegration:
    """T102: Tests for handoff section integration in _generate_mode_entry."""

    def test_mode_entry_includes_handoff_section_when_handoffs_exist(self, tmp_path):
        """Handoff section appears in generated mode entry."""
        subagent = Subagent(
            name="code-reviewer",
            description="Reviews code for quality",
            markdown_body="# Code Reviewer",
            permissions={},
        )
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[subagent],
            handoffs=["code-reviewer"],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        assert result.success
        content = result.files[0].path.read_text()
        assert "## Available Subagents for Delegation" in content
        assert "| code-reviewer |" in content

    def test_mode_entry_excludes_handoff_section_when_no_handoffs(self, tmp_path):
        """No handoff section when agent has no handoffs."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            handoffs=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        assert result.success
        content = result.files[0].path.read_text()
        assert "## Available Subagents for Delegation" not in content


class TestModesGenerator:
    """T045: Tests for custom_modes.yaml generation."""

    def test_generator_exists(self):
        """ModesGenerator can be instantiated."""
        generator = ModesGenerator()
        assert generator is not None

    def test_generate_single_agent(self, tmp_path):
        """Generate custom_modes.yaml for single agent."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect\n\nYou are an architect.",
            permissions={"edit": PermissionLevel.ALLOW},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        assert result.success
        assert len(result.files) == 1
        assert result.files[0].path.name == "custom_modes.yaml"

    def test_generate_multiple_agents(self, tmp_path):
        """Generate custom_modes.yaml for multiple agents."""
        agents = [
            PrimaryAgent(
                name="architect",
                description="Software architect",
                markdown_body="# Architect",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            ),
            PrimaryAgent(
                name="developer",
                description="Software developer",
                markdown_body="# Developer",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            ),
        ]

        generator = ModesGenerator()
        result = generator.generate(agents, tmp_path)

        assert result.success
        assert len(result.files) == 1

    def test_output_contains_agent_slug(self, tmp_path):
        """Generated file contains agent slug."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "architect" in content

    def test_output_contains_description(self, tmp_path):
        """Generated file contains agent description."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect specialist",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "Software architect specialist" in content

    def test_output_contains_markdown_body(self, tmp_path):
        """Generated file contains markdown body as roleDefinition."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Role\n\nYou are an expert.",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "roleDefinition" in content
        assert "You are an expert" in content

    def test_permissions_map_to_groups(self, tmp_path):
        """Permissions map to appropriate groups."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={"edit": PermissionLevel.ALLOW, "bash": PermissionLevel.ALLOW},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "groups" in content

    def test_empty_agents_list(self, tmp_path):
        """Handle empty agents list gracefully."""
        generator = ModesGenerator()
        result = generator.generate([], tmp_path)

        # Should have error files
        assert result.error_count > 0
        assert len(result.files) > 0

    def test_yaml_is_valid(self, tmp_path):
        """Generated YAML is valid."""
        import yaml

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()

        # Should be valid YAML
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            pytest.fail(f"Generated YAML is invalid: {e}")

    def test_file_written_to_disk(self, tmp_path):
        """File is actually written to target directory."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        output_path = tmp_path / "custom_modes.yaml"
        assert output_path.exists()
        assert output_path.read_text() == result.files[0].path.read_text()


class TestEmojiInName:
    """T506: Tests for emoji inclusion in generated agent name."""

    def test_emoji_from_agent_field_included_in_name(self, tmp_path):
        """T506: Explicit emoji from agent.emoji field appears in name."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            handoffs=[],
            rules=[],
            skills=[],
            emoji="🏗️",
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        assert result.success
        content = result.files[0].path.read_text()
        assert "🏗️ Architect" in content

    def test_no_emoji_field_excludes_emoji_from_name(self, tmp_path):
        """T506: Agent with no emoji field uses display_name without emoji prefix."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            handoffs=[],
            rules=[],
            skills=[],
            emoji=None,
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        assert result.success
        content = result.files[0].path.read_text()
        # No emoji prefix, just plain display name
        assert "name: Architect" in content

    def test_emoji_appears_before_display_name(self, tmp_path):
        """T506: Emoji appears at beginning of name field."""
        agent = PrimaryAgent(
            name="security-agent",
            description="Security specialist",
            markdown_body="# Security",
            permissions={},
            subagents=[],
            handoffs=[],
            rules=[],
            skills=[],
            emoji="🔒",
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        content = result.files[0].path.read_text()
        assert "name: 🔒 Security Agent" in content
