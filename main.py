import gradio as gr
import webbrowser
import argparse
import sys
sys.path.append('./')
from parse import Parse
from src.gradio_demo import SadTalker  

try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--api', action="store_true", default=False)
    parser.add_argument("--share", action="store_true", default=False, help="share gradio app")
    parser.add_argument("--colab", action="store_true", default=False, help="share gradio app")
    args = parser.parse_args()
    ps = Parse()
    sad_talker = SadTalker('checkpoints', 'src/config', lazy_load=True)

    with gr.Blocks() as app:
        gr.Markdown(
            "# <center> chat with Anime characters\n"
            "### <center> base on chatglm/vits/sadtalker\n"
        )
        with gr.Row().style(equal_height=False):
            with gr.Column():
                textbox = gr.TextArea(label="对话内容",
                                        placeholder="Type your sentence here",
                                        value="你好！", elem_id=f"tts-input")
                with gr.Row():
                    with gr.Column():
                        max_length = gr.Slider(label="max length", minimum=0, maximum=4096, value=2048, step=1.0, interactive=True)
                        top_p = gr.Slider(label="top p", minimum=0, maximum=1, value=0.7, step=0.01, interactive=True)
                        temperature = gr.Slider(label="temperature", minimum=0, maximum=1, value=0.95, step=0.01, interactive=True)
                    with gr.Column():
                        ns = gr.Slider(label="emotion change", minimum=0.1, maximum=1.0, step=0.1, value=0.6, interactive=True)
                        nsw = gr.Slider(label="noise_scale", minimum=0.1, maximum=1.0, step=0.1, value=0.668, interactive=True)
                        ls = gr.Slider(label="language speed", minimum=0.1, maximum=2.0, step=0.1, value=1.2, interactive=True)
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = gr.Image(label="Source image", source="upload", type="filepath", elem_id="img2img_image").style(width=512)

                        
                # with gr.Tabs(elem_id="sadtalker_driven_audio"):
                #     with gr.TabItem('Upload OR TTS'):
                #         with gr.Column(variant='panel'):
                #             # driven_audio = gr.Audio(label="Input audio", source="upload", type="filepath")
                #             # driven_audio = ps.audio_path
                #             driven_audio = './0.wav'
                #             print(     123123   )
                #             print(driven_audio)
                #         if sys.platform != 'win32' and not in_webui:
                #             from src.utils.text2speech import TTSTalker
                #             tts_talker = TTSTalker()
                #             with gr.Column(variant='panel'):
                #                 input_text = gr.Textbox(label="Generating audio from text", lines=5, placeholder="please enter some text here, we genreate the audio from text using @Coqui.ai TTS.")
                #                 tts = gr.Button('Generate audio',elem_id="sadtalker_audio_generate", variant='primary')
                #                 tts.click(fn=tts_talker.test, inputs=[input_text], outputs=[driven_audio])
            with gr.Column():
                text_output = gr.Textbox(label="回复信息")
                audio_output = gr.Audio(label="音频信息", elem_id="tts-audio")
                generate = gr.Button("生成对话")
                upload = gr.UploadButton('读取聊天记录', file_types=['file'])
                logdown = gr.Button("记录当前聊天记录")
                upload.upload(ps.loadHistory, inputs=[upload])
                logdown.click(ps.logContent)
                generate.click(ps.PipeChat,
                            inputs=[textbox, max_length, top_p, temperature, ns, nsw, ls],
                            outputs=[text_output, audio_output])
            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('Settings'):
                        gr.Markdown("need help? please visit our [[best practice page](https://github.com/OpenTalker/SadTalker/blob/main/docs/best_practice.md)] for more detials")
                        with gr.Column(variant='panel'):
                            # width = gr.Slider(minimum=64, elem_id="img2img_width", maximum=2048, step=8, label="Manually Crop Width", value=512) # img2img_width
                            # height = gr.Slider(minimum=64, elem_id="img2img_height", maximum=2048, step=8, label="Manually Crop Height", value=512) # img2img_width
                            with gr.Row():
                                pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="Pose style", value=0) #
                                exp_weight = gr.Slider(minimum=0, maximum=3, step=0.1, label="expression scale", value=1) # 

                            with gr.Row():
                                size_of_image = gr.Radio([256, 512], value=256, label='face model resolution', info="use 256/512 model?") # 
                                preprocess_type = gr.Radio(['crop', 'resize','full', 'extcrop', 'extfull'], value='crop', label='preprocess', info="How to handle input image?")
                            
                            with gr.Row():
                                is_still_mode = gr.Checkbox(label="Still Mode (fewer hand motion, works with preprocess `full`)")
                                batch_size = gr.Slider(label="batch size in generation", step=1, maximum=10, value=2)
                                enhancer = gr.Checkbox(label="GFPGAN as Face enhancer")
                                
                            submit = gr.Button('Generate', elem_id="sadtalker_generate", variant='primary')
                            

                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="Generated video", format="mp4").style(width=256)
    
        submit.click(
                    fn=sad_talker.test, 
                    inputs=[source_image,
                            audio_output,
                            preprocess_type,
                            is_still_mode,
                            enhancer,
                            batch_size,                            
                            size_of_image,
                            pose_style,
                            exp_weight
                            ], 
                    outputs=[gen_video]
                    )        
    webbrowser.open("http://127.0.0.1:7860")
    app.launch(share=args.share)