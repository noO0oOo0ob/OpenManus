import os
import urllib.request
import urllib.parse
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

def download_png(puml_file, output_dir):
    """从PlantUML服务器下载PNG图片"""
    # 读取PUML文件内容
    with open(puml_file, 'r', encoding='utf-8') as f:
        puml_content = f.read()
    
    # 编码内容
    encoded = encode_plantuml(puml_content)
    
    # 构建URL
    url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    
    # 输出文件名
    output_file = output_dir / f"{puml_file.stem}.png"
    
    print(f"下载 {puml_file.name} -> {output_file}")
    
    # 下载图片
    try:
        urllib.request.urlretrieve(url, output_file)
        return True
    except Exception as e:
        print(f"下载 {puml_file.name} 时出错: {e}")
        return False

def main():
    """主函数"""
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 确保输出目录存在
    output_dir = Path("png")
    output_dir.mkdir(exist_ok=True)
    
    # 获取所有PUML文件
    puml_files = list(Path(".").glob("*.puml"))
    
    if not puml_files:
        print("未找到PUML文件")
        return
    
    print(f"找到 {len(puml_files)} 个PUML文件")
    
    # 下载所有图片
    success_count = 0
    for puml_file in puml_files:
        if download_png(puml_file, output_dir):
            success_count += 1
    
    print(f"成功下载 {success_count}/{len(puml_files)} 个PNG图片到 {output_dir}/ 目录")

if __name__ == "__main__":
    main() 