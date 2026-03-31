"""Tests for BrandedHeader widget.

Implements T603: User Story 6 - Visual Redesign (Branded Header).
"""

from riseon_agents.widgets.header import BrandedHeader


class TestBrandedHeader:
    """T603: Tests for BrandedHeader widget."""

    def test_branded_header_class_exists(self):
        """T603: BrandedHeader class exists."""
        header = BrandedHeader()
        assert header is not None

    def test_branded_header_has_app_name(self):
        """T603: BrandedHeader contains application name."""
        header = BrandedHeader()
        assert hasattr(header, "APP_NAME")
        assert "RiseOn" in header.APP_NAME

    def test_branded_header_has_version(self):
        """T603: BrandedHeader can display version."""
        header = BrandedHeader()
        assert hasattr(header, "APP_VERSION")
        assert isinstance(header.APP_VERSION, str)

    def test_branded_header_has_compose_method(self):
        """T603: BrandedHeader has compose method."""
        header = BrandedHeader()
        assert hasattr(header, "compose")
        assert callable(header.compose)

    def test_branded_header_is_widget(self):
        """T603: BrandedHeader is a Widget subclass."""
        from textual.widget import Widget

        assert issubclass(BrandedHeader, Widget)

    def test_branded_header_has_css(self):
        """T603: BrandedHeader has CSS styling."""
        assert BrandedHeader.DEFAULT_CSS is not None
        assert len(BrandedHeader.DEFAULT_CSS) > 0
