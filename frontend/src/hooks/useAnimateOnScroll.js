// src/hooks/useAnimateOnScroll.js
import { useRef, useEffect } from 'react';

export const useAnimateOnScroll = (options = {}) => {
  const {
    threshold = 0.1,
    rootMargin = '0px',
    animateClass = 'animate-in',
    initialStyles = { opacity: '0', transform: 'translateY(30px)' },
    animatedStyles = { opacity: '1', transform: 'translateY(0)' },
    once = true // Анимировать только один раз
  } = options;

  const ref = useRef(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    // Применяем начальные стили
    Object.assign(element.style, {
      opacity: initialStyles.opacity,
      transform: initialStyles.transform,
      transition: 'opacity 0.6s ease, transform 0.6s ease',
      willChange: 'opacity, transform' // Оптимизация для браузера
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Применяем анимированные стили
          Object.assign(element.style, animatedStyles);
          element.classList.add(animateClass);
          
          // Если once=true — отключаем наблюдение после анимации
          if (once) {
            observer.unobserve(element);
          }
        } else if (!once) {
          // Если once=false — возвращаем начальные стили при выходе из зоны
          Object.assign(element.style, initialStyles);
          element.classList.remove(animateClass);
        }
      });
    }, { threshold, rootMargin });

    observer.observe(element);

    // Cleanup при размонтировании
    return () => {
      observer.disconnect();
    };
  }, [threshold, rootMargin, animateClass, once]);

  return ref;
};