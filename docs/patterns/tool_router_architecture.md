# Tool Router Architecture

A tool router maps user intent to the proper tool or action. It performs a critical role in agentic systems by keeping routing logic separate from business logic.

## Good design characteristics

- fast intent matching
- clean fallback behavior
- explicit tool descriptions
- readable dispatch rules

## Example

If a user asks to look up a document, route to a search tool. If the user asks for a sum, route to a calculator. If no tool matches, respond gracefully with a fallback.
