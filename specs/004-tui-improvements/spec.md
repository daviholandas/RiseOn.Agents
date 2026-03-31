# Feature Specification: TUI Improvements for RiseOn.Agents Kilo Code Generator

**Feature Branch**: `004-tui-improvements`  
**Created**: 2026-03-30  
**Status**: Draft  
**Input**: User description: "Implementar melhorias na TUI do RiseOn.Agents Kilo Code Generator, uma ferramenta que converte definições de agents (formato RiseOn) para configurações Kilo Code VSCode Extension (formato legacy YAML). As melhorias abrangem 8 áreas principais: 1. HANDOFF ENTRE AGENTS (CRÍTICO): O campo handoffs nos PrimaryAgents é parseado mas não utilizado na geração. Deve-se gerar uma seção '## Available Subagents for Delegation' no final do roleDefinition em custom_modes.yaml, listando os subagents disponíveis com suas descrições em formato de tabela Markdown. Isso permite que o modelo saiba quais subagents pode invocar via task tool. Validar que handoffs apontam para subagents existentes. 2. MODAL DE SELEÇÃO LOCAL VS GLOBAL: Substituir o toggle invisível (tecla L) por uma modal que aparece ANTES de iniciar a geração, com RadioSet mostrando as duas opções (Local: .kilo/ no projeto, Global: ~/.kilocode/) com os paths completos de cada tipo de arquivo. Botões Generate e Cancel. Criar novo arquivo screens/target_dialog.py com TargetSelectionDialog. 3. DIALOG DE OVERRIDE COM CANCEL: O ConfirmDialog atual só tem Yes/No. Adicionar botão Cancel, ajustar CSS para layout horizontal de 3 botões, corrigir callback em main.py linha 241 para tratar None/cancel corretamente, adicionar binding ESC para cancelar. 4. PREVIEW PARA RULES E SKILLS: O preview panel só aplica syntax highlighting (Rich Syntax) para primary_agent e subagent. Aplicar Syntax(markdown) para Rules e Skills também. Melhorar visualização de descrições longas com scroll e seção de metadata formatada. 5. EMOJIS NOS NOMES DOS AGENTS: Adicionar campo opcional emoji no modelo PrimaryAgent, parsear do frontmatter. Criar emojis default baseados em palavras-chave do nome (architect=🏗️, engineer=🧑‍💻, writer=📝, devops=⚙️, security=🔒, default=🤖). Incluir emoji no campo name do custom_modes.yaml gerado. 6. REDESIGN VISUAL COMPLETO: (a) Splash screen com ASCII art logo RiseOn.Agents exibido por 1.5s no ... (line truncated to 2000 chars)

## Clarifications

### Session 2026-03-30

- Q: Como deve funcionar a lógica de atribuição de emoji quando o nome do agent contém múltiplas palavras-chave (ex: 'security-architect')? → A: Emoji keywords são matched case-insensitively, com a primeira palavra-chave que aparece no nome tendo precedência. O emoji aparece no início do field `name` no custom_modes.yaml (e.g., "🏗️ Architect").

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enable Agent Handoff Delegation (Priority: P1)

Agentes primários precisam ser capazes de delegar tarefas para sub-agentes especializados. Atualmente, o campo `handoffs` é definido nos agents mas não é utilizado no gerador de configurações. Isso quebra o pilar de arquitetura de multi-agentes do projeto. O usuário precisa que os handoffs sejam gerados no arquivo custom_modes.yaml para que o modelo do Kilo Code saiba quais sub-agentes podem ser invocados via task tool.

**Why this priority**: Sem handoffs funcionais, o pilar de Sub-agent Architecture do projeto está quebrado. Esta é a funcionalidade mais crítica para o sucesso da ferramenta.

**Independent Test**: Pode ser testado gerando uma configuração com um agent que tem handoffs definidos e verificando que a seção "Available Subagents for Delegation" aparece no roleDefinition com as tabelas formatadas corretamente.

**Acceptance Scenarios**:

1. **Given** um PrimaryAgent com handoffs definidos para subagents existentes, **When** o usuário gera a configuração, **Then** o custom_modes.yaml deve incluir uma seção "## Available Subagents for Delegation" no final do roleDefinition com uma tabela Markdown listando os subagents com suas descrições
2. **Given** um PrimaryAgent com handoffs definidos, **When** um dos subagents referenciados não existe, **Then** o gerador deve apresentar um erro de validação informando qual handoff é inválido
3. **Given** um PrimaryAgent sem handoffs definidos, **When** o usuário gera a configuração, **Then** o custom_modes.yaml deve ser gerado sem a seção de handoffs (não adicionar seção vazia)

