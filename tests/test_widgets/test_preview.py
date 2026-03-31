"""Tests for PreviewPanel widget.

Implements T060-T061: User Story 3 - Preview Generated Configuration.
Implements T401-T404: User Story 4 - Enhanced Preview for Rules and Skills.
"""

import pytest
from rich.syntax import Syntax

from riseon_agents.models.agent import PermissionLevel, PrimaryAgent, Subagent
from riseon_agents.models.rule import Rule
from riseon_agents.models.skill import Skill
from riseon_agents.widgets.preview import PreviewPanel


class TestPreviewPanel:
    """Test suite for PreviewPanel widget."""

    @pytest.fixture
    def sample_primary_agent(self):
        """Create a sample PrimaryAgent for testing."""
        return PrimaryAgent(
            name="test-agent",
            description="A test agent for preview",
            markdown_body="# Test Agent\n\nThis is a test agent.",
            permissions={
                "edit": PermissionLevel.ALLOW,
                "bash": PermissionLevel.ASK,
            },
            subagents=[
                Subagent(
                    name="sub-1",
                    description="Subagent 1",
                    markdown_body="Subagent content",
                    permissions={"edit": PermissionLevel.ALLOW},
                    temperature=0.7,
                    parent_agent="test-agent",
                )
            ],
            rules=[
                Rule(
                    name="rule-1",
                    content="Always do this",
                )
            ],
            skills=[
                Skill(
                    name="skill-1",
                    description="Test skill",
                    content="Skill content here",
                )
            ],
        )

    @pytest.fixture
    def sample_subagent(self):
        """Create a sample Subagent for testing."""
        return Subagent(
            name="sample-sub",
            description="A sample subagent",
            markdown_body="# Sample Subagent\n\nContent here.",
            permissions={"edit": PermissionLevel.ALLOW},
            temperature=0.5,
            parent_agent="parent-agent",
        )

    @pytest.fixture
    def sample_rule(self):
        """Create a sample Rule for testing."""
        return Rule(
            name="test-rule",
            content="This is the rule content",
        )

    @pytest.fixture
    def sample_skill(self):
        """Create a sample Skill for testing."""
        return Skill(
            name="test-skill",
            description="A test skill",
            content="Skill implementation details",
        )

    def test_panel_initialization(self):
        """T060: Test preview panel initializes correctly."""
        panel = PreviewPanel()
        assert panel is not None
        # content_widget is created in compose(), not in __init__

    def test_preview_generation_for_primary_agent(self, sample_primary_agent):
        """T060: Test preview content generation for PrimaryAgent."""
        panel = PreviewPanel()
        content = panel.generate_preview_for_agent(sample_primary_agent)

        # Should show custom_modes.yaml format
        assert "custom_modes.yaml" in content or "slug:" in content
        assert sample_primary_agent.slug in content
        assert sample_primary_agent.display_name in content

    def test_preview_generation_for_subagent(self, sample_subagent):
        """T060: Test preview content generation for Subagent."""
        panel = PreviewPanel()
        content = panel.generate_preview_for_subagent(sample_subagent)

        # Should show .kilo/agents/*.md format
        assert "subagent" in content.lower() or "mode:" in content
        assert sample_subagent.slug in content
        assert sample_subagent.description in content

    def test_preview_generation_for_rule(self, sample_rule):
        """T060: Test preview content generation for Rule."""
        panel = PreviewPanel()
        content = panel.generate_preview_for_rule(sample_rule)

        assert sample_rule.name in content
        assert sample_rule.content in content

    def test_preview_generation_for_skill(self, sample_skill):
        """T060: Test preview content generation for Skill."""
        panel = PreviewPanel()
        content = panel.generate_preview_for_skill(sample_skill)

        assert sample_skill.name in content
        assert sample_skill.description in content

    def test_panel_has_scrollable_content(self):
        """T060: Test panel content is scrollable (US3-AC4)."""
        panel = PreviewPanel()
        # Panel should have overflow/scroll capability through CSS
        assert "overflow: auto scroll" in PreviewPanel.DEFAULT_CSS

    def test_preview_includes_syntax_highlighting_indicators(self, sample_primary_agent):
        """T060: Test preview has syntax highlighting markers."""
        panel = PreviewPanel()
        content = panel.generate_preview_for_agent(sample_primary_agent)

        # YAML content should be present
        assert "slug:" in content or "customModes:" in content


class TestPreviewEnhanced:
    """T401-T404: Tests for enhanced preview with Markdown highlighting and handoffs."""

    @pytest.fixture
    def sample_rule(self):
        """Create a sample Rule for testing."""
        return Rule(
            name="test-rule",
            content="# Test Rule\n\nAlways follow best practices.\n\n- Use type hints\n- Write tests",
        )

    @pytest.fixture
    def sample_skill(self):
        """Create a sample Skill for testing."""
        return Skill(
            name="test-skill",
            description="A test skill",
            content="---\nname: test-skill\ndescription: A test skill\n---\n\n# Skill Content",
        )

    @pytest.fixture
    def agent_with_handoffs(self):
        """Create a PrimaryAgent with handoffs defined."""
        subagent = Subagent(
            name="code-reviewer",
            description="Reviews code quality",
            markdown_body="# Code Reviewer",
            permissions={},
        )
        return PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect\n\nDesigns software systems.",
            permissions={},
            subagents=[subagent],
            handoffs=["code-reviewer"],
            rules=[],
            skills=[],
        )

    def test_rule_preview_uses_markdown_syntax(self, sample_rule):
        """T401: Rules preview uses Syntax(markdown)."""
        panel = PreviewPanel()
        syntax = panel.get_rule_syntax(sample_rule)
        assert isinstance(syntax, Syntax)
        assert syntax._lexer == "markdown"

    def test_skill_preview_uses_markdown_syntax(self, sample_skill):
        """T402: Skills preview uses Syntax(markdown)."""
        panel = PreviewPanel()
        syntax = panel.get_skill_syntax(sample_skill)
        assert isinstance(syntax, Syntax)
        assert syntax._lexer == "markdown"

    def test_long_descriptions_have_vertical_scroll(self):
        """T403: Long descriptions have vertical scroll capability."""
        # Panel CSS must include overflow scroll support
        assert "overflow: auto scroll" in PreviewPanel.DEFAULT_CSS

    def test_primary_agent_preview_includes_handoffs_section(self, agent_with_handoffs):
        """T404: PrimaryAgent preview includes handoffs section when handoffs defined."""
        panel = PreviewPanel()
        content = panel.generate_preview_for_agent(agent_with_handoffs)
        assert "Available Subagents for Delegation" in content
        assert "code-reviewer" in content

    def test_primary_agent_preview_no_handoffs_section_when_empty(self):
        """T404: PrimaryAgent preview omits handoffs section when none defined."""
        agent = PrimaryAgent(
            name="simple-agent",
            description="No handoffs",
            markdown_body="# Simple",
            permissions={},
            handoffs=[],
            subagents=[],
            rules=[],
            skills=[],
        )
        panel = PreviewPanel()
        content = panel.generate_preview_for_agent(agent)
        assert "Available Subagents for Delegation" not in content
