"""Tests for SplashScreen.

Implements T601-T602: User Story 6 - Visual Redesign (Splash Screen).
"""

from riseon_agents.screens.splash import ASCII_LOGO, SplashScreen


class TestSplashScreen:
    """T601-T602: Tests for SplashScreen behavior."""

    def test_splash_screen_class_exists(self):
        """T601: SplashScreen class exists and can be instantiated."""
        screen = SplashScreen()
        assert screen is not None

    def test_ascii_logo_constant_exists(self):
        """T601: ASCII_LOGO constant is defined."""
        assert ASCII_LOGO is not None
        assert isinstance(ASCII_LOGO, str)
        assert len(ASCII_LOGO) > 0

    def test_ascii_logo_contains_riseon_agents(self):
        """T601: ASCII art contains 'RiseOn.Agents' text."""
        assert "RiseOn" in ASCII_LOGO or "RISEON" in ASCII_LOGO

    def test_splash_screen_has_compose_method(self):
        """T601: SplashScreen has a compose method."""
        screen = SplashScreen()
        assert hasattr(screen, "compose")
        assert callable(screen.compose)

    def test_splash_screen_display_duration(self):
        """T602: SplashScreen uses correct display duration (1.5s)."""
        screen = SplashScreen()
        assert screen.DISPLAY_DURATION == 1.5

    def test_splash_screen_is_modal(self):
        """T601: SplashScreen is a Screen subclass."""
        from textual.screen import Screen

        assert issubclass(SplashScreen, Screen)

    def test_splash_screen_has_css(self):
        """T601: SplashScreen has CSS styling defined."""
        assert SplashScreen.DEFAULT_CSS is not None
        assert len(SplashScreen.DEFAULT_CSS) > 0
