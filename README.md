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

### Policy Enforcement
- Content filtering and safety checks
- Configurable forbidden phrases and patterns
- Multi-stage policy validation:
  - Input validation
  - Response validation
  - Post-tool validation
- Constitutional AI principles

### Tool Integration
- Pluggable tool system
- Built-in example tools:
  - Search functionality
  - Wikipedia queries
- Easy addition of new tools
- Tool result incorporation into context

### Performance Features
- Built-in caching system
- Metrics collection and monitoring
- Request tracking middleware
- Async processing pipeline

## 📁 Project Structure

```
my_mcp/
├─ config/                  # Configuration management
│  ├─ settings.py          # Global settings and constants
├─ models/                 # LLM client implementations
│  ├─ base_client.py      # Abstract base class
│  ├─ openai_client.py    # OpenAI integration
│  ├─ ollama_client.py    # Ollama integration
├─ tools/                 # External tool integrations
│  ├─ search_tool.py     # Search functionality
│  ├─ wiki_tool.py       # Wikipedia queries
├─ policies/             # Policy enforcement
│  ├─ policy_checker.py  # Content validation
│  ├─ constitution.txt   # System rules
├─ protocol/            # Core MCP implementation
│  ├─ context.py       # Context management
│  ├─ handler.py       # Main protocol handler
│  ├─ caching.py       # Caching system
│  ├─ metrics.py       # Performance metrics
│  ├─ middleware.py    # Request middleware
└─ main.py             # Application entry point
```

## 🚀 Getting Started

1. **Installation**
```bash
git clone https://github.com/w4ester/MCP_4ester.git
cd MCP_4ester
pip install -r requirements.txt  # Coming soon
```

2. **Configuration**
Edit `config/settings.py` to set up your:
- API keys
- Model preferences
- Policy rules
- Tool configurations

3. **Basic Usage**
```python
from config.settings import MCPSettings
from protocol.context import ContextLayers
from protocol.handler import ModelContextProtocolHandler

# Create context
context = ContextLayers(
    system=["Follow safety guidelines"],
    developer=["Use search for queries"],
    user=["Tell me about AI safety"]
)

# Initialize handler
handler = ModelContextProtocolHandler(
    settings=MCPSettings(),
    tools={"search": search_tool},
    model_clients={"ollama": ollama_client}
)

# Process request
response = await handler.process_request(context)
```

## 🔧 Extending the Framework

### Adding a New Model
1. Create a new class in `models/`
2. Inherit from `ModelClient`
3. Implement the `generate` method
```python
class NewModelClient(ModelClient):
    async def generate(self, prompt: str, **kwargs) -> str:
        # Implementation here
        pass
```

### Adding a New Tool
1. Create a new function in `tools/`
2. Register in the tools dictionary
```python
def new_tool(params: Dict[str, Any]) -> str:
    # Tool implementation
    pass

tools = {
    "new_tool": new_tool,
    # ... other tools
}
```

## 📊 Metrics and Monitoring

The framework provides built-in metrics collection:
- Request counts
- Success/failure rates
- Response latencies
- Tool usage statistics

Access metrics through the `Metrics` class:
```python
metrics = handler.metrics.get_stats()
print(f"Success rate: {metrics['success_rate']}%")
```

## 🔒 Security and Safety

- All requests go through policy validation
- Content filtering at multiple stages
- Constitutional AI principles enforced
- Secure tool execution environment

## 🎯 Future Roadmap

- [ ] Add more model integrations
- [ ] Enhance policy enforcement
- [ ] Add distributed caching
- [ ] Implement rate limiting
- [ ] Add authentication layer
- [ ] Create web API interface
- [ ] Add streaming support
- [ ] Implement conversation memory

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests for any enhancements.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for API patterns
- Ollama for local model support
- The LLM community for insights and best practices