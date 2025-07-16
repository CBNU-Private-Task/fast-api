# FastAPI AI Code Generation Server

A FastAPI backend server that bridges VS Code extensions with the Ollama LLM API to provide AI-powered JavaScript code generation. This server acts as a proxy and code processor, handling requests from VS Code extensions and delivering clean, executable JavaScript code.

## 🚀 Overview

This FastAPI server is designed to work seamlessly with VS Code extensions, providing:
- AI-powered JavaScript code generation via Ollama LLM
- Real-time communication with VS Code extensions
- Code cleaning and formatting
- Dynamic port management for VS Code integration
- Health monitoring and connection testing

## ��️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   VS Code       │    │  Local FastAPI   │    │  Ollama API     │
│   Extensions    │    │  Server          │    │ (ksga.info)     │
│                 │◄──►│  (Port: 8000)    │───►│                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
   File Operations         API Proxy               AI Processing
   Command Execution       Code Cleaning           LLM Generation
```

## 🔑 Key Features

- **Real-time AI Integration**: Direct connection to Ollama LLM for code generation
- **Multi-Extension Architecture**: Separate extensions for different functionalities
- **Dynamic Configuration**: Auto-port detection and configuration management
- **Cross-Platform Support**: Works on Windows, macOS, and Linux
- **Developer-Friendly**: Easy setup and debugging capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both extensions
5. Submit a pull request

## 📝 License

MIT License - see individual extension directories for specific license information.

## 🐛 Troubleshooting

### Common Issues

1. **FastAPI server not starting**: Check if port 8000 is available
2. **Extension not loading**: Ensure all dependencies are installed via `npm install`
3. **AI generation not working**: Verify FastAPI server is running and accessible
4. **File writing issues**: Check VS Code workspace permissions

### Debug Mode

Both extensions can be run in debug mode:
1. Open the extension directory in VS Code
2. Press `F5` to launch Extension Development Host
3. Test functionality in the new VS Code window

## 📞 Support

For issues and questions:
- Check the individual extension README files
- Review the FastAPI server logs
- Ensure all dependencies are properly installed

---

**Developed by:** rotanakkosal  
**Repository:** [CBNU Private Task](https://github.com/CBNU-Private-Task)
```
