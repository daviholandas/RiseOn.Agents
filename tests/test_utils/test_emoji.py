"""Tests for EmojiMapper utility.

Implements T501-T504: User Story 5 - Emoji support.
"""

from riseon_agents.utils.emoji import EmojiMapper


class TestEmojiMapper:
    """T501-T504: Tests for EmojiMapper keyword matching."""

    def test_get_emoji_returns_keyword_match(self):
        """T501: EmojiMapper.get_emoji() returns correct emoji for known keyword."""
        assert EmojiMapper.get_emoji("architect") == "🏗️"
        assert EmojiMapper.get_emoji("engineer") == "🧑‍💻"
        assert EmojiMapper.get_emoji("writer") == "📝"
        assert EmojiMapper.get_emoji("devops") == "⚙️"
        assert EmojiMapper.get_emoji("security") == "🔒"

    def test_get_emoji_case_insensitive(self):
        """T502: EmojiMapper case-insensitive matching."""
        assert EmojiMapper.get_emoji("ARCHITECT") == "🏗️"
        assert EmojiMapper.get_emoji("Engineer") == "🧑‍💻"
        assert EmojiMapper.get_emoji("SECURITY") == "🔒"
        assert EmojiMapper.get_emoji("DevOps") == "⚙️"

    def test_get_emoji_keyword_in_longer_name(self):
        """T501: Keyword can appear as part of agent name."""
        assert EmojiMapper.get_emoji("software-architect") == "🏗️"
        assert EmojiMapper.get_emoji("senior-engineer") == "🧑‍💻"
        assert EmojiMapper.get_emoji("security-analyst") == "🔒"

    def test_get_emoji_first_match_precedence(self):
        """T503: First keyword match wins for names with multiple keywords.

        architect appears before engineer in KEYWORD_MAP, so 'architect-engineer'
        should return the architect emoji.
        """
        result = EmojiMapper.get_emoji("architect-engineer")
        assert result == "🏗️"  # architect comes first in KEYWORD_MAP

    def test_get_emoji_default_emoji_when_no_match(self):
        """T504: EmojiMapper returns default emoji (🤖) when no keyword matches."""
        assert EmojiMapper.get_emoji("unknown-role") == "🤖"
        assert EmojiMapper.get_emoji("some-agent") == "🤖"
        assert EmojiMapper.get_emoji("xyz") == "🤖"

    def test_get_emoji_empty_name_returns_default(self):
        """T504: Empty name returns default emoji."""
        assert EmojiMapper.get_emoji("") == "🤖"

    def test_keyword_map_is_ordered(self):
        """T503: KEYWORD_MAP maintains insertion order for priority."""
        # architect should appear before engineer in the map
        keywords = [k for k, _ in EmojiMapper.KEYWORD_MAP]
        assert keywords.index("architect") < keywords.index("engineer")

    def test_default_emoji_is_robot(self):
        """T504: Default emoji is 🤖."""
        assert EmojiMapper.DEFAULT_EMOJI == "🤖"
