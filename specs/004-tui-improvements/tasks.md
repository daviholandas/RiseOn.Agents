# Tasks: TUI Improvements for RiseOn.Agents Kilo Code Generator

**Input**: Design documents from `/specs/004-tui-improvements/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Required per constitution (Principle IV: Test-First Development)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/riseon_agents/`, `tests/` at repository root
- All paths are relative to repository root

---

## Phase 1: Foundational (No Blocking Prerequisites)

**Purpose**: This feature builds on existing infrastructure. No new foundational tasks required.

**Note**: All 6 user stories can be developed in parallel since they affect different files. Phase 4 (Preview) depends on Phase 1 (Handoffs) for handoff preview functionality.

**Checkpoint**: ✅ Phases 2, 3, 4 complete - User Stories 1, 2, 3 implemented and tested

---

## Phase 2: User Story 1 - Enable Agent Handoff Delegation (Priority: P1) 🎯 MVP

**Goal**: Generate handoff delegation section in custom_modes.yaml so primary agents can invoke subagents via task tool

**Status**: ✅ COMPLETE

**Independent Test**: Generate configuration with an agent that has handoffs defined and verify "Available Subagents for Delegation" section appears in roleDefinition

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T101 [P] [US1] Test HandoffSectionGenerator.generate() returns Markdown table in `tests/test_generation/test_modes.py::TestHandoffSection`
- [x] T102 [P] [US1] Test handoff section integrated into _generate_mode_entry in `tests/test_generation/test_modes.py::TestHandoffSection`
- [x] T103 [P] [US1] Test empty handoffs returns empty string in `tests/test_generation/test_modes.py::TestHandoffSection`
- [x] T104 [P] [US1] Test _validate_handoffs detects invalid subagent in `tests/test_generation/test_generator.py::TestHandoffValidation`
- [x] T105 [P] [US1] Test _validate_handoffs passes for valid subagents in `tests/test_generation/test_generator.py::TestHandoffValidation`

### Implementation for User Story 1

- [x] T106 [US1] Create HandoffSectionGenerator class in `src/riseon_agents/generation/modes.py`
- [x] T107 [US1] Implement generate() method returning Markdown table with slug/description columns in `src/riseon_agents/generation/modes.py`
- [x] T108 [US1] Integrate handoff section at end of roleDefinition in _generate_mode_entry in `src/riseon_agents/generation/modes.py`
- [x] T109 [US1] Skip section when handoffs list is empty in `src/riseon_agents/generation/modes.py`
- [x] T110 [US1] Add _validate_handoffs method to KiloCodeGenerator in `src/riseon_agents/generation/generator.py`
- [x] T111 [US1] Return ValidationError with file path for invalid handoff references in `src/riseon_agents/generation/generator.py`

**Checkpoint**: User Story 1 complete - handoffs generate correctly in custom_modes.yaml

---

## Phase 3: User Story 2 - Select Target Location Before Generation (Priority: P2)

**Goal**: Display modal dialog before generation allowing user to select Local vs Global target with full paths

**Status**: ✅ COMPLETE

**Independent Test**: Start generation and verify modal appears with Local/Global options showing complete paths

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T201 [P] [US2] Test TargetSelectionResult dataclass in `tests/test_screens/test_target_dialog.py`
- [x] T202 [P] [US2] Test TargetSelectionDialog mounts with RadioSet in `tests/test_screens/test_target_dialog.py`
- [x] T203 [P] [US2] Test Local option shows .kilo/ and .kilocode/skills/ paths in `tests/test_screens/test_target_dialog.py`
- [x] T204 [P] [US2] Test Global option shows ~/.kilocode/ paths in `tests/test_screens/test_target_dialog.py`
- [x] T205 [P] [US2] Test Cancel button dismisses without result in `tests/test_screens/test_target_dialog.py`
- [x] T206 [P] [US2] Test ESC key dismisses dialog in `tests/test_screens/test_target_dialog.py`

### Implementation for User Story 2

