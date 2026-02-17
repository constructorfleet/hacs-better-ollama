# Better Ollama

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

<!--
Uncomment and customize these badges if you want to use them:

[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]
[![Discord][discord-shield]][discord]
-->

**✨ Develop in the cloud:** Want to contribute or customize this integration? Open it directly in GitHub Codespaces - no local setup required!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/constructorfleet/hacs-better-ollama?quickstart=1)

## ✨ Features

- **Easy Setup**: Simple configuration through the UI - no YAML required
- **Multiple Agents**: Create conversation and AI task agents with different models
- **Vision Support**: Use multimodal models (LLaVA, Moondream) to process images 📷
- **Streaming Responses**: Real-time conversation streaming for immediate feedback
- **Tool Integration**: Connect with Home Assistant services and entities
- **Conversation History**: Configurable message history for context retention
- **Smart Control**: Adjust context window, keep-alive, and other model parameters
- **Think Mode**: Enable reasoning traces for supported models
- **Reconfigurable**: Change models and settings anytime without removing the integration
- **Options Flow**: Adjust settings like context window and history after setup

**This integration will set up the following platforms.**

Platform | Description
-- | --
`conversation` | AI conversation agents with streaming support
`ai_task` | Structured data generation with vision support

## 🚀 Quick Start

### Step 1: Install the Integration

**Prerequisites:** This integration requires [HACS](https://hacs.xyz/) (Home Assistant Community Store) to be installed.

Click the button below to open the integration directly in HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=constructorfleet&repository=hacs-better-ollama&category=integration)

Then:

1. Click "Download" to install the integration
2. **Restart Home Assistant** (required after installation)

> **Note:** The My Home Assistant redirect will first take you to a landing page. Click the button there to open your Home Assistant instance.

<details>
<summary>**Manual Installation (Advanced)**</summary>

If you prefer not to use HACS:

1. Download the `custom_components/ollama/` folder from this repository
2. Copy it to your Home Assistant's `custom_components/` directory
3. Restart Home Assistant

</details>

### Step 2: Add and Configure the Integration

**Important:** You must have installed the integration first (see Step 1) and restarted Home Assistant!

#### Option 1: One-Click Setup (Quick)

Click the button below to open the configuration dialog:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=ollama)

Follow the setup wizard:

1. Enter your Ollama server URL (e.g., `http://localhost:11434`)
2. Click Submit
3. Add conversation or AI task agents
4. Select a model (📷 indicates vision-capable models like LLaVA)
5. Configure optional settings

That's it! The integration will start and you can use your Ollama models in Home Assistant.

#### Option 2: Manual Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for "Ollama"
4. Follow the same setup steps as Option 1

### Step 3: Adjust Settings (Optional)

After setup, you can adjust options for each agent:

1. Go to **Settings** → **Devices & Services**
2. Find **Ollama**
3. Click on an agent device
4. Click **Configure** to adjust:
   - Context window size (num_ctx)
   - Conversation history length
   - Keep-alive timeout
   - Think mode (for reasoning traces)

You can also **Reconfigure** to change the model without removing the agent.

### Step 4: Start Using!

#### Conversation Agents

Use conversation agents through Home Assistant's Assist:

1. Go to **Settings** → Voice Assistants → **Assist**
2. Select your Ollama conversation agent
3. Start chatting!

For vision models (marked with 📷), you can send images through supported interfaces.

#### AI Task Agents

Use AI task agents in automations and scripts:

```yaml
action: ai_task.generate_data
target:
  entity_id: ai_task.ollama_task
data:
  task: "Extract the vendor and total from this receipt"
  attachments:
    - /local/receipt.jpg
  structure:
    type: object
    properties:
      vendor:
        type: string
      total:
        type: number
```

See [docs/user/VISION.md](docs/user/VISION.md) for detailed vision model usage and examples.

## Available Agent Types

### Conversation Agents

Conversation agents provide interactive chat experiences with:
- Streaming responses for real-time feedback
- Conversation history retention
- Tool/service integration (when configured with LLM Home Assistant API)
- Vision support for image understanding (with vision models)

### AI Task Agents

AI Task agents generate structured data from natural language:
- Extract specific data with JSON schemas
- Process images for OCR and analysis
- Generate formatted responses for automations
- Support complex data structures

## Vision Models 📷

Vision-capable models can process and understand images. Use them for:
- Image description and captioning
- Visual question answering
- OCR (text extraction from images)
- Scene understanding and object detection

**Supported vision models:**
- llava (general purpose)
- llava-llama3 (improved reasoning)
- llava-phi3 (efficient, smaller)
- bakllava (alternative)
- minicpm-v (compact)
- moondream (lightweight)

