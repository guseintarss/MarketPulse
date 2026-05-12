# test_parser.py
import asyncio
import sys
from avito_parser import AvitoParser

async def main():
    # Замените на реальную ссылку с Avito для теста
    test_url = "https://www.avito.ru/cherkessk/tovary_dlya_kompyutera/samsung_860_evo_1tb_original_zdorove_66_7901741841?context=H4sIAAAAAAAA_wE_AMD_YToyOntzOjEzOiJsb2NhbFByaW9yaXR5IjtiOjA7czoxOiJ4IjtzOjE2OiJNaFdUclVuUk1vMDVoTk5PIjt99EsP9z8AAAA"
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
    
    parser = AvitoParser(delay=3.0)
    
    try:
        result = await parser.parse(test_url)
        print("\n✅ Результат парсинга:")
        print(result.model_dump_json(indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())