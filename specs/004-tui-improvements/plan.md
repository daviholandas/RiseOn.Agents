# Implementation Plan: TUI Improvements

**Branch**: `004-tui-improvements` | **Date**: 2026-03-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-tui-improvements/spec.md`

## Summary

Implement comprehensive TUI improvements for the RiseOn.Agents Kilo Code Generator across 6 priority areas: (1) **Handoff generation** in custom_modes.yaml enabling agent-to-subagent delegation, (2) **Target selection modal** for Local vs Global path choice, (3) **Enhanced override dialog** with Cancel button, (4) **Syntax highlighting** for Rules/Skills preview, (5) **Emoji assignment** for agent names, and (6) **Visual redesign** with splash screen, branded header, tree icons, and color palette.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Textual >=0.47.0, Rich >=13.0.0, PyYAML >=6.0, python-frontmatter >=1.0
**Storage**: File system (`.kilo/`, `.kilocode/`, `~/.kilocode/`)
**Testing**: pytest with PYTHONPATH=src
**Target Platform**: Cross-platform terminals (Linux, macOS, Windows) with Unicode support
**Project Type**: TUI desktop application (CLI tool)
**Performance Goals**: Generation < 3 minutes for typical agent set, splash screen 1.5s ±0.1s
**Constraints**: All 166 existing tests must pass, backward-compatible changes only
**Scale/Scope**: Single-user tool, ~10-50 agents typical, ~500 LOC new code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Documentation-First | ✅ PASS | Handoffs follow Kilo Code VSCode format, spec references official patterns |
| II. Modern TUI Design | ✅ PASS | Using Textual/Rich, modal dialogs, keyboard navigation, visual feedback |
| III. Phase-Based Validation | ✅ PASS | 6 phases with testable artifacts, user validation gates |
| IV. Test-First Development | ✅ PASS | Tests defined before implementation, TDD approach |
| V. Agent Modularity | ✅ PASS | EmojiMapper, HandoffSectionGenerator as independent classes |
| VI. Observability | ✅ PASS | Validation errors include file path, handoff tracing |
| VII. Simplicity | ✅ PASS | Minimal new dependencies, additive changes only |

**Gate Result**: PASS - No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/004-tui-improvements/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: Technical research
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Implementation guide
├── contracts/
│   └── ui-contracts.md  # Phase 1: UI widget contracts
└── checklists/
    └── requirements.md  # Quality checklist (existing)
```

### Source Code (repository root)

```text
src/riseon_agents/
├── __init__.py
├── __main__.py
├── app.py                    # MODIFY: Splash integration, color palette
├── generation/
│   ├── __init__.py
│   ├── generator.py          # MODIFY: Handoff validation
│   └── modes.py              # MODIFY: Handoff section, emoji in name
├── models/
│   ├── __init__.py
│   ├── agent.py              # MODIFY: Add emoji field
│   ├── generation.py
│   ├── rule.py
│   ├── selection.py
│   └── skill.py
├── parsing/
│   ├── __init__.py
│   ├── agent_parser.py       # MODIFY: Parse emoji from frontmatter
│   └── repository.py
├── screens/
│   ├── __init__.py
│   ├── dialogs.py            # MODIFY: 3-button ConfirmDialog
│   ├── main.py               # MODIFY: Target modal integration
│   ├── splash.py             # NEW: SplashScreen
│   └── target_dialog.py      # NEW: TargetSelectionDialog
├── utils/
│   ├── __init__.py           # NEW
│   └── emoji.py              # NEW: EmojiMapper
└── widgets/
    ├── __init__.py
    ├── agent_tree.py         # MODIFY: Emoji icons
    ├── header.py             # NEW: BrandedHeader
    ├── help_overlay.py
    └── preview.py            # MODIFY: Markdown syntax for rules/skills

tests/
├── test_generation/
│   ├── test_generator.py     # ADD: Handoff validation tests
│   └── test_modes.py         # ADD: Handoff section, emoji tests
├── test_screens/
│   ├── test_dialogs.py       # ADD: 3-button dialog tests
│   ├── test_splash.py        # NEW: Splash screen tests
│   └── test_target_dialog.py # NEW: Target modal tests
├── test_widgets/
│   ├── test_agent_tree.py    # ADD: Icon tests
│   └── test_preview.py       # ADD: Markdown syntax tests
└── test_utils/
    └── test_emoji.py         # NEW: EmojiMapper tests
```

**Structure Decision**: Single project layout maintained. New files added to existing directories. New `utils/` package created for emoji utilities.

---

## Implementation Phases

### Phase 1: Handoffs (Priority P1 - Critical)

**Duration**: 2-3 hours
**Dependencies**: None (foundational)

#### Tasks