See [docs/user/VISION.md](docs/user/VISION.md) for detailed vision usage guide.

## Custom Services

The integration provides services for advanced automation:

### `ai_task.generate_data`

Generate structured data from natural language or images.

**Example:**

```yaml
action: ai_task.generate_data
target:
  entity_id: ai_task.ollama_task
data:
  task: "What's in this image?"
  attachments:
    - /local/photo.jpg
```

### Configuration Entry Management

Standard Home Assistant config entry services are available for managing agents.

Use these services in automations or scripts for more control.

## Configuration Options

### During Setup

Name | Required | Description
-- | -- | --
Ollama URL | Yes | URL of your Ollama server (e.g., http://localhost:11434)

### After Setup (Options)

You can change these anytime by clicking **Configure** on an agent:

Name | Default | Description
-- | -- | --
Model | - | The Ollama model to use (📷 indicates vision support)
Context Window | 8192 | Size of the context window (num_ctx)
History Length | 20 | Number of conversation rounds to retain
Keep Alive | -1 | How long to keep model in memory (-1 = forever)
Think Mode | Off | Enable reasoning traces (supported models only)
Prompt Template | - | Custom system prompt (conversation agents only)

## Troubleshooting

### Connection Issues

If setup fails or agents become unavailable:

1. Verify the Ollama server URL is correct and reachable
2. Ensure Ollama is running (`ollama serve`)
3. Check that the model is downloaded (`ollama list`)
4. Review Home Assistant logs for error messages

### Models Not Showing

If models don't appear in the dropdown:

1. Verify Ollama server is running and accessible
2. Check that models are downloaded (`ollama list`)
3. Try manually entering a model name if auto-detection fails

### Vision Not Working

If vision models don't process images:

1. Ensure you're using a vision-capable model (marked with 📷)
2. Verify image format is supported (JPEG, PNG, WebP, GIF)
3. Check image file size is under 20MB
4. See [docs/user/VISION.md](docs/user/VISION.md) for detailed troubleshooting

### Debug Logging

Enable debug logging to troubleshoot issues:

```yaml
logger:
  default: warning
  logs:
    custom_components.ollama: debug
```

Add this to `configuration.yaml`, restart, and reproduce the issue. Check logs for detailed information.

## Next Steps

- See [docs/user/VISION.md](docs/user/VISION.md) for vision model usage
- See [docs/user/CONFIGURATION.md](docs/user/CONFIGURATION.md) for detailed configuration
- Report issues at [GitHub Issues](https://github.com/constructorfleet/hacs-better-ollama/issues)

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request if you have suggestions or improvements.

### 🛠️ Development Setup

Want to contribute or customize this integration? You have two options:

#### Cloud Development (Recommended)

The easiest way to get started - develop directly in your browser with GitHub Codespaces:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/constructorfleet/hacs-better-ollama?quickstart=1)

- ✅ Zero local setup required
- ✅ Pre-configured development environment
- ✅ Home Assistant included for testing
- ✅ 60 hours/month free for personal accounts

#### Local Development

Prefer working on your machine? You'll need:

- Docker Desktop
- VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

Then:

1. Clone this repository
2. Open in VS Code
3. Click "Reopen in Container" when prompted

Both options give you the same fully-configured development environment with Home Assistant, Python 3.13, and all necessary tools.

---

## 🤖 AI-Assisted Development

> **ℹ️ Transparency Notice**
>
> This integration was developed with assistance from AI coding agents (GitHub Copilot, Claude, and others). While the codebase follows Home Assistant Core standards, AI-generated code may not be reviewed or tested to the same extent as manually written code.
>
> AI tools were used to:
>
> - Generate boilerplate code following Home Assistant patterns
> - Implement standard integration features (config flow, coordinator, entities)
> - Ensure code quality and type safety
> - Write documentation and comments
>
> Please be aware that AI-assisted development may result in unexpected behavior or edge cases that haven't been thoroughly tested. If you encounter any issues, please [open an issue](../../issues) on GitHub.
>
> *Note: This section can be removed or modified if AI assistance was not used in your integration's development.*

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [@constructorfleet][user_profile]**

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/constructorfleet/hacs-better-ollama.svg?style=for-the-badge
[commits]: https://github.com/constructorfleet/hacs-better-ollama/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/constructorfleet/hacs-better-ollama.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40constructorfleet-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/constructorfleet/hacs-better-ollama.svg?style=for-the-badge
[releases]: https://github.com/constructorfleet/hacs-better-ollama/releases
[user_profile]: https://github.com/jpawlowski

<!-- Optional badge definitions - uncomment if needed:
[buymecoffee]: https://www.buymeacoffee.com/jpawlowski
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
-->
