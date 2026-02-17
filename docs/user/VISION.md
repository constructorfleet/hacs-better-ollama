# Vision Models and Multimodal Support

Better Ollama supports vision-capable models that can process and understand images alongside text. This enables powerful use cases like image description, visual question answering, OCR (text extraction), and scene understanding.

## Supported Vision Models

The following models include vision capabilities and can process images:

- **llava** - Large Language and Vision Assistant (general purpose)
- **llava-llama3** - LLaVA powered by Llama 3 (improved reasoning)
- **llava-phi3** - LLaVA with Phi-3 (efficient, smaller model)
- **bakllava** - Alternative vision model
- **minicpm-v** - Compact vision model
- **moondream** - Lightweight vision model

Vision models are marked with a 📷 camera emoji in the model selection dropdown during configuration.

## How Vision Models Work

Vision models combine:
- **Vision Encoder**: Processes and understands image content
- **Language Model**: Generates text responses based on the image and your prompt

This allows the model to:
- Describe what's in an image
- Answer questions about images
- Extract text from images (OCR)
- Analyze charts, graphs, and diagrams
- Identify objects, scenes, and actions

## Using Vision Models

### Setup

1. **Install a Vision Model**:
   - Go to **Settings** → **Devices & Services**
   - Click on your Ollama integration
   - Click **Add Entry** to create a new conversation or AI task agent
   - Select a vision model (marked with 📷) from the dropdown
   - If the model isn't downloaded, it will be automatically downloaded from Ollama

2. **Configure the Agent**:
   - For **Conversation** agents: Can use vision in chat interfaces
   - For **AI Task** agents: Can process images in structured data extraction

### In Conversations

When using a conversation agent with a vision model:

1. Start a conversation through Home Assistant's Assist interface
2. Include an image in your message (if supported by the interface)
3. Ask questions about the image:
   - "What do you see in this image?"
   - "Describe this photo"
   - "What text is shown in this screenshot?"

### In AI Tasks

AI Task entities with vision models can process images for structured data extraction:

```yaml
service: ai_task.generate_data
target:
  entity_id: ai_task.ollama_vision_task
data:
  task: "Extract text from image"
  attachments:
    - /local/receipt.jpg
  structure:
    type: object
    properties:
      vendor:
        type: string
      total:
        type: number
      date:
        type: string
```

### In Automations

Use vision models to analyze camera feeds or images:

```yaml
automation:
  - alias: "Analyze Security Camera"
    trigger:
      - trigger: state
        entity_id: binary_sensor.front_door_motion
        to: "on"
    action:
      - action: camera.snapshot
        target:
          entity_id: camera.front_door
        data:
          filename: /tmp/door_snapshot.jpg
      
      - action: ai_task.generate_data
        target:
          entity_id: ai_task.ollama_vision
        data:
          task: "Describe what you see at the front door"
          attachments:
            - /tmp/door_snapshot.jpg
        response_variable: analysis
      
      - action: notify.mobile_app
        data:
          title: "Front Door Activity"
          message: "{{ analysis.data }}"
          data:
            image: /tmp/door_snapshot.jpg
```

## Image Requirements

- **Supported formats**: JPEG, PNG, WebP, GIF
- **Recommended size**: Under 20MB, ideally 1024x1024 pixels or less
- **Best quality**: Higher resolution images work better for OCR and detail recognition
- **Performance**: Larger images take longer to process

## Example Use Cases

### Security & Monitoring
- Analyze security camera footage for unusual activity
- Identify packages delivered to your doorstep
- Monitor elderly family members for falls or emergencies

### Home Automation
- Detect when the garage door is open/closed from camera feed
- Check if lights are on/off in photos
- Verify appliance states

### Document Processing
- Extract text from receipts and invoices
- Read meter displays
- Parse product labels and barcodes

### Smart Notifications
- Generate natural language descriptions of camera events
- Provide context for door camera notifications
- Summarize what happened during an alert

## Tips for Best Results

1. **Clear images**: Use well-lit, focused images for better recognition
2. **Specific prompts**: Ask clear, specific questions about what you want to know
3. **Model selection**: 
   - Use **llava** or **llava-llama3** for general purpose vision tasks
   - Use **moondream** for faster processing on resource-constrained systems
   - Use **bakllava** or **minicpm-v** for alternative perspectives
4. **Context window**: Larger models have better understanding but require more memory
5. **Prompt engineering**: Include relevant context in your prompts for better answers

## Troubleshooting

### Images Not Being Processed

If your vision model isn't processing images:

1. **Check model compatibility**: Ensure you're using a vision model (marked with 📷)
2. **Verify image format**: Use supported formats (JPEG, PNG, WebP, GIF)
3. **Check file size**: Keep images under 20MB
4. **Review logs**: Enable debug logging to see detailed error messages

### Poor Recognition Quality

If the model gives inaccurate responses:

1. **Image quality**: Use higher resolution, well-lit images
2. **Try different models**: Some models work better for specific tasks
3. **Refine prompts**: Be more specific about what you're asking
4. **Model size**: Larger models (13B, 34B parameters) generally perform better than smaller ones (7B)

### Performance Issues

If vision processing is slow:

1. **Use smaller models**: Try **moondream** or **llava:7b** instead of larger variants
2. **Reduce image size**: Resize images to 1024x1024 or smaller before processing
3. **Adjust context window**: Reduce `num_ctx` in model configuration if needed
4. **Hardware**: Vision models benefit from GPU acceleration

## Technical Details

### How Attachments Are Processed

The integration handles image attachments through the Home Assistant conversation system:

1. Images are passed as `Attachment` objects with MIME type and file path
2. The `_convert_content` function converts attachments to Ollama `Image` objects
3. Images are sent to the Ollama API alongside the text prompt
4. The model processes both image and text to generate a response

### Supported in Entity Types

- ✅ **AI Task Entities**: Full support via `SUPPORT_ATTACHMENTS` feature flag
- ✅ **Conversation Entities**: Infrastructure in place, works with vision models

## Further Reading

- [Ollama Vision Models](https://ollama.com/library?q=vision) - Official model library
- [LLaVA Project](https://llava-vl.github.io/) - Research behind LLaVA models
- [Home Assistant AI](https://www.home-assistant.io/docs/assist/) - Assist and conversation features
