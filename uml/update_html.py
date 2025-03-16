import os
import base64
import zlib
from pathlib import Path

def encode_plantuml(puml_content):
    """将PlantUML内容编码为URL安全的字符串"""
    # 压缩内容
    zlibbed = zlib.compress(puml_content.encode('utf-8'))
    # 去掉zlib头部的两个字节
    compressed = zlibbed[2:-4]
    # Base64编码
    b64 = base64.b64encode(compressed)
    # 替换URL不安全的字符
    encoded = b64.decode('utf-8').replace('+', '-').replace('/', '_')
    return encoded

def create_direct_html():
    """创建一个直接包含所有UML图的HTML文件"""
    # 获取所有PUML文件
    puml_files = list(Path(".").glob("*.puml"))
    
    if not puml_files:
        print("未找到PUML文件")
        return
    
    print(f"找到 {len(puml_files)} 个PUML文件")
    
    # HTML头部
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenManus UML 图 - PNG 下载</title>
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
            margin-bottom: 15px;
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
        .download-btn {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 10px 15px;
            text-decoration: none;
            border-radius: 4px;
            margin-bottom: 30px;
        }
        .download-btn:hover {
            background-color: #2980b9;
        }
        .instructions {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>OpenManus UML 图 - PNG 下载</h1>
    
    <div class="instructions">
        <h3>下载说明</h3>
        <p>请按照以下步骤下载PNG图片：</p>
        <ol>
            <li>点击下方的"查看图片"按钮，将在新标签页中打开图片</li>
            <li>右键点击图片，选择"图片另存为..."保存PNG图片到本地</li>
        </ol>
    </div>
"""
    
    # 图片描述
    descriptions = {
        "class_diagram": "类图展示了 OpenManus 项目中的主要类及其关系。包括代理系统的继承层次（BaseAgent → ReActAgent → ToolCallAgent → Manus）、流程管理系统（BaseFlow → PlanningFlow）以及工具系统等。",
        "sequence_diagram": "序列图展示了 OpenManus 项目的执行流程，从用户输入提示词开始，到最终返回执行结果的整个过程。包括 FlowFactory 创建流程、PlanningFlow 执行计划、Manus 代理执行工具调用等关键步骤。",
        "component_diagram": "组件图展示了 OpenManus 项目的主要组件及其依赖关系。包括入口点、代理系统、流程管理、工具系统和核心服务等模块。",
        "activity_diagram": "活动图展示了 OpenManus 项目的执行活动流程，从用户输入到返回结果的整个过程，包括计划创建、步骤执行和结果返回等关键活动。",
        "deployment_diagram": "部署图展示了 OpenManus 项目的部署结构，包括用户环境、系统组件和外部服务等，以及它们之间的交互关系。",
        "flow_diagram": "流程图展示了 OpenManus 项目的执行流程，从用户输入到返回结果的整个过程。"
    }
    
    # 图片标题
    titles = {
        "class_diagram": "类图 (Class Diagram)",
        "sequence_diagram": "序列图 (Sequence Diagram)",
        "component_diagram": "组件图 (Component Diagram)",
        "activity_diagram": "活动图 (Activity Diagram)",
        "deployment_diagram": "部署图 (Deployment Diagram)",
        "flow_diagram": "流程图 (Flow Diagram)"
    }
    
    # 添加每个UML图
    for puml_file in puml_files:
        # 读取PUML文件内容
        with open(puml_file, 'r', encoding='utf-8') as f:
            puml_content = f.read()
        
        # 编码内容
        encoded = encode_plantuml(puml_content)
        
        # 构建URL
        url = f"https://www.plantuml.com/plantuml/png/{encoded}"
        
        # 文件名（不含扩展名）
        file_stem = puml_file.stem
        
        # 获取标题和描述
        title = titles.get(file_stem, f"{file_stem.replace('_', ' ').title()}")
        description = descriptions.get(file_stem, f"{file_stem.replace('_', ' ').title()} 图")
        
        # 添加到HTML内容
        html_content += f"""
    <h2>{title}</h2>
    <div class="description">
        <p>{description}</p>
    </div>
    <div class="uml-container">
        <img src="{url}" alt="{title}" class="uml-image">
        <a href="{url}" class="download-btn" target="_blank">查看图片</a>
    </div>
"""
    
    # HTML尾部
    html_content += """
</body>
</html>"""
    
    # 写入HTML文件
    html_file = Path("png_download.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"已创建 {html_file} 文件")

def main():
    """主函数"""
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    create_direct_html()

if __name__ == "__main__":
    main() 