import os
import subprocess
import sys
from pathlib import Path

def check_plantuml():
    """检查是否安装了PlantUML"""
    try:
        # 尝试运行plantuml命令
        result = subprocess.run(
            ["plantuml", "-version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def generate_images():
    """生成UML图像文件"""
    # 确保输出目录存在
    output_dir = Path("images")
    output_dir.mkdir(exist_ok=True)
    
    # 获取所有PUML文件
    puml_files = list(Path(".").glob("*.puml"))
    
    if not puml_files:
        print("未找到PUML文件")
        return
    
    print(f"找到 {len(puml_files)} 个PUML文件")
    
    # 使用PlantUML生成图像
    try:
        cmd = ["plantuml", "-tpng", "-o", str(output_dir)]
        cmd.extend([str(f) for f in puml_files])
        
        print("运行命令:", " ".join(cmd))
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode == 0:
            print(f"成功生成图像文件到 {output_dir}/ 目录")
            print("生成的文件:")
            for img in output_dir.glob("*.png"):
                print(f"  - {img.name}")
        else:
            print("生成图像时出错:")
            print(result.stderr)
    except Exception as e:
        print(f"执行过程中出错: {e}")

def main():
    """主函数"""
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if not check_plantuml():
        print("未检测到PlantUML。请确保已安装PlantUML并将其添加到PATH环境变量中。")
        print("您可以从 http://plantuml.com/download 下载PlantUML。")
        print("\n或者，您可以使用在线服务查看UML图：")
        print("  - 打开 html/index.html 文件在浏览器中查看")
        return
    
    generate_images()

if __name__ == "__main__":
    main() 