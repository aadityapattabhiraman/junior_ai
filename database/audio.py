import os 
import torch  
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS


ckpt_converter = 'openvoice/checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

reference_speaker = '/home/akugyo/GitHub/personal/AUD-20240531-WA0069.m4a' # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

text = "Did you ever hear a folk tale about a giant turtle?"  # The newest English base speaker model

src_path = "tmp.wav"
speed = 1.0

model = TTS(language="EN", device=device)
speaker_ids = model.hps.data.spk2id

source_se = torch.load(f'openvoice/checkpoints_v2/base_speakers/ses/en-india.pth', map_location=device)
model.tts_to_file(text, speaker_ids['EN_INDIA'], "tmp.wav", speed=speed)

encode_message = "@MyShell"
tone_color_converter.convert(
    audio_src_path=src_path, 
    src_se=source_se, 
    tgt_se=target_se, 
    output_path="audio.wav",
    message=encode_message)