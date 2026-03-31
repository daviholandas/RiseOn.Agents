# UI Contracts: TUI Improvements

**Feature**: 004-tui-improvements  
**Date**: 2026-03-30

## Overview

This document defines the UI contracts for new dialogs and widgets introduced in the TUI Improvements feature.

---

## 1. TargetSelectionDialog

### Purpose
Modal dialog for selecting generation target (Local vs Global) before file generation.

### Visual Contract

```
┌─────────────────────────────────────────────────────────┐
│                  Select Generation Target               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Choose where to generate configuration files:          │
│                                                         │
│  ◉ Local (Project Directory)                           │
│    └─ custom_modes.yaml  → ./.kilo/custom_modes.yaml   │
│    └─ agents/*.md        → ./.kilo/agents/             │
│    └─ rules/*.md         → ./.kilo/rules/              │
│    └─ skills/*/SKILL.md  → ./.kilocode/skills/         │
│                                                         │
│  ○ Global (User Directory)                             │
│    └─ custom_modes.yaml  → ~/.kilocode/custom_modes.yaml│
│    └─ agents/*.md        → ~/.kilocode/agents/         │
│    └─ rules/*.md         → ~/.kilocode/rules/          │
│    └─ skills/*/SKILL.md  → ~/.kilocode/skills/         │
│                                                         │
│            ┌──────────┐    ┌──────────┐                │
│            │ Generate │    │  Cancel  │                │
│            └──────────┘    └──────────┘                │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Dimensions
- Width: 70 characters
- Height: Auto (approx 20 lines)
- Center aligned in terminal

### Interactions

| Input | Action | Result |
|-------|--------|--------|
| Click "Generate" | Dismiss with selection | Returns `TargetSelectionResult(level=selected)` |
| Click "Cancel" | Close dialog | Returns `TargetSelectionResult(cancelled=True)` |
| Press ESC | Close dialog | Returns `TargetSelectionResult(cancelled=True)` |
| Press Enter | Confirm current selection | Same as "Generate" click |
| Arrow keys | Navigate RadioSet | Changes selection |

### CSS Classes
```css
TargetSelectionDialog { }
TargetSelectionDialog > Container { }
TargetSelectionDialog > Container > Label.title { }
TargetSelectionDialog > Container > RadioSet { }
TargetSelectionDialog > Container > Static.paths { }
TargetSelectionDialog > Container > Horizontal.buttons { }
```

---

## 2. ConfirmDialog (Enhanced)

### Purpose
Three-button confirmation dialog with Yes/No/Cancel options.

### Visual Contract

```
┌───────────────────────────────────────────────────┐
│           Overwrite Existing Files?               │
├───────────────────────────────────────────────────┤
│                                                   │
│  The following files already exist:               │
│                                                   │
│  - custom_modes.yaml                              │
│  - agents/architect.md                            │
│  - rules/coding-standards.md                      │
│  ... and 2 more files                             │
│                                                   │
│  Do you want to overwrite them?                   │
│                                                   │
│     ┌─────┐    ┌─────┐    ┌────────┐             │
│     │ Yes │    │ No  │    │ Cancel │             │
│     └─────┘    └─────┘    └────────┘             │
│                                                   │
└───────────────────────────────────────────────────┘
```

### Dimensions
- Width: 60 characters
- Height: Auto (max 20 lines)
- Center aligned in terminal

### Button Layout
- Horizontal container
- Equal spacing: `margin: 0 1`
- Minimum width: 10 characters each

### Interactions

| Input | Action | Result |
|-------|--------|--------|
| Click "Yes" | Confirm action | Returns `ConfirmResult.YES` |
| Click "No" | Reject action | Returns `ConfirmResult.NO` |
| Click "Cancel" | Cancel operation | Returns `ConfirmResult.CANCEL` |
| Press ESC | Cancel operation | Returns `ConfirmResult.CANCEL` |
| Press Y | Shortcut for Yes | Returns `ConfirmResult.YES` |
| Press N | Shortcut for No | Returns `ConfirmResult.NO` |

### CSS Changes
```css
/* Before (vertical) */
ConfirmDialog > Container > Vertical > Button { }

/* After (horizontal) */
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

---

## 3. SplashScreen

### Purpose
Branding splash screen displayed on application startup.

### Visual Contract

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                                                                 │
│                                                                 │
│         ██████╗ ██╗███████╗███████╗ ██████╗ ███╗   ██╗         │
│         ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗████╗  ██║         │
│         ██████╔╝██║███████╗█████╗  ██║   ██║██╔██╗ ██║         │
│         ██╔══██╗██║╚════██║██╔══╝  ██║   ██║██║╚██╗██║         │
│         ██║  ██║██║███████║███████╗╚██████╔╝██║ ╚████║         │
│         ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝         │
│                                                                 │
│                      █████╗  ██████╗ ███████╗███╗   ██╗████████╗███████╗
│                     ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝██╔════╝
│                     ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║   ███████╗
│                     ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
│                     ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║   ███████║
│                     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝
│                                                                 │
│                    Kilo Code Configuration Generator            │
│                           v1.0.0                                │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Dimensions
- Full screen
- Center aligned content
- Works on 80x24 minimum terminal

### Timing
- Display duration: 1.5 seconds (±0.1s tolerance)
- Auto-dismiss via timer
- No user interaction required

### Fallback (smaller terminals)
```
┌────────────────────────────────┐
│                                │
│      RiseOn.Agents             │
│                                │
│  Kilo Code Generator v1.0.0   │
│                                │
└────────────────────────────────┘
```

