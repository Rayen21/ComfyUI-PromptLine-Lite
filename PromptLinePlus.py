#首先感谢easy-use作者的付出https://github.com/yolain/ComfyUI-Easy-Use
#因为只需要其中的提示词的批处理功能所以截取了原版的代码,加入了一个可以追加自定义提示词的框
import re

# -----------------------------------------------------------
# PromptLinePlus (提示词批次生成)
# -----------------------------------------------------------

class PromptLinePlus:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "prompt A\nprompt B\nprompt C"}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),
            },
            "optional": {
                # 新增一个可选的自定义提示词输入
                "custom_prompt": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter custom prompt to combine..."}),
                "combination_mode": (["append", "prepend", "replace"], {"default": "append", "tooltip": "How to combine the custom prompt with each line: append (add comma to line end then append), prepend (add comma to custom prompt end then prepend), replace (replace the line entirely with custom prompt)"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    OUTPUT_IS_LIST = (True,)  # 关键：输出为字符串列表
    FUNCTION = "generate_strings"
    CATEGORY = "utils"

    def generate_strings(self, prompt, start_index, max_rows, custom_prompt="", combination_mode="append"):
        # 按换行符分割，去除空行
        lines = [line.strip() for line in prompt.split('\n') if line.strip()]
        
        # --- 处理 custom_prompt ---
        # 1. 按换行符分割
        custom_parts = custom_prompt.split('\n')
        # 2. 去除每部分的首尾空格，并过滤掉空字符串
        #custom_parts_stripped = [part.strip() for part in custom_parts if part.strip()]
        # 3. 删除每个部分内部的所有空格
        #custom_parts_no_spaces = [re.sub(r'\s+', '', part) for part in custom_parts_stripped]
        # 4. 将所有处理后的部分直接拼接成一个字符串，不添加任何分隔符
        #processed_custom_prompt = "".join(custom_parts_no_spaces)
        # 不处理空格，直接换行符分割输出了，否则反而会把文字间的空格删了
        processed_custom_prompt = "".join(custom_parts)
        # --- 处理结束 ---
        
        # 裁剪范围
        start = max(0, start_index)
        end = min(start + max_rows, len(lines))
        selected_lines = lines[start:end]
        
        # 如果提供了自定义提示词，则根据模式进行组合
        if processed_custom_prompt: # 检查处理后的提示词是否非空
            combined_lines = []
            for line in selected_lines:
                if combination_mode == "append":
                    # 将处理后的自定义提示词追加到每一行后面
                    # 先给原行添加逗号，再拼接 custom_prompt
                    # 如果原行为空，则直接使用 processed_custom_prompt
                    combined_line = f"{line}, {processed_custom_prompt}" if line else processed_custom_prompt
                elif combination_mode == "prepend":
                    # 将处理后的自定义提示词前置到每一行前面
                    # 先给 custom_prompt 添加逗号，再拼接原行
                    # 如果原行为空，则直接使用 processed_custom_prompt
                    combined_line = f"{processed_custom_prompt}, {line}" if line else processed_custom_prompt
                elif combination_mode == "replace":
                    # 完全替换为处理后的自定义提示词
                    combined_line = processed_custom_prompt
                
                combined_lines.append(combined_line)
            selected_lines = combined_lines
        
        # 如果最终列表为空，返回至少一个空字符串以避免报错
        if not selected_lines:
            selected_lines = [""]
            
        return (selected_lines,)

# -----------------------------------------------------------
# 注册节点
# -----------------------------------------------------------

NODE_CLASS_MAPPINGS = {
    "PromptLinePlus": PromptLinePlus,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptLinePlus": "PromptLinePlus",
}