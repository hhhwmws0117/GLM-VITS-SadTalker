# ChatGLM + VITS + SadTalker

## base on chatGLM-6B-int4/vits/SadTalker

### 本项目开源，严禁商用

- 本项目基于清华大学开源模型chatGLM-6B以及vits/Sadtalker

  -灵感来源：https://huggingface.co/spaces/JavaFXpert/Chat-GPT-LangChain

  - chatGLM-6B模型为清华大学开源，使用时请注意查看对应的使用需知，严格遵守使用规定

    - 模型下载链接 [点击这里](https://huggingface.co/THUDM) 请仔细阅读说明根据自己的硬件配置下载对应模型
    - 模型下载后请将模型及响应的文件放置在./chatglm-model路径下
    - 参数下载方式可参考[这里](https://space.bilibili.com/3493270982232856)的视频

  - vits模型来自up主“saya睡大觉中”，严禁商用
    - 下载后请将模型以及配置文件放在./model-vits路径下
    - 内部含有多种模型，可根据自己的需求进行选择 选择参数在soundmaker.py中的self.speaker_choice中进行修改

- 自行部署项目时，使用下面命令以安装模块，注意：pip安装的torch可能为cpu版本，请按照torch官网的安装方式安装对应的cuda版本，如果出现模块兼容性问题，请使用python3.9.6
  
  pip install -r requirements.txt

- 运行项目时，使用 
  python main.py 即可运行

在运行main文件后,按顺序，填写问题，提供人物图片，生成对话，生成对话视频

主要程序和模型参数打包在如下的网盘链接中：

包含所有模型参数，文件较大，后续抽时间传到huggingface

参考：

[1]https://github.com/ruoqiu6/chat-with-Elysia2.0.git

[2]https://github.com/THUDM/ChatGLM-6B

[3]https://github.com/datawhalechina/prompt-engineering-for-developers

[4]https://github.com/imClumsyPanda/langchain-ChatGLM

[5]https://github.com/OpenTalker/SadTalker  

[6]https://huggingface.co/spaces/zomehwh/vits-uma-genshin-honkai
