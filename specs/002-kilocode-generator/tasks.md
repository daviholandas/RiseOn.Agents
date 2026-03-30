# Tasks: Kilo Code Configuration Generator

**Input**: Design documents from `/specs/002-kilocode-generator/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests included per constitution requirement for TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/riseon_agents/`, `tests/` at repository root
- Paths follow structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per plan.md (`src/riseon_agents/`, `tests/`)
- [ ] T002 Initialize Python project with pyproject.toml (Textual >=0.47.0, Rich >=13.0.0, PyYAML >=6.0, python-frontmatter >=1.0)
- [ ] T003 [P] Configure ruff, black, and mypy in pyproject.toml
- [ ] T004 [P] Create package __init__.py with version in src/riseon_agents/__init__.py
- [ ] T005 [P] Create __main__.py entry point in src/riseon_agents/__main__.py
- [ ] T006 Create pytest configuration in tests/conftest.py with shared fixtures

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models and parsing infrastructure that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

### Data Models (from data-model.md)

- [ ] T007 [P] Implement PermissionLevel enum in src/riseon_agents/models/agent.py
- [ ] T008 [P] Implement PrimaryAgent dataclass in src/riseon_agents/models/agent.py
- [ ] T009 [P] Implement Subagent dataclass in src/riseon_agents/models/agent.py
- [ ] T010 [P] Implement Rule dataclass in src/riseon_agents/models/rule.py
- [ ] T011 [P] Implement Skill dataclass in src/riseon_agents/models/skill.py
- [ ] T012 [P] Implement SelectionState enum and SelectableNode dataclass in src/riseon_agents/models/selection.py
- [ ] T013 [P] Implement GenerationLevel, GenerationTarget, FileStatus, GeneratedFile, GenerationResult in src/riseon_agents/models/generation.py
- [ ] T014 Create models package __init__.py with exports in src/riseon_agents/models/__init__.py
- [ ] T014a [P] Create widgets package __init__.py with exports in src/riseon_agents/widgets/__init__.py
- [ ] T014b [P] Create screens package __init__.py with exports in src/riseon_agents/screens/__init__.py

### Parsing Infrastructure

- [ ] T015 Implement frontmatter parser (YAML + Markdown body) in src/riseon_agents/parsing/frontmatter.py
- [ ] T016 Implement AgentRepository for agent discovery in src/riseon_agents/parsing/repository.py
- [ ] T017 Create parsing package __init__.py with exports in src/riseon_agents/parsing/__init__.py

### Test Fixtures

- [ ] T018 [P] Create sample agent fixtures in tests/fixtures/agents/ (at least 1 primary, 2 subagents, 1 rule, 1 skill)
- [ ] T019 [P] Create tests for data models in tests/test_models/test_agent.py
- [ ] T020 [P] Create tests for selection model in tests/test_models/test_selection.py
- [ ] T021 [P] Create tests for generation model in tests/test_models/test_generation.py
- [ ] T022 Create tests for frontmatter parser in tests/test_parsing/test_frontmatter.py
- [ ] T023 Create tests for AgentRepository in tests/test_parsing/test_repository.py

**Checkpoint**: Foundation ready - data models, parsing, and fixtures complete. User story implementation can now begin.

---

## Phase 3: User Story 1 - View Agent Hierarchy (Priority: P1)

**Goal**: Display complete hierarchy of all defined agents in a tree view with keyboard navigation

**Independent Test**: Launch TUI, verify tree shows all 5 Primary Agents with their subagents, rules, and skills as nested items. Navigate using arrow keys.

**From spec.md**:
- US1-AC1: Tree shows all 5 Primary Agents on launch
- US1-AC2: Expand shows subagents, rules, skills as nested items
- US1-AC3: Keyboard navigation (arrows) works smoothly
- US1-AC4: Malformed agents show warning without crashing

### Tests for User Story 1

- [ ] T024 [P] [US1] Test basic Textual Tree widget in tests/test_widgets/test_agent_tree.py
- [ ] T025 [P] [US1] Test tree population from AgentRepository in tests/test_widgets/test_agent_tree.py
- [ ] T026 [P] [US1] Test keyboard navigation (arrows, Enter) in tests/test_widgets/test_agent_tree.py

### Implementation for User Story 1

