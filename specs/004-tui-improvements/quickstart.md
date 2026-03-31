# Quickstart: TUI Improvements

**Feature**: 004-tui-improvements  
**Date**: 2026-03-30

## Overview

Quick reference for implementing the TUI Improvements feature. Follow the phases in order.

---

## Pre-Implementation Checklist

- [ ] Feature branch `004-tui-improvements` exists
- [ ] All 166 existing tests pass: `PYTHONPATH=src pytest tests/ -v`
- [ ] Spec reviewed: `specs/004-tui-improvements/spec.md`
- [ ] Research reviewed: `specs/004-tui-improvements/research.md`

---

## Phase 1: Handoffs (P1 - Critical)

### Goal
Generate handoff delegation section in custom_modes.yaml.

### Files to Modify
1. `src/riseon_agents/generation/modes.py`

### Implementation Steps

```python
# 1. Add HandoffSectionGenerator class (modes.py)
class HandoffSectionGenerator:
    SECTION_HEADER = "## Available Subagents for Delegation"
    
    @classmethod
    def generate(cls, handoffs: list[str], subagents: list[Subagent]) -> str | None:
        # Return None if no handoffs
        # Build markdown table with slug and description
        pass

# 2. Update _generate_mode_entry() to append handoff section
def _generate_mode_entry(self, agent: PrimaryAgent) -> list[str]:
    # ... existing code ...
    
    # Add handoffs section if present
    handoff_section = HandoffSectionGenerator.generate(
        agent.handoffs, agent.subagents
    )
    if handoff_section:
        for line in handoff_section.split("\n"):
            lines.append(f"      {line}")
    
    return lines
```

### Validation (generator.py)

```python
def _validate_handoffs(self, agents: list[PrimaryAgent]) -> list[ValidationError]:
    errors = []
    for agent in agents:
        subagent_slugs = {s.slug for s in agent.subagents}
        for handoff in agent.handoffs:
            if handoff not in subagent_slugs:
                errors.append(ValidationError(
                    file_path=agent.source_path,
                    message=f"Handoff '{handoff}' references non-existent subagent",
                ))
    return errors
```

### Tests
- Test handoff section generation with valid handoffs
- Test no section when handoffs empty
- Test validation error for invalid handoff

---

## Phase 2: Target Modal (P2)

### Goal
New dialog for Local vs Global selection before generation.

### Files to Create
1. `src/riseon_agents/screens/target_dialog.py`

### Files to Modify
1. `src/riseon_agents/screens/main.py`

### Implementation

```python
# target_dialog.py
class TargetSelectionDialog(ModalScreen):
    BINDINGS = [("escape", "cancel", "Cancel")]
    
    def compose(self) -> ComposeResult:
        with Container():
            yield Label("Select Generation Target")
            yield RadioSet(
                RadioButton("Local (Project Directory)", id="local"),
                RadioButton("Global (User Directory)", id="global"),
            )
            # Path previews as Static widgets
            with Horizontal():
                yield Button("Generate", id="generate", variant="primary")
                yield Button("Cancel", id="cancel")
    
    def on_button_pressed(self, event):
        if event.button.id == "generate":
            # Get selected radio option
            level = GenerationLevel.LOCAL if self.query_one("#local").value else GenerationLevel.GLOBAL
            self.dismiss(TargetSelectionResult.selected(level))
        else:
            self.dismiss(TargetSelectionResult.cancelled_result())
```

### Integration (main.py)

```python
def action_generate(self) -> None:
    # Step 1: Show target selection
    self.app.push_screen(
        TargetSelectionDialog(),
        self._on_target_selected
    )

def _on_target_selected(self, result: TargetSelectionResult) -> None:
    if result.cancelled:
        return
    self.generation_level = result.level
    # Continue with existing flow...
```

---

## Phase 3: Override Dialog (P3)

### Goal
Add Cancel button, horizontal layout, ESC binding.

### Files to Modify
1. `src/riseon_agents/screens/dialogs.py`
2. `src/riseon_agents/screens/main.py`

### Implementation

```python
# dialogs.py - ConfirmDialog changes
BINDINGS = [("escape", "cancel", "Cancel")]

def compose(self) -> ComposeResult:
    with Container():
        yield Label(self.title)
        yield Static(self.message)
        with Horizontal():  # Changed from Vertical
            yield Button("Yes", id="yes", variant="primary")
            yield Button("No", id="no", variant="error")
            yield Button("Cancel", id="cancel")  # New button

def action_cancel(self) -> None:
    self.dismiss("cancel")
```

### Callback Fix (main.py:241)

```python
# Before
lambda confirmed: self._do_generate(selected_agents) if confirmed else None

# After
lambda result: self._do_generate(selected_agents) if result == "yes" else None
```

---

## Phase 4: Preview Rules/Skills (P3)

