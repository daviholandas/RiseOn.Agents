# Data Model: TUI Improvements

**Feature**: 004-tui-improvements  
**Date**: 2026-03-30

## Overview

This document defines the data model changes and new entities for the TUI Improvements feature. Changes are additive and backward-compatible with existing 166 tests.

---

## Entity Changes

### PrimaryAgent (Modified)

**File**: `src/riseon_agents/models/agent.py`

```python
@dataclass
class PrimaryAgent:
    """Primary agent definition (maps to Kilo Code Custom Mode)."""
    
    # Identity
    name: str
    description: str
    
    # Content
    markdown_body: str
    
    # Configuration
    tools: list[str] = field(default_factory=list)
    temperature: float = 0.1
    steps: int = 40
    permissions: dict[str, PermissionLevel] = field(default_factory=dict)
    handoffs: list[str] = field(default_factory=list)
    
    # NEW: Optional emoji field
    emoji: str | None = None  # Parsed from frontmatter or auto-assigned
    
    # Children
    subagents: list[Subagent] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)
    
    # Metadata
    source_path: Path | None = None
```

**Changes**:
- Added `emoji: str | None = None` field
- No breaking changes to existing interface

**Validation**:
- Emoji is optional, defaults to None
- If provided, must be a single emoji character or short sequence

---

### EmojiMapper (New)

**File**: `src/riseon_agents/utils/emoji.py`

```python
@dataclass
class EmojiMapping:
    """Maps a keyword to an emoji."""
    keyword: str
    emoji: str


class EmojiMapper:
    """Maps agent names to emojis based on keywords.
    
    Keywords are matched case-insensitively with first-match precedence.
    """
    
    MAPPINGS: ClassVar[list[EmojiMapping]] = [
        EmojiMapping("architect", "🏗️"),
        EmojiMapping("engineer", "🧑‍💻"),
        EmojiMapping("writer", "📝"),
        EmojiMapping("devops", "⚙️"),
        EmojiMapping("security", "🔒"),
    ]
    
    DEFAULT_EMOJI: ClassVar[str] = "🤖"
    
    @classmethod
    def get_emoji(cls, name: str, explicit_emoji: str | None = None) -> str:
        """Get emoji for an agent name.
        
        Args:
            name: Agent name to match keywords against.
            explicit_emoji: Explicit emoji from frontmatter (takes precedence).
            
        Returns:
            Emoji string.
        """
        if explicit_emoji:
            return explicit_emoji
            
        name_lower = name.lower()
        for mapping in cls.MAPPINGS:
            if mapping.keyword in name_lower:
                return mapping.emoji
        return cls.DEFAULT_EMOJI
    
    @classmethod
    def format_name_with_emoji(cls, name: str, emoji: str) -> str:
        """Format agent name with emoji prefix.
        
        Args:
            name: Display name (e.g., "Architect").
            emoji: Emoji to prepend.
            
        Returns:
            Formatted name (e.g., "🏗️ Architect").
        """
        return f"{emoji} {name}"
```

**Relationships**:
- Used by `ModesGenerator` when generating custom_modes.yaml
- Uses `PrimaryAgent.emoji` field if present

---

### HandoffSection (New Helper)

**File**: `src/riseon_agents/generation/modes.py`

```python
@dataclass
class HandoffEntry:
    """Entry in the handoffs section."""
    slug: str
    description: str


class HandoffSectionGenerator:
    """Generates the '## Available Subagents for Delegation' section."""
    
    SECTION_HEADER: ClassVar[str] = "## Available Subagents for Delegation"
    
    @classmethod
    def generate(cls, handoffs: list[str], subagents: list[Subagent]) -> str | None:
        """Generate handoff section markdown.
        
        Args:
            handoffs: List of subagent slugs from handoffs field.
            subagents: List of available Subagent objects.
            
        Returns:
            Markdown string or None if no valid handoffs.
        """
        if not handoffs:
            return None
            
        # Build slug -> description map
        subagent_map = {s.slug: s.description for s in subagents}
        
        entries = []
        for slug in handoffs:
            if slug in subagent_map:
                entries.append(HandoffEntry(slug, subagent_map[slug]))
        
        if not entries:
            return None
            
        lines = [
            "",
            cls.SECTION_HEADER,
            "",
            "| Subagent | Description |",
            "|----------|-------------|",
        ]
        
        for entry in entries:
            lines.append(f"| {entry.slug} | {entry.description} |")
        
        return "\n".join(lines)
```

**Relationships**:
- Called by `ModesGenerator._generate_mode_entry()`
- Validates handoffs against available subagents

---

### TargetSelectionResult (New)

**File**: `src/riseon_agents/screens/target_dialog.py`

```python
@dataclass
class TargetSelectionResult:
    """Result of target selection dialog."""
    level: GenerationLevel | None  # None if cancelled
    cancelled: bool = False
    
    @classmethod
    def cancelled_result(cls) -> "TargetSelectionResult":
        """Create a cancelled result."""
        return cls(level=None, cancelled=True)
    
    @classmethod
    def selected(cls, level: GenerationLevel) -> "TargetSelectionResult":
        """Create a successful selection result."""
        return cls(level=level, cancelled=False)
```

