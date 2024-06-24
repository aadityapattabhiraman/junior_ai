from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import load_dataset
import os 
import torch  
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from melo.api import TTS
import gc
from rag import rag


def hey(aud, gender):
    torch.cuda.empty_cache()
    gc.collect()
    torch.cuda.empty_cache()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-large-v3"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True,
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=64,
        chunk_length_s=32,
        batch_size=16,
        torch_dtype=torch_dtype,
        device=device,
    )

    result = pipe(aud,generate_kwargs={"task": "translate"})
    torch.cuda.empty_cache()
    gc.collect()
    torch.cuda.empty_cache()
    text = rag(result["text"])
    # print(text1)
    torch.cuda.empty_cache()
    gc.collect()
    torch.cuda.empty_cache()

    ckpt_converter = 'openvoice/checkpoints_v2/converter'
    device = "cpu"#"cuda:0" if torch.cuda.is_available() else "cpu"

    tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
    tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

    if gender == "Male":
        reference_speaker = 'untitled.mp3'

    elif gender == "Female":
        reference_speaker = '/home/akugyo/GitHub/personal/AUD-20240531-WA0069.m4a'

    target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=False)

    text = text  # The newest English base speaker model

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