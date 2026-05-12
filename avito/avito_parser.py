# avito_parser_safe.py
import re
import json
import asyncio
import random
import httpx
from datetime import datetime, timezone
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, HttpUrl
from bs4 import BeautifulSoup
from loguru import logger

# ==================== CONFIG ====================
class Config:
    MIN_DELAY = 4.0          # Мин. задержка между запросами (сек)
    MAX_DELAY = 12.0         # Макс. задержка при ретраях
    MAX_RETRIES = 3          # Сколько раз пробовать при 429/503
    TIMEOUT = 25.0           # Таймаут запроса
    USER_AGENTS = [         # Ротация User-Agent
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    ]

# ==================== MODEL ====================
class AvitoListing(BaseModel):
    url: HttpUrl
    title: str
    price_rub: Optional[int] = None
    is_available: bool = True
    location: Optional[str] = None
    published_at: Optional[str] = None
    seller_name: Optional[str] = None
    parsed_at: datetime
    model_config = {"extra": "ignore"}

# ==================== PARSER ====================
class AvitoParser:
    def __init__(self, proxy: Optional[str] = None, debug: bool = False):
        self.proxy = proxy
        self.debug = debug
        self._last_request_time = 0
        
    def _get_headers(self) -> Dict[str, str]:
        """Возвращает случайные заголовки для обхода детекта"""
        return {
            "User-Agent": random.choice(Config.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        }

    async def _rate_limit(self):
        """Rate limiting: ждём, если прошло мало времени с последнего запроса"""
        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request_time
        if elapsed < Config.MIN_DELAY:
            wait = Config.MIN_DELAY - elapsed + random.uniform(0.5, 2.0)
            if self.debug:
                print(f"⏱ Rate limit: жду {wait:.1f} сек")
            await asyncio.sleep(wait)
        self._last_request_time = asyncio.get_event_loop().time()

    async def _fetch(self, url: str) -> str:
        """Запрос с ретраями и обработкой 429"""
        await self._rate_limit()
        
        for attempt in range(Config.MAX_RETRIES):
            try:
                if self.debug:
                    print(f"🌐 Запрос #{attempt+1} к {url}")
                
                async with httpx.AsyncClient(
                    headers=self._get_headers(),
                    timeout=Config.TIMEOUT,
                    follow_redirects=True,
                    proxy=self.proxy
                ) as client:
                    resp = await client.get(url)
                    
                    # ✅ Успех
                    if resp.status_code == 200:
                        if self.debug:
                            print(f"✅ Получено {len(resp.text)} байт")
                        return resp.text
                    
                    # ⚠️ Rate limit — ждём и пробуем снова
                    if resp.status_code == 429:
                        retry_after = int(resp.headers.get("Retry-After", Config.MAX_DELAY))
                        wait = min(retry_after, Config.MAX_DELAY) * (2 ** attempt)
                        if self.debug:
                            print(f"⚠️ 429 Too Many Requests — жду {wait} сек перед ретраем")
                        await asyncio.sleep(wait)
                        continue
                    
                    # ⚠️ Другие ошибки клиента
                    if 400 <= resp.status_code < 500:
                        raise httpx.HTTPStatusError(
                            f"Client error {resp.status_code} — возможно, ссылка невалидна или заблокирована",
                            request=resp.request,
                            response=resp
                        )
                    
                    # ⚠️ Ошибки сервера — ретрай
                    if resp.status_code >= 500:
                        wait = (2 ** attempt) + random.uniform(1, 3)
                        if self.debug:
                            print(f"⚠️ Server error {resp.status_code} — ретрай через {wait} сек")
                        await asyncio.sleep(wait)
                        continue
                        
            except httpx.ConnectTimeout:
                if attempt == Config.MAX_RETRIES - 1:
                    raise Exception("Таймаут соединения — проверь интернет или добавь прокси")
                await asyncio.sleep(2 ** attempt)
                
            except httpx.ReadTimeout:
                if attempt == Config.MAX_RETRIES - 1:
                    raise Exception("Таймаут чтения — Avito не отвечает")
                await asyncio.sleep(2 ** attempt)
        
        raise Exception(f"Не удалось получить страницу после {Config.MAX_RETRIES} попыток")

    def _find_in_json(self, obj: Any, *keys: str) -> Optional[Any]:
        """Рекурсивный поиск значения по ключам в JSON"""
        if isinstance(obj, dict):
            for k in keys:
                if k in obj and obj[k]:
                    return obj[k]
            for v in obj.values():
                res = self._find_in_json(v, *keys)
                if res is not None:
                    return res
        elif isinstance(obj, list):
            for item in obj:
                res = self._find_in_json(item, *keys)
                if res is not None:
                    return res
        return None

    async def parse(self, url: str) -> AvitoListing:
        """Основной метод парсинга"""
        print(f"⏳ Парсинг: {url}")
        
        try:
            html = await self._fetch(url)
            soup = BeautifulSoup(html, "html.parser")

            # 🔍 DEBUG: покажи, что есть в странице
            if self.debug:
                print("\n🔍 DEBUG: Анализирую структуру...")
                json_ld = soup.find("script", type="application/ld+json")
                next_data = soup.find("script", id="__NEXT_DATA__")
                print(f"  • JSON-LD: {'✅' if json_ld else '❌'}")
                print(f"  • __NEXT_DATA__: {'✅' if next_data else '❌'}")
                if json_ld and self.debug:
                    print(f"  • JSON-LD preview: {(json_ld.string or json_ld.text)[:200]}...")

            # 1️⃣ JSON-LD (Schema.org) — самый стабильный источник
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or script.text)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        if item.get("@type") == "Product":
                            offers = item.get("offers", {})
                            price = offers.get("price")
                            return AvitoListing(
                                url=url,
                                title=item.get("name", "Unknown"),
                                price_rub=int(float(price)) if price else None,
                                is_available=offers.get("availability") == "https://schema.org/InStock",
                                parsed_at=datetime.now(timezone.utc)
                            )
                except (json.JSONDecodeError, TypeError, ValueError) as e:
                    if self.debug:
                        print(f"⚠️ JSON-LD parse error: {e}")

            # 2️⃣ __NEXT_DATA__ (Next.js)
            next_script = soup.find("script", id="__NEXT_DATA__")
            if next_script:
                try:
                    next_data = json.loads(next_script.string or next_script.text)
                    title = self._find_in_json(next_data, "title", "name", "itemTitle", "pageTitle")
                    price = self._find_in_json(next_data, "price", "priceValue", "value", "amount")
                    
                    if title:
                        return AvitoListing(
                            url=url,
                            title=title,
                            price_rub=int(price) if price and str(price).isdigit() else None,
                            parsed_at=datetime.now(timezone.utc)
                        )
                except (json.JSONDecodeError, TypeError) as e:
                    if self.debug:
                        print(f"⚠️ __NEXT_DATA__ parse error: {e}")

            # 3️⃣ Fallback: CSS-селекторы + meta-теги
            title_el = (
                soup.select_one('[data-marker="item-title"]') or
                soup.select_one('h1[itemprop="name"]') or
                soup.select_one('h1') or
                soup.select_one('meta[property="og:title"]')
            )
            price_el = (
                soup.select_one('[data-marker="item-price"]') or
                soup.select_one('[itemprop="price"]') or
                soup.select_one('meta[property="product:price:amount"]')
            )
            
            title = title_el.text.strip() if title_el and title_el.text else "Unknown"
            price_text = price_el.text.strip() if price_el and price_el.text else None
            if price_text:
                price_text = re.sub(r"[^\d]", "", price_text)
                price = int(price_text) if price_text else None
            else:
                price = None

            return AvitoListing(
                url=url,
                title=title,
                price_rub=price,
                parsed_at=datetime.now(timezone.utc)
            )

        except httpx.HTTPStatusError as e:
            print(f"❌ HTTP ошибка: {e}")
            return AvitoListing(url=url, title="HTTP_ERROR", parsed_at=datetime.now(timezone.utc))
        except Exception as e:
            print(f"❌ Ошибка парсинга: {type(e).__name__}: {e}")
            return AvitoListing(url=url, title="PARSE_ERROR", parsed_at=datetime.now(timezone.utc))

    async def parse_batch(self, urls: List[str]) -> List[AvitoListing]:
        """Парсинг списка ссылок с задержками"""
        results = []
        for i, url in enumerate(urls):
            try:
                print(f"\n[{i+1}/{len(urls)}] {url}")
                result = await self.parse(url)
                results.append(result)
                
                # Доп. задержка между товарами
                if i < len(urls) - 1:
                    extra_delay = random.uniform(2, 5)
                    print(f"⏱ Жду {extra_delay:.1f} сек перед следующим...")
                    await asyncio.sleep(extra_delay)
                    
            except Exception as e:
                print(f"❌ Пропуск {url}: {e}")
                results.append(AvitoListing(url=url, title="ERROR", parsed_at=datetime.now(timezone.utc)))
        return results

# ==================== RUN ====================
async def main():
    # 🔥 ЗАМЕНИ НА РЕАЛЬНУЮ ССЫЛКУ С AVITO
    # Важно: ссылка должна вести на карточку товара, а не на поиск!
    test_url = "https://www.avito.ru/moskva/tovary_dlya_kompyutera/noutbuk_asus_123456789"
    
    print("🚀 Avito Parser (Safe Mode)\n")
    
    parser = AvitoParser(debug=True)
    
    try:
        result = await parser.parse(test_url)
        print("\n📦 РЕЗУЛЬТАТ:")
        print(result.model_dump_json(indent=2, ensure_ascii=False))
        
        # Проверка качества
        if result.title in ["Unknown", "HTTP_ERROR", "PARSE_ERROR", "JS_REQUIRED"]:
            print("\n⚠️  Данные не извлечены. Возможные причины:")
            print("   • Ссылка ведёт не на карточку товара")
            print("   • Объявление удалено или скрыто")
            print("   • Avito требует выполнения JS → нужен Playwright")
            print("   • Блокировка по IP → добавь прокси")
            
    except KeyboardInterrupt:
        print("\n⚠️  Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())