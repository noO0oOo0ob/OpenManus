# OpenManus UML 图

本目录包含 OpenManus 项目的 UML 图，用于说明项目的架构、组件关系和执行流程。

## 文件说明

- `class_diagram.puml`: 类图，展示项目中的主要类及其关系
- `sequence_diagram.puml`: 序列图，展示项目的执行流程
- `component_diagram.puml`: 组件图，展示项目的主要组件及其依赖关系
- `activity_diagram.puml`: 活动图，展示项目的执行活动流程
- `deployment_diagram.puml`: 部署图，展示项目的部署结构

## 工具脚本

- `generate_images.py`: 用于生成 UML 图像文件（需要安装 PlantUML）
- `html/index.html`: 在线查看 UML 图的 HTML 页面
- `html/local.html`: 本地查看 UML 图的 HTML 页面（需要先生成图像文件）

## 查看方式

1. **在线查看**：
   - 打开 `html/index.html` 文件，通过浏览器查看所有 UML 图
   - 该方式需要互联网连接，因为图片是通过 PlantUML 在线服务生成的

2. **本地查看**：
   - 运行 `python generate_images.py` 生成图像文件
   - 图像文件将保存在 `images/` 目录下
   - 或者使用支持 PlantUML 的编辑器/IDE 插件（如 VS Code 的 PlantUML 插件）

3. **命令行生成图片**：
   ```bash
   cd uml
   plantuml -tpng -o images *.puml
   ```

## 图片说明

1. **类图**：展示了代理系统的继承层次、流程管理系统以及工具系统等类及其关系
2. **序列图**：展示了从用户输入到返回结果的整个执行流程
3. **组件图**：展示了项目的主要组件及其依赖关系
4. **活动图**：展示了项目的执行活动流程
5. **部署图**：展示了项目的部署结构及组件交互

## 项目调用逻辑

OpenManus 项目的调用逻辑从 `run_flow.py` 开始：

1. **初始化阶段**：
   - 创建 Manus 代理实例
   - 进入主循环等待用户输入

2. **用户输入处理**：
   - 接收用户输入 prompt
   - 通过 FlowFactory.create_flow 创建 PlanningFlow 实例
   - 调用 flow.execute(prompt) 执行请求处理

3. **Flow 执行流程**：
   - 初始化执行环境
   - 创建初始计划
   - 循环执行计划步骤
   - 完成计划并返回结果

4. **代理执行流程**：
   - 初始化代理状态
   - 循环执行 think-act 方法
   - 使用工具执行任务
   - 返回执行结果
