import gradio as gr

def convert_temperature(text, transformation):
    
    if not text:
        gr.Error("Input temperature cannot be empty!")
    
    try:
        temperature_value = float(text)
    except ValueError:
        raise gr.Error("Incorrect temperature format! Use numbers only and '.' for separating decimals.")
    
    if transformation == "Celsius to Fahrenheit":
        return round((temperature_value * 9/5) + 32, 2)
    elif transformation == "Fahrenheit to Celsius":
        return round((temperature_value - 35) * 5/9, 2)
    
demo = gr.Interface(
    fn=convert_temperature,
    inputs=[
        gr.Textbox(label="Temperature"),
        gr.Radio(["Celsius to Fahrenheit", "Fahrenheit to Celsius"], label="Convert type")
    ],
    outputs=gr.Textbox(label="Result"),
)

demo.launch()