- [x] T207 [US2] Create TargetSelectionResult dataclass in `src/riseon_agents/screens/target_dialog.py`
- [x] T208 [US2] Create TargetSelectionDialog ModalScreen in `src/riseon_agents/screens/target_dialog.py`
- [x] T209 [US2] Add RadioSet with Local/Global options in `src/riseon_agents/screens/target_dialog.py`
- [x] T210 [US2] Display full paths for each file type per option in `src/riseon_agents/screens/target_dialog.py`
- [x] T211 [US2] Add Generate and Cancel buttons in `src/riseon_agents/screens/target_dialog.py`
- [x] T212 [US2] Add ESC binding to dismiss dialog in `src/riseon_agents/screens/target_dialog.py`
- [x] T213 [US2] Integrate TargetSelectionDialog into action_generate in `src/riseon_agents/screens/main.py`
- [x] T214 [US2] Update __init__.py exports in `src/riseon_agents/screens/__init__.py`

**Checkpoint**: User Story 2 complete - target selection modal works before generation

---

## Phase 4: User Story 3 - Improve Override Confirmation Dialog (Priority: P3)

**Goal**: Add Cancel button to override confirmation dialog with horizontal 3-button layout

**Status**: ✅ COMPLETE

**Independent Test**: Generate with existing files and verify dialog shows Yes/No/Cancel buttons horizontally

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T301 [P] [US3] Test ConfirmResult enum values in `tests/test_screens/test_dialogs.py::TestConfirmDialog`
- [x] T302 [P] [US3] Test 3-button horizontal layout in `tests/test_screens/test_dialogs.py::TestConfirmDialog`
- [x] T303 [P] [US3] Test Cancel button returns ConfirmResult.CANCEL in `tests/test_screens/test_dialogs.py::TestConfirmDialog`
- [x] T304 [P] [US3] Test ESC binding returns ConfirmResult.CANCEL in `tests/test_screens/test_dialogs.py::TestConfirmDialog`

### Implementation for User Story 3

- [x] T305 [US3] Add ConfirmResult enum (YES, NO, CANCEL) in `src/riseon_agents/screens/dialogs.py`
- [x] T306 [US3] Change Vertical to Horizontal container for buttons in `src/riseon_agents/screens/dialogs.py`
- [x] T307 [US3] Add Cancel button (id="cancel") in `src/riseon_agents/screens/dialogs.py`
- [x] T308 [US3] Add ESC binding for cancel action in `src/riseon_agents/screens/dialogs.py`
- [x] T309 [US3] Update CSS for horizontal 3-button layout in `src/riseon_agents/screens/dialogs.py`
- [x] T310 [US3] Fix callback in main.py to handle ConfirmResult.CANCEL in `src/riseon_agents/screens/main.py`

**Checkpoint**: User Story 3 complete - confirmation dialog has Yes/No/Cancel with ESC support

---

## Phase 5: User Story 4 - Enhanced Preview for Rules and Skills (Priority: P3)

**Goal**: Apply Markdown syntax highlighting to Rules and Skills preview, add handoffs to agent preview

**Depends on**: Phase 2 (US1) for handoffs preview functionality

**Independent Test**: Select Rule/Skill in tree and verify Markdown syntax highlighting in preview

### Tests for User Story 4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T401 [P] [US4] Test Rules preview uses Syntax(markdown) in `tests/test_widgets/test_preview.py`
- [ ] T402 [P] [US4] Test Skills preview uses Syntax(markdown) in `tests/test_widgets/test_preview.py`
- [ ] T403 [P] [US4] Test long descriptions have vertical scroll in `tests/test_widgets/test_preview.py`
- [ ] T404 [P] [US4] Test PrimaryAgent preview includes handoffs section in `tests/test_widgets/test_preview.py`

### Implementation for User Story 4

- [ ] T405 [US4] Apply Syntax(markdown) for Rules in _render_rule() in `src/riseon_agents/widgets/preview.py`
- [ ] T406 [US4] Apply Syntax(markdown) for Skills in _render_skill() in `src/riseon_agents/widgets/preview.py`
- [ ] T407 [US4] Ensure ScrollableContainer for long content in `src/riseon_agents/widgets/preview.py`
- [ ] T408 [US4] Add handoffs section to PrimaryAgent preview in _render_primary_agent() in `src/riseon_agents/widgets/preview.py`

