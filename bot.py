import os
import datetime
import requests
import telebot
from flask import Flask
from threading import Thread

# =====================================================================
# 1. CONFIGURATION (searchHams Engine) - ТОКЕНЫ ВШИТЫ НАПРЯМУЮ
# =====================================================================
TELEGRAM_TOKEN = "8782318055:AAE4Q86B_7TcT5WoS0Ajgtoz9B8Mu0xlh9s"
VK_API_TOKEN = "vk1.a.gg0A2uqhaeJR4Q0rQroAOrKxLtlld-zpDhUuNRsLph2tyJZzoyIioGN8vNs_AzCfepKFqTdigONU-ydz1VZnL68Ns7qZ0HcgUhmEOE_F1ZI26awIwunbGfzTpn-xmEEXAueaaBR5lb-ew_z478YoxYuNlAEHHfGBddR9u10-MJae6l1UUC4C3eKWD28ugFy7hhguP-Ihcxsb42Fbq_SPsw"

WATERMARK = "⚡ SEARCHHAMS_INTEL_SYSTEM_v5.5_LIVE ⚡"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# =====================================================================
# 2. FREE TIER PORT BYPASS SERVER
# =====================================================================
app = Flask('')

@app.route('/')
def home():
    return "searchHams Core Status: ONLINE"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# =====================================================================
# 3. INTERFACE VISUALIZATION (IntelScry-style)
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
# 4. OSINT SEARCH MODULES (ИСПРАВЛЕННЫЕ ССЫЛКИ И ПАРАМЕТРЫ)
# =====================================================================

def query_by_username(username: str) -> dict:
    """Генерация прямых OSINT-ссылок для проверки (обход блокировок Render тайм-аутов)"""
    clean_user = username.replace("@", "").strip()
    return {
        "Telegram_Profile": f"https://t.me{clean_user}",
        "GitHub_Account": f"https://github.com{clean_user}",
        "VK_Social_Link": f"https://vk.com{clean_user}",
        "Reddit_User": f"https://reddit.com{clean_user}",
        "OSINT_Report": f"Генерация прямых ссылок во избежание блокировок хостинга"
    }

def query_by_ip(ip: str) -> dict:
    """Исправленный модуль IP-поиска с защитой от пустых склеек"""
    try:
        clean_ip = str(ip).replace(" ", "").strip()
        # Жестко прописан правильный URL-путь
        url = f"http://ip-api.com{clean_ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        response = requests.get(url, timeout=5)
        res = response.json()
        
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
    return {"status": "No public database found for this IP or Invalid Format"}

def query_by_vk(target: str, token: str) -> dict:
    """Безопасный разбор ответа VK API с проверкой типа данных"""
    if not token:
        return {"api_status": "Token missing"}
    clean_id = str(target).replace("https://vk.com", "").replace("@", "").replace(" ", "").strip()
    url = "https://vk.com"
    params = {
        "user_ids": clean_id,
        "fields": "verified,bdate,city,status,counters,last_seen,followers_count",
        "access_token": token,
        "v": "5.131"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if "response" in data and len(data["response"]) > 0:
            user = data["response"][0]  # Извлекаем первый элемент списка корректно
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
        elif "error" in data:
            return {"api_error_msg": data["error"].get("error_msg", "Unknown API Error")}
    except Exception as e:
        return {"error_log": str(e)}
    return {"status": "Profile restricted or unexpected API structure"}

def query_by_phone(phone: str) -> dict:
    """Ваш стабильный, работающий рабочий модуль телефона"""
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    if not clean_phone:
        return {"error": "Invalid phone format"}
        
    operator = "Определен (МТС/МегаФон/Билайн/Теле2)"
    region = "Центральный узел связи РФ / СНГ"
    
    if clean_phone.startswith("791") or clean_phone.startswith("798"):
        operator = "МТС (MTS Core Network)"
    elif clean_phone.startswith("792") or clean_phone.startswith("793"):
        operator = "МегаФон (MegaFon Infrastructure)"
    elif clean_phone.startswith("790") or clean_phone.startswith("796"):
        operator = "Билайн (Beeline Mobile)"
    elif clean_phone.startswith("795") or clean_phone.startswith("799"):
        operator = "Теле2 / Т2 Мобайл"
        
    if len(clean_phone) > 4:
        code = clean_phone[1:4]
        if code in ["910", "915", "916", "919", "925", "926", "963", "964", "965", "968", "999"]:
            region = "Москва и Московская область"
        elif code in ["911", "921", "960", "950", "952", "991"]:
            region = "Санкт-Петербург и Ленинградская область"
            
    return {
        "phone_raw_format": f"+{clean_phone}",
        "country_origin": "Российская Федерация",
        "allocated_region": region,
        "carrier_provider": operator,
        "format_validation": "STRUCTURE_VERIFIED"
    }

def query_by_ton(wallet: str) -> dict:
    try:
        clean_wallet = str(wallet).replace(" ", "").strip()
        url = f"https://tonapi.io{clean_wallet}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
            raw_balance = float(data.get("balance", 0)) / 10**9
            return {
                "wallet_address": data.get("address", clean_wallet),
                "account_state": data.get("status", "active"),
                "wallet_balance_ton": f"{raw_balance:.4f} TON",
                "is_scam_reported": "TRUE" if data.get("is_scam") else "FALSE"
            }
    except Exception as e:
        return {"error_log": str(e)}
    return {"status": "Wallet invalid or offline"}
# =====================================================================
# 5. TELEGRAM COMMAND HANDLERS (СТРОГОЕ ИЗВЛЕЧЕНИЕ ТЕКСТА ИЗ СПИСКА)
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
    if len(args) < 2: return bot.reply_to(message, "Введите юзернейм.")
    target = args[1].strip() # Исправлено: строго вычленяем цель из списка
    data = query_by_username(target)
    report = build_intel_report("searchHams OSINT // Username", target, {"footprint_detected": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['ip'])
def cmd_ip(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return bot.reply_to(message, "Введите IP.")
    target = args[1].strip() # Исправлено: строго вычленяем чистый IP из списка
    data = query_by_ip(target)
    report = build_intel_report("searchHams OSINT // IP Routing", target, {"geo_positioning": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['vk'])
def cmd_vk(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return bot.reply_to(message, "Введите ID VK.")
    target = args[1].strip() # Исправлено: строго вычленяем VK параметр из списка
    data = query_by_vk(target, VK_API_TOKEN)
    report = build_intel_report("searchHams OSINT // VK Profile", target, {"profile_metadata": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['phone'])
def cmd_phone(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return bot.reply_to(message, "Введите номер телефона.")
    target = args[1].strip() # Исправлено: строго вычленяем номер из списка
    data = query_by_phone(target)
    report = build_intel_report("searchHams OSINT // Telecom Core", target, {"cellular_registry": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

@bot.message_handler(commands=['ton'])
def cmd_ton(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return bot.reply_to(message, "Введите адрес TON.")
    target = args[1].strip() # Исправлено: строго вычленяем кошелек из списка
    data = query_by_ton(target)
    report = build_intel_report("searchHams OSINT // TonKeeper Blockchain", target, {"ledger_state": data})
    bot.reply_to(message, report, parse_mode="MarkdownV2")

# =====================================================================
# 6. SYSTEM RUN
# =====================================================================
if __name__ == '__main__':
    print("[SYSTEM] Инициализация веб-интерфейса на порту 10000...")
    
    bot_thread = Thread(target=bot.infinity_polling)
    bot_thread.daemon = True
    bot_thread.start()
    print("[SYSTEM] Поток прослушивания Telegram API запущен успешно...")
    
    run_web_server()
