# 天气查询MCP服务

# 天气服务 MCP 服务器

这是一个基于FastMCP的天气服务服务器，可以提供实时天气查询和天气预报功能。
主程序：weather_mcp_server.py

## 功能特性

- 根据地区名称获取地区ID和名称信息
- 获取详细的实时天气信息
- 获取详细的天气预报（支持3天、7天、10天、15天、30天预报）
- 整合了地区查询和天气查询的便捷功能

## 部署指南

### 1. 设置API密钥

为了安全地部署到网络服务器上，API密钥应该通过环境变量传入，而不是硬编码在代码中。

#### Windows系统

**临时设置（仅当前会话有效）**：

```cmd
set WEATHER_API_KEY=your_api_key_here
```

**永久设置**：

1. 右键点击"此电脑"或"计算机"，选择"属性"
2. 点击"高级系统设置"
3. 点击"环境变量"
4. 在"系统变量"区域，点击"新建"
5. 变量名输入 `WEATHER_API_KEY`，变量值输入您的实际API密钥
6. 点击"确定"保存

#### Linux/macOS系统

**临时设置（仅当前会话有效）**：

```bash
export WEATHER_API_KEY=your_api_key_here
```

**永久设置**：

编辑您的shell配置文件（如`~/.bashrc`、`~/.zshrc`等），添加以下行：

```bash
export WEATHER_API_KEY=your_api_key_here
```

保存后，运行以下命令使其生效：

```bash
source ~/.bashrc  # 或对应您的shell配置文件
```

### 2. 安装依赖

确保您已安装Python 3.7或更高版本。然后安装项目依赖：

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

开发环境中，您可以直接运行：

```bash
python weather_mcp_server.py
```

默认情况下，服务器以SSE模式运行在127.0.0.1:8000上。


## 使用示例

服务启动后，您可以通过以下工具调用来使用天气服务：

### 获取地区信息

```
get_location_info("福建")
```

返回结果示例：
```json
{
  "location_id": "101230101",
  "location_name": "福州"
}
```

### 获取实时天气信息

```
get_realtime_weather_info("101230101")
```

返回结果示例：
```json
{
  "weather": "晴",
  "temperature": "25",
  "wind_dir": "东北风",
  "wind_scale": "2级",
  "humidity": "45",
  "feels_like": "24"
}
```

### 获取天气预报信息

```
get_forecast_weather_info("101230101", "7d")
```

参数说明：
- `location_id`: 地区ID，如"101230101"
- `days`: 预报天数，支持最多30天预报，可选值：3d（3天预报）、7d（7天预报）、10d（10天预报）、15d（15天预报）、30d（30天预报）

返回结果示例：
```json
{
  "forecast": [
    {
      "date": "2023-10-01",
      "day_weather": "晴",
      "night_weather": "晴",
      "max_temp": "26",
      "min_temp": "18",
      "sunrise": "06:15",
      "sunset": "18:30",
      "moonrise": "19:45",
      "moonset": "07:30",
      "wind_dir_day": "东北风",
      "wind_scale_day": "2-3级",
      "wind_dir_night": "北风",
      "wind_scale_night": "1-2级",
      "humidity": "45",
      "precip": "0",
      "pressure": "1015",
      "vis": "25",
      "uv_index": "7"
    },
    {
      "date": "2023-10-02",
      "day_weather": "多云",
      "night_weather": "多云",
      "max_temp": "25",
      "min_temp": "17",
      "sunrise": "06:16",
      "sunset": "18:28",
      "moonrise": "20:30",
      "moonset": "08:15",
      "wind_dir_day": "东风",
      "wind_scale_day": "1-2级",
      "wind_dir_night": "东北风",
      "wind_scale_night": "1级",
      "humidity": "50",
      "precip": "0",
      "pressure": "1013",
      "vis": "20",
      "uv_index": "5"
    },
    {
      "date": "2023-10-03",
      "day_weather": "小雨",
      "night_weather": "小雨",
      "max_temp": "23",
      "min_temp": "16",
      "sunrise": "06:17",
      "sunset": "18:27",
      "moonrise": "21:15",
      "moonset": "09:00",
      "wind_dir_day": "东南风",
      "wind_scale_day": "2-3级",
      "wind_dir_night": "南风",
      "wind_scale_night": "2级",
      "humidity": "75",
      "precip": "15",
      "pressure": "1010",
      "vis": "8",
      "uv_index": "2"
    }
  ]
}
```

### 获取整合的天气信息

```
get_weather_info("101230101")
```

返回结果示例：
```json
{
  "realtime": {
    "weather": "晴",
    "temperature": "25"
  },
  "forecast": [
    {
      "date": "2023-10-01",
      "day_weather": "晴",
      "night_weather": "晴",
      "max_temp": "26",
      "min_temp": "18"
    },
    {
      "date": "2023-10-02",
      "day_weather": "多云",
      "night_weather": "多云",
      "max_temp": "25",
      "min_temp": "17"
    },
    {
      "date": "2023-10-03",
      "day_weather": "小雨",
      "night_weather": "小雨",
      "max_temp": "23",
      "min_temp": "16"
    }
  ]
}
```

### 直接通过地区名称获取天气

```
get_weather_by_location_name("福建")
```

返回结果示例：
```json
{
  "location": {
    "id": "101230101",
    "name": "福州"
  },
  "realtime": {
    "weather": "晴",
    "temperature": "25"
  },
  "forecast": [
    {
      "date": "2023-10-01",
      "day_weather": "晴",
      "night_weather": "晴",
      "max_temp": "26",
      "min_temp": "18"
    },
    {
      "date": "2023-10-02",
      "day_weather": "多云",
      "night_weather": "多云",
      "max_temp": "25",
      "min_temp": "17"
    },
    {
      "date": "2023-10-03",
      "day_weather": "小雨",
      "night_weather": "小雨",
      "max_temp": "23",
      "min_temp": "16"
    }
  ]
}
```


注意：请根据您的实际文件路径调整上述配置中的路径。

## 注意事项

- **必须设置环境变量`WEATHER_API_KEY`**才能运行服务
- 在网络服务器上部署时，确保服务器的防火墙已开放相应端口
- 为了提高安全性，建议在生产环境中使用HTTPS协议
- 生产环境中建议使用WSGI服务器（如gunicorn）来运行服务，以提高性能和稳定性
- 请妥善保管您的API密钥，不要在代码中硬编码或提交到版本控制系统中