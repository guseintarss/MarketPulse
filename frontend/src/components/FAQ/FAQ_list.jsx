import { useState, useRef, useEffect } from 'react';

const FAQ_list = (props) => {
  // Состояние: индекс открытого вопроса (null = все закрыты)
  const [openIndex, setOpenIndex] = useState(null);

  // Данные вопросов (вынесем в массив — так чище и масштабируемее)
  const faqItems = [
    {
      question: "Какие площадки поддерживает MarketPulse?",
      answer: "Мы поддерживаем Wildberries, Ozon, Avito, Яндекс Маркет, AliExpress, MegaMarket, а также ряд региональных маркетплейсов и досок объявлений. Список площадок постоянно расширяется."
    },
    {
      question: "Как часто обновляются данные?",
      answer: "Частота обновления зависит от тарифа: на бесплатном — раз в сутки, на Профессиональном — каждые 15 минут, на Корпоративном — в реальном времени."
    },
    {
      question: "Нужно ли подключать мои магазины?",
      answer: "Нет, для базового мониторинга конкурентов подключение вашего магазина не требуется. Вы просто указываете товары или категории, которые хотите отслеживать. Подключение нужно только для функции автоценообразования."
    },
    {
      question: "Есть ли бесплатный тариф?",
      answer: "Да! Стартовый тариф полностью бесплатный и позволяет отслеживать до 50 товаров на 2 маркетплейсах. Кроме того, на платных тарифах доступен 14-дневный бесплатный trial."
    },
    {
      question: "Могу ли я интегрировать MarketPulse с моей CRM?",
      answer: "Да, на тарифах Профессиональный и Корпоративный доступен REST API и вебхуки. Мы также имеем готовые интеграции с популярными CRM-системами и сервисами аналитики."
    }
  ];

  // Обработчик клика: открываем нажатый, закрываем остальные
  const handleClick = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="faq-list">
      {faqItems.map((item, index) => (
        <FaqItem
          key={index}
          question={item.question}
          answer={item.answer}
          isOpen={openIndex === index}
          onToggle={() => handleClick(index)}
        />
      ))}
    </div>
  );
};

// Отдельный компонент для одного элемента (переиспользуемый)
const FaqItem = ({ question, answer, isOpen, onToggle }) => {
  const answerRef = useRef(null);
  const [maxHeight, setMaxHeight] = useState('0px');

  // Обновляем высоту при изменении состояния или контента
  useEffect(() => {
    if (answerRef.current) {
      setMaxHeight(isOpen ? `${answerRef.current.scrollHeight}px` : '0px');
    }
  }, [isOpen, answer]);

  return (
    <div className={`faq-item ${isOpen ? 'active' : ''}`}>
      <button
        className="faq-question"
        onClick={onToggle}
        aria-expanded={isOpen}
      >
        {question}
        <span className={`faq-icon ${isOpen ? 'rotate-45' : ''}`}>+</span>
      </button>
      
      <div
        ref={answerRef}
        className="faq-answer"
        style={{ maxHeight }}
      >
        <p>{answer}</p>
      </div>
    </div>
  );
};

export default FAQ_list;