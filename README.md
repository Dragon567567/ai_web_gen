## 介绍
使用生成web应用的代码。

## 技术选项
大模型：智谱AI，理由：不花钱

前端：vue3 + vite + Ant Design X Vue，理由：vue3、vite是本人比较熟悉的技术栈，Ant Design X Vue有专门的客服机器人聊天组件。

后端：Python + FastApi + sqlalchemy + Jwt，理由：Python在AI领域的生态较好，FastApi是Python是现代化、高性能的异步微框架，能够自动生成API文档，功能比Flask多，也没有Django笨重。
sqlalchemy操作数据库灵活便捷。
Jwt是目前流行的登录功能实现方式，支持过期、无状态和可跨域等好处。

## 设计思路
通过提示词让大模型生成代码，生成代码后再让大模型检查代码并改正（响应速度太慢，已经关闭检查）。

优化思路：
1、不断优化提示词，因为：1、目前有时候生成的内容并非是JSON格式；2、还可以进一步提升生成代码的准率。
2、完善工作流。
![img_2.png](img_2.png)

大模型重写用户的问题，通过多模型生成不同代码，再交给多模型打分选出最优，最优代码再进行检查并改正，再部署运行，若是运行成功，直接返回给用户，若是失败，携带报错信息和出错代码让大模型重新生成。

3、记录上下文。此demo并没有记忆大模型与用户对话的上下文。记录上下文，可以让用户作出反馈，例如：评估功能是否完成、代码是否正确、添加新需求。在大模型生成时加入用户的反馈信息，可以让大模型更好生成代码。
上下文较短时，可以把所有上下文喂给大模型。
上下文较长时，可以提取每个对话的摘要。
上下午超长时，可以给对话打分是否保留，再生成摘要。

4、有条件的情况下可以对模型微调和增加RAG。

## 启动
### 前端启动
```shell
cd app/frontend

pnpm install

pnpm run dev
```

### 后端启动
安装Python3.12，把backend目录标记为源代码目录。
![img.png](img.png)


```shell
cd app/backend

pip3 install -r requirements

uvicorn uvicorn main:app --reload # 也可通过Pycharm启动
```

![img_1.png](img_1.png)