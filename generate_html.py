import os

# 确保输出目录存在
os.makedirs("uml/html", exist_ok=True)

# 创建HTML文件
html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenManus UML 图</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        h2 {
            color: #3498db;
            margin-top: 40px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .uml-container {
            margin: 20px 0;
            text-align: center;
        }
        .uml-image {
            max-width: 100%;
            height: auto;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .description {
            margin: 20px 0;
            text-align: left;
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
        }
        .note {
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>OpenManus 项目 UML 图</h1>
    
    <p>本页面展示了 OpenManus 项目的各种 UML 图，用于说明项目的架构、组件关系和执行流程。</p>
    
    <h2>类图 (Class Diagram)</h2>
    <div class="description">
        <p>类图展示了 OpenManus 项目中的主要类及其关系。包括代理系统的继承层次（BaseAgent → ReActAgent → ToolCallAgent → Manus）、流程管理系统（BaseFlow → PlanningFlow）以及工具系统等。</p>
    </div>
    <div class="uml-container">
        <img src="https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/username/OpenManus/main/uml/class_diagram.puml" alt="类图" class="uml-image">
    </div>
    <div class="note">
        <p>注：如果图片无法显示，请确保您的网络可以访问 plantuml.com，或者使用本地 PlantUML 工具生成图片。</p>
    </div>
    
    <h2>序列图 (Sequence Diagram)</h2>
    <div class="description">
        <p>序列图展示了 OpenManus 项目的执行流程，从用户输入提示词开始，到最终返回执行结果的整个过程。包括 FlowFactory 创建流程、PlanningFlow 执行计划、Manus 代理执行工具调用等关键步骤。</p>
    </div>
    <div class="uml-container">
        <img src="https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/username/OpenManus/main/uml/sequence_diagram.puml" alt="序列图" class="uml-image">
    </div>
    
    <h2>组件图 (Component Diagram)</h2>
    <div class="description">
        <p>组件图展示了 OpenManus 项目的主要组件及其依赖关系。包括入口点、代理系统、流程管理、工具系统和核心服务等模块。</p>
    </div>
    <div class="uml-container">
        <img src="https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/username/OpenManus/main/uml/component_diagram.puml" alt="组件图" class="uml-image">
    </div>
    
    <h2>活动图 (Activity Diagram)</h2>
    <div class="description">
        <p>活动图展示了 OpenManus 项目的执行活动流程，从用户输入到返回结果的整个过程，包括计划创建、步骤执行和结果返回等关键活动。</p>
    </div>
    <div class="uml-container">
        <img src="https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/username/OpenManus/main/uml/activity_diagram.puml" alt="活动图" class="uml-image">
    </div>
    
    <h2>部署图 (Deployment Diagram)</h2>
    <div class="description">
        <p>部署图展示了 OpenManus 项目的部署结构，包括用户环境、系统组件和外部服务等，以及它们之间的交互关系。</p>
    </div>
    <div class="uml-container">
        <img src="https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/username/OpenManus/main/uml/deployment_diagram.puml" alt="部署图" class="uml-image">
    </div>
    
    <div class="note" style="margin-top: 50px; text-align: center;">
        <p>注：以上 UML 图使用 PlantUML 生成。如需查看原始 PlantUML 代码，请查看 uml/ 目录下的相应 .puml 文件。</p>
    </div>
</body>
</html>
"""

# 创建一个本地版本的HTML文件（使用本地文件路径）
local_html_content = html_content.replace(
    "https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/username/OpenManus/main/uml/",
    "../"
)

# 写入HTML文件
with open("uml/html/index.html", "w") as f:
    f.write(html_content)

with open("uml/html/local.html", "w") as f:
    f.write(local_html_content)

print("HTML 文件已生成到 uml/html/ 目录")

# 创建一个README文件，说明如何查看UML图
readme_content = """# OpenManus UML 图

本目录包含 OpenManus 项目的 UML 图，用于说明项目的架构、组件关系和执行流程。

## 文件说明

- `class_diagram.puml`: 类图，展示项目中的主要类及其关系
- `sequence_diagram.puml`: 序列图，展示项目的执行流程
- `component_diagram.puml`: 组件图，展示项目的主要组件及其依赖关系
- `activity_diagram.puml`: 活动图，展示项目的执行活动流程
- `deployment_diagram.puml`: 部署图，展示项目的部署结构

## 查看方式

1. **在线查看**：
   - 打开 `html/index.html` 文件，通过浏览器查看所有 UML 图
   - 该方式需要互联网连接，因为图片是通过 PlantUML 在线服务生成的

2. **本地查看**：
   - 安装 PlantUML（http://plantuml.com/download）
   - 使用 PlantUML 打开 `.puml` 文件生成图片
   - 或者使用支持 PlantUML 的编辑器/IDE 插件（如 VS Code 的 PlantUML 插件）

3. **命令行生成图片**：
   ```bash
   java -jar plantuml.jar *.puml
   ```

## 图片说明

1. **类图**：展示了代理系统的继承层次、流程管理系统以及工具系统等类及其关系
2. **序列图**：展示了从用户输入到返回结果的整个执行流程
3. **组件图**：展示了项目的主要组件及其依赖关系
4. **活动图**：展示了项目的执行活动流程
5. **部署图**：展示了项目的部署结构及组件交互
"""

with open("uml/README.md", "w") as f:
    f.write(readme_content)

print("README 文件已生成到 uml/ 目录") 