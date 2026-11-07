# AgentCore

A local-first computer operator for Windows.

AgentCore lets you interact with your computer using simple, natural language commands. It can find files, open folders, read files, launch applications, and search the web.

## Features

- 🔍 Fast file and folder search using a local index
- ⚡ Live file watching for common user folders
- 📂 Open files and folders
- 📖 Read text-based files directly in the terminal
- 💻 Open files and folders in VS Code
- 🚀 Find and launch installed applications
- 🌐 Search the web using your preferred browser
- 🗣️ Simple natural language commands

## Examples

```text
Find mypanpic
Open mypanpic
Read main.py
Open agentcore in VS Code
Open Chrome
Open Chrome and search for committ.in
```

## Installation

### Clone the repository

```bash
git clone https://github.com/kkj4u2t7/agentcore.git
cd agentcore
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run AgentCore

```bash
python main.py
```

## How It Works

AgentCore uses a local file index to make searching faster than scanning your entire computer every time.

```text
Your instruction
      ↓
Command interpretation
      ↓
File / App / Browser routing
      ↓
Local computer action
```

The file watcher keeps the index updated when files are added or changed in watched locations.

## Project Structure

```text
agentcore/
├── tools/          # Computer interaction tools
├── agent/          # Agent runtime components
├── tests/          # Tests
├── data/           # Local data, not committed to Git
├── main.py         # Application entry point
└── requirements.txt
```

## Roadmap

- [x] Fast indexed file search
- [x] Live file watching
- [x] Open files and folders
- [x] Read files from the terminal
- [x] Launch installed applications
- [x] Browser web search
- [ ] More natural language commands
- [ ] Command history
- [ ] Safer action confirmation
- [ ] Cross-platform support
- [ ] AI-powered command understanding

## Contributing

Contributions, ideas, and bug reports are welcome.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a Pull Request

## License

This project is licensed under the MIT License.

## Author

Created and maintained by **Avinash**.