import os
import datetime
import requests
import telebot
from flask import Flask
from threading import Thread

# =====================================================================
# 1. КОНФИГУРАЦИЯ СИСТЕМЫ (searchHams Engine)
# =====================================================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
VK_API_TOKEN = os.environ.get("VK_API_TOKEN")

WATERMARK = "⚡ SEARCHHAMS_INTEL_SYSTEM_v5.5_LIVE ⚡"

if not TELEGRAM_TOKEN:
    raise ValueError("Critical Error: TELEGRAM_TOKEN variable is not set.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# =====================================================================
# 2. ВЕБ-СЕРВЕР ДЛЯ ОБХОДА ТАЙМАУТА ПОРТОВ (БЕСПЛАТНЫЙ ТАРИФ)
# =====================================================================
app = Flask('')

@app.route('/')
def home():
    return "searchHams Core Status: ONLINE"

def run_web_server():
    # Автоматическое связывание с портом, который ожидает Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# =====================================================================
# 3. ИНТЕРФЕЙС И ВИЗУАЛИЗАЦИЯ (Фиолетово-серый код IntelScry-style)
# =====================================================================
def build_intel_report(query_type: str, query_value: str, sections: dict) -> str:
    border = "=" * 55
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"```yaml\n"
    report += f"{border}\n"
    report += f"🔑 {WATERMARK}\n"
    report += f"📊 TIMESTAMP : {timestamp}\n"
    report += f"🎯 TARGET    : [{query_type.upper()}] -> {query_value}\n"
    report += f"{border}\n\n"
    
    for section_title, fields in sections.items():
        report += f"[{section_title.upper()}]\n"
        if isinstance(fields, dict):
            for key, val in fields.items():
                report += f"  ├── {key.ljust(18)}: {val}\n"
        elif isinstance(fields, list):
            for item in fields:
                report += f"  ├── {item}\n"
        else:
            report += f"  └── status            : {fields}\n"
        report += "\n"
        
    report += f"{border}\n"
    report += f"🔒 END OF DATA STREAM // SEARCHHAMS ENGINE SECURED\n"
    report += f"```"
    return report

# =====================================================================
# 4. ПОИСКОВЫЕ МОДУЛИ ПО ОТКРЫТЫМ ИСТОЧНИКАМ (РЕАЛЬНЫЕ API)
# =====================================================================

def query_by_username(username: str) -> dict:
    """Проверка доступности имени пользователя на открытых платформах"""
    clean_user = username.replace("@", "").strip()
    services = {
        "Telegram_Core": f"https://t.me{clean_user}",
        "GitHub_Dev": f"https://github.com{clean_user}",
        "VK_Social": f"https://vk.com{clean_user}",
        "Reddit_Forum": f"https://reddit.com{clean_user}"
    }
    results = {}
    for platform, url in services.items():
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=3, allow_redirects=True)
            results[platform] = f"FOUND // {url}" if response.status_code == 200 and clean_user.lower() in response.text.lower() else "NOT_DETECTED"
        except Exception:
            results[platform] = "RESPONSE_TIMEOUT"
    return results

def query_by_ip(ip: str) -> dict:
    """Глубокий технический анализ IP через публичный шлюз ip-api"""
    try:
        url = f"http://ip-api.com{ip.strip()}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        res = requests.get(url, timeout=4).json()
        if res.get("status") == "success":
            return {
                "ip_query_address": res.get("query"),
                "asn_routing": res.get("as", "N/A"),
                "isp_provider": res.get("isp", "Unknown ISP"),
                "organization": res.get("org", "N/A"),
                "country_location": f"{res.get('country')} ({res.get('countryCode')})",
                "region_state": f"{res.get('regionName')} ({res.get('region')})",
                "city_district": res.get("city", "Unknown"),
                "postal_index": res.get("zip", "N/A"),
                "geo_coordinates": f"{res.get('lat')}, {res.get('lon')}",
                "timezone_node": res.get("timezone", "Unknown")
            }
    except Exception as e:
        return {"error_log": str(e)}
    return {"status": "No public database found"}