---

### User Story 2 - Select Target Location Before Generation (Priority: P2)

O usuário precisa escolher entre gerar configurações locais (no projeto) ou globais (user-wide) antes de iniciar a geração. O toggle atual (tecla 'l') é invisível e não fornece feedback visual claro. O usuário precisa de uma interface intuitiva que mostre claramente as opções e os paths completos de cada tipo de arquivo antes de gerar.

**Why this priority**: Definir o target location antes da geração é essencial para garantir que o usuário não sobrescreva arquivos indevidamente e entenda onde os arquivos serão gerados.

**Independent Test**: Pode ser testado iniciando a geração de uma configuração e verificando que uma modal aparece antes da geração, permitindo selecionar Local ou Global com paths completos visíveis.

**Acceptance Scenarios**:

1. **Given** o usuário está pronto para gerar uma configuração, **When** a geração é iniciada, **Then** uma modal de seleção de target deve aparecer com opções Local e Global
2. **Given** a modal de seleção de target está aberta, **When** o usuário seleciona Local, **Then** os paths mostrados devem incluir `.kilo/` para modes/agents/rules e `.kilocode/` para skills
3. **Given** a modal de seleção de target está aberta, **When** o usuário seleciona Global, **Then** os paths mostrados devem incluir `~/.kilocode/` para todos os tipos de arquivos
4. **Given** a modal de seleção de target está aberta, **When** o usuário clica em Cancel, **Then** a geração não é iniciada e o usuário permanece na tela de seleção de agents
5. **Given** a modal de seleção de target está aberta, **When** o usuário pressiona ESC, **Then** a modal é fechada e a geração não é iniciada

---

### User Story 3 - Improve Override Confirmation Dialog (Priority: P3)

Quando o usuário tenta gerar configurações e existem arquivos existentes, o diálogo de confirmação atual só oferece opções Yes/No sem uma forma clara de cancelar. O usuário precisa de uma ontrol de fluxo consistente e intuitiva.

**Why this priority**: Melhorar a UX do dialog de override é essencial para evitar perda involuntária de arquivos e fornecer um fluxo de usuário consistente.

**Independent Test**: Pode ser testado iniciando a geração com arquivos existentes e verificando que o diálogo mostra opções Yes/No/Cancel claramente organizadas.

**Acceptance Scenarios**:

1. **Given** existem arquivos que seriam sobrescritos, **When** o usuário tenta gerar, **Then** um diálogo de confirmação deve aparecer com botões Yes, No e Cancel
2. **Given** o diálogo de confirmação está aberto, **When** o usuário clica em Yes, **Then** a geração proceed com overwriting dos arquivos
3. **Given** o diálogo de confirmação está aberto, **When** o usuário clica em No, **Then** a geração não é iniciada e o usuário permanece na tela
4. **Given** o diálogo de confirmação está aberto, **When** o usuário clica em Cancel ou pressiona ESC, **Then** a geração não é iniciada e o usuário permanece na tela

---

### User Story 4 - Enhanced Preview for Rules and Skills (Priority: P3)

O usuário precisa visualizar a configuração gerada de Rules e Skills com destaque de syntax adequado (Markdown) e descrições completas legíveis. Atualmente, Rules e Skills mostram texto plain sem formatação adequada, e descrições longas são truncadas.

**Why this priority**: Preview adequado é essencial para que o usuário possa revisar e validar a configuração antes de gerar, garantindo qualidade do output.

**Independent Test**: Pode ser testado selecionando Rules e Skills na árvore e verificando que o preview panel aplica syntax highlighting apropriado e mostra descrições completas com scroll.

**Acceptance Scenarios**:

1. **Given** o usuário seleciona um Rule no tree, **When** o preview é exibido, **Then** o conteúdo deve usar syntax highlighting Markdown
2. **Given** o usuário seleciona uma Skill no tree, **When** o preview é exibido, **Then** o conteúdo deve usar syntax highlighting Markdown/YAML frontmatter
3. **Given** um Rule ou Skill com descrição longa, **When** o preview é exibido, **Then** a descrição deve ser legível com scroll vertical
4. **Given** o preview de um PrimaryAgent, **When** o preview é exibido, **Then** deve incluir a seção de handoffs listando os subagents disponíveis para delegação