**Relationships**:
- Returned by `TargetSelectionDialog.dismiss()`
- Consumed by `MainScreen.action_generate()`

---

### ConfirmDialogResult (Enhanced)

**File**: `src/riseon_agents/screens/dialogs.py`

```python
class ConfirmResult(Enum):
    """Result of confirmation dialog."""
    YES = "yes"
    NO = "no"
    CANCEL = "cancel"
```

**Changes**:
- Currently returns string "yes"/"no"
- Enhanced to use enum for type safety
- Adds CANCEL option

---

## Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Generation Flow                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   MainScreen    │
                    │ action_generate │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
    │TargetSelection  │ │ConfirmDialog│ │ ResultDialog│
    │     Dialog      │ │ (enhanced)  │ │             │
    └────────┬────────┘ └──────┬──────┘ └─────────────┘
             │                 │
             ▼                 ▼
    ┌─────────────────┐ ┌─────────────┐
    │TargetSelection  │ │ConfirmResult│
    │     Result      │ │   (enum)    │
    └─────────────────┘ └─────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        Data Processing                          │
└─────────────────────────────────────────────────────────────────┘

    ┌─────────────┐          ┌─────────────────┐
    │PrimaryAgent │◄─────────│  AgentParser    │
    │  (+emoji)   │          │ (parses emoji)  │
    └──────┬──────┘          └─────────────────┘
           │
           │ handoffs[]
           │ subagents[]
           ▼
    ┌──────────────────┐     ┌─────────────────┐
    │  ModesGenerator  │────►│HandoffSection   │
    │                  │     │   Generator     │
    └────────┬─────────┘     └─────────────────┘
             │
             │ uses
             ▼
    ┌─────────────────┐
    │   EmojiMapper   │
    │ get_emoji()     │
    │ format_name()   │
    └─────────────────┘
```

---

## State Transitions

### ConfirmDialog State Machine

```
              ESC                    ESC
               │                      │
    ┌──────────┼──────────────────────┼──────────┐
    │          ▼                      ▼          │
    │    ┌──────────┐           ┌──────────┐    │
    │    │  CANCEL  │           │  CANCEL  │    │
    │    └──────────┘           └──────────┘    │
    │                                            │
    │  ┌─────────────────────────────────────┐  │
    │  │            ConfirmDialog            │  │
    │  │  ┌─────┐  ┌─────┐  ┌────────┐      │  │
    │  │  │ Yes │  │ No  │  │ Cancel │      │  │
    │  │  └──┬──┘  └──┬──┘  └───┬────┘      │  │
    │  └─────┼────────┼─────────┼───────────┘  │
    │        │        │         │              │
    └────────┼────────┼─────────┼──────────────┘
             ▼        ▼         ▼
         PROCEED   ABORT    ABORT
       (overwrite) (keep)  (return)
```

### TargetSelectionDialog State Machine

```
         ┌──────────────────────────────────────┐
         │          TargetSelectionDialog       │
         │  ┌─────────────────────────────────┐ │
         │  │  RadioSet                       │ │
         │  │  ○ Local (.kilo/)              │ │
         │  │  ○ Global (~/.kilocode/)       │ │
         │  └─────────────────────────────────┘ │
         │  ┌──────────┐  ┌──────────┐         │
         │  │ Generate │  │  Cancel  │         │
         │  └────┬─────┘  └────┬─────┘         │
         └───────┼─────────────┼────────────────┘
                 │             │
                 ▼             ▼
           TargetSelection    TargetSelection
           Result(LOCAL)      Result(cancelled)
                 │             │
                 ▼             │
           Continue to        ◄┘
           ConfirmDialog      Return to
                              MainScreen
```

---

## Validation Rules

### Handoff Validation

| Rule | Error Message |
|------|---------------|
| Handoff slug not in subagents | "Handoff '{slug}' references non-existent subagent" |
| Empty handoffs list | (No error - section simply not generated) |

### Emoji Validation

| Rule | Behavior |
|------|----------|
| Explicit emoji in frontmatter | Use as-is |
| No emoji, name matches keyword | Use keyword emoji |
| No emoji, no keyword match | Use default 🤖 |

### Target Path Validation

| Level | custom_modes.yaml | agents/ | rules/ | skills/ |
|-------|-------------------|---------|--------|---------|
| LOCAL | `.kilo/` | `.kilo/agents/` | `.kilo/rules/` | `.kilocode/skills/` |
| GLOBAL | `~/.kilocode/` | `~/.kilocode/agents/` | `~/.kilocode/rules/` | `~/.kilocode/skills/` |

---

## Backward Compatibility

All changes are additive:

1. **PrimaryAgent.emoji** - Optional field with default None
2. **ConfirmDialog** - New button, same dismiss pattern
3. **PreviewPanel** - Enhanced rendering, same interface
4. **AgentTreeNode** - Different icons, same data structure

No existing tests should break. New tests will cover new functionality.
