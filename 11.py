import requests

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

def get_forecast_weather(api_key, location):
    """获取天气预报信息"""
    url = "https://devapi.heweather.net/v7/weather/3d"
    params = {
        "key": api_key,
        "location": location
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main():
    api_key = ""#your api key
    
    # 获取用户输入的地区名称
    location_name = input("请输入地区名称（如：福建）：")
    
    # 获取地区ID
    location_id, location_name = get_location_id(location_name, api_key)
    
    if location_id:
        print(f"已找到地区：{location_name}，ID：{location_id}")
        
        # 获取实时天气和天气预报
        realtime_weather = get_realtime_weather(api_key, location_id)
        forecast_weather = get_forecast_weather(api_key, location_id)
        
        if realtime_weather and forecast_weather:
            print(f"实时天气：{realtime_weather['now']['text']}，温度：{realtime_weather['now']['temp']}℃")
            print("未来三天天气预报：")
            for day in forecast_weather['daily']:
                print(f"{day['fxDate']}：白天{day['textDay']}，夜间{day['textNight']}，最高温度{day['tempMax']}℃，最低温度{day['tempMin']}℃")
        else:
            print("获取天气数据失败")
    else:
        print("未找到该地区，请检查输入是否正确")

if __name__ == "__main__":
    main()