---
name: coding-rules
description: Context and preferences for programming sessions.
---
# Programming Philosophy

## Naming: descriptive but concise

Variable and function names should be as descriptive as possible without
becoming long. Prioritize readability over exhaustiveness.

## Readability over abstraction

Write clean code and look for opportunities to improve it, but if an
abstraction or refactor adds complexity at the cost of readability or
scalability, drop it. When in doubt, the option that is easier to read wins.

## Single responsibility

Each algorithm should solve one task. If a piece of logic can work in isolation
by receiving its data as parameters, extract it into a function.

Exceptions: if that logic won't be reused elsewhere and isn't particularly
long, leave it inline. In that case, precede it with a short comment acting as
a section title.

## Type declarations

Type your variables and add type validation whenever the language allows it.

Skip it when: it would limit the flexibility the task requires, it would make
the code disproportionately longer or more complicated, or the task is simple
enough that typing adds nothing.

## Language: English

Name variables and functions in English.

When working on legacy code written in Spanish, keep the original names of
what already exists. When extending it, keep the part that references the
original element in Spanish and write the new part in English, so the
connection isn't lost. Example: if `calcularNomina` exists, a derived function
would be `calcularNominaWithRetry`, not `calculatePayrollWithRetry`.