---

### User Story 5 - Include Emojis in Agent Names (Priority: P4)

O usuário precisa que os nomes dos agents no custom_modes.yaml incluam emojis para melhor identificação visual. Emojis devem ser retirados do frontmatter do agent ou atribuídos automaticamente baseados em palavras-chave do nome do agent.

**Why this priority**: Emojis melhoram a experiência visual ao navegar por múltiplos agents no Kilo Code, tornando mais fácil identificar cada agent por seu propósito.

**Independent Test**: Pode ser testado gerando uma configuração com agents que têm emojis definidos ou por palavras-chave e verificando que o campo `name` no custom_modes.yaml inclui o emoji.

**Acceptance Scenarios**:

1. **Given** um PrimaryAgent com emoji definido no frontmatter, **When** o usuário gera a configuração, **Then** o campo `name` no custom_modes.yaml deve incluir o emoji definido
2. **Given** um PrimaryAgent sem emoji definido, **When** o usuário gera a configuração, **Then** o campo `name` deve incluir um emoji default baseado em palavras-chave (architect=🏗️, engineer=🧑‍💻, writer=📝, devops=⚙️, security=🔒, default=🤖)
3. **Given** um PrimaryAgent com nome que combina múltiplas palavras-chave, **When** o usuário gera a configuração, **Then** o emoji default deve ser escolhido baseado na prioridade (scaler primeiro: architect > engineer > writer > devops > security)

---

### User Story 6 - Complete Visual Redesign (Priority: P4)

O usuário precisa de uma interface visual atraente e intuitiva com splash screen, header estilizado, ícones nos nós da árvore e paleta de cores consistente. Isso melhora significativamente a primeira impressão e a usabilidade da ferramenta.

**Why this priority**: Uma interface visual competente é essencial para adotar a ferramenta por novos usuários e melhorar a experiência geral.

**Independent Test**: Pode ser testado iniciando a aplicação e verificando que splash screen, header, árvore com ícones e tema de cores são apresentados corretamente.

**Acceptance Scenarios**:

1. **Given** o usuário inicia a aplicação, **When** o splash screen é exibido, **Then** uma ASCII art com "RiseOn.Agents" deve aparecer por 1.5 segundos
2. **Given** a tela principal é exibida, **When** o header é renderizado, **Then** deve mostrar o nome "RiseOn.Agents" com versão estilizada
3. **Given** o usuário navega na árvore de agents, **When** os nós são exibidos, **Then** cada tipo deve ter um ícone visual (📦 Agent, 🤖 Subagent, 📋 Rule, ⚡ Skill)
4. **Given** a aplicação é exibida, **When** o tema é renderizado, **Then** deve usar uma paleta de cores verde/ciano consistente com bordas estilizadas nos painéis

---

### Edge Cases

