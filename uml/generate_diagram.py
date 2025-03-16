import urllib.request
import urllib.parse
import base64
import zlib
import os

def encode_plantuml(plantuml_text):
    """
    将 PlantUML 文本编码为可用于在线服务的格式
    """
    # 压缩文本
    compressed = zlib.compress(plantuml_text.encode('utf-8'))
    # 移除前8个字节（zlib头）
    compressed = compressed[2:-4]
    # Base64编码
    encoded = base64.b64encode(compressed)
    # 替换特殊字符以适应URL
    encoded = encoded.decode('utf-8')
    encoded = encoded.replace('+', '-')
    encoded = encoded.replace('/', '_')
    return encoded

def generate_diagram(plantuml_file, output_file):
    """
    从PlantUML文件生成图像
    """
    # 读取PlantUML文件
    with open(plantuml_file, 'r', encoding='utf-8') as f:
        plantuml_text = f.read()
    
    # 编码PlantUML文本
    encoded = encode_plantuml(plantuml_text)
    
    # 构建URL
    url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    
    print(f"生成图像中，请稍候...")
    print(f"在线查看链接: http://www.plantuml.com/plantuml/uml/{encoded}")
    
    # 下载图像
    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"图像已保存到: {output_file}")
    except Exception as e:
        print(f"下载图像时出错: {e}")

if __name__ == "__main__":
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 生成图像
    generate_diagram("class_diagram.puml", "output/class_diagram.png") 