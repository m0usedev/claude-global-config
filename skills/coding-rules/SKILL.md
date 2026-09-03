---
name: coding-rules
description: Context and preferences for programming sessions.
---

# Programming Philosophy

## Language: English

Name variables and functions in English.

When working on legacy code written in Spanish, keep the original names of whatever already exists. When extending it, keep in Spanish the part that refers to the original element and write the new part in English, so the connection isn't lost. Example: if `calcularNomina` exists, a derived function would be `calcularNominaWithRetry`, not `calculatePayrollWithRetry`.

## Naming: descriptive but concise

Variable and function names should be as descriptive as possible without becoming long. Prioritize readability over exhaustiveness.

## Readability over abstraction

Write clean code and look for opportunities to improve it, but if an abstraction or refactor adds complexity at the cost of readability or scalability, drop it. When in doubt, the easier option to read wins. You can also show me the options and I'll decide.

## Single responsibility

Each algorithm should solve a single task. If a piece of logic can work in isolation receiving its data as parameters, extract it into a function.

Exceptions: if that logic isn't going to be reused anywhere else and isn't particularly long, leave it inline. In that case, precede it with a short comment that acts as a section title.

## Comments in the code

Every function carries a comment explaining its purpose. The depth depends on the complexity of the function: one line if it's simple, more detail if it deserves it. The comment must add something the name and the signature don't already say; if it just repeats the name, it's redundant.

When a function has several segments and it isn't clear on its own what each one does, precede each segment with a short comment that serves as a title and lets you follow the flow.

When a part of the code —a function or an algorithm— is more complex or more specialized than the rest, add an explanatory comment before it for maintenance purposes.

## Type declarations

Type your variables and add type validation whenever the language allows it.

Skip it when: it would limit the flexibility the task requires, it would make the code disproportionately longer or more complicated, or the task is simple enough that typing adds nothing.

## Sequence orchestration

Functions should have a single responsibility: do one specific thing, with the option of returning a response.

When a sequence of functions has to be executed, that sequence lives inside an orchestrating function that keeps control: it calls each function in order and passes the data between them if necessary.

What must not be done is chaining: having a function call the next one in the sequence from inside itself, and that one call the next, and so on. Chaining breaks single responsibility, abstraction and control over the code, and makes it harder to scale or modify the sequence in the future.

```js
// ❌ Chained: each function drags in the next one
function validateOrder(order) {
  const validated = /* ... */;
  return enrichOrder(validated); // it no longer just validates
}

// ✅ Orchestrated: the sequence and the control live in one place
function processOrder(order) {
  const validated = validateOrder(order);
  const enriched = enrichOrder(validated);
  return persistOrder(enriched);
}
```

## Error handling

A single-responsibility function detects the error, but doesn't decide what to do with it. If it can't fulfill its contract, it throws. The one who catches and decides is the orchestrating function, because it's the only one with a view of the whole sequence.

Don't use empty return values (`null`, `false`, `-1`, an empty array) to signal a failure: they force you to check the result at every step and drag that check through the whole execution, with the same problem as prop drilling. Reserve `null` for "there is no data" when the absence is a legitimate outcome, not an error.

Throw your own error types when the orchestrator has to distinguish the cause in order to act differently. If it doesn't have to distinguish, a generic error with a clear message is enough.

The orchestrator wraps the sequence, not each call. One `try` per step brings back the very problem you were trying to avoid.

Never catch in order to silence. An empty `catch` turns a failure into odd behavior with no trace: either the error is resolved there, or it's logged, or it's rethrown.

**Exception — explicit result**: when the failure isn't exceptional but an expected outcome of the flow (form validation, a resource that may not exist), return an object with the result and the reason, and treat it as data, not as an exception. The rule: what's predictable is returned, what's exceptional is thrown.

```js
function processOrder(order) {
  try {
    const validated = validateOrder(order);   // throws if the order is invalid
    const enriched = enrichOrder(validated);
    return persistOrder(enriched);
  } catch (error) {
    if (error instanceof ValidationError) return rejectOrder(order, error);
    throw error; // I don't know what to do with this: let it bubble up
  }
}
```

## Prop drilling

This is when we make a value, variable or property travel across different functions, one inside another. It happens for two reasons:

1. They are chained executions that use or work on that data as it passes through them.
2. It's a piece of data that starts at one point of the execution and travels through it, but is only useful in one specific function further along, not in the sequence as a whole.

In these cases the data must be lifted to a higher level that belongs to the sequence as a whole: a property of the class where those functions live, or —in environments like React or Angular— a context or service that shares the value among them. In short, centralize the data so that those who really need it can access it, and avoid dragging it around.

A case like this is usually a badly distributed sequence of functions; in that case review [Sequence orchestration](#sequence-orchestration).

## Classes

Before creating a class, check that it's actually needed. If the language allows exporting standalone functions, a function that shares neither topic nor data with others doesn't need a class wrapping it: declare it in its own module and export it from there. A class with a single static method and no properties is a folder disguised as an object.

Group those functions by topic, not by leftovers: `dateFormatting`, `currency`, `fileNaming`. A generic `utils` ends up being the drawer where everything you don't know where to put goes, and stops saying anything about what it contains.

### When to create a class

Create a class when a set of properties and/or functions are related to each other and together represent a common concept. The link can come from three places:

- **Properties**: several pieces of data that belong to the same entity and are used across several functions. Example: name and age are data of the same person and represent something, a person.
- **Functions**: several functions that solve small parts of a bigger problem. Example: one reads a document's fields and another fills them in; both are "working with documents".
- **Both**: related properties that feed those functions. Example: the list of a document's fields, the function that retrieves it and the one that uses it to fill them in.

### Properties

- **Class properties**: the same data across all instances of the class, regardless of whether it changes or not.
- **Instance properties**: they only make sense within an individual instance and their value must not be shared between instances of the same class.

#### When should a function parameter become a class or instance property?

When a parameter meets these points:

1. That parameter can originate and makes sense in the construction of an instance of the class.
2. It makes sense as a property of the class, and not as an external value passed to its functions.
3. Turning it from a parameter into a property doesn't break single responsibility, abstraction, or the purpose contract of the class or of the affected functions.

### Functions

- **Class functions**: when we need to work with class properties.
- **Instance functions**: when we need to work with instance properties. From them we can access class properties, but they still depend on an instance.

### Visibility

Always start with the most restrictive visibility and open it up only when something outside genuinely needs it.

- **Private**: the property or function is only useful inside the class or instance itself; neither from outside nor from child classes. Example: a helper method that normalizes a field's format before saving it, or an internal result cache.
- **Protected**: same as private, but inheriting classes need them too. Example: in a base `Repository` class, a `buildQuery` that each child repository reuses or overrides, but that nobody calls from outside.
- **Public**: they form the class's contract, what others use of it. Example: `save()` or `getFields()`, the entry points through which the class is worked with from outside.