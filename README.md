# Model Context Protocol (MCP) Framework

A flexible and extensible framework for integrating Large Language Models (LLMs) with various tools and services. This framework provides a structured approach to managing context, enforcing policies, and handling interactions between LLMs and external tools.

## 🌟 Features

### Model Integration
- Support for multiple LLM providers (OpenAI, Ollama)
- Abstract base class for easy addition of new model providers
- Async/await pattern for efficient request handling
- Configurable model parameters (temperature, max tokens)

### Context Management
- Three-layer context system:
  - System: Core rules and constraints
  - Developer: Tool integrations and middleware
  - User: Input and conversation history
- Clean separation of concerns
- Flexible prompt building and formatting

[Full content from above...]