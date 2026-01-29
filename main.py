import requests
import os
import webbrowser
import time

def save_to_html(data, filename="osint_result.html"):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>OSINT Результаты</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }}
            h1 {{ color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
            .section {{ background: #2d2d2d; padding: 20px; margin: 20px 0; border-radius: 10px; border-left: 4px solid #4CAF50; }}
            .item {{ margin: 10px 0; padding: 8px; background: #3d3d3d; border-radius: 5px; }}
            .found {{ color: #4CAF50; }}
            .not-found {{ color: #ff4444; }}
            .error {{ color: #ffaa00; }}
            .timestamp {{ color: #aaa; font-size: 12px; text-align: right; }}
        </style>
    </head>
    <body>
        <h1>OSINT Результаты проверки</h1>
        <div class="timestamp">Создано: {time.strftime("%Y-%m-%d %H:%M:%S")}</div>
    """
    
    for section in data:
        html_content += f'<div class="section"><h2>{section["title"]}</h2>'
        for item in section["content"]:
            status_class = ""
            if "СУЩЕСТВУЕТ" in item or "✓" in item:
                status_class = "found"
            elif "не найден" in item or "✗" in item:
                status_class = "not-found"
            elif "ошибка" in item or "!" in item or "?" in item:
                status_class = "error"
            
            item_text = item.replace("✓", "✅").replace("✗", "❌").replace("!", "⚠️")
            html_content += f'<div class="item {status_class}">{item_text}</div>'
        html_content += '</div>'
    
    html_content += """
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def ipsearch(ip_address):
    def get_ip_info(ip_address):
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)
        data = response.json()
        return data

    def get_ip_type(ip_address):
        url = f"https://ipwho.is/{ip_address}"
        response = requests.get(url)
        ip_info = response.json()
        return ip_info

    results = []
    
    print("╔" + "─" * 65 + "╗")
    print("◆ ОБЩАЯ ИНФОРМАЦИЯ:")
    results.append({"title": "Информация об IP", "content": []})
    
    ip_info = get_ip_info(ip_address)
    
    if 'ip' in ip_info:
        print(f"◆ [+] IP-адрес: {ip_info['ip']}")
        results[-1]["content"].append(f"◆ [+] IP-адрес: {ip_info['ip']}")
        ip_type_info = get_ip_type(ip_address)
    else:
        print("◆ [-] IP-адрес недоступен")
        results[-1]["content"].append("◆ [-] IP-адрес недоступен")

    print(f"◆ [+] Город: {ip_info.get('city', 'недоступен')}")
    results[-1]["content"].append(f"◆ [+] Город: {ip_info.get('city', 'недоступен')}")
    
    print(f"◆ [+] Регион: {ip_info.get('region', 'недоступен')}")
    results[-1]["content"].append(f"◆ [+] Регион: {ip_info.get('region', 'недоступен')}")
    
    print(f"◆ [+] Континент: {ip_type_info.get('continent', 'недоступен')} {ip_type_info.get('continent_code', '')}")
    results[-1]["content"].append(f"◆ [+] Континент: {ip_type_info.get('continent', 'недоступен')} {ip_type_info.get('continent_code', '')}")
    
    print(f"◆ [+] Страна: {ip_type_info.get('country', 'недоступна')} {ip_type_info.get('country_code', '')}")
    results[-1]["content"].append(f"◆ [+] Страна: {ip_type_info.get('country', 'недоступна')} {ip_type_info.get('country_code', '')}")
    
    print(f"◆ [+] Почтовый Индекс: {ip_type_info.get('postal', 'недоступен')}")
    results[-1]["content"].append(f"◆ [+] Почтовый Индекс: {ip_type_info.get('postal', 'недоступен')}")
    
    print(f"◆ [+] Часовой пояс: {ip_info.get('timezone', 'недоступен')}")
    results[-1]["content"].append(f"◆ [+] Часовой пояс: {ip_info.get('timezone', 'недоступен')}")

    print("◆ ГЕОЛОКАЦИЯ:")
    if 'loc' in ip_info:
        latitude, longitude = ip_info['loc'].split(',')
        print(f"◆ [+] Координаты: {ip_info['loc']}")
        results[-1]["content"].append(f"◆ [+] Координаты: {ip_info['loc']}")
        
        google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
        yandex_maps_url = f"https://yandex.ru/maps/?ll={longitude},{latitude}&z=10"
        
        print(f"◆ [+] Ссылка на Google Maps: {google_maps_url}")
        results[-1]["content"].append(f"◆ [+] Ссылка на Google Maps: {google_maps_url}")
        print(f"◆ [+] Ссылка на Yandex Maps: {yandex_maps_url}")
        results[-1]["content"].append(f"◆ [+] Ссылка на Yandex Maps: {yandex_maps_url}")
    else:
        print("◆ [-] Координаты недоступны")
        results[-1]["content"].append("◆ [-] Координаты недоступны")

    print("◆ ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ:")
    print(f"◆ [+] Тип IP-адреса: {ip_type_info.get('type', 'недоступен')}")
    results[-1]["content"].append(f"◆ [+] Тип IP-адрес: {ip_type_info.get('type', 'недоступен')}")
    
    print(f"◆ [+] Hostname: {ip_info.get('hostname', 'недоступен')}")
    results[-1]["content"].append(f"◆ [+] Hostname: {ip_info.get('hostname', 'недоступен')}")
    
    print(f"◆ [+] Организация: {ip_info.get('org', 'недоступна')}")
    results[-1]["content"].append(f"◆ [+] Организация: {ip_info.get('org', 'недоступна')}")

    print("◆ ПОИСК IP В IoT:")
    results.append({"title": "Ссылки для проверки IP", "content": []})
    
    shodan_url = f"https://www.shodan.io/search?query={ip_address}"
    censys_url = f"https://censys.io/ipv4/{ip_address}"
    zoomeye_url = f"https://www.zoomeye.org/searchResult?q={ip_address}"
    criminalip_url = f"https://www.criminalip.io/asset/report/{ip_address}"
    virustotal_url = f"https://www.virustotal.com/gui/ip-address/{ip_address}"

    print(f"◆ [+] Shodan: {shodan_url}")
    results[-1]["content"].append(f"◆ [+] Shodan: {shodan_url}")
    print(f"◆ [+] Censys: {censys_url}")
    results[-1]["content"].append(f"◆ [+] Censys: {censys_url}")
    print(f"◆ [+] Zoomeye: {zoomeye_url}")
    results[-1]["content"].append(f"◆ [+] Zoomeye: {zoomeye_url}")
    print(f"◆ [+] CriminalIP: {criminalip_url}")
    results[-1]["content"].append(f"◆ [+] CriminalIP: {criminalip_url}")
    print(f"◆ [+] VirusTotal: {virustotal_url}")
    results[-1]["content"].append(f"◆ [+] VirusTotal: {virustotal_url}")
    
    print("╚" + "─" * 65 + "╝")
    
    return results

def search_username(username):
    results = []
    
    print("=== OSINT Link Generator ===")
    print(f"Проверка username: {username}")
    
    results.append({"title": "Проверка username", "content": [f"Username: {username}"]})
    
    templates = [
        ("VK", f"https://vk.com/{username}"),
        ("VK (ID)", f"https://vk.com/id{username}"),
        ("Telegram", f"https://t.me/{username}"),
        ("Instagram", f"https://instagram.com/{username}"),
        ("GitHub", f"https://github.com/{username}"),
        ("YouTube", f"https://youtube.com/@{username}"),
        ("Steam", f"https://steamcommunity.com/id/{username}"),
        ("Pinterest", f"https://pinterest.com/{username}"),
        ("Twitch", f"https://twitch.tv/{username}"),
        ("TikTok", f"https://tiktok.com/@{username}"),
    ]
    
    print("\n[+] Сгенерированные ссылки:")
    results.append({"title": "Сгенерированные ссылки", "content": []})
    
    for i, (site, url) in enumerate(templates, 1):
        print(f"{i:2}. {site:15} {url}")
        results[-1]["content"].append(f"{site}: {url}")
    
    print("\n[+] Проверка существования профилей...")
    results.append({"title": "Результаты проверки профилей", "content": []})
    
    for site, url in templates:
        try:
            r = requests.head(url, timeout=3)
            if r.status_code == 200:
                result_text = f"✓ {site}: СУЩЕСТВУЕТ - {url}"
                print(result_text)
                results[-1]["content"].append(result_text)
            elif r.status_code == 404:
                result_text = f"✗ {site}: не найден"
                print(result_text)
                results[-1]["content"].append(result_text)
            else:
                result_text = f"? {site}: код {r.status_code}"
                print(result_text)
                results[-1]["content"].append(result_text)
        except Exception as e:
            result_text = f"! {site}: ошибка проверки"
            print(result_text)
            results[-1]["content"].append(result_text)
    
    return results

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                  OSINT TOOL v1.0                         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    print("Выберите тип поиска:")
    print("1. Поиск по IP-адресу")
    print("2. Поиск по username")
    print()
    
    choice = input("Введите номер выбора (1 или 2): ").strip()
    
    results = []
    
    if choice == "1":
        ip_address = input("\nВведите IP-адрес: ").strip()
        results = ipsearch(ip_address)
    elif choice == "2":
        username = input("\nВведите username: ").strip()
        results = search_username(username)
    else:
        print("Неверный выбор!")
        return
    
    print("\n" + "═" * 60)
    print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
    print("═" * 60)
    
    save_choice = input("\nСохранить результаты в HTML файл? (y/N): ").lower()
    
    if save_choice == 'y':
        filename = save_to_html(results)
        print(f"\nРезультаты сохранены в файл: {filename}")
        
        open_choice = input("\nОткрыть файл в браузере? (y/N): ").lower()
        if open_choice == 'y':
            webbrowser.open(f'file://{os.path.abspath(filename)}')
            print("Файл открывается в браузере...")
    else:
        print("Результаты не сохранены.")
    
    print("\n" + "═" * 60)
    print("ПРОВЕРКА ЗАВЕРШЕНА")
    print("═" * 60)

if __name__ == "__main__":
    main()