- [ ] T027 [US1] Create base SelectableTree widget extending Textual Tree in src/riseon_agents/widgets/agent_tree.py
- [ ] T028 [US1] Implement tree node building from PrimaryAgent hierarchy in src/riseon_agents/widgets/agent_tree.py
- [ ] T029 [US1] Add node type icons (from tui-interactions.md: Primary Agent, Subagent, Rule, Skill) in src/riseon_agents/widgets/agent_tree.py
- [ ] T030 [US1] Implement warning indicator for malformed agents in src/riseon_agents/widgets/agent_tree.py
- [ ] T031 [US1] Create basic MainScreen with tree panel layout in src/riseon_agents/screens/main.py
- [ ] T032 [US1] Create KiloGeneratorApp with agent loading on startup in src/riseon_agents/app.py
- [ ] T033 [US1] Add error screen for missing/empty agents/ folder in src/riseon_agents/screens/dialogs.py
- [ ] T034 [US1] Wire __main__.py to launch KiloGeneratorApp

**Checkpoint**: User Story 1 complete. TUI launches, shows agent hierarchy, keyboard navigation works.

---

## Phase 4: User Story 2 - Select Agents for Generation (Priority: P1)

**Goal**: Enable tri-state selection (SELECTED, UNSELECTED, PARTIAL) with space toggle and propagation

**Independent Test**: Toggle selection on agents, verify parent shows PARTIAL when some children selected, bulk select/deselect works.

**From spec.md**:
- US2-AC1: Space/Enter toggles selection with visual indicator
- US2-AC2: Selecting Primary Agent selects all subagents
- US2-AC3: Deselecting subagent shows PARTIAL on parent
- US2-AC4: Selection count visible in summary

### Tests for User Story 2

- [ ] T035 [P] [US2] Test SelectionState transitions in tests/test_widgets/test_agent_tree.py
- [ ] T036 [P] [US2] Test selection propagation (parent to children) in tests/test_widgets/test_agent_tree.py
- [ ] T037 [P] [US2] Test PARTIAL state calculation in tests/test_widgets/test_agent_tree.py
- [ ] T038 [P] [US2] Test bulk selection (a/A keys) in tests/test_widgets/test_agent_tree.py

### Implementation for User Story 2

- [ ] T039 [US2] Implement tri-state toggle on Space key in src/riseon_agents/widgets/agent_tree.py
- [ ] T040 [US2] Implement selection propagation down (parent to children) in src/riseon_agents/widgets/agent_tree.py
- [ ] T041 [US2] Implement PARTIAL state calculation up (children to parent) in src/riseon_agents/widgets/agent_tree.py
- [ ] T042 [US2] Add selection state icons (from tui-interactions.md: selected, unselected, partial) in src/riseon_agents/widgets/agent_tree.py
- [ ] T043 [US2] Implement bulk selection (a = select all, A = deselect all) in src/riseon_agents/widgets/agent_tree.py
- [ ] T044 [US2] Add selection count to status bar in src/riseon_agents/screens/main.py

**Checkpoint**: User Story 2 complete. Selection works with tri-state, propagation, and bulk operations.

---

## Phase 5: User Story 5 - Generate Configuration Files (Priority: P1)

**Goal**: Generate valid Kilo Code configuration files to Local (.kilo/) target

**Independent Test**: Select agents, trigger generation (g key), verify files created with correct content per generator-output.md contracts.

**From spec.md**:
- US5-AC1: Generate creates appropriate files for selected agents
- US5-AC2: Progress indicator during generation
- US5-AC3: Summary shows files created with paths
- US5-AC4: Prompt before overwriting existing files

### Tests for User Story 5

- [ ] T045 [P] [US5] Test custom_modes.yaml generation in tests/test_generation/test_modes.py
- [ ] T046 [P] [US5] Test subagent .md generation in tests/test_generation/test_subagents.py
- [ ] T047 [P] [US5] Test rules generation in tests/test_generation/test_rules.py
- [ ] T048 [P] [US5] Test skills generation in tests/test_generation/test_skills.py
- [ ] T049 [P] [US5] Test KiloCodeGenerator orchestrator in tests/test_generation/test_generator.py

### Implementation for User Story 5

- [ ] T050 [P] [US5] Implement custom_modes.yaml generator (per generator-output.md) in src/riseon_agents/generation/modes.py
- [ ] T051 [P] [US5] Implement subagent .md generator (per generator-output.md) in src/riseon_agents/generation/subagents.py
- [ ] T052 [P] [US5] Implement rules generator (shared + mode-specific) in src/riseon_agents/generation/rules.py
- [ ] T053 [P] [US5] Implement skills generator (SKILL.md + subdirs) in src/riseon_agents/generation/skills.py
- [ ] T054 [US5] Create KiloCodeGenerator orchestrator in src/riseon_agents/generation/generator.py
- [ ] T055 [US5] Create generation package __init__.py with exports in src/riseon_agents/generation/__init__.py
- [ ] T056 [US5] Implement generate action (g key) in MainScreen in src/riseon_agents/screens/main.py
- [ ] T057 [US5] Add generation progress indicator widget in src/riseon_agents/screens/main.py
- [ ] T058 [US5] Implement ResultDialog for generation summary in src/riseon_agents/screens/dialogs.py
- [ ] T059 [US5] Implement ConfirmDialog for overwrite confirmation in src/riseon_agents/screens/dialogs.py

