import os
import json
import gradio as gr
from weather_mcp_server import (
    get_api_key,
    get_location_id,
    get_realtime_weather,
    get_forecast_weather,
    get_weather_by_location_name
)

# 确保中文正常显示
os.environ['GRADIO_THEME'] = 'gradio/soft'

# 自定义CSS样式
CUSTOM_CSS = """
# 容器样式
.gradio-container { max-width: 900px !important; }

# 卡片样式
.card {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
}

# 标题样式
h1 {
    color: #1a73e8;
    text-align: center;
    margin-bottom: 30px;
}

# 天气信息显示区域
.weather-info {
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #1a73e8;
}

# 温度显示
.temperature {
    font-size: 36px;
    font-weight: bold;
    color: #ff6b35;
}

# 天气状态
.weather-status {
    font-size: 24px;
    color: #4285f4;
}

# 预报卡片
.forecast-card {
    background-color: #e8f0fe;
    border-radius: 8px;
    padding: 10px;
    margin: 5px;
    text-align: center;
}

# 按钮样式
.gradio-button-primary {
    background-color: #1a73e8 !important;
    color: white !important;
}

# 结果标签
.result-label {
    font-weight: bold;
    color: #5f6368;
}
"""

# 天气图标映射
theme_map = {
    "晴": "☀️",
    "多云": "⛅",
    "阴": "☁️",
    "小雨": "🌦️",
    "中雨": "🌧️",
    "大雨": "⛈️",
    "暴雨": "⛈️",
    "雷阵雨": "⛈️",
    "小雪": "🌨️",
    "中雪": "❄️",
    "大雪": "❄️",
    "雾": "🌫️",
    "霾": "😷"
}

def get_weather_icon(weather_text):
    """根据天气文本返回对应的天气图标"""
    for key, icon in theme_map.items():
        if key in weather_text:
            return icon
    return "🌤️"  # 默认图标

def query_weather(location_name, forecast_days):
    """\查询天气信息"""
    try:
        # 获取API密钥
        api_key = get_api_key()
        
        # 获取地区ID
        location_id, actual_location_name = get_location_id(location_name, api_key)
        
        if not location_id:
            return f"错误：未找到地区 '{location_name}'，请检查输入是否正确"
        
        # 获取实时天气
        realtime_weather = get_realtime_weather(api_key, location_id)
        if not realtime_weather:
            return f"错误：获取实时天气数据失败"
        
        # 获取天气预报
        forecast_weather = get_forecast_weather(api_key, location_id, forecast_days)
        if not forecast_weather:
            return f"错误：获取天气预报数据失败"
        
        # 构建返回结果
        result = []
        
        # 实时天气卡片
        realtime_result = {
            "location": actual_location_name,
            "weather": realtime_weather['now']['text'],
            "temperature": realtime_weather['now']['temp'],
            "wind_dir": realtime_weather['now']['windDir'],
            "wind_scale": realtime_weather['now']['windScale'],
            "humidity": realtime_weather['now']['humidity'],
            "feels_like": realtime_weather['now']['feelsLike']
        }
        
        result.append(f"地区：{realtime_result['location']}")
        result.append(f"天气：{realtime_result['weather']} {get_weather_icon(realtime_result['weather'])}")
        result.append(f"温度：{realtime_result['temperature']}°C")
        result.append(f"体感温度：{realtime_result['feels_like']}°C")
        result.append(f"风向：{realtime_result['wind_dir']}")
        result.append(f"风力：{realtime_result['wind_scale']}级")
        result.append(f"湿度：{realtime_result['humidity']}%")
        
        result.append("\n=== 天气预报 ===")
        
        # 天气预报卡片
        for day in forecast_weather['daily']:
            date = day['fxDate']
            day_weather = day['textDay']
            night_weather = day['textNight']
            max_temp = day['tempMax']
            min_temp = day['tempMin']
            
            result.append(f"\n日期：{date}")
            result.append(f"白天：{day_weather} {get_weather_icon(day_weather)}")
            result.append(f"夜晚：{night_weather} {get_weather_icon(night_weather)}")
            result.append(f"温度范围：{min_temp}°C ~ {max_temp}°C")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"查询出错：{str(e)}"

def check_api_key():
    """检查API密钥是否已设置"""
    try:
        api_key = get_api_key()
        return f"API密钥已设置：{api_key[:5]}****{api_key[-5:]}"  # 部分隐藏API密钥
    except Exception as e:
        return f"API密钥未设置：{str(e)}"

def create_gui():
    """创建Gradio GUI界面"""
    with gr.Blocks(title="天气查询服务", css=CUSTOM_CSS) as demo:
        gr.Markdown("# 🌤️ 天气查询服务")
        
        with gr.Row():
            with gr.Column(scale=3):
                # 输入区域
                location_input = gr.Textbox(
                    label="请输入地区名称", 
                    placeholder="例如：北京、上海、福州",
                    value="北京"
                )
                
                # 预报天数选择
                forecast_days = gr.Radio(
                    label="选择预报天数",
                    choices=["3d", "7d", "10d", "15d", "30d"],
                    value="3d"
                )
                
                # 查询按钮
                query_btn = gr.Button("查询天气", variant="primary")
                
                # API密钥检查按钮
                api_key_btn = gr.Button("检查API密钥设置")
                
            with gr.Column(scale=7):
                # 结果显示区域
                result_output = gr.Textbox(
                    label="天气查询结果",
                    lines=20,
                    interactive=False,
                    placeholder="查询结果将显示在这里..."
                )
        
        # 绑定事件
        query_btn.click(
            fn=query_weather,
            inputs=[location_input, forecast_days],
            outputs=result_output
        )
        
        api_key_btn.click(
            fn=check_api_key,
            inputs=[],
            outputs=result_output
        )
        
        # 添加说明
        gr.Markdown("""
        ### 使用说明
        1. 确保已设置环境变量 `WEATHER_API_KEY` 包含有效的天气API密钥
        2. 在输入框中输入您想查询的地区名称
        3. 选择需要获取的天气预报天数
        4. 点击"查询天气"按钮获取天气信息
        5. 点击"检查API密钥设置"按钮可验证API密钥是否正确设置
        """)
    
    return demo

if __name__ == "__main__":
    # 创建并启动GUI
    demo = create_gui()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True
    )