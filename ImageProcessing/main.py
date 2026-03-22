import gradio as gr
from Services.ImageProcessingService import ImageProcessingService

PROCESSING_METHODS = {
    "To Grayscale": ImageProcessingService.to_grayscale,
    "Extract Details": None,
    "Detect Objects": None
}

def process_image(image_input, processing_type):
    if image_input is None:
        confirmation_text = f"Error: You did not upload any image..."
        return None, confirmation_text
    try:
        processing_method = PROCESSING_METHODS[processing_type]
    except:
        confirmation_text = f"Error: Method '{processing_type}' does not exist..."
        return None, confirmation_text
    
    try:
        image_output = processing_method(image_input)
    except:
        confirmation_text = f"Error: Method '{processing_type}' is not working..."
        return None, confirmation_text
    
    confirmation_text = f"Success: Processing '{processing_type}' is completed!"
    return image_output, confirmation_text
    

with gr.Blocks(title="Birds Viewer") as demo:
    gr.Markdown("## Image Processing")
    
    with gr.Row():        
        with gr.Column():
            
            radio_processing_type = gr.Radio(
                choices=["To Grayscale", "Extract details"],
                label="Processing Type",
                value="To Grayscale"
            )
            
            btn_process = gr.Button("Convert", variant="primary")
            
            
            info_box = gr.Textbox(label="Processing Result:", interactive=False)
            
        with gr.Column():
            image_input = gr.Image(
                label="Upload an Image",
                type="numpy",
                sources=["upload", "webcam", "clipboard"],
                height=500
            )
            
        with gr.Column():
            image_output = gr.Image(label="Preview", height=500)

    btn_process.click(
        fn=process_image,
        inputs=[image_input, radio_processing_type],
        outputs=[image_output, info_box]
    )

demo.launch()