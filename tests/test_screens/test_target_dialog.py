"""Tests for target selection dialog.

T201-T206: Tests for TargetSelectionDialog.
"""

import pytest

from riseon_agents.models.generation import GenerationLevel
from riseon_agents.screens.target_dialog import TargetSelectionDialog, TargetSelectionResult


class TestTargetSelectionResult:
    """T201: Tests for TargetSelectionResult dataclass."""

    def test_cancelled_result_has_cancelled_true(self):
        """Cancelled result has cancelled=True."""
        result = TargetSelectionResult.cancelled_result()
        assert result.cancelled is True
        assert result.level is None

    def test_selected_local_level(self):
        """Selected result with LOCAL level."""
        result = TargetSelectionResult.selected(GenerationLevel.LOCAL)
        assert result.cancelled is False
        assert result.level == GenerationLevel.LOCAL

    def test_selected_global_level(self):
        """Selected result with GLOBAL level."""
        result = TargetSelectionResult.selected(GenerationLevel.GLOBAL)
        assert result.cancelled is False
        assert result.level == GenerationLevel.GLOBAL

    def test_result_dataclass_fields(self):
        """Result has expected fields."""
        result = TargetSelectionResult(level=GenerationLevel.LOCAL, cancelled=False)
        assert result.level == GenerationLevel.LOCAL
        assert result.cancelled is False


class TestTargetSelectionDialog:
    """T202-T206: Tests for TargetSelectionDialog structure."""

    def test_dialog_class_exists(self):
        """TargetSelectionDialog class exists."""
        assert TargetSelectionDialog is not None

    def test_dialog_has_compose_method(self):
        """Dialog has compose method."""
        dialog = TargetSelectionDialog()
        assert hasattr(dialog, "compose")
        assert callable(dialog.compose)

    def test_dialog_has_cancel_binding(self):
        """Dialog has ESC binding for cancel."""
        dialog = TargetSelectionDialog()
        bindings = getattr(dialog, "BINDINGS", [])
        escape_bindings = [b for b in bindings if "escape" in b[0]]
        assert len(escape_bindings) > 0

    def test_dialog_uses_modal_screen(self):
        """Dialog inherits from ModalScreen."""
        from textual.screen import ModalScreen

        assert issubclass(TargetSelectionDialog, ModalScreen)

    def test_dialog_default_css_is_defined(self):
        """Dialog has DEFAULT_CSS defined."""
        assert hasattr(TargetSelectionDialog, "DEFAULT_CSS")
        assert "TargetSelectionDialog" in TargetSelectionDialog.DEFAULT_CSS