### CSS Classes
```css
SplashScreen {
    align: center middle;
    background: $surface;
}

SplashScreen > Static.logo {
    text-align: center;
    color: $primary;
}

SplashScreen > Static.subtitle {
    text-align: center;
    color: $text-muted;
}
```

---

## 4. PreviewPanel (Enhanced)

### Purpose
Display generated configuration preview with syntax highlighting.

### Visual Contract - Rules Preview

```
┌─ Preview ──────────────────────────────────────────────┐
│ # Target: ./.kilo/rules/coding-standards.md            │
│ # Rule: Coding Standards                               │
│                                                        │
│ ## Code Style                                          │
│                                                        │
│ All code must follow these conventions:                │
│                                                        │
│ - Use 4 spaces for indentation                         │
│ - Maximum line length: 100 characters                  │
│ - Use descriptive variable names                       │
│                                                        │
│ ## Documentation                                       │
│                                                        │
│ Every function must have:                              │
│ - Docstring with description                           │
│ - Args section listing parameters                      │
│ - Returns section describing output                    │
│                                                        │
│ ▼ (scroll for more)                                    │
└────────────────────────────────────────────────────────┘
```

### Visual Contract - Skills Preview

```
┌─ Preview ──────────────────────────────────────────────┐
│ # Target: ./.kilocode/skills/speckit/SKILL.md          │
│ # Skill: Speckit                                       │
│ # Description: Specification toolkit for planning      │
│                                                        │
│ ---                                                    │
│ name: speckit                                          │
│ description: Specification toolkit for planning        │
│ ---                                                    │
│                                                        │
│ # Speckit Skill                                        │
│                                                        │
│ This skill provides tools for creating and managing    │
│ feature specifications...                              │
│                                                        │
│ ## Commands                                            │
│                                                        │
│ - `/speckit.spec` - Create new specification           │
│ - `/speckit.plan` - Generate implementation plan       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Syntax Highlighting

| Node Type | Lexer | Theme |
|-----------|-------|-------|
| primary_agent | yaml | monokai |
| subagent | yaml | monokai |
| rule | markdown | monokai |
| skill | markdown | monokai |

### Scrolling
- Vertical scroll enabled for all previews
- CSS: `overflow: auto scroll`
- Mouse wheel and arrow key navigation

---

## 5. AgentTree (Enhanced Icons)

### Visual Contract

```
┌─ Agents ───────────────────────────────────────────────┐
│ ▼ Agents                                               │
│   ├─ ☑ 📦 Architect                                   │
│   │   ├─ Subagents                                     │
│   │   │   ├─ ☑ 🤖 Code Reviewer                       │
│   │   │   └─ ☑ 🤖 Tech Lead                           │
│   │   ├─ Rules                                         │
│   │   │   └─ ☐ 📋 Coding Standards                    │
│   │   └─ Skills                                        │
│   │       └─ ☐ ⚡ Speckit                              │
│   └─ ☐ 📦 Writer                                      │
│       ├─ Subagents                                     │
│       │   └─ ☐ 🤖 Editor                              │
│       └─ Rules                                         │
│           └─ ☐ 📋 Writing Style                       │
│                                                        │
│ Selected: 3/8 | Target: Local                          │
└────────────────────────────────────────────────────────┘
```

### Icon Mapping

| Node Type | Old Icon | New Icon | Description |
|-----------|----------|----------|-------------|
| primary_agent | ◉ | 📦 | Package/Agent container |
| subagent | ○ | 🤖 | Robot/AI agent |
| rule | ▪ | 📋 | Clipboard/Document |
| skill | ★ | ⚡ | Lightning/Ability |

### Selection State Icons (Unchanged)

| State | Icon |
|-------|------|
| UNSELECTED | ☐ |
| SELECTED | ☑ |
| PARTIAL | ◪ |

---

## 6. BrandedHeader

### Purpose
Stylized header with application branding and version.

### Visual Contract

```
┌─────────────────────────────────────────────────────────────────┐
│ 🚀 RiseOn.Agents                           Kilo Code Generator │
│    ══════════════                                    v1.0.0    │
└─────────────────────────────────────────────────────────────────┘
```

### Elements
- Left: Logo emoji + Application name with underline
- Right: Subtitle + Version number
- Background: Gradient or solid color from palette

### CSS Classes
```css
BrandedHeader {
    dock: top;
    height: 2;
    background: $primary;
    color: $text;
}

BrandedHeader > Static.title {
    text-style: bold;
}

BrandedHeader > Static.version {
    text-align: right;
    color: $text-muted;
}
```

---

## Color Palette

### Primary Colors

| Variable | RGB | Hex | Usage |
|----------|-----|-----|-------|
| $primary | rgb(0, 200, 150) | #00C896 | Borders, accents |
| $secondary | rgb(100, 255, 200) | #64FFC8 | Highlights |
| $accent | rgb(0, 180, 130) | #00B482 | Focus states |

### Semantic Colors (Unchanged)

| Variable | Usage |
|----------|-------|
| $success | Success dialogs, checkmarks |
| $error | Error dialogs, warnings |
| $warning | Validation warnings |
| $surface | Dialog backgrounds |
| $text | Primary text |
| $text-muted | Secondary text |

---

## Accessibility Notes

1. **Keyboard Navigation**: All dialogs support full keyboard control
2. **Focus Indicators**: Clear visual focus state on buttons and options
3. **Color Contrast**: Minimum 4.5:1 ratio for text on backgrounds
4. **Screen Reader**: Labels provided for all interactive elements
5. **Escape Route**: ESC always cancels/closes dialogs
