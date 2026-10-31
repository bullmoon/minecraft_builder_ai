# AI Workflow — Minecraft Builder

## 1. Team Roles and Responsibilities

The project uses a multi-model AI workflow with human supervision.

### Project Owner — Human

- Defines project goals and requirements.
- Reviews all proposed changes.
- Applies code modifications through VS Code.
- Runs tests and verifies functionality.
- Approves all Git commits and pushes.
- Has final decision-making authority.

### Architect / Orchestrator — ChatGPT

- Maintains the overall project context.
- Analyzes requirements and existing architecture.
- Breaks work into manageable tasks.
- Prepares technical specifications for developers.
- Reviews findings from other AI models.
- Resolves conflicting recommendations.
- Approves the technical direction before implementation.

### Developer — Claude

- Analyzes the assigned task and relevant source files.
- Implements approved changes.
- Provides complete modified files or Git patches.
- Explains implementation decisions.
- Does not independently modify the GitHub repository.

### Reviewer / QA — Google Antigravity

- Independently reviews source code and proposed changes.
- Identifies defects, edge cases, and architectural weaknesses.
- Reviews test coverage.
- Suggests additional test scenarios.
- Verifies developer recommendations when requested.
- Does not independently modify project files.

## 2. Repository Access and Change Control

- GitHub is the single source of truth for project files.
- All AI models operate in read-only mode with respect to the repository.
- No AI model is authorized to commit, push, or independently merge changes.
- All source-code modifications are performed manually by the Project Owner through VS Code.
- All accepted changes must be tested before being committed.

## 3. Task Execution Workflow

1. Project Owner defines a task.
2. Architect analyzes the task and prepares a technical specification.
3. Reviewer may independently verify requirements and identify potential risks.
4. Developer implements the approved specification.
5. Project Owner applies the proposed changes locally.
6. Project Owner runs automated tests.
7. Reviewer examines the implementation and test results.
8. Architect evaluates review findings and determines whether further changes are required.
9. Project Owner approves and commits the final implementation.

## 4. General Principles

- One task should have one clearly defined objective.
- No implementation without an agreed specification.
- Independent review is required for significant changes.
- All important architectural decisions must be documented.
- Existing functionality must not be unintentionally broken.
- No unnecessary refactoring during bug-fix tasks.
- Project documentation must reflect the actual implementation.
- The Project Owner has final authority over all changes.
