# RiseOn.Agents

**Context-Engineered Sub-agent Architecture Framework for AI Coding Platforms**

RiseOn.Agents é um framework que transforma definições centralizadas de agentes em configurações otimizadas para múltiplas plataformas de AI Coding, utilizando **Sub-agent Architecture** como modelo canônico de distribuição de contexto.

## Visão do Projeto

Imagine definir seus agentes de IA uma única vez e ter configurações otimizadas geradas automaticamente para qualquer plataforma de AI Coding que você utiliza. Sem duplicação, sem inconsistências, sem manutenção manual de múltiplos formatos.

**RiseOn.Agents** nasceu da necessidade de:

- **Centralizar definições**: Uma fonte de verdade para todos os agentes
- **Eliminar fragmentação**: Fim da manutenção manual em múltiplos formatos
- **Otimizar contexto**: Distribuição inteligente que maximiza eficiência
- **Garantir consistência**: Mesmos agentes, mesma qualidade, em todas as plataformas

## O Problema

AI Coding Agents são poderosos, mas enfrentam dois desafios críticos:

```
PROBLEMA 1: Contexto Monolítico
┌─────────────────────────────────────────────────────────────┐
│ 1 Agent com TODO o contexto (200k tokens)                   │
│ ├── Identity (500 tokens)                                   │
│ ├── ALL Skills (50k tokens)  ← DESPERDÍCIO                 │
│ ├── ALL Rules (10k tokens)   ← RUÍDO                       │
│ └── ALL Knowledge (140k tokens)                             │
└─────────────────────────────────────────────────────────────┘

PROBLEMA 2: Formato Fragmentado
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│ Kilo Code  │  │  OpenCode  │  │  GitHub    │  │  Windsurf  │
│ .kilo/     │  │ .opencode/ │  │ .github/   │  │ .windsurf/ │
│ YAML+MD    │  │ MD only    │  │ MD+YAML    │  │ YAML       │
└────────────┘  └────────────┘  └────────────┘  └────────────┘
     ↑               ↑               ↑               ↑
     └───────────────┴───────────────┴───────────────┘
                 Manutenção manual = INCONSISTÊNCIA
```

## A Solução: Sub-agent Architecture

Sub-agent Architecture não é apenas delegação de tarefas - é uma **estratégia de Context Engineering**:

```
┌─────────────────────────────────────────────────────────────────┐
│              SUB-AGENT CONTEXT DISTRIBUTION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Primary Agent: software-engineer (8k tokens)                   │
│  ├── Identity + Guardrails (700 tokens)                         │
│  ├── Handoff Registry (300 tokens) ← SABE QUEM DELEGAR         │
│  └── Core Skills only (7k tokens)                               │
│                                                                 │
│      ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│      │@code-reviewer│  │ @test-writer │  │@refactoring  │      │
│      │ 4k tokens    │  │  5k tokens   │  │ 3k tokens    │      │
│      │  ON-DEMAND   │  │  ON-DEMAND   │  │  ON-DEMAND   │      │
│      └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                                 │
│  Resultado: 8k base + 5k quando necessário                      │
│             vs. 200k tokens sempre carregados                   │
└─────────────────────────────────────────────────────────────────┘
```

### Modelo de Contexto em Camadas

| Camada | Quando Carrega | Conteúdo | Tokens |
|--------|----------------|----------|--------|
| **Layer 1: Orchestration** | Sempre | Identity, Guardrails, Handoff Registry | ~1k |
| **Layer 2: Delegation** | No handoff | Subagent Identity, Task Context | ~4k |
| **Layer 3: Execution** | On-demand | Skills específicos da tarefa | ~2-5k |

## Benefícios

### Para Desenvolvedores

- **Uma definição, múltiplas plataformas**: Defina uma vez, gere para todas
- **TUI intuitivo**: Interface visual moderna para configuração e preview
- **Validação automática**: Garante compatibilidade com cada plataforma
- **Zero lock-in**: Troque de plataforma sem retrabalho

### Para Times

- **Consistência garantida**: Mesmos agentes em todos os ambientes
- **Onboarding simplificado**: Novos membros têm os mesmos agentes configurados
- **Versionamento centralizado**: Agentes no Git, junto com o código
- **Colaboração facilitada**: Contribuições em formato único e padronizado

