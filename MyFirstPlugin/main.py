
class MyFirstPlugin(PluginBase):
    description = "我的第一个插件"
    author = "Your Name"
    version = "1.0.0"

    def __init__(self):
        super().__init__()

        # 获取配置文件路径
        config_path = os.path.join(os.path.dirname(__file__), "config.toml")

        try:
            with open(config_path, "rb") as f:
                config = tomllib.load(f)

            # 读取基本配置
            basic_config = config.get("basic", {})
            self.enable = basic_config.get("enable", False)  # 读取插件开关
            self.trigger_word = basic_config.get("trigger_word", "你好")  # 读取触发词

        except Exception as e:
            logger.error(f"加载MyFirstPlugin配置文件失败: {str(e)}")
            self.enable = False  # 如果加载失败，禁用插件

    @on_text_message(priority=50)
    async def handle_text(self, bot: WechatAPIClient, message: dict):
        """处理文本消息"""
        if not self.enable:
            return True  # 插件未启用，允许后续插件处理

        content = message["Content"]

        # 检查是否包含触发词
        if self.trigger_word in content:
            # 发送回复
            await bot.send_text_message(
                message["FromWxid"],
                f"你好！我是你的第一个插件。你说了：{content}"
            )
            return False  # 阻止后续插件处理

        return True  # 允许后续插件处理