| ID | Task | Files | Tests |
|----|------|-------|-------|
| T101 | Create HandoffSectionGenerator class | modes.py | test_modes.py |
| T102 | Generate Markdown table with slug/description | modes.py | test_modes.py |
| T103 | Integrate handoff section into _generate_mode_entry | modes.py | test_modes.py |
| T104 | Add _validate_handoffs method to generator | generator.py | test_generator.py |
| T105 | Return ValidationError for invalid handoffs | generator.py | test_generator.py |
| T106 | Skip section when handoffs empty | modes.py | test_modes.py |
| T107 | Update preview to show handoffs | preview.py | test_preview.py |

#### Acceptance Criteria
- [x] custom_modes.yaml includes "## Available Subagents for Delegation" section
- [x] Table format: | Subagent | Description |
- [x] Validation error if handoff references non-existent subagent
- [x] No section generated for agents without handoffs

#### Validation Gate
```bash
PYTHONPATH=src pytest tests/test_generation/test_modes.py::TestHandoffSection -v
PYTHONPATH=src pytest tests/test_generation/test_generator.py::TestHandoffValidation -v
```

---

### Phase 2: Target Selection Modal (Priority P2)

**Duration**: 2-3 hours
**Dependencies**: None (parallel with Phase 1)

#### Tasks

| ID | Task | Files | Tests |
|----|------|-------|-------|
| T201 | Create TargetSelectionResult dataclass | target_dialog.py | test_target_dialog.py |
| T202 | Create TargetSelectionDialog ModalScreen | target_dialog.py | test_target_dialog.py |
| T203 | Add RadioSet for Local/Global options | target_dialog.py | test_target_dialog.py |
| T204 | Display full paths for each option | target_dialog.py | test_target_dialog.py |
| T205 | Add Generate and Cancel buttons | target_dialog.py | test_target_dialog.py |
| T206 | Add ESC binding to dismiss | target_dialog.py | test_target_dialog.py |
| T207 | Integrate modal into action_generate | main.py | test_main.py |
| T208 | Remove hidden 'l' toggle (or keep as shortcut) | main.py | test_main.py |

#### Acceptance Criteria
- [x] Modal appears before generation starts
- [x] Local option shows .kilo/ and .kilocode/skills/ paths
- [x] Global option shows ~/.kilocode/ paths
- [x] Cancel/ESC returns to main screen without generating

#### Validation Gate
```bash
PYTHONPATH=src pytest tests/test_screens/test_target_dialog.py -v
```

---

### Phase 3: Override Dialog Enhancement (Priority P3)

**Duration**: 1-2 hours
**Dependencies**: None (parallel)

#### Tasks

| ID | Task | Files | Tests |
|----|------|-------|-------|
| T301 | Add ConfirmResult enum | dialogs.py | test_dialogs.py |
| T302 | Change Vertical to Horizontal for buttons | dialogs.py | test_dialogs.py |
| T303 | Add Cancel button (id="cancel") | dialogs.py | test_dialogs.py |
| T304 | Add ESC binding for cancel action | dialogs.py | test_dialogs.py |
| T305 | Update CSS for horizontal 3-button layout | dialogs.py | test_dialogs.py |
| T306 | Fix callback in main.py to handle "cancel" | main.py | test_main.py |

#### Acceptance Criteria
- [x] Dialog shows Yes, No, Cancel buttons horizontally
- [x] ESC dismisses dialog with cancel result
- [x] Callback handles all three results correctly

#### Validation Gate
```bash
PYTHONPATH=src pytest tests/test_screens/test_dialogs.py::TestConfirmDialog -v
```

---

### Phase 4: Preview Rules/Skills (Priority P3)

**Duration**: 1-2 hours
**Dependencies**: Phase 1 (for handoffs preview)

#### Tasks

| ID | Task | Files | Tests |
|----|------|-------|-------|
| T401 | Apply Syntax(markdown) for Rules | preview.py | test_preview.py |
| T402 | Apply Syntax(markdown) for Skills | preview.py | test_preview.py |
| T403 | Ensure vertical scroll for long content | preview.py | test_preview.py |
| T404 | Add handoffs list to PrimaryAgent preview | preview.py | test_preview.py |

#### Acceptance Criteria
- [x] Rules preview shows Markdown syntax highlighting
- [x] Skills preview shows Markdown/YAML frontmatter highlighting
- [x] Long descriptions scrollable
- [x] PrimaryAgent preview shows handoffs

#### Validation Gate
```bash
PYTHONPATH=src pytest tests/test_widgets/test_preview.py -v
```

---

### Phase 5: Emoji Support (Priority P4)

**Duration**: 2-3 hours
**Dependencies**: None (parallel)

#### Tasks