**Checkpoint**: User Story 4 complete - Rules/Skills have Markdown highlighting, agents show handoffs

---

## Phase 6: User Story 5 - Include Emojis in Agent Names (Priority: P4)

**Goal**: Add emoji support to agent names via frontmatter or keyword-based defaults

**Independent Test**: Generate configuration and verify name field includes emoji (explicit or keyword-based)

### Tests for User Story 5

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T501 [P] [US5] Test EmojiMapper.get_emoji() returns keyword match in `tests/test_utils/test_emoji.py`
- [ ] T502 [P] [US5] Test EmojiMapper case-insensitive matching in `tests/test_utils/test_emoji.py`
- [ ] T503 [P] [US5] Test EmojiMapper first-match precedence in `tests/test_utils/test_emoji.py`
- [ ] T504 [P] [US5] Test EmojiMapper default emoji (🤖) in `tests/test_utils/test_emoji.py`
- [ ] T505 [P] [US5] Test PrimaryAgent.emoji field parsing in `tests/test_parsing/test_agent_parser.py`
- [ ] T506 [P] [US5] Test emoji included in custom_modes.yaml name in `tests/test_generation/test_modes.py::TestEmojiInName`

### Implementation for User Story 5

- [ ] T507 [US5] Create utils/__init__.py package in `src/riseon_agents/utils/__init__.py`
- [ ] T508 [US5] Create EmojiMapper class with KEYWORD_MAP in `src/riseon_agents/utils/emoji.py`
- [ ] T509 [US5] Implement get_emoji() with case-insensitive, first-match logic in `src/riseon_agents/utils/emoji.py`
- [ ] T510 [US5] Add emoji: str | None field to PrimaryAgent dataclass in `src/riseon_agents/models/agent.py`
- [ ] T511 [US5] Parse emoji from frontmatter in agent_parser.py in `src/riseon_agents/parsing/agent_parser.py`
- [ ] T512 [US5] Include emoji in name field in _generate_mode_entry in `src/riseon_agents/generation/modes.py`
- [ ] T513 [US5] Create tests/__init__.py for test_utils if needed in `tests/test_utils/__init__.py`

**Checkpoint**: User Story 5 complete - agents have emojis in generated names

---

## Phase 7: User Story 6 - Complete Visual Redesign (Priority: P4)

**Goal**: Add splash screen, branded header, tree icons, and consistent color palette

**Depends on**: All other user stories complete (integrates visual changes)

**Independent Test**: Start application and verify splash, header, tree icons, and color palette

### Tests for User Story 6

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T601 [P] [US6] Test SplashScreen displays ASCII art in `tests/test_screens/test_splash.py`
- [ ] T602 [P] [US6] Test SplashScreen timer (1.5s ±0.1s) in `tests/test_screens/test_splash.py`
- [ ] T603 [P] [US6] Test BrandedHeader shows name and version in `tests/test_widgets/test_header.py`
- [ ] T604 [P] [US6] Test tree icons (📦, 🤖, 📋, ⚡) in `tests/test_widgets/test_agent_tree.py::TestTreeIcons`

### Implementation for User Story 6

- [ ] T605 [US6] Create ASCII_LOGO constant in `src/riseon_agents/screens/splash.py`
- [ ] T606 [US6] Create SplashScreen with 1.5s timer in `src/riseon_agents/screens/splash.py`
- [ ] T607 [US6] Integrate splash into app.py on_mount in `src/riseon_agents/app.py`
- [ ] T608 [US6] Create BrandedHeader widget in `src/riseon_agents/widgets/header.py`
- [ ] T609 [US6] Update tree node labels with emoji icons in `src/riseon_agents/widgets/agent_tree.py`
- [ ] T610 [US6] Define CSS color palette variables in `src/riseon_agents/app.py`
- [ ] T611 [US6] Apply green/cyan palette to borders and highlights in `src/riseon_agents/app.py`
- [ ] T612 [US6] Add styled borders to panels in `src/riseon_agents/screens/main.py`
- [ ] T613 [US6] Update screens/__init__.py with SplashScreen export in `src/riseon_agents/screens/__init__.py`
- [ ] T614 [US6] Update widgets/__init__.py with BrandedHeader export in `src/riseon_agents/widgets/__init__.py`