**Checkpoint**: User Story 5 complete. MVP COMPLETE - can view agents, select, and generate Local configurations.

---

## Phase 6: User Story 3 - Preview Generated Configuration (Priority: P2)

**Goal**: Real-time preview panel showing generated configuration for focused agent

**Independent Test**: Navigate to agent in tree, verify preview panel shows generated configuration with syntax highlighting.

**From spec.md**:
- US3-AC1: Preview panel shows generated config for selected agent
- US3-AC2: Primary Agent preview shows custom_modes.yaml entry
- US3-AC3: Subagent preview shows .kilo/agents/*.md format
- US3-AC4: Preview scrollable for complete content

### Tests for User Story 3

- [ ] T060 [P] [US3] Test preview content generation in tests/test_widgets/test_preview.py
- [ ] T061 [P] [US3] Test preview update on tree navigation in tests/test_widgets/test_preview.py

### Implementation for User Story 3

- [ ] T062 [US3] Create PreviewPanel widget with syntax highlighting in src/riseon_agents/widgets/preview.py
- [ ] T063 [US3] Implement preview content generation for each node type in src/riseon_agents/widgets/preview.py
- [ ] T064 [US3] Add preview panel to MainScreen layout (right side, 60%) in src/riseon_agents/screens/main.py
- [ ] T065 [US3] Wire tree focus events to preview updates in src/riseon_agents/screens/main.py
- [ ] T066 [US3] Add Tab navigation between tree and preview panels in src/riseon_agents/screens/main.py

**Checkpoint**: User Story 3 complete. Preview panel shows real-time configuration.

---

## Phase 7: User Story 4 - Choose Generation Level (Priority: P2)

**Goal**: Toggle between Local (.kilo/) and Global (~/.kilocode/) generation targets

**Independent Test**: Toggle Local/Global (l key), verify target path changes, preview paths update.

**From spec.md**:
- US4-AC1: Toggle visible for Local vs Global
- US4-AC2: Local shows ./.kilo/ path
- US4-AC3: Global shows ~/.kilocode/ path
- US4-AC4: Preview paths update on toggle

### Tests for User Story 4

- [ ] T068 [P] [US4] Test GenerationTarget path resolution in tests/test_models/test_generation.py
- [ ] T069 [P] [US4] Test Local vs Global path differences in tests/test_generation/test_generator.py

### Implementation for User Story 4

- [ ] T070 [US4] Add generation level toggle widget (l key) in src/riseon_agents/screens/main.py
- [ ] T071 [US4] Implement target path display based on level in src/riseon_agents/screens/main.py
- [ ] T072 [US4] Wire level toggle to preview path updates in src/riseon_agents/screens/main.py
- [ ] T073 [US4] Update KiloCodeGenerator to use GenerationTarget in src/riseon_agents/generation/generator.py

**Checkpoint**: User Story 4 complete. Local and Global generation targets work.

---

## Phase 8: User Story 6 - Validate Configuration Format (Priority: P3)

**Goal**: Validate generated YAML and Markdown configuration files

**Independent Test**: Generate configs, view validation report with pass/fail status and error locations.

**From spec.md**:
- US6-AC1: Validation report shows pass/fail status
- US6-AC2: Format errors show specific messages with locations
- US6-AC3: Success confirmation when all valid

### Tests for User Story 6

- [ ] T074 [P] [US6] Test YAML validation in tests/test_generation/test_generator.py
- [ ] T075 [P] [US6] Test Markdown structure validation in tests/test_generation/test_generator.py

### Implementation for User Story 6

- [ ] T076 [US6] Implement YAML syntax validation in src/riseon_agents/generation/generator.py
- [ ] T077 [US6] Implement Markdown structure validation in src/riseon_agents/generation/generator.py
- [ ] T078 [US6] Add validation results to generation summary in src/riseon_agents/screens/dialogs.py
- [ ] T079 [US6] Show validation errors with file and line info in ResultDialog

**Checkpoint**: User Story 6 complete. Validation catches format errors.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Edge cases, error handling, performance, documentation

### Edge Cases (from spec.md)

- [ ] T080 [P] Handle empty agents/ folder with clear guidance in src/riseon_agents/app.py
- [ ] T081 [P] Handle write permission errors with suggested resolution in src/riseon_agents/generation/generator.py
- [ ] T082 [P] Handle generation interruption (Ctrl+C) with cleanup (delete incomplete files, preserve completed) in src/riseon_agents/generation/generator.py
- [ ] T083 [P] Create Global config directory automatically with confirmation in src/riseon_agents/generation/generator.py

### Help System (from tui-interactions.md)

- [ ] T084 Implement help overlay (? key) with keyboard shortcuts in src/riseon_agents/screens/main.py

### Error Handling

- [ ] T085 [P] Implement ErrorDialog for permission/disk errors in src/riseon_agents/screens/dialogs.py

### Performance (from SC-001, SC-004, SC-005)

- [ ] T087 Verify tree load <2s for 5 Primary + 26 Subagents
- [ ] T088 Verify preview update <500ms
- [ ] T089 Verify full generation <10s

### Documentation

- [ ] T090 Run quickstart.md validation scenarios
- [ ] T091 Update AGENTS.md with final command references

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - US1, US2, US5 are P1 and form the MVP
  - US3, US4 are P2 (preview and level toggle)
  - US6 is P3 (validation)
- **Polish (Phase 9)**: Can start after MVP (US1+US2+US5) complete

### User Story Dependencies

- **User Story 1 (P1)**: View Agent Hierarchy - No dependencies on other stories
- **User Story 2 (P1)**: Select Agents - Can start after US1 (needs tree)
- **User Story 5 (P1)**: Generate Files - Can start after US2 (needs selection)
- **User Story 3 (P2)**: Preview - Can start after US1 (needs tree)
- **User Story 4 (P2)**: Generation Level - Can start after US5 (needs generation)
- **User Story 6 (P3)**: Validation - Can start after US5 (needs generation)

### MVP Completion Path

```
Setup → Foundational → US1 → US2 → US5 → MVP COMPLETE
```

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models/data before logic
- Core implementation before UI integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational model tasks (T007-T013) can run in parallel
- All Foundational test tasks (T018-T021) can run in parallel
- Tests for each user story marked [P] can run in parallel
- Generation module tasks (T050-T053) can run in parallel

---

## Parallel Example: User Story 5 (Generation)

```bash
# Launch all tests together:
Task: "Test custom_modes.yaml generation in tests/test_generation/test_modes.py"
Task: "Test subagent .md generation in tests/test_generation/test_subagents.py"
Task: "Test rules generation in tests/test_generation/test_rules.py"
Task: "Test skills generation in tests/test_generation/test_skills.py"

# Launch all generators together:
Task: "Implement custom_modes.yaml generator in src/riseon_agents/generation/modes.py"
Task: "Implement subagent .md generator in src/riseon_agents/generation/subagents.py"
Task: "Implement rules generator in src/riseon_agents/generation/rules.py"
Task: "Implement skills generator in src/riseon_agents/generation/skills.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 5)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 - View Agent Hierarchy
4. Complete Phase 4: User Story 2 - Select Agents
5. Complete Phase 5: User Story 5 - Generate Files
6. **STOP and VALIDATE**: Test MVP independently
7. Deploy/demo: TUI launches, shows tree, selection works, generates files

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → Tree view works → Demo
3. Add US2 → Selection works → Demo
4. Add US5 → Generation works → **MVP Complete!**
5. Add US3 → Preview panel → Enhanced UX
6. Add US4 → Local/Global toggle → Full generation options
7. Add US6 → Validation → Production quality

---

## Summary

| Phase | Tasks | Parallel | Description |
|-------|-------|----------|-------------|
| 1. Setup | 6 | 3 | Project scaffolding |
| 2. Foundational | 19 | 16 | Models, parsing, fixtures, package inits |
| 3. US1 (P1) | 11 | 3 | View Agent Hierarchy |
| 4. US2 (P1) | 10 | 4 | Select Agents |
| 5. US5 (P1) | 15 | 9 | Generate Files (MVP) |
| 6. US3 (P2) | 7 | 2 | Preview Panel |
| 7. US4 (P2) | 6 | 2 | Generation Level |
| 8. US6 (P3) | 6 | 2 | Validation |
| 9. Polish | 11 | 5 | Edge cases, docs |
| **Total** | **91** | **44** | |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = US1 + US2 + US5 (View, Select, Generate)
