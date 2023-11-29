- # 项目名称：llm-universe 大模型应用

  ## 项目简介

  该项目是基于 [llm-universe](https://github.com/datawhalechina/llm-universe) 的作业，通过课程学习大模型的使用和知识库的创建，完成了一个带知识库大模型的项目作业。

  ## 启动项目

  在项目根目录下执行以下命令启动项目：

  ```
  python serve/run_gradio.py
  ```

  ## 优化调整

  根据 [llm-universe](https://github.com/datawhalechina/llm-universe) 下的项目进行了优化和调整，具体包括：

  1. **MP4文件转txt加入知识库**：使用 faster_whisper 进行文字识别，将 MP4 文件中的文字加入知识库。
  2. **图片转txt加入知识库**：调用 https://www.aigcaas.cn/ 的API，通过 PaddleOCR 识别图像中的文字，并将其加入知识库。
  3. **知识库的向量化**：使用 m3e 进行知识库的向量化。
  4. **向量化方法**：采用 chroma 方法进行知识库的向量化。
  5. **修正问题**：修正了使用星火大模型 v2、v3 时，在知识库问答时 domain 和 url 错误的问题。

  ## 截图示例

- ![](.\figures\使用截图.png)

## 项目架构

### 整体架构

本项目是一个基于大模型的个人知识库助手，使用了LangChain框架，核心技术包括LLM API调用、向量数据库、检索问答链等。项目整体架构如下：

![整体架构](.\figures\structure.jpg)

项目代码结构在`project`目录下，包括`llm`、`embedding`、`data`、`database`、`chain`和`serve`等子目录。

### 代码结构

```
diffCopy code-project
    -readme.md 项目说明
    -llm LLM调用封装
        -self_llm.py 自定义 LLM 基类
        -wenxin_llm.py 自定义百度文心 LLM
        -spark_llm.py 自定义讯飞星火 LLM
        -zhipuai_llm.py 自定义智谱AI LLM
        -call_llm.py 将各个 LLM 的原生接口封装在一起
    -embedding embedding调用封装
        -zhipuai_embedding.py 自定义智谱AI embedding
    -data 源数据路径
    -database 数据库层封装
        -create_db.py 处理源数据及初始化数据库封装
    -chain 应用层封装
        -qa_chain.py 封装检索问答链，返回一个检索问答链对象
        -chat_qa_chian.py：封装对话检索链，返回一个对话检索链对象
        -prompt_template.py 存放多个版本的 Template
    -serve 服务层封装
        -run_gradio.py 启动 Gradio 界面
        -api.py 封装 FastAPI
        -run_api.sh 启动 API
```

### 项目逻辑

1. 用户可以通过`run_gradio`或`run_api`启动整个服务。
2. 服务层调用`qa_chain.py`或`chat_qa_chain`实例化检索问答链对象，实现核心功能。
3. 服务层和应用层可以调用切换`prompt_template.py`中的prompt模板。
4. 也可以直接调用`call_llm`中的`get_completion`函数来实现不使用数据库的LLM。
5. 应用层调用已存在的数据库和llm中的自定义LLM来构建检索链。
6. 如果数据库不存在，应用层调用`create_db.py`创建数据库，该脚本可以使用OpenAI Embedding也可以使用`embedding.py`中的自定义embedding。

### 各层简析

#### 1. LLM 层

LLM 层将国内外四种知名 LLM API（OpenAI-ChatGPT、百度文心、讯飞星火、智谱GLM）进行了封装，隐藏了不同 API 的调用差异，实现在同一个对象或函数中通过不同的`model`参数来使用不同来源的LLM。

详细学习每一种LLM的调用方式、封装方式，请阅读教程第二章《调用大模型 API》。

#### 4.2 数据层

数据层主要包括个人知识库的源数据和Embedding对象。源数据需要经过Embedding处理才能进入向量数据库。在数据层，我们自定义了智谱提供的Embedding API的封装，支持上层以统一方式调用智谱Embedding或OpenAI Embedding。

#### 4.3 数据库层

数据库层存放了向量数据库文件。我们在该层实现了源数据处理、创建向量数据库的方法。

详细学习向量数据库的原理、源数据处理方法以及构建向量数据库的具体实现，请阅读教程第四章《数据库搭建》。

#### 4.4 应用层

应用层封装了整个项目的全部核心功能。基于LangChain提供的检索问答链，在LLM层、数据库层的基础上，实现了本项目检索问答链的封装。自定义的检索问答链除了具备基本的检索问答功能外，还支持通过`model`参数来灵活切换使用的LLM。实现了两个检索问答链，分别是有历史记录的`Chat_QA_Chain`和没有历史记录的`QA_Chain`。

详细学习Prompt的构造与检索问答链的构建细节，请阅读教程第五章《Prompt 设计》。

#### 4.5 服务层

服务层是基于应用层的核心功能封装