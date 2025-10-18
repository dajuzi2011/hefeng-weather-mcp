import os
import requests
from fastmcp import FastMCP

# 创建MCP服务器实例
mcp = FastMCP("Weather Service")

# 从环境变量中获取API密钥
def get_api_key():
    """从环境变量中获取API密钥"""
    # 从环境变量获取
    api_key = os.environ.get('WEATHER_API_KEY')
    # 如果环境变量不存在，抛出错误
    if not api_key:
        raise EnvironmentError("错误：未在环境变量中找到WEATHER_API_KEY。请设置环境变量后再运行服务。")
    return api_key

def get_location_id(location_name, api_key):
    """获取指定地区的ID"""
    api_url = "https://geoapi.qweather.com/v2/city/lookup"
    params = {
        "location": location_name,
        "key": api_key
    }
    
    response = requests.get(api_url, params=params)
    data = response.json()
    
    if data.get("code") == "200" and data.get("location"):
        # 提取第一个地区的id
        return data["location"][0]["id"], data["location"][0]["name"]
    else:
        return None, None

def get_realtime_weather(api_key, location):
    """获取实时天气信息"""
    url = "https://devapi.heweather.net/v7/weather/now"
    params = {
        "key": api_key,
        "location": location
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast_weather(api_key, location, days="3d"):
    """获取天气预报信息"""
    # 验证days参数是否有效
    valid_days = ["3d", "7d", "10d", "15d", "30d"]
    if days not in valid_days:
        days = "3d"  # 默认使用3天预报
        
    url = f"https://devapi.heweather.net/v7/weather/{days}"
    params = {
        "key": api_key,
        "location": location
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@mcp.tool()
def get_location_info(location_name: str) -> str:
    """
    获取指定地区的ID和名称信息
    
    参数:
        location_name: 地区名称，如"福建"、"北京"等
        
    返回:
        地区ID和名称的JSON格式字符串
    """
    api_key = get_api_key()
    location_id, location_name = get_location_id(location_name, api_key)
    
    if location_id:
        return f'{{"location_id": "{location_id}", "location_name": "{location_name}"}}'
    else:
        return '{"error": "未找到该地区，请检查输入是否正确"}'

@mcp.tool()
def get_realtime_weather_info(location_id: str) -> str:
    """
    获取指定地区的实时天气信息
    
    参数:
        location_id: 地区ID，如"101230101"
        
    返回:
        实时天气信息的JSON格式字符串
    """
    api_key = get_api_key()
    
    # 获取实时天气
    realtime_weather = get_realtime_weather(api_key, location_id)
    
    if realtime_weather:
        result = {
            "weather": realtime_weather['now']['text'],
            "temperature": realtime_weather['now']['temp'],
            "wind_dir": realtime_weather['now']['windDir'],
            "wind_scale": realtime_weather['now']['windScale'],
            "humidity": realtime_weather['now']['humidity'],
            "feels_like": realtime_weather['now']['feelsLike']
        }
        
        return str(result).replace("'", '"')
    else:
        return '{"error": "获取实时天气数据失败"}'

@mcp.tool()
def get_forecast_weather_info(location_id: str, days: str = "3d") -> str:
    """
    获取指定地区的天气预报
    
    参数:
        location_id: 地区ID，如"101230101"
        days: 预报天数，支持最多30天预报，可选值：3d（3天预报）、7d（7天预报）、10d（10天预报）、15d（15天预报）、30d（30天预报）
        
    返回:
        天气预报信息的JSON格式字符串
    """
    api_key = get_api_key()
    
    # 获取天气预报
    forecast_weather = get_forecast_weather(api_key, location_id, days)
    
    if forecast_weather:
        result = {
            "forecast": []
        }
        
        for day in forecast_weather['daily']:
            result["forecast"].append({
                "date": day['fxDate'],
                "day_weather": day['textDay'],
                "night_weather": day['textNight'],
                "max_temp": day['tempMax'],
                "min_temp": day['tempMin'],
                "sunrise": day.get('sunrise', ''),
                "sunset": day.get('sunset', ''),
                "moonrise": day.get('moonrise', ''),
                "moonset": day.get('moonset', ''),
                "wind_dir_day": day.get('windDirDay', ''),
                "wind_scale_day": day.get('windScaleDay', ''),
                "wind_dir_night": day.get('windDirNight', ''),
                "wind_scale_night": day.get('windScaleNight', ''),
                "humidity": day.get('humidity', ''),
                "precip": day.get('precip', ''),
                "pressure": day.get('pressure', ''),
                "vis": day.get('vis', ''),
                "uv_index": day.get('uvIndex', '')
            })
            
        return str(result).replace("'", '"')
    else:
        return '{"error": "获取天气预报数据失败"}'

@mcp.tool()
def get_weather_info(location_id: str) -> str:
    """
    获取指定地区的实时天气和未来三天的天气预报（整合功能）
    
    参数:
        location_id: 地区ID，如"101230101"
        
    返回:
        天气信息的JSON格式字符串
    """
    api_key = get_api_key()
    
    # 获取实时天气和天气预报（默认使用3天预报）
    realtime_weather = get_realtime_weather(api_key, location_id)
    forecast_weather = get_forecast_weather(api_key, location_id, "3d")
    
    if realtime_weather and forecast_weather:
        result = {
            "realtime": {
                "weather": realtime_weather['now']['text'],
                "temperature": realtime_weather['now']['temp']
            },
            "forecast": []
        }
        
        for day in forecast_weather['daily']:
            result["forecast"].append({
                "date": day['fxDate'],
                "day_weather": day['textDay'],
                "night_weather": day['textNight'],
                "max_temp": day['tempMax'],
                "min_temp": day['tempMin']
            })
            
        return str(result).replace("'", '"')
    else:
        return '{"error": "获取天气数据失败"}'

@mcp.tool()
def get_weather_by_location_name(location_name: str) -> str:
    """
    根据地区名称直接获取天气信息（整合了获取地区ID和天气信息的功能）
    
    参数:
        location_name: 地区名称，如"福建"、"北京"等
        
    返回:
        天气信息的JSON格式字符串
    """
    api_key = get_api_key()
    
    # 获取地区ID
    location_id, location_name = get_location_id(location_name, api_key)
    
    if not location_id:
        return '{"error": "未找到该地区，请检查输入是否正确"}'
    
    # 获取实时天气和天气预报（默认使用3天预报）
    realtime_weather = get_realtime_weather(api_key, location_id)
    forecast_weather = get_forecast_weather(api_key, location_id, "3d")
    
    if realtime_weather and forecast_weather:
        result = {
            "location": {
                "id": location_id,
                "name": location_name
            },
            "realtime": {
                "weather": realtime_weather['now']['text'],
                "temperature": realtime_weather['now']['temp']
            },
            "forecast": []
        }
        
        for day in forecast_weather['daily']:
            result["forecast"].append({
                "date": day['fxDate'],
                "day_weather": day['textDay'],
                "night_weather": day['textNight'],
                "max_temp": day['tempMax'],
                "min_temp": day['tempMin']
            })
            
        return str(result).replace("'", '"')
    else:
        return '{"error": "获取天气数据失败"}'

if __name__ == "__main__":
    # 默认使用STDIO模式，适合Claude Desktop直接调用
    # 如需使用SSE模式，请修改为：
    # mcp.run(transport='sse', port=8000)
    mcp.run()