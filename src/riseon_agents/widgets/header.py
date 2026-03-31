"""Branded header widget for RiseOn.Agents TUI application.

T608: BrandedHeader widget showing application name and version.
Implements US6 - Complete Visual Redesign.
"""

from importlib.metadata import PackageNotFoundError, version

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


def _get_version() -> str:
    """Get the package version, returning 'dev' if not installed."""
    try:
        return version("riseon-agents")
    except PackageNotFoundError:
        return "dev"


class BrandedHeader(Widget):
    """Stylized application header displaying name and version.

    T608: Shows 'RiseOn.Agents' with the current version in a styled banner.
    """

    APP_NAME = "RiseOn.Agents"
    APP_VERSION = _get_version()

    DEFAULT_CSS = """
    BrandedHeader {
        width: 100%;
        height: 3;
        background: $surface-darken-1;
        border-bottom: solid $success;
        content-align: center middle;
    }

    BrandedHeader #header-content {
        width: 100%;
        height: 100%;
        content-align: center middle;
        color: $success;
        text-style: bold;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the branded header."""
        title = f"🤖 {self.APP_NAME} v{self.APP_VERSION} — Kilo Code Configuration Generator"
        yield Static(title, id="header-content")