- What happens when all files already exist and user selects overwrite?  
- How does system handle generation interruption (Ctrl+C) with partial files created?
- What happens when a subagent referenced in handoffs exists but has malformed YAML?
- How does system handle special characters in agent names that might conflict with filename restrictions?
- What happens when target directory doesn't have write permissions?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST generate a section "## Available Subagents for Delegation" at the end of the `roleDefinition` field in custom_modes.yaml for each PrimaryAgent that has handoffs defined
- **FR-002**: System MUST render the available subagents list as a Markdown table with columns for subagent slug and description
- **FR-003**: System MUST validate that all subagent names referenced in handoffs exist in the agent repository before generation
- **FR-004**: System MUST display a validation error if any handoff references a non-existent subagent
- **FR-005**: System MUST NOT include the handoffs section if the PrimaryAgent has no handoffs defined
- **FR-006**: System MUST display a modal dialog before generation starts that allows users to select between Local and Global target locations
- **FR-007**: System MUST show complete file paths for each file type (custom_modes.yaml, agents/, rules/, skills/) for both Local and Global options
- **FR-008**: System MUST include buttons for Generate, No (cancel operation), and Cancel (close dialog) in the override confirmation dialog
- **FR-009**: System MUST support ESC key to close confirmation dialogs (both override and target selection)
- **FR-010**: System MUST apply Markdown syntax highlighting to Rules preview in the preview panel
- **FR-011**: System MUST apply Markdown syntax highlighting to Skills preview in the preview panel
- **FR-012**: System MUST enable vertical scrolling for long descriptions in Rules and Skills preview
- **FR-013**: System MUST include the handoffs section in the PrimaryAgent preview when a PrimaryAgent is selected
- **FR-014**: System MUST allow the PrimaryAgent model to optionally include an `emoji` field parsed from YAML frontmatter
- **FR-015**: System MUST include the emoji field value in the `name` field of the custom_modes.yaml entry when present
- **FR-016**: System MUST generate default emojis for agents based on keyword matching (architect=🏗️, engineer=🧑‍💻, writer=📝, devops=⚙️, security=🔒) when no emoji is defined in frontmatter
- **FR-017**: System MUST display a splash screen with ASCII art "RiseOn.Agents" for 1.5 seconds at application startup
- **FR-018**: System MUST display a stylized header with the application name and version in the main screen
- **FR-019**: System MUST render node icons in the agent tree for Primary Agents (📦), Subagents (🤖), Rules (📋), and Skills (⚡)
- **FR-020**: System MUST apply a consistent green/cyan color palette throughout the UI
- **FR-021**: System MUST apply stylized borders to all panels (tree panel, preview panel, status bar)
- **FR-022**: System MUST document in comments that Local generation uses `.kilo/` for modes/agents/rules and `.kilocode/` for skills, while Global uses `~/.kilocode/` for all types
- **FR-023**: System MUST provide backward compatibility notes explaining that Kilo Code VSCode supports both `.kilo/` and `.kilocode/` directories

### Key Entities

- **PrimaryAgent**: Represents a top-level agent that can delegate tasks to subagents via handoffs. Contains name, description, markdown body (roleDefinition), and list of subagent slugs for delegation.

- **Subagent**: A specialized agent that can be invoked by primary agents. Contains name, description, markdown body (system prompt), and permission configuration.

- **Handoff**: A reference from a PrimaryAgent to a Subagent that can be invoked via the task tool. Stored as a list of subagent slugs in the PrimaryAgent model.

- **Generation Target**: Specifies where configuration files should be generated - either Local (project directory) or Global (user home directory). Determines the base paths for all generated files.

- **Emoji Mapping**: A mapping of keywords to emoji characters used for automatic emoji assignment when no emoji is explicitly defined in agent frontmatter.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully generate a complete configuration with handoffs in under 3 minutes from first agent selection
- **SC-002**: 100% of PrimaryAgents with handoffs must generate valid custom_modes.yaml files with handoffs section correctly formatted
- **SC-003**: All generation targets (Local and Global) must produce files in the correct directory structure verified by file system
- **SC-004**:Preview panel must correctly display all node types (Agents, Subagents, Rules, Skills) with appropriate syntax highlighting
- **SC-005**: 95% of target selection must be correct on first attempt without needing to toggle between Local and Global
- **SC-006**: All confirmation dialogs must be navigable with both mouse clicks and keyboard (ESC, Enter, Tab)
- **SC-007**: Emoji assignment must be successful for 100% of agents (either explicit from frontmatter or default from keywords)
- **SC-008**: Splash screen must display for exactly 1.5 seconds (±0.1s tolerance) without blocking application initialization
- **SC-009**: All 166 existing tests must continue to pass after implementation
- **SC-010**: Visual redesign must be perceived as an improvement by users with clear contrast between new and old UI

## Assumptions

- The Kilo Code VSCode Extension uses the legacy YAML format (`custom_modes.yaml`) rather than the newer CLI format
- Users have read access to the agents directory at startup
- The agent repository can be fully loaded into memory for screening operations
- Target directories (`.kilo/` and `~/.kilocode/`) are accessible with write permissions when generation is initiated
- Handoff references must point to subagents that exist in the same primary agent's subagents collection
- Emoji keywords are matched case-insensitively against agent names, with the first matching keyword taking precedence
- Emoji appears at the beginning of the `name` field in custom_modes.yaml (e.g., "🏗️ Architect")
- Users can navigate the preview panel with arrow keys or mouse click for scrolling
- The application runs on terminals that support Unicode characters (emojis, tree characters)
- Git is available for feature branch creation (using existing script infrastructure)
- Textual 0.47.0+ and Rich 13.0.0+ are available in the Python environment