### Goal
Apply Markdown syntax highlighting to Rules and Skills preview.

### Files to Modify
1. `src/riseon_agents/widgets/preview.py`

### Implementation

```python
# preview.py - update_preview() method
def update_preview(self, node_type: str, data: Any, level: GenerationLevel) -> None:
    # ... existing code ...
    
    if self.content_widget:
        # Apply syntax highlighting based on node type
        if node_type in ("primary_agent", "subagent"):
            syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
        elif node_type in ("rule", "skill"):
            syntax = Syntax(content, "markdown", theme="monokai", line_numbers=True)
        else:
            syntax = Text(content)
        
        self.content_widget.update(syntax)
```

### Preview Update for Handoffs

```python
def generate_preview_for_agent(self, agent: PrimaryAgent, level: GenerationLevel) -> str:
    # ... existing code ...
    
    # Add handoffs preview
    if agent.handoffs:
        lines.append("")
        lines.append("# Handoffs:")
        for handoff in agent.handoffs:
            lines.append(f"#   - {handoff}")
    
    return "\n".join(lines)
```

---

## Phase 5: Emojis (P4)

### Goal
Add emoji support for agent names in custom_modes.yaml.

### Files to Create
1. `src/riseon_agents/utils/__init__.py`
2. `src/riseon_agents/utils/emoji.py`

### Files to Modify
1. `src/riseon_agents/models/agent.py`
2. `src/riseon_agents/generation/modes.py`
3. `src/riseon_agents/parsing/agent_parser.py`

### Implementation

```python
# utils/emoji.py
class EmojiMapper:
    MAPPINGS = [
        ("architect", "🏗️"),
        ("engineer", "🧑‍💻"),
        ("writer", "📝"),
        ("devops", "⚙️"),
        ("security", "🔒"),
    ]
    DEFAULT = "🤖"
    
    @classmethod
    def get_emoji(cls, name: str, explicit: str | None = None) -> str:
        if explicit:
            return explicit
        name_lower = name.lower()
        for keyword, emoji in cls.MAPPINGS:
            if keyword in name_lower:
                return emoji
        return cls.DEFAULT

# modes.py - Update _generate_mode_entry
def _generate_mode_entry(self, agent: PrimaryAgent) -> list[str]:
    emoji = EmojiMapper.get_emoji(agent.name, agent.emoji)
    display_name = f"{emoji} {agent.display_name}"
    
    lines = [
        f"  - slug: {agent.slug}",
        f"    name: {display_name}",  # Now includes emoji
        # ...
    ]
```

---

## Phase 6: Visual Redesign (P4)

### Goal
Splash screen, branded header, tree icons, color palette.

### Files to Create
1. `src/riseon_agents/screens/splash.py`
2. `src/riseon_agents/widgets/header.py`

### Files to Modify
1. `src/riseon_agents/app.py`
2. `src/riseon_agents/widgets/agent_tree.py`

### Splash Screen

```python
# screens/splash.py
class SplashScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static(ASCII_ART, id="logo")
        yield Static("Kilo Code Configuration Generator", id="subtitle")
    
    def on_mount(self) -> None:
        self.set_timer(1.5, self.dismiss)
```

### Tree Icons Update

```python
# agent_tree.py - AgentTreeNode.get_icon()
type_icons = {
    "primary_agent": "📦",
    "subagent": "🤖",
    "rule": "📋",
    "skill": "⚡",
}
```

### Color Palette (app.py)

```css
CSS = """
$primary: rgb(0, 200, 150);
$secondary: rgb(100, 255, 200);
$accent: rgb(0, 180, 130);
/* ... rest of styles ... */
"""
```

---

## Test Commands

```bash
# Run all tests
PYTHONPATH=src pytest tests/ -v

# Run specific phase tests
PYTHONPATH=src pytest tests/test_generation/test_modes.py -v  # Phase 1
PYTHONPATH=src pytest tests/test_screens/ -v                   # Phases 2-3
PYTHONPATH=src pytest tests/test_widgets/test_preview.py -v   # Phase 4

# Lint and type check
ruff check src tests
mypy src/riseon_agents

# Full validation
ruff check src tests && black --check src tests && mypy src/riseon_agents && PYTHONPATH=src pytest tests/ -v
```

---

## Success Criteria Checklist

- [ ] SC-001: Generation with handoffs < 3 minutes
- [ ] SC-002: 100% valid custom_modes.yaml with handoffs
- [ ] SC-003: Correct directory structure for Local/Global
- [ ] SC-004: Preview works for all node types
- [ ] SC-005: Target selection clear on first attempt
- [ ] SC-006: Dialogs navigable with keyboard
- [ ] SC-007: All agents get emojis
- [ ] SC-008: Splash screen 1.5s ±0.1s
- [ ] SC-009: All 166 existing tests pass
- [ ] SC-010: Visual improvement perceived
