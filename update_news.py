import os
import re
import google.generativeai as genai

# 配置 API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 提示词
prompt = """
请作为新闻主编，编写本周（2026年1月）的海内外新闻简报。
要求格式如下：
1. 包含三个 <div> 容器，ID 分别为 domestic, intl, tech。
2. 每个容器内包含 2-3 篇新闻，每篇新闻先写一段中文（约 200 字），再紧跟一段对应的英文翻译。
3. 英文段落必须包含属性 onmouseup="quickTranslate(event)" 以便取词。
4. 总字数丰富，内容要深入浅出。
仅返回 <div> 部分的代码，不要包含其他 Markdown 标记。
"""

try:
    response = model.generate_content(prompt)
    new_content = response.text
    
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # 使用正则表达式替换 main 标签内容
    pattern = r'<main id="content".*?>(.*?)</main>'
    replacement = f'<main id="content" class="max-w-4xl mx-auto p-4 mt-2">{new_content}</main>'
    updated_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_html)
    print("Update successful")
except Exception as e:
    print(f"Error occurred: {e}")
