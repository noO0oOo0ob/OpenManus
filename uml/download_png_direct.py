import os
import base64
import zlib
import urllib.request
from pathlib import Path
import time

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

def download_png_direct():
    """直接下载PNG图片到本地"""
    # 确保输出目录存在
    output_dir = Path("png")
    output_dir.mkdir(exist_ok=True)
    
    # 获取所有PUML文件
    puml_files = list(Path(".").glob("*.puml"))
    
    if not puml_files:
        print("未找到PUML文件")
        return
    
    print(f"找到 {len(puml_files)} 个PUML文件")
    
    # 下载每个UML图
    for puml_file in puml_files:
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
            # 添加User-Agent头，模拟浏览器请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response, open(output_file, 'wb') as out_file:
                out_file.write(response.read())
            print(f"  成功下载 {puml_file.stem}.png")
            
            # 添加延迟，避免请求过快
            time.sleep(1)
        except Exception as e:
            print(f"  下载 {puml_file.name} 时出错: {e}")
    
    print(f"\n所有PNG图片已下载到 {output_dir}/ 目录")
    print("如果下载失败，请尝试使用浏览器打开 png_download.html 文件手动下载")

def main():
    """主函数"""
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    download_png_direct()

if __name__ == "__main__":
    main() 