### Para Organizações

- **Governança de AI Agents**: Controle centralizado de comportamentos
- **Auditoria simplificada**: Uma fonte de verdade para compliance
- **Escalabilidade**: Adicione plataformas sem multiplicar esforço
- **Redução de custos**: Menos tokens = menos gastos com API

## Arquitetura de Agentes

### Hierarquia: 5 Primary Agents + 26 Subagents

```
Primary Agents (5)
│
├── architect
│   ├── adr-generator
│   ├── ddd-specialist
│   ├── governance-specialist
│   ├── hlbpa-specialist
│   ├── mermaid-diagrammer
│   ├── microservices-specialist
│   ├── system-architecture-reviewer
│   └── technical-writer
│
├── software-engineer
│   ├── api-architect
│   ├── code-reviewer
│   ├── dotnet-specialist
│   ├── frontend-developer
│   ├── refactoring-specialist
│   └── test-writer
│
├── devops-engineer
│   ├── cicd-specialist
│   ├── cloud-architect
│   └── security-auditor
│
├── product-manager
│   ├── market-researcher
│   ├── mvp-definer
│   ├── product-strategist
│   ├── requirements-analyst
│   └── roadmap-planner
│
└── product-owner
    ├── acceptance-criteria-writer
    ├── agile-coach
    ├── backlog-manager
    └── sprint-planner
```

### Estrutura de Definição (Fonte Canônica)

```
agents/{agent-name}/
├── {agent-name}.agent.md    # Definição principal do agente
├── rules/                   # Regras e guardrails
│   ├── shared.guardrails.md       # Aplicadas a todos
│   └── {domain}.instructions.md   # Específicas do domínio
├── skills/                  # Conhecimento especializado
│   ├── skill-1/SKILL.md
│   └── skill-2/SKILL.md
└── subagents/              # Sub-agentes especializados
    ├── subagent-1.agent.md
    └── subagent-2.agent.md
```

## Plataformas Suportadas

RiseOn.Agents gera configurações nativas para múltiplas plataformas de AI Coding:

| Plataforma | IDE/Editor | Formato de Saída |
|------------|------------|------------------|
| **Kilo Code** | JetBrains IDEs | `.kilo/`, `.kilocode/`, `kilo.json` |
| **OpenCode** | Terminal/CLI | `.opencode/` |
| **GitHub Copilot** | VS Code, JetBrains | `.github/agents/`, `.github/prompts/` |
| **Windsurf** | Windsurf Editor | `.windsurf/` |

### Mapeamento Conceitual

O framework traduz conceitos universais para cada plataforma:

| RiseOn.Agents | Conceito | Descrição |
|---------------|----------|-----------|
| `{agent}.agent.md` | Primary Agent | Agente principal com orquestração |
| `subagents/*.md` | Subagent | Especialista delegado on-demand |
| `rules/` | Guardrails/Rules | Comportamentos e restrições |
| `skills/` | Skills/Knowledge | Conhecimento especializado |
| `handoffs` | Delegation | Roteamento entre agentes |

### Exemplo: Estrutura Gerada

Ao selecionar uma plataforma no TUI, a seguinte estrutura é gerada:

```
projeto/
├── .{platform}/
│   ├── modes.yaml              # Primary Agents como Modes/Agents
│   ├── agents/                 # Subagents
│   │   ├── code-reviewer.md
│   │   ├── test-writer.md
│   │   └── ...
│   ├── rules/                  # Rules compartilhadas
│   │   └── collaboration.md
│   └── rules-{mode}/           # Rules específicas por mode
│
├── .{platform}code/
│   ├── skills/                 # Skills genéricos
│   └── skills-{mode}/          # Skills por mode
│
└── {platform}.json             # Configurações (permissions, models)
```

### Exemplo: Agente Gerado

```yaml
# Primary Agent (Mode)
- slug: software-engineer
  name: Software Engineer
  description: Expert-level implementation, testing, and code quality
  roleDefinition: |
    You are an expert Software Engineer with deep expertise in 
    software design patterns, clean code principles, and testing.
  groups:
    - read
    - edit
    - command
  whenToUse: |
    Use for implementing features, writing tests, code review, 
    and refactoring tasks.
```

