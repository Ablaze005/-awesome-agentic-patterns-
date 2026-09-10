# Workflow Design Principles

## Keep workflows explicit

State machines and orchestrators work best when each step has a clear purpose. Avoid mixing planning, execution, and post-processing in a single block of code.

## Make failure paths visible

When a tool or step fails, the workflow should surface the error in a way that can be debugged.

## Prefer small, composable actions

Large tasks should be split into small, testable steps. This makes it easier to reason about the system.
