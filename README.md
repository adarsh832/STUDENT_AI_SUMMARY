# CodeBuddy - Your Computer Engineering Study Assistant 🤖

CodeBuddy is an AI-powered study assistant specifically designed for computer engineering students. It helps you understand complex concepts, analyze study materials, and improve your programming skills.

## Features 🌟

- **Interactive Chat Interface**: Ask questions and get detailed explanations
- **File Analysis**: Upload and analyze PDFs and PowerPoint presentations
- **Code Help**: Get programming assistance with explanations
- **Note Taking**: Save your study sessions for later review
- **Smart Context**: Maintains conversation context for better assistance
- **User-Friendly**: Modern, intuitive dark-themed interface

## Installation 🔧

### Prerequisites

Make sure you have Python 3.8+ installed on your system. You can download it from [python.org](https://python.org)

### Required Packages

Install the required packages using pip: 
```bash
pip install customtkinter
pip install PyPDF2
pip install python-pptx
pip install ollama
```

### Installing Ollama

1. Visit [ollama.ai](https://ollama.ai) and download the appropriate version for your system
2. Install Ollama following the website instructions
3. Pull the required model:
```bash
ollama pull llama3.2
```

## Getting Started 🚀

1. Clone or download this repository
2. Navigate to the project directory
3. Run the application:
```bash
python gui.py
```

## How to Use 📚

### Basic Usage

1. **Ask Questions**: Type your question in the input field and press Enter or click "Send"
2. **Upload Files**: Click "Upload File" to analyze PDFs or PowerPoints
3. **Save Notes**: Click "Save Notes" to save the conversation
4. **Clear Chat**: Click "Clear Chat" to start fresh

### File Support

- PDF Documents (*.pdf)
- PowerPoint Presentations (*.pptx, *.ppt)

### Example Questions

- "Explain how binary search trees work"
- "Help me debug this Python code..."
- "What are the key concepts in computer networking?"
- "Can you explain the time complexity of quicksort?"

## Features in Detail 🔍

### Chat Interface
- Modern dark theme for reduced eye strain
- Clear message separation with timestamps
- Code block formatting with syntax highlighting
- Emoji support for better readability

### File Analysis
- Extracts text from PDFs and PowerPoints
- Generates summaries of uploaded materials
- Allows follow-up questions about the content
- Maintains context for better responses

### Note Taking
- Save conversations with timestamps
- Structured format for easy review
- Includes study tips and summaries
- Saves files in the 'saved_notes' directory

## Troubleshooting 🔧

Common issues and solutions:

1. **Ollama Connection Error**
   - Make sure Ollama is installed and running
   - Verify the model is properly pulled

2. **File Upload Issues**
   - Check if the file format is supported
   - Ensure the file isn't corrupted
   - Verify file permissions

3. **Display Issues**
   - Update customtkinter package
   - Check Python version compatibility

## Contributing 🤝

Feel free to contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 👏

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Powered by [Ollama](https://ollama.ai)
- Uses [PyPDF2](https://github.com/py-pdf/pypdf) for PDF processing
- Uses [python-pptx](https://python-pptx.readthedocs.io) for PowerPoint processing

## Contact 📧

For support or queries:
- Create an issue in the GitHub repository
- Contact the maintainers directly

---

Made with ❤️ for Computer Engineering Students