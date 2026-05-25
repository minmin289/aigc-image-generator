import requests  # 用于发送网络请求
import base64  # 用于解码base64编码的图片数据
import json  # 处理JSON数据（这里实际没用到）
import time  # 控制时间间隔，用于重试和延迟
from PIL import Image  # 图像处理库，用于创建和保存图片
from io import BytesIO  # 将字节数据转换为文件-like对象
import os  # 操作系统接口，用于文件和目录操作

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"  # Stable Diffusion API的地址

DEFAULTa_PAYLOAD = {  # 默认的参数配置（变量名有拼写错误，应该是DEFAULT_PAYLOAD）
    "negative_prompt": "ugly,blurry,low quality",  # 负面提示词（也有拼写错误，应该是negative_prompt）
    "steps": 20,  # 生成步数，越多质量越好但速度越慢
    "cfg_scale": 7,  # 提示词相关性，值越大越遵循提示词
    "width": 512,  # 图片宽度
    "height": 512,  # 图片高度
    "sampler_index": "Euler a"  # 采样器类型
}


def generate_image(prompt, retries=2):
    """
    调用 SD API 生成一张图片
    :param prompt: 提示词（你想要生成的图片描述）
    :param retries: 失败重试次数（默认2次）
    :return: PIL Image 对象，失败返回 None
    """
    payload = DEFAULTa_PAYLOAD.copy()  # 复制默认配置，避免修改原字典
    payload["prompt"] = prompt  # 添加用户的提示词

    for attempt in range(retries):  # 循环重试，最多retries次
        try:
            response = requests.post(url, json=payload, timeout=60)
            # 发送POST请求到API，超时时间60秒

            if response.status_code == 200:  # HTTP状态码200表示成功
                r = response.json()  # 将响应解析为JSON
                if "images" in r and len(r["images"]) > 0:
                    # 检查返回数据中是否有图片
                    image_data = base64.b64decode(r["images"][0])
                    # 解码base64格式的图片数据
                    image = Image.open(BytesIO(image_data))
                    # 将字节数据转换为PIL图片对象
                    return image  # 成功返回图片
                else:
                    print(f"⚠️ API 返回成功但无图片数据，尝试{attempt + 1}/{retries}")
            else:
                print(f"❌ HTTP{response.status_code}:{response.text[:100]},尝试{attempt + 1}/{retries}")
                # 显示HTTP错误信息
        except Exception as e:
            print(f"❗ 请求异常:{e},尝试{attempt + 1}/{retries}")
            # 捕获所有异常（如网络错误）

        time.sleep(2)  # 重试前等待2秒

    print(f"❌ 生成失败:{prompt[:50]}...")  # 所有尝试都失败
    return None  # 返回None表示失败


def sanitize_filename(prompt, max_len=50):
    """将 prompt 转换为安全的文件名（去掉非法字符）"""
    safe = "".join(c for c in prompt if c.isalnum() or c in (' ', '_', '-'))
    # 只保留字母、数字、空格、下划线、连字符，去掉其他特殊字符
    safe = safe.replace(' ', '_')  # 将空格替换为下划线
    return safe[:max_len]  # 限制文件名长度，最多50个字符


def main():
    if not os.path.exists("prompts.txt"):
        # 检查prompts.txt文件是否存在
        print("❌ 未找到 prompts.txt 文件，请在当前目录下创建它。")
        return  # 文件不存在则退出

    with open("prompts.txt", "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]
        # 读取文件，每行去除首尾空白，跳过空行

    if not prompts:  # 检查是否读到了内容
        print("❌ prompts.txt 为空，请至少写一个 prompt。")
        return

    print(f"📖 共读取 {len(prompts)} 条 prompt")  # 显示读取到的提示词数量

    output_dir = "generated_images"  # 输出目录名称
    os.makedirs(output_dir, exist_ok=True)
    # 创建目录，如果已存在也不报错

    for idx, prompt in enumerate(prompts):
        # 遍历所有提示词，idx是索引（从0开始）
        print(f"\n🖼️ 正在生成第{idx + 1}/{len(prompts)}张：{prompt[:50]}...")
        # 显示进度，只显示前50个字符

        image = generate_image(prompt)  # 调用函数生成图片

        if image:  # 如果生成成功
            safe_name = sanitize_filename(prompt)  # 生成安全的文件名
            filename = f"{idx + 1:03d}_{safe_name}.png"
            # 格式化文件名，如：001_a_cute_cat.png
            filepath = os.path.join(output_dir, filename)
            # 拼接完整路径
            image.save(filepath)  # 保存图片
            print(f"✅ 已保存: {filepath}")
        else:
            print(f"❌ 跳过: {prompt[:50]}...")  # 生成失败则跳过

        time.sleep(1)  # 每张图之间间隔1秒

    print("\n🎉 批量生成完成！")  # 全部完成


if __name__ == "__main__":
    main()
    # 当直接运行这个脚本时，调用main函数
