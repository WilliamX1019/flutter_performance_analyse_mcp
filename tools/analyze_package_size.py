import subprocess
import os
import sys

def analyze_package_size(platform='apk'):
    """
    运行 'flutter build' 命令并捕获其 --analyze-size 输出。
    支持 'apk', 'aab', 'ipa' 平台。
    """
    if platform not in ['apk', 'aab', 'ipa']:
        error_msg = f"[PackageSizeAgent] 错误: 不支持的平台 '{platform}'。有效值为 'apk', 'aab', 'ipa'。"
        print(error_msg)
        return error_msg

    if platform == 'ipa' and sys.platform != 'darwin':
        error_msg = "[PackageSizeAgent] 错误: 只能在 macOS 上构建 IPA 包。"
        print(error_msg)
        return error_msg

    platform_name_map = {
        'apk': 'Android APK',
        'aab': 'Android App Bundle',
        'ipa': 'iOS IPA'
    }
    platform_name = platform_name_map[platform]
    build_target = 'appbundle' if platform == 'aab' else platform

    print(f"[PackageSizeAgent] 开始构建 {platform_name} 并分析应用包大小...")
    command = ["flutter", "build", build_target, "--analyze-size"]
    
    cwd = os.getcwd()
    print(f"[PackageSizeAgent] 当前工作目录: {cwd}")
    
    try:
        result = subprocess.run(
            command, shell=False, check=True, capture_output=True, text=True, encoding='utf-8'
        )
        print(f"[PackageSizeAgent] {platform_name} 包大小分析完成。")
        report_content = f"### 应用包大小分析 ({platform_name})\n\n"
        report_content += "```\n" + result.stdout.strip() + "\n```"
        return report_content
    except FileNotFoundError:
        error_msg = "[PackageSizeAgent] 错误: 'flutter' 命令未找到。请确保 Flutter SDK 已安装并在您的 PATH 环境变量中。"
        print(error_msg)
        return error_msg
    except subprocess.CalledProcessError as e:
        error_msg = f"[PackageSizeAgent] 错误: 'flutter build {build_target}' 命令执行失败，返回码: {e.returncode}\n错误信息:\n{e.stderr}"
        print(error_msg)
        return error_msg
