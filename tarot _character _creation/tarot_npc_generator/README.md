# 塔罗牌NPC生成器

基于塔罗牌抽牌机制，结合大语言模型，生成饱满的NPC人物形象。

## ✨ 功能特性

- 🃏 **塔罗牌抽牌**：随机抽取3张塔罗牌（包含正/逆位）
- 🎭 **人物形象生成**：根据牌意和故事背景生成完整的人物设定
- 🔄 **反馈迭代**：支持多次反馈修改，优化人物形象
- 🎨 **精美UI**：塔罗风格界面，支持逆位牌旋转展示
- 📱 **响应式设计**：适配桌面端和移动端

## 🛠️ 技术栈

### 后端
- **Python 3.10+**
- **FastAPI**：高性能 API 框架
- **LangGraph**：状态图工作流管理
- **DeepSeek API**：大语言模型调用
- **Pydantic**：数据验证

### 前端
- **HTML5**：页面结构
- **CSS3**：样式设计（动画、响应式）
- **JavaScript**：交互逻辑

## 📁 项目结构

```
tarot_npc_generator/
├── backend/                 # 后端代码
│   ├── __init__.py
│   ├── cards.py            # 塔罗牌数据处理
│   ├── config.py           # API配置
│   ├── graph.py            # LangGraph工作流
│   ├── llm.py              # 大模型调用封装
│   ├── main.py             # FastAPI入口
│   ├── models.py           # 数据模型
│   └── prompts.py          # 提示词模板
├── data/                   # 静态数据
│   ├── background/         # 背景图片
│   │   ├── beijing.png     # 页面背景
│   │   ├── choupai.png     # 抽牌按钮
│   │   ├── paidui_0.png    # 牌堆动画图1
│   │   ├── paidui_1.png    # 牌堆动画图2
│   │   └── paidui_2.png    # 牌堆动画图3
│   ├── image/              # 塔罗牌图片
│   │   ├── 0_愚人.png
│   │   ├── 1_魔术师.png
│   │   └── ...
│   └── json/
│       └── tarot.json      # 塔罗牌数据
├── frontend/               # 前端代码
│   ├── index.html          # 主页面
│   ├── script.js           # 交互逻辑
│   └── style.css           # 样式文件
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn pydantic langgraph openai python-dotenv
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

### 3. 启动服务

```bash
cd tarot_npc_generator
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

访问 `http://localhost:8000` 即可使用。

## 📡 API 接口

### POST /start

创建会话并抽取塔罗牌。

**请求体**：
```json
{}
```

**响应**：
```json
{
  "thread_id": "uuid-string",
  "drawn_cards": ["0_愚人_正位", "5_教皇_逆位", "2_女祭司_正位"],
  "card_images": ["/data/image/0_愚人.png", "/data/image/5_教皇.png", "/data/image/2_女祭司.png"],
  "status": "waiting_background"
}
```

### POST /continue

继续会话，提交背景或反馈。

**请求体**（首次提交背景）：
```json
{
  "thread_id": "uuid-string",
  "user_background": "中世纪奇幻世界"
}
```

**请求体**（提交反馈）：
```json
{
  "thread_id": "uuid-string",
  "feedback": "希望人物性格更阴暗一些"
}
```

**响应**：
```json
{
  "thread_id": "uuid-string",
  "generated_profile": "人物形象描述...",
  "status": "waiting_feedback"
}
```

## 🎮 使用说明

1. **点击抽牌**：点击「抽牌」按钮，观看牌堆动画
2. **查看结果**：三张塔罗牌展示，逆位牌会倒置显示
3. **输入背景**：填写故事背景（如：中世纪、中国古代）
4. **生成角色**：点击「生成角色」按钮
5. **查看结果**：阅读生成的人物形象
6. **反馈修改**（可选）：输入修改意见，点击「重新生成」
7. **结束会话**：点击「满意，结束」

## 🃏 塔罗牌体系

- **第1张·内核**：性格底色、核心欲望
- **第2张·土壤**：出身背景、成长环境  
- **第3张·齿轮**：行动动机、推动情节的力量

## 📄 输出格式

生成的人物形象包含：

- **人物姓名**：姓名及寓意
- **最终人物形象**：年龄、职业、性格、背景、动机
- **牌的本意解析**：三张牌的核心含义
- **映射关系**：牌意到人物特征的转化逻辑

## 📝 注意事项

1. 需要有效的 DeepSeek API Key
2. 塔罗牌图片需放置在 `data/image/` 目录
3. 背景图片需放置在 `data/background/` 目录
4. 首次使用建议先测试 `/start` 接口是否正常

## 📄 许可证

MIT License