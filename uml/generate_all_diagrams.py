import os
import plantuml

def generate_diagram(plantuml_file, output_file):
    """
    使用 plantuml 库从 PlantUML 文件生成图像
    """
    # 读取 PlantUML 文件
    with open(plantuml_file, 'r', encoding='utf-8') as f:
        plantuml_text = f.read()
    
    # 创建 PlantUML 对象
    plantuml_server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/')
    
    # 生成图像
    try:
        print(f"生成图像中: {output_file}...")
        
        # 获取编码后的 URL
        url = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/uml/').get_url(plantuml_text)
        print(f"在线查看链接: {url}")
        
        # 生成图像并保存到文件
        with open(output_file, 'wb') as f:
            f.write(plantuml_server.processes(plantuml_text))
        
        print(f"图像已保存到: {output_file}")
    except Exception as e:
        print(f"生成图像时出错: {e}")

if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 要生成的图表列表
    diagrams = [
        ("class_diagram.puml", "output/class_diagram.png"),
        ("flow_diagram.puml", "output/flow_diagram.png"),
        ("component_diagram.puml", "output/component_diagram.png")
    ]
    
    # 生成所有图表
    for puml_file, output_file in diagrams:
        generate_diagram(puml_file, output_file) 