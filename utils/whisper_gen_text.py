import sys
import importlib
importlib.reload(sys)
from faster_whisper import WhisperModel
import datetime
import gradio as gr
import os
import torch
import time
import nltk
from tqdm import tqdm

SENTENCE_SIZE = 512
SAMPLE_RATE = 16000
os.makedirs("output", exist_ok=True)
# 设置环境变量
NLTK_DATA_PATH = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path
os.environ["PATH"] = os.environ["PATH"]+':'+os.path.join(os.path.dirname(__file__), "ffmpeg_release")

os.environ['http_proxy'] = 'http://127.0.0.1:10809'
os.environ['https_proxy'] = 'http://127.0.0.1:10809'

for i in range(10):
    try:
        model = WhisperModel("medium", device="cuda" if torch.cuda.is_available() else "cpu")
        # model = WhisperModel("medium", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="int8_float16")
        print("medium  FasterWhisper模型加载完毕")
        break
    except Exception as e:
        print(e)
        print(f"重新加载medium FasterWhisper模型【网络问题】，次数：{i}")


# 音频或者视频转写为文本
def speech_to_text(video_file_path):
    print("开始转写音频或者视频")
    video_file_path = video_file_path.replace(".wav", ".mp4")
    filename, file_ending = os.path.splitext(f'{video_file_path}')
    new_video_file_path = filename + "_" + time.strftime("%Y%m%d%H%M%S", time.localtime()) + file_ending
    os.rename(video_file_path, new_video_file_path)
    audio_file = new_video_file_path.replace(file_ending, ".wav")
    os.system(f'ffmpeg -i "{new_video_file_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{audio_file}"')

    options = dict(language="zh", beam_size=5, best_of=5)
    transcribe_options = dict(task="transcribe", **options)
    segments_raw, info = model.transcribe(audio_file, **transcribe_options)

    segments = []
    for segment_chunk in tqdm(segments_raw):
        segments.append(segment_chunk.text)

    # 返回文件的前缀和转写后的文本
    return os.path.basename(new_video_file_path).split(".")[0], " ".join(segments)


# 离线视频分析
def offline_video_analyse(video_file_path):
    print("开始分析离线视频")
    # 视频转文本
    file_prefix, transcribe_text = speech_to_text(video_file_path)
    print(f"File prefix: {file_prefix}")
    print(f"Transcribed text: {transcribe_text}")

    # 转写文本保存
    output_txt_path = os.path.join("output",  file_prefix + ".txt")
    with open(output_txt_path, "w", encoding="utf-8") as wf:
        wf.write(transcribe_text)
    return output_txt_path


