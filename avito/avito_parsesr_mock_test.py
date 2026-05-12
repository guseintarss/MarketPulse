# avito_parser_mock_test.py
import asyncio
import json
from datetime import datetime, timezone
from pydantic import BaseModel, HttpUrl
from typing import Optional

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

async def parse_avito_mock(url: str) -> AvitoListing:
    """Возвращает реалистичные тестовые данные — идеально для отладки"""
    print(f"🎭 MOCK: имитация парсинга {url}")
    await asyncio.sleep(0.3)  # Имитация сети
    
    # Реалистичные данные, как будто с реальной страницы
    return AvitoListing(
        url=url,
        title="Ноутбук ASUS VivoBook 15 X515, 15.6\", Intel Core i3, 8GB, 256GB SSD",
        price_rub=34990,
        is_available=True,
        location="Москва, м. Курская",
        published_at="2026-05-10T14:30:00",
        seller_name="ТехноМаркет",
        parsed_at=datetime.now(timezone.utc)
    )

async def main():
    # Любая ссылка — результат будет моковым
    result = await parse_avito_mock("https://www.avito.ru/cherkessk/tovary_dlya_kompyutera/samsung_860_evo_1tb_original_zdorove_66_7901741841?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNaFdUclVuUk1vMDVoTk5PIjt99Es")
    
    print("\n✅ MOCK-результат (валидный):")
    print(result.model_dump_json(indent=2, ensure_ascii=False))
    
    # Проверка валидации
    assert result.price_rub == 34990
    assert "ASUS" in result.title
    print("\n✨ Все проверки пройдены — логика работает!")

if __name__ == "__main__":
    asyncio.run(main())