**Checkpoint**: User Story 6 complete - visual redesign implemented

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [ ] T701 Run full test suite (166 existing + ~50 new tests) via `PYTHONPATH=src pytest tests/ -v`
- [ ] T702 [P] Run linting via `ruff check src tests`
- [ ] T703 [P] Run type checking via `mypy src/riseon_agents`
- [ ] T704 [P] Run formatting check via `black --check src tests`
- [ ] T705 Manual TUI walkthrough (splash → header → tree → preview → generate flow)
- [ ] T706 Verify all edge cases from spec.md (permissions, interruption, malformed YAML)
- [ ] T707 Run quickstart.md validation steps

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Foundational)**: No blocking tasks - can start immediately
- **Phase 2-4, 6 (US1, US2, US3, US5)**: Can run in parallel (different files)
- **Phase 5 (US4 - Preview)**: Depends on Phase 2 (US1) for handoff preview
- **Phase 7 (US6 - Visual)**: Should be done last (integrates all changes)
- **Phase 8 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

```
US1 (Handoffs P1) ─────────────────────┐
                                       │
US2 (Target Modal P2) ─────────────────┤
                                       ├──► US6 (Visual P4) ──► Phase 8 (Polish)
US3 (Override Dialog P3) ──────────────┤
                                       │
US4 (Preview P3) ──────────────────────┤
   └── depends on US1 for handoffs     │
                                       │
US5 (Emojis P4) ───────────────────────┘
```

### Within Each User Story

1. Tests MUST be written and FAIL before implementation
2. Implementation tasks follow test tasks
3. Each story is independently testable at checkpoint

### Parallel Opportunities

- All test tasks within a user story marked [P] can run in parallel
- US1, US2, US3, US5 can be developed in parallel (different files)
- US4 depends on US1 but only for the handoff preview portion
- US6 should wait for other stories to avoid merge conflicts

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 2: User Story 1 (Handoffs - P1 Critical)
2. **STOP and VALIDATE**: Test handoff generation independently
3. Deploy/demo if ready - core functionality working

### Incremental Delivery

1. Complete US1 (Handoffs) → Test → Critical functionality working
2. Complete US2 (Target Modal) → Test → UX improvement
3. Complete US3 (Override Dialog) → Test → UX improvement
4. Complete US4 (Preview) → Test → UX improvement
5. Complete US5 (Emojis) → Test → Visual enhancement
6. Complete US6 (Visual Redesign) → Test → Polish complete
7. Phase 8: Final validation

### Priority Order for Sequential Implementation

```
P1: US1 (Handoffs) - CRITICAL, enables sub-agent architecture
P2: US2 (Target Modal) - Essential UX improvement
P3: US3 + US4 (Override + Preview) - UX improvements
P4: US5 + US6 (Emojis + Visual) - Polish and visual enhancements
```

---

## Task Summary

| Phase | User Story | Tests | Implementation | Total | Status |
|-------|------------|-------|----------------|-------|--------|
| 2 | US1 Handoffs (P1) | 5 | 6 | 11 | ✅ DONE |
| 3 | US2 Target Modal (P2) | 6 | 8 | 14 | ✅ DONE |
| 4 | US3 Override Dialog (P3) | 4 | 6 | 10 | ✅ DONE |
| 5 | US4 Preview (P3) | 4 | 4 | 8 | Pending |
| 6 | US5 Emojis (P4) | 6 | 7 | 13 | Pending |
| 7 | US6 Visual (P4) | 4 | 10 | 14 | Pending |
| 8 | Polish | - | 7 | 7 | Pending |
| **Total** | | **29** | **48** | **77** | **35 done** |

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests FAIL before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All 191 tests pass (166 existing + 25 new tests for US1, US2, US3)
- Phases 2, 3, 4 (US1, US2, US3) fully implemented and tested
