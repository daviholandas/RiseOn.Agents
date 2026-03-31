# Research: TUI Improvements

**Feature**: 004-tui-improvements  
**Date**: 2026-03-30

## Summary

This document captures the technical research conducted for the TUI Improvements feature. All technical decisions are documented with rationale and alternatives considered.

---

## R1: Handoff Generation in custom_modes.yaml

### Question
How should handoffs be rendered in the roleDefinition field of custom_modes.yaml?

### Research Findings

The Kilo Code VSCode Extension expects handoffs to be documented in the agent's roleDefinition so the model knows which subagents can be invoked via the `task` tool.

**Existing Code Analysis:**
- `modes.py:104-109` generates roleDefinition as a YAML literal block (`|`)
- `agent.py:40` already has `handoffs: list[str]` parsed but unused
- Subagent descriptions are available in `agent.subagents[].description`

**Kilo Code Documentation Pattern:**
```markdown
## Available Subagents for Delegation

| Subagent | Description |
|----------|-------------|
| architect | Handles architectural decisions |
| code-reviewer | Reviews code for quality |
```

### Decision
Append a Markdown table section to the roleDefinition when handoffs exist. The section uses H2 heading "Available Subagents for Delegation" with a two-column table (Subagent slug, Description).

### Rationale
1. Markdown tables are well-rendered by LLMs during inference
2. H2 heading provides clear semantic separation
3. Table format is compact and parseable
4. Slug as identifier matches task tool invocation pattern

### Alternatives Considered
1. **Bullet list** - Less structured, harder for model to parse
2. **Separate YAML field** - Not supported by Kilo Code format
3. **Inline prose** - Harder to maintain and less scannable

---

## R2: Target Selection Modal Architecture

### Question
How should the target selection modal integrate with the existing generation flow?

### Research Findings

**Current Flow (main.py:211-245):**
1. `action_generate()` called on 'g' key
2. Check for selected agents
3. Check for existing files
4. Show ConfirmDialog if files exist
5. Call `_do_generate()` with overwrite flag

**Textual Modal Patterns:**
- `ModalScreen` subclass with `compose()` method
- `dismiss(result)` returns value to caller
- RadioSet widget for mutually exclusive options
- Can chain modals: target → confirm → generate

### Decision
Create `TargetSelectionDialog(ModalScreen)` in new file `screens/target_dialog.py`. Insert modal push before file existence check. Modal returns `GenerationLevel` or `None` (cancelled).

### Architecture
```
action_generate()
    ↓
[TargetSelectionDialog] → returns GenerationLevel or None
    ↓
check_existing_files(level)
    ↓
[ConfirmDialog if needed] → returns "yes"/"no"/"cancel"
    ↓
_do_generate()
```

### Rationale
1. Clean separation: target selection is independent concern
2. Follows existing dialog pattern (ConfirmDialog, ResultDialog)
3. Returns typed value, not string, for type safety

### Alternatives Considered
1. **Inline RadioButtons in main screen** - Clutters UI, always visible
2. **Command palette** - Inconsistent with existing patterns
3. **Footer action** - Limited space, no path preview

---

## R3: Three-Button Dialog Layout

### Question
How to add Cancel button to ConfirmDialog with horizontal layout?

### Research Findings

**Current ConfirmDialog (dialogs.py:113-179):**
- Uses `Vertical` container for buttons
- Only Yes/No buttons
- No ESC binding

**Textual Button Layout:**
- `Horizontal` container for side-by-side
- `Button.variant` for styling: "primary", "error", "default"
- `BINDINGS` class attribute for keyboard shortcuts
- ESC should dismiss with `None` result

### Decision
Modify `ConfirmDialog`:
1. Change button container from `Vertical` to `Horizontal`
2. Add third "Cancel" button with id="cancel"
3. Add `("escape", "cancel", "Cancel")` binding
4. Update CSS for horizontal 3-button layout

### CSS Design
```css
ConfirmDialog > Container > Horizontal {
    height: auto;
    align: center middle;
    width: 100%;
}

ConfirmDialog > Container > Horizontal > Button {
    margin: 0 1;
    min-width: 10;
}
```

### Rationale
1. Horizontal layout is standard for dialog buttons
2. Cancel as third option prevents accidental confirm/deny
3. ESC is universal cancel shortcut

### Alternatives Considered
1. **Keep vertical layout** - Takes more space, non-standard
2. **Remove No button** - Confusing semantics (Yes/Cancel)

---

## R4: Syntax Highlighting for Rules and Skills

### Question
How to apply syntax highlighting to Rules and Skills in PreviewPanel?

### Research Findings

**Current Implementation (preview.py:94-100):**
```python
if node_type in ("primary_agent", "subagent"):
    syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
    self.content_widget.update(syntax)
else:
    self.content_widget.update(Text(content))  # Plain text!
```

**Rules Format:**
- Pure Markdown content
- No frontmatter
- Generated as `.md` files

**Skills Format:**
- YAML frontmatter (name, description)
- Markdown body
- Uses `---` delimiters

### Decision
1. Rules: Use `Syntax(content, "markdown", theme="monokai")`
2. Skills: Use `Syntax(content, "markdown", theme="monokai")` - Rich handles frontmatter in markdown
3. Add `overflow: auto scroll` CSS for long content

### Rationale
1. Markdown lexer handles both pure markdown and yaml frontmatter
2. Consistent styling across all preview types
3. Rich's Syntax widget handles scrolling natively

### Alternatives Considered
1. **Split view for Skills** - Complexity without benefit
2. **Custom lexer** - Overkill for this use case

---

## R5: Emoji Keyword Mapping

### Question
How to implement case-insensitive keyword matching with priority?

### Research Findings