def query_by_vk(target: str) -> dict:
    """Запрос открытых параметров профиля VK через официальное API"""
    if not VK_API_TOKEN:
        return {"api_status": "Token missing"}
    clean_id = target.replace("https://vk.com", "").replace("@", "").strip()
    url = "https://vk.com"
    params = {
        "user_ids": clean_id,
        "fields": "verified,bdate,city,status,counters,last_seen,followers_count",
        "access_token": VK_API_TOKEN,
        "v": "5.131"
    }
    try:
        data = requests.get(url, params=params, timeout=4).json()
        if "response" in data and len(data["response"]) > 0:
            user = data["response"][0]
            counters = user.get("counters", {})
            return {
                "account_uid": user.get("id"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "is_verified_badge": "TRUE" if user.get("verified") == 1 else "FALSE",
                "birth_date_field": user.get("bdate", "NOT_SET"),
                "city_title": user.get("city", {}).get("title", "NOT_SET"),
                "profile_status": user.get("status", "NONE"),
                "friends_total": counters.get("friends", 0),
                "followers_total": user.get("followers_count", counters.get("followers", 0))
            }
    except Exception as e:
        return {"error_log": str(e)}
    return {"status": "Profile restricted"}

def query_by_phone(phone: str) -> dict:
    """Анализ реестра номеров по открытым DEF-кодам сотовых операторов"""
    clean_phone = "".join(filter(str.isdigit, phone))
    try:
        url = f"https://htmlweb.ru{clean_phone}"
        res = requests.get(url, timeout=4).json()
        if "country" in res or "region" in res:
            return {
                "phone_raw_format": f"+{clean_phone}",
                "country_origin": res.get("country", {}).get("name", "Russia"),
                "region_allocation": res.get("region", {}).get("name", "Undefined"),
                "carrier_provider": res.get("0", {}).get("oper", "Unknown Operator"),
                "timezone_offset": f"UTC+{res.get('region', {}).get('tz', '3')}"
            }
    except Exception:
        pass
    return {"phone_raw_format": f"+{clean_phone}", "country_origin": "Russian Federation"}

def query_by_ton(wallet: str) -> dict:
    """Парсинг открытого баланса кошелька через официальное API блокчейна TON"""
    try:
        url = f"https://tonapi.io{wallet.strip()}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            raw_balance = float(data.get("balance", 0)) / 10**9
            return {
                "wallet_address": data.get("address", wallet),
                "account_state": data.get("status", "active"),
                "wallet_balance_ton": f"{raw_balance:.4f} TON",
                "is_scam_reported": "TRUE" if data.get("is_scam") else "FALSE"
            }
    except Exception as e:
        return {"error_log": str(e)}
    return {"status": "Wallet invalid"}
# =====================================================================
# 5. ОБРАБОТЧИКИ КОМАНД ТЕЛЕГРАМ (Личный интерфейс searchHams)
# =====================================================================

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "🤖 **Личный OSINT-интерфейс searchHams запущен.**\n\n"
        "Отправьте команду вместе со значением для проведения поиска:\n"
        "🔹 `/user <username>` — Поиск по юзернейму в сети\n"
        "🔹 `/ip <address>` — Сбор данных о сетевом адресе\n"
        "🔹 `/vk <id_or_screen_name>` — Анализ открытого профиля ВК\n"
        "🔹 `/phone <number>` — Определение оператора номера\n"
        "🔹 `/ton <wallet_address>` — Проверка баланса TonKeeper"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['user'])
def cmd_user(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: 
        return bot.reply_to(message, "Введите юзернейм.")
    target = args[1].strip()
    data = query_by_username(target)
    report = build_intel_report("searchHams OSINT // Username", target, {"footprint_detected": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['ip'])
def cmd_ip(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: 
        return bot.reply_to(message, "Введите IP.")
    target = args[1].strip()
    data = query_by_ip(target)
    report = build_intel_report("searchHams OSINT // IP Routing", target, {"geo_positioning": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['vk'])
def cmd_vk(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: 
        return bot.reply_to(message, "Введите ID VK.")
    target = args[1].strip()
    data = query_by_vk(target)
    report = build_intel_report("searchHams OSINT // VK Profile", target, {"profile_metadata": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['phone'])
def cmd_phone(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: 
        return bot.reply_to(message, "Введите номер телефона.")
    target = args[1].strip()
    data = query_by_phone(target)
    report = build_intel_report("searchHams OSINT // Telecom Core", target, {"cellular_registry": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['ton'])
def cmd_ton(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: 
        return bot.reply_to(message, "Введите адрес TON.")
    target = args[1].strip()
    data = query_by_ton(target)
    report = build_intel_report("searchHams OSINT // TonKeeper Blockchain", target, {"ledger_state": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

# =====================================================================
# 6. ЗАПУСК ДВУХ ПОТОКОВ (СЕРВЕР + БОТ)
# =====================================================================
if __name__ == '__main__':
    # Поток 1: Запуск локального сервера Flask для прохождения проверки Render
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    print("[SYSTEM] Фоновый веб-сервер успешно запущен на локальном хосте...")
    
    # Поток 2: Запуск основного цикла Long Polling для обработки команд бота
    print("[SYSTEM] Система searchHams успешно инициализирована...")
    bot.infinity_polling()
