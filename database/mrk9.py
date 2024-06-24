import gradio as gr
from src.gradio_demo import SadTalker 
from mrk10 import hey
import gc
import torch
from stream import upload_and_stream


checkpoint_path='checkpoints'
config_path='src/config'
sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

def trial(gender, audio):
    hey(audio, gender)
    torch.cuda.empty_cache()
    gc.collect()
    video = sad_talker.test(gender, "audio.wav")
    return upload_and_stream(video)


gender_input = gr.Radio(["Male", "Female"], label="Select Gender", elem_id="gender_input")
audio_input = gr.Audio(label="Upload Audio", type="filepath", elem_id="audio_input")
video_output = gr.Video(label="Generated Video", format="mp4", elem_id="video_output")

interface = gr.Interface(
    fn=trial,
    inputs=[gender_input, audio_input],
    outputs=[video_output],
    title="Intern App",
    description=f"Interface for speech to video"
)

interface.launch()