**Spec Requirements:**
- Keywords: architect, engineer, writer, devops, security
- Match case-insensitively
- First match wins (priority order)
- Default emoji: 🤖

**Python Pattern:**
```python
EMOJI_MAP = [
    ("architect", "🏗️"),
    ("engineer", "🧑‍💻"),
    ("writer", "📝"),
    ("devops", "⚙️"),
    ("security", "🔒"),
]

def get_emoji(name: str) -> str:
    name_lower = name.lower()
    for keyword, emoji in EMOJI_MAP:
        if keyword in name_lower:
            return emoji
    return "🤖"
```

### Decision
Create `utils/emoji.py` with:
1. `EMOJI_KEYWORDS` list (ordered by priority)
2. `EmojiMapper.get_emoji(name: str) -> str` class method
3. `EmojiMapper.format_name(emoji: str, name: str) -> str` for output

### Rationale
1. List preserves order for priority matching
2. Simple `in` check for substring matching
3. Class encapsulates logic for testing

### Alternatives Considered
1. **Dict with priority keys** - More complex, same result
2. **Regex patterns** - Overkill for simple contains
3. **External config** - Unnecessary flexibility

---

## R6: Splash Screen Implementation

### Question
How to implement a 1.5s splash screen without blocking?

### Research Findings

**Textual Timer Pattern:**
```python
class SplashScreen(Screen):
    def on_mount(self) -> None:
        self.set_timer(1.5, self.dismiss)
```

**ASCII Art:**
- Should fit 80-character terminals
- Use Static widget for display
- Center alignment

### Decision
Create `screens/splash.py` with:
1. `SplashScreen(Screen)` that auto-dismisses after 1.5s
2. ASCII art stored as multiline string constant
3. Push splash first, then main screen after dismiss callback

### App Integration (app.py):
```python
def on_mount(self) -> None:
    self.push_screen(SplashScreen(), self._after_splash)

def _after_splash(self, _: None) -> None:
    # existing agent loading logic
```

### Rationale
1. Textual's timer is non-blocking
2. Splash dismisses itself, clean callback chain
3. 1.5s is perceptible but not annoying

### Alternatives Considered
1. **Overlay on main screen** - More complex state management
2. **Loading indicator** - Different purpose (progress vs branding)

---

## R7: Tree Node Icons

### Question
How to add visual icons to tree nodes?

### Research Findings

**Current Icons (agent_tree.py:50-79):**
```python
type_icons = {
    "primary_agent": "◉",
    "subagent": "○",
    "rule": "▪",
    "skill": "★",
}
```

**Spec Icons:**
- Primary Agent: 📦
- Subagent: 🤖
- Rule: 📋
- Skill: ⚡

### Decision
Update `AgentTreeNode.get_icon()` to use emoji icons:
```python
type_icons = {
    "primary_agent": "📦",
    "subagent": "🤖",
    "rule": "📋",
    "skill": "⚡",
}
```

### Rationale
1. Single location change (get_icon method)
2. Emojis are more visually distinct
3. Terminal Unicode support is assumed (per spec)

### Alternatives Considered
1. **Nerd Fonts** - Requires user font installation
2. **ASCII art** - Less visually appealing
3. **Color only** - Accessibility concerns

---

## R8: Handoff Validation

### Question
How to validate that handoff references point to existing subagents?

### Research Findings

**Current Flow:**
1. `repository.py` parses handoffs from frontmatter
2. `PrimaryAgent.handoffs` contains list of subagent slugs
3. `PrimaryAgent.subagents` contains actual Subagent objects

**Validation Point:**
Best done at generation time in `generator.py` or `modes.py`.

### Decision
Add validation in `KiloCodeGenerator.generate()`:
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

### Rationale
1. Validation before generation prevents invalid output
2. Error includes file path for debugging
3. Consistent with existing ValidationError pattern

### Alternatives Considered
1. **Parse-time validation** - Agent not fully loaded yet
2. **UI-only warning** - Allows invalid generation

---

## R9: Color Palette Implementation

### Question
How to implement consistent green/cyan color palette?

### Research Findings

**Textual CSS Variables:**
- `$primary`, `$secondary`, `$accent` - Built-in colors
- Custom colors via CSS: `color: rgb(0, 255, 200);`
- Theme-aware: light/dark mode

**Current Styling:**
- `$primary` used for borders (main.py CSS)
- `$error`, `$success` for dialogs

### Decision
Define custom CSS in `app.py` CSS section:
```css
$primary: rgb(0, 200, 150);    /* Cyan-green */
$secondary: rgb(100, 255, 200); /* Light cyan */
$accent: rgb(0, 180, 130);     /* Darker green */
```

Apply to:
- Panel borders: `border: solid $primary`
- Header: Custom styled widget
- Tree highlight: `$secondary` background

### Rationale
1. CSS variables maintain consistency
2. Single location for color definitions
3. Easy to adjust entire palette

### Alternatives Considered
1. **Hardcoded colors** - Maintenance nightmare
2. **Full theme file** - Overkill for palette change

---

## Summary of Technical Decisions

| Area | Decision | Key Files |
|------|----------|-----------|
| Handoffs | Markdown table in roleDefinition | `modes.py` |
| Target Modal | New TargetSelectionDialog | `screens/target_dialog.py` |
| Override Dialog | Horizontal 3-button layout | `screens/dialogs.py` |
| Preview Syntax | Markdown highlighting for all | `widgets/preview.py` |
| Emojis | Keyword list with priority | `utils/emoji.py` |
| Splash Screen | Timer-based auto-dismiss | `screens/splash.py` |
| Tree Icons | Emoji icons | `widgets/agent_tree.py` |
| Handoff Validation | Generator-time validation | `generation/generator.py` |
| Color Palette | CSS variables | `app.py` |
