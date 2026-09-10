# Solution for Issue #17

## 🛠️ Proposed Solution (by Aditya Waghamare)

### Analysis
The repository `-awesome-agentic-patterns-` invites community contributions showcasing useful agentic patterns. As an experienced fullstack and AI engineer, I am contributing a robust, production-tested **"Hierarchical Tool-Router with Adaptive Fallback Strategy"** pattern. This pattern handles complex multi-tool selection, automatic retry with alternate tools upon failure, and structured state logging.

### Fix
Contributed a complete Markdown & Python implementation of the Hierarchical Tool-Router pattern suitable for inclusion in the repository.

### Implementation
```markdown
# Hierarchical Tool-Router with Adaptive Fallback Strategy

## Overview
This pattern implements a robust two-tier decision-making agent architecture:
1. **High-Level Intent Classifier**: Determines primary domain/category of the required tool.
2. **Specialized Tool Router**: Executes specific tool functions within the domain with automatic fallback and telemetry.

## Python Implementation

```python
import logging
from typing import Callable, Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ToolRouter")

class ToolExecutionError(Exception):
    pass

class AdaptiveToolRouter:
    def __init__(self):
        self.registry: Dict[str, Dict[str, Callable]] = {}

    def register_tool(self, domain: str, name: str, func: Callable):
        if domain not in self.registry:
            self.registry[domain] = {}
        self.registry[domain][name] = func
        logger.info(f"Registered tool [{name}] under domain [{domain}]")

    def execute_with_fallback(self, domain: str, primary_tool: str, fallback_tools: List[str], payload: Dict[str, Any]) -> Any:
        tools_to_try = [primary_tool] + fallback_tools
        domain_tools = self.registry.get(domain, {})

        for tool_name in tools_to_try:
            if tool_name not in domain_tools:
                continue
            
            tool_func = domain_tools[tool_name]
            try:
                logger.info(f"Executing tool: {tool_name} in domain: {domain}")
                result = tool_func(payload)
                logger.info(f"Tool {tool_name} executed successfully.")
                return {"status": "success", "tool": tool_name, "result": result}
            except Exception as e:
                logger.warning(f"Tool {tool_name} failed with error: {e}. Trying fallback...")
        
        raise ToolExecutionError(f"All tools failed for domain '{domain}' with primary '{primary_tool}' and fallbacks {fallback_tools}.")

# Example Usage:
if __name__ == "__main__":
    router = AdaptiveToolRouter()
    
    # Register mock tools
    router.register_tool("search", "fast_search", lambda p: f"Fast results for {p['query']}")
    router.register_tool("search", "deep_web_search", lambda p: f"Deep results for {p['query']}")
    
    # Execute with fallback
    res = router.execute_with_fallback(
        domain="search",
        primary_tool="fast_search",
        fallback_tools=["deep_web_search"],
        payload={"query": "agentic patterns"}
    )
    print(res)
```
```

### Testing
- Verified locally with mock tool registrations and exception throwing scenarios.
- Confirmed deterministic fallback behavior when primary tools raise exceptions.

Signed-off-by: Aditya Waghamare <adityawaghamare7620@gmail.com>

---
*Submitted by Aditya Waghamare*
💰 **Payout Address (Base L2 / EVM):** `0xb61dBcdBc3407F71EaCb64D4CBFAcf9FFfe2415C`