"""Emoji mapping utilities for RiseOn.Agents.

T508-T509: EmojiMapper class for assigning emojis to agent names.
Implements US5 - Include Emojis in Agent Names.
"""


class EmojiMapper:
    """Maps agent name keywords to emojis.

    Keywords are matched case-insensitively with first-match precedence.
    The KEYWORD_MAP order defines priority: earlier entries win.
    """

    # T508: Keyword-to-emoji mapping, ordered by priority (first match wins)
    KEYWORD_MAP: list[tuple[str, str]] = [
        ("architect", "🏗️"),
        ("engineer", "🧑‍💻"),
        ("writer", "📝"),
        ("devops", "⚙️"),
        ("security", "🔒"),
        ("reviewer", "🔍"),
        ("analyst", "📊"),
        ("designer", "🎨"),
        ("tester", "🧪"),
        ("manager", "📋"),
        ("planner", "🗓️"),
        ("researcher", "🔬"),
        ("coach", "🎓"),
        ("data", "📈"),
        ("infra", "🏗️"),
        ("backend", "⚙️"),
        ("frontend", "🎨"),
        ("mobile", "📱"),
        ("cloud", "☁️"),
        ("api", "🔌"),
        ("database", "🗄️"),
        ("ops", "⚙️"),
    ]

    DEFAULT_EMOJI = "🤖"

    @classmethod
    def get_emoji(cls, name: str) -> str:
        """Get the emoji for an agent name using keyword matching.

        T509: Implements case-insensitive, first-match logic.

        Args:
            name: The agent name to match against keywords.

        Returns:
            The matched emoji or the default emoji (🤖) if no match found.
        """
        name_lower = name.lower()
        for keyword, emoji in cls.KEYWORD_MAP:
            if keyword.lower() in name_lower:
                return emoji
        return cls.DEFAULT_EMOJI