| ID | Task | Files | Tests |
|----|------|-------|-------|
| T501 | Create utils/__init__.py | utils/__init__.py | - |
| T502 | Create EmojiMapper class | utils/emoji.py | test_emoji.py |
| T503 | Implement keyword-to-emoji mapping | utils/emoji.py | test_emoji.py |
| T504 | Implement case-insensitive matching | utils/emoji.py | test_emoji.py |
| T505 | Implement first-match precedence | utils/emoji.py | test_emoji.py |
| T506 | Add emoji field to PrimaryAgent | agent.py | test_agent.py |
| T507 | Parse emoji from frontmatter | agent_parser.py | test_parser.py |
| T508 | Include emoji in custom_modes.yaml name | modes.py | test_modes.py |

#### Acceptance Criteria
- [x] Explicit emoji from frontmatter takes precedence
- [x] Keywords matched case-insensitively
- [x] First keyword match wins
- [x] Default emoji 🤖 when no match
- [x] Name in custom_modes.yaml: "🏗️ Architect"

#### Validation Gate
```bash
PYTHONPATH=src pytest tests/test_utils/test_emoji.py -v
PYTHONPATH=src pytest tests/test_generation/test_modes.py::TestEmojiInName -v
```

---

### Phase 6: Visual Redesign (Priority P4)

**Duration**: 3-4 hours
**Dependencies**: Phases 1-5 complete

#### Tasks

| ID | Task | Files | Tests |
|----|------|-------|-------|
| T601 | Create ASCII art logo constant | splash.py | test_splash.py |
| T602 | Create SplashScreen with 1.5s timer | splash.py | test_splash.py |
| T603 | Integrate splash into app.py on_mount | app.py | test_app.py |
| T604 | Create BrandedHeader widget | header.py | test_header.py |
| T605 | Update tree icons to emojis | agent_tree.py | test_agent_tree.py |
| T606 | Define color palette CSS variables | app.py | - |
| T607 | Apply palette to borders and highlights | app.py, main.py | - |
| T608 | Add styled borders to panels | main.py | - |

#### Acceptance Criteria
- [x] Splash screen displays for 1.5s ±0.1s
- [x] Header shows "RiseOn.Agents" with version
- [x] Tree uses 📦, 🤖, 📋, ⚡ icons
- [x] Green/cyan palette applied consistently

#### Validation Gate
```bash
PYTHONPATH=src pytest tests/test_screens/test_splash.py -v
PYTHONPATH=src pytest tests/test_widgets/test_agent_tree.py::TestTreeIcons -v
```

---

## Dependency Graph

```
Phase 1 (Handoffs) ─────────────────────┐
                                        │
Phase 2 (Target Modal) ─────────────────┤
                                        ├──► Phase 6 (Visual Redesign)
Phase 3 (Override Dialog) ──────────────┤
                                        │
Phase 4 (Preview) ──────────────────────┤
   └── depends on Phase 1 for handoffs  │
                                        │
Phase 5 (Emojis) ───────────────────────┘
```

**Parallel Opportunities**:
- Phases 1, 2, 3, 5 can be developed in parallel
- Phase 4 depends on Phase 1 for handoff preview
- Phase 6 should be done last (integrates all changes)

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Textual API changes | Low | High | Pin version >=0.47.0, test on CI |
| Unicode/emoji rendering issues | Medium | Medium | Fallback ASCII art, test on multiple terminals |
| Splash screen timing variance | Low | Low | Use ±0.1s tolerance in tests |
| Existing test breakage | Low | High | Run full suite after each phase |
| Complex merge conflicts | Medium | Medium | Small, focused commits per task |

---

## Testing Strategy

### Unit Tests (per phase)
- Each task has corresponding test file
- Test positive and negative cases
- Mock Textual widgets where needed

### Integration Tests
- Full generation flow with handoffs
- Dialog chain: Target → Confirm → Result
- Preview updates on tree navigation

### Regression Tests
- All 166 existing tests must pass
- Run after each phase completion

### Manual Validation
- Visual inspection of splash screen
- Emoji rendering on different terminals
- Keyboard navigation through all dialogs

---

## Post-Implementation Checklist

- [ ] All 166 existing tests pass
- [ ] All new tests pass (target: ~30-40 new tests)
- [ ] Linting passes: `ruff check src tests`
- [ ] Type checking passes: `mypy src/riseon_agents`
- [ ] Formatting passes: `black --check src tests`
- [ ] Manual TUI walkthrough completed
- [ ] Documentation updated (if needed)
- [ ] PR created with summary

---

## Constitution Re-Check (Post-Design)

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Documentation-First | ✅ PASS | All patterns documented in research.md |
| II. Modern TUI Design | ✅ PASS | Modal dialogs, visual feedback, keyboard nav |
| III. Phase-Based Validation | ✅ PASS | 6 phases with gates |
| IV. Test-First Development | ✅ PASS | Tests defined per task |
| V. Agent Modularity | ✅ PASS | New classes are self-contained |
| VI. Observability | ✅ PASS | Validation errors traceable |
| VII. Simplicity | ✅ PASS | No over-engineering, additive changes |

**Final Gate Result**: PASS - Ready for `/speckit.tasks` to generate task breakdown.
