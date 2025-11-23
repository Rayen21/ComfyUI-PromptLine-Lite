#首先感谢easy-use作者的付出https://github.com/yolain/ComfyUI-Easy-Use
#因为只需要其中的提示词的批处理功能所以截取了原版的代码，精简使用
class PromptLineLite:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "prompt A\nprompt B\nprompt C"}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 9999}),
                "max_rows": ("INT", {"default": 1000, "min": 1, "max": 9999}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    OUTPUT_IS_LIST = (True,)  # 关键：输出为字符串列表
    FUNCTION = "generate_strings"
    CATEGORY = "utils"

    def generate_strings(self, prompt, start_index, max_rows):
        # 按换行符分割，去除空行
        lines = [line.strip() for line in prompt.split('\n') if line.strip()]
        # 裁剪范围
        start = max(0, start_index)
        end = min(start + max_rows, len(lines))
        selected_lines = lines[start:end]
        # 如果为空，返回至少一个空字符串以避免报错
        if not selected_lines:
            selected_lines = [""]
        return (selected_lines,)


# 注册节点
NODE_CLASS_MAPPINGS = {
    "PromptLineLite": PromptLineLite
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptLineLite": "Prompt Line (Lite)"
}