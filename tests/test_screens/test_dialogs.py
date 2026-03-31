"""Tests for confirm dialog enhancements.

T301-T304: Tests for 3-button confirm dialog with Cancel.
"""

import pytest

from riseon_agents.screens.dialogs import ConfirmDialog


class TestConfirmDialog:
    """T301-T304: Tests for 3-button confirm dialog."""

    def test_confirm_result_enum_exists(self):
        """T301: ConfirmResult enum exists with YES, NO, CANCEL values."""
        from riseon_agents.screens.dialogs import ConfirmResult

        assert hasattr(ConfirmResult, "YES")
        assert hasattr(ConfirmResult, "NO")
        assert hasattr(ConfirmResult, "CANCEL")

    def test_confirm_result_values(self):
        """ConfirmResult has correct string values."""
        from riseon_agents.screens.dialogs import ConfirmResult

        assert ConfirmResult.YES.value == "yes"
        assert ConfirmResult.NO.value == "no"
        assert ConfirmResult.CANCEL.value == "cancel"

    def test_horizontal_button_layout(self):
        """T302: Buttons are in Horizontal container, not Vertical."""
        dialog = ConfirmDialog(title="Test", message="Test message")
        css = ConfirmDialog.DEFAULT_CSS
        assert "Horizontal" in css

    def test_cancel_button_in_compose_signature(self):
        """T303: Cancel button is yielded in compose method."""
        import inspect

        source = inspect.getsource(ConfirmDialog.compose)
        assert "Cancel" in source
        assert 'id="cancel"' in source

    def test_escape_binding_for_cancel(self):
        """T304: ESC binding exists for cancel action."""
        bindings = getattr(ConfirmDialog, "BINDINGS", [])
        has_escape = any("escape" in str(b).lower() for b in bindings)
        assert has_escape

    def test_dialog_inherits_from_modal_screen(self):
        """Dialog inherits from ModalScreen."""
        from textual.screen import ModalScreen

        assert issubclass(ConfirmDialog, ModalScreen)

    def test_cancel_action_method_exists(self):
        """action_cancel method exists."""
        dialog = ConfirmDialog(title="Test", message="Test message")
        assert hasattr(dialog, "action_cancel")
        assert callable(dialog.action_cancel)

    def test_on_button_pressed_handles_cancel(self):
        """on_button_pressed handles cancel button."""
        import inspect

        source = inspect.getsource(ConfirmDialog.on_button_pressed)
        assert "cancel" in source
        assert "ConfirmResult.CANCEL" in source