```markdown
# Subagent
---
description: Reviews code for quality, security, and best practices
mode: subagent
temperature: 0.1
permission:
  edit: deny
  bash: deny
---

# Code Reviewer

You are a senior code reviewer focused on identifying issues
and suggesting improvements without making direct changes.

## Focus Areas
- Security vulnerabilities
- Performance implications
- Code quality and maintainability
```

## Instalação

```bash
# Clone o repositório
git clone https://github.com/your-org/RiseOn.Agents.git
cd RiseOn.Agents

# Instale as dependências
npm install

# Execute
npm start
```

## Uso

### Terminal User Interface (TUI)

```bash
riseon-agents
```

O comando abre uma interface TUI moderna e interativa onde você pode:

- **Navegar** pela hierarquia completa de agentes
- **Selecionar** quais agentes incluir na geração
- **Escolher** a plataforma de destino
- **Visualizar** preview das configurações antes de gerar
- **Configurar** opções específicas de cada plataforma
- **Validar** compatibilidade e detectar problemas

```
┌─────────────────────────────────────────────────────────────┐
│  RiseOn.Agents                              v1.0.0          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ Agents ─────────────────┐  ┌─ Preview ───────────────┐ │
│  │ ▼ architect              │  │ # software-engineer     │ │
│  │   ├── adr-generator      │  │                         │ │
│  │   └── ddd-specialist     │  │ roleDefinition: |       │ │
│  │ ▼ software-engineer  ✓   │  │   You are an expert...  │ │
│  │   ├── code-reviewer  ✓   │  │                         │ │
│  │   └── test-writer    ✓   │  │ groups:                 │ │
│  │ ▶ devops-engineer        │  │   - read                │ │
│  │ ▶ product-manager        │  │   - edit                │ │
│  │ ▶ product-owner          │  │   - command             │ │
│  └──────────────────────────┘  └─────────────────────────┘ │
│                                                             │
│  Target: [Kilo Code ▼]    [Generate]    [Validate]         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Estrutura do Projeto

```
RiseOn.Agents/
├── agents/                   # Definições canônicas dos agentes
│   ├── architect/
│   │   ├── architect.agent.md
│   │   ├── rules/
│   │   ├── skills/
│   │   └── subagents/
│   ├── software-engineer/
│   ├── devops-engineer/
│   ├── product-manager/
│   └── product-owner/
├── src/                      # Código fonte
│   ├── tui/                  # Interface TUI
│   ├── generators/           # Geradores por plataforma
│   │   ├── kilo/
│   │   ├── opencode/
│   │   ├── github/
│   │   └── windsurf/
│   ├── parsers/              # Parsers de definições
│   └── analyzers/            # Análise de contexto
├── .specify/                 # Spec-driven development
│   └── memory/
│       └── constitution.md
└── docs/
```

## Documentação de Referência

### Plataformas

| Plataforma | Documentação |
|------------|--------------|
| Kilo Code | [kilo.ai/docs/customize](https://kilo.ai/docs/customize) |
| OpenCode | [opencode.ai/docs](https://opencode.ai/docs) |
| GitHub Copilot | [docs.github.com/copilot](https://docs.github.com/copilot) |
| Windsurf | [docs.windsurf.com](https://docs.windsurf.com) |

### Standards

- [AgentSkills.io](https://agentskills.io/) - Agent Skills Specification
- [AGENTS.md Standard](https://agents.md) - Universal Agent Configuration

## Princípios de Desenvolvimento

Este projeto segue a constituição definida em `.specify/memory/constitution.md`:

1. **Documentation-First**: Configurações baseadas em documentação oficial
2. **Modern TUI Design**: Interface moderna, intuitiva e visualmente atraente
3. **Phase-Based Validation**: Validação do usuário em cada fase
4. **Test-First Development**: TDD obrigatório
5. **Agent Modularity**: Agentes independentes e reutilizáveis
6. **Observability**: Operações rastreáveis e auditáveis
7. **Simplicity**: Começar simples, adicionar complexidade quando justificado

## Contribuindo

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Siga os princípios da constituição
4. Inclua testes para novas funcionalidades
5. Abra um Pull Request

## Licença

[MIT License](LICENSE)

---

**Status**: Em desenvolvimento ativo
