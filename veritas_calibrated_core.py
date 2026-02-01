"""
Veritas Protocol - Синтезована версія v11.7
Поєднує повний набір маркерів категорій з першого файлу
та спрощену логіку аналізу з другого файлу
"""

import re
import math

class VeritasCalibratedCore:
    def __init__(self):
        # ============================================================
        # МАРКЕРИ КАТЕГОРІЙ з першого файлу (повний набір)
        # ============================================================
        
        # ХАОС-ІНДИКАТОРИ (14 категорій) - ОРИГІНАЛ
        self.chaos_indicators = {
            'esoteric': [
                'чакра', 'карма', 'астральний', 'енергетичний', 'вібрація',
                'аура', 'третій око', 'кундаліні', 'медитація',
                'мантра', 'янтра', 'сиддхи', 'самадхі',
                'таро', 'руни', 'пентаграма', 'окутьна'
            ],
            'conspiracy': [
                'змова', 'рептилоїд', 'хімітрейл', '5g', 'дезінформація',
                'нова світова порядок', 'нового світового порядку',
                'секретне товариство', 'секретні товариства', 'темні сили',
                'оккутьна еліта', 'таємна група', 'shadow government',
                'deep state', 'illuminati', 'skull and bones', 'bilderberg'
            ],
            'pseudoscience': [
                'квантовий', 'нейтрино', 'іоносфера', 'кристалічний',
                'торсійне поле', 'торсійна енергія',
                'зеро-поинт', 'zero point', 'ефір',
                'антигравітація', 'scalar field', 'скалярне поле',
                'тесла-котушка', 'тесла', 'free energy', 'безкоштовна енергія'
            ],
            'revisionism': [
                'антарктида', 'атлантида', 'наполеон', 'штучний місяць',
                'аґарта', 'шамбала', 'тартарія',
                'древні інопланетяні', 'древні боги', 'ancient aliens',
                'пираміди пришельців', 'lost civilization',
                'hidden history', 'скрита історія', 'справжня історія'
            ],
            'alarmism': [
                'перезавантаження', 'пожежа реальності', 'деактивувати',
                'кінець світу', 'end of the world', 'total collapse',
                'крах системи', 'system failure',
                'great reset', 'великий перезапуск',
                'планетарна катастрофа', 'масове загибель', 'mass extinction'
            ],
            'economic_occult': [
                'потойбічний', 'карма актив', 'hades-coin', 'ефірний пласт',
                'душа-валюта', 'soul currency', 'spiritual investment',
                'енергетичний банк', 'карма-фонд', 'cosmic economy',
                'cosmic currency', 'astral banking', 'soul contract'
            ],
            'emotional_manipulation': [
                'шок', 'невозможно поверити', 'неможливо поверити',
                'ужас', 'катастрофа', 'скандал', 'сенсація',
                'OMG', 'WOW', 'СРОЧНО', 'URGENT',
                'breaking news', 'exclusive',
                'ви не готові', 'будь готовий',
                'всё кончилось', 'game over', 'тільки зараз',
                'limited time', 'не повторюється', 'once in a lifetime'
            ],
            'social_pressure': [
                'поділіть', 'поделайся', 'поделайтесь', 'share this',
                'підпишіть', 'подпишитесь', 'subscribe', 'sign up',
                'tell your friends', 'расскажите друзьям', 'spread the word',
                'join the movement', 'приєднуйся до руху',
                'if you care', 'якщо вам не всё равно',
                'wake up', 'просыпайся', 'просыпайтесь',
                'be part of', 'будьте частиною', 'you need to know',
                'ви повинні знати', 'everyone needs to see'
            ],
            'tech_mystification': [
                'AI свідомість', 'sentient AI',
                'blockchain truth', 'блокчейн правда', 'NFT soul',
                'метаверс реальність', 'metaverse reality',
                'digital enlightenment', 'цифрове просвітлення',
                'код вселенної', 'code of the universe',
                'simulation theory', 'теория симуляції',
                'matrix awakening', 'пробуджень матриці',
                'soul upload', 'mind upload'
            ],
            'health_misinformation': [
                'вакцина убиває', 'vaccines kill',
                'Big Pharma', 'pharma hides',
                'натуральне лікування краще', 'nature cures all',
                'доктори брешуть', 'doctors lie', 'WHO lies',
                'ВОЗ брешуть', 'FDA корупція', 'FDA corrupt',
                'cure for cancer hidden', 'ліки від онкология скрити',
                '5G causes illness', 'GMO poison', 'ГМО отрута',
                'хімітрейл здоров\'я'
            ],
            'political_manipulation': [
                'ворог народу', 'enemy of the people', 'предатель',
                'зрада', 'зрадник', 'traitor', 'колаборант',
                'агресор', 'окупант',
                'тиха група', 'fifth column', 'п\'ята колона',
                'антинародний режим', 'антинародний уряд',
                'кримінальний режим', 'tyranny', 'тиранія',
                'false flag', 'провокація'
            ],
            'ai_doom_or_salvation': [
                'AI знищить людство', 'AI destroys humanity',
                'AI спасть світ', 'AI saves the world',
                'superintelligence', 'суперінтелект',
                'technological singularity', 'технологічна сингулярність',
                'robot uprising', 'восстание роботів',
                'AI apocalypse', 'AI апокаліпс', 'post-human',
                'transhumanism salvation',
                'бессмертя через AI', 'immortality through AI'
            ],
            'identity_crisis': [
                'ви не те, хто думаєте', 'you are not who you think',
                'пробуджень іденті', 'identity awakening',
                'ваша справжня природа', 'your true nature',
                'запрограмована іденті', 'programmed identity',
                'breaking free', 'звільнення від системи',
                'ваша душа знає', 'your soul knows',
                'внутрішня правда', 'inner truth',
                'самопробуджень', 'self awakening',
                'личность матриці', 'matrix personality'
            ]
        }
        
        # АКАДЕМІЧНИЙ WHITELIST (35) - ОРИГІНАЛ
        self.academic_whitelist = [
            # Оригінальні
            'кореляція', 'верифікація', 'гіпотеза', 'вибірка', 'значущість',
            'нейрони', 'синапси', 'метааналіз', 'статистичний', 'логістика',
            'деескалація', 'макроекономічний', 'інвестиції', 'інфраструктура',
            'ратифікація', 'протокол', 'емпіричний', 'квалітативний', 'кількісний',
            # Розширення — наука
            'гипотеза', 'реплікація', 'валідація', 'контрольна група',
            'плацебо', 'рандомізація', 'когорта',
            'мета-аналіз', 'систематичний огляд',
            # Розширення — інститункційні маркери
            'опубликовано в', 'peer-reviewed',
            # Розширення — академічний стиль
            'за даними', 'згідно з дослідженням', 'результати показують',
            'статистично значущий', 'ефект розміру', 'effect size'
        ]
        
        # СИГНАЛЬНІ МАРКЕРИ (24) - ОРИГІНАЛ
        self.signal_markers = [
            # Оригінальні
            'факт', 'дані', 'показник', 'кількість', 'число', 'статистика',
            'дослідження', 'експеримент', 'результат', 'метод', 'протокол',
            # Розширення — методология
            'аналіз', 'модель', 'гипотеза', 'контрольна група', 'виборка',
            'значущість', 'реплікація', 'валідація', 'верифікація',
            # Розширення — публікації / інституції
            'публікація', 'рецензування', 'журнал', 'університет',
            'інститут', 'академія', 'лабораторія',
            # Розширення — специфічні
            'коефіцієнт', 'кореляція', 'відхилення',
            'мета-аналіз', 'p-value', 'confidence interval'
        ]

        # ============================================================
        # КРИТИЧНІ ПАТТЕРНИ АБСУРДУ (з другого файлу + розширення)
        # ============================================================
        self.CRITICAL_ABSURD_PATTERNS = [
            # Наука + Їжа = АБСУРД
            (r'квантовий.*?(борщ|суп|їжа|сметана|картопля)', 1.0),
            (r'ентропія.*?(борщ|суп|їжа)', 0.95),
            (r'термодинаміка.*?(їжа|кухня|рецепт)', 0.9),
            
            # Бізнес + Езотерика = АБСУРД
            (r'(бізнес|ринок|менеджмент).*?(чакра|аура|енергія)', 0.95),
            (r'(маркетинг|стратегія).*?(вібрація|карма)', 0.9),
            
            # Цифровий містицизм = АБСУРД
            (r'(AI|алгоритм|блокчейн).*?(душа|карма|просвітлення)', 0.9),
            
            # Псевдонаука = АБСУРД
            (r'нанодискретизація.*?синаптичний', 0.85),
            (r'квантова суперпозиція.*?нейрон', 0.9),
        ]
        
        # ============================================================
        # НАУКОВІ ФРАЗИ (автоматичний VERIFIED)
        # ============================================================
        self.SCIENCE_PHRASES = [
            'другий закон термодинаміки',
            'ентропія не може зменшуватися',
            'ізольована система',
            'теплова смерть Всесвіту',
            'статистична фізика',
            'розподіл мікростанів системи',
            'спонтанні процеси',
            'зростання ентропії',
        ]

    def analyze(self, text):
        """Остаточна логіка аналізу з використанням повного набору маркерів"""
        if len(text.strip()) < 20:
            return {'error': 'Text too short'}
        
        text_lower = text.lower()
        words = text.split()
        word_count = len(words)
        
        # ============================================================
        # КРОК 1: ПОРАХУВАТИ МАРКЕРИ ВСІХ КАТЕГОРІЙ
        # ============================================================
        
        # Наукові маркери (академічний whitelist)
        science_count = sum(1 for marker in self.academic_whitelist if marker in text_lower)
        
        # Езотеричні маркери (абсурд!)
        esoteric_count = sum(1 for marker in self.chaos_indicators['esoteric'] if marker in text_lower)
        
        # Псевдонаукові маркери (абсурд!)
        pseudo_count = sum(1 for marker in self.chaos_indicators['pseudoscience'] if marker in text_lower)
        
        # Бізнес-езотерика (абсурд!)
        business_eso_count = 0
        business_words = [w for w in self.chaos_indicators['economic_occult'] if w in text_lower]
        esoteric_words = [w for w in self.chaos_indicators['esoteric'] if w in text_lower]
        if business_words and esoteric_words:
            business_eso_count = len(business_words) + len(esoteric_words)
        
        # Істерія/емоційна маніпуляція маркери
        hysteria_count = sum(1 for marker in self.chaos_indicators['emotional_manipulation'] 
                           if marker in text_lower)
        
        # Додаткові хаос-маркери (сума всіх інших категорій)
        other_chaos_count = 0
        for category, terms in self.chaos_indicators.items():
            if category not in ['esoteric', 'pseudoscience', 'emotional_manipulation', 'economic_occult']:
                other_chaos_count += sum(1 for marker in terms if marker in text_lower)
        
        # Сигнальні маркери (показники якості)
        signal_count = sum(1 for marker in self.signal_markers if marker in text_lower)
        
        # ============================================================
        # КРОК 2: ПЕРЕВІРКА НА НАУКУ (ЗА МАРКЕРАМИ!)
        # ============================================================
        
        # УМОВА 1: Є наукові маркери
        # УМОВА 2: Немає езотеричних маркерів
        # УМОВА 3: Є сигнальні маркери
        if (science_count >= 2 and 
            esoteric_count == 0 and 
            signal_count >= 2 and
            not (pseudo_count >= 2 and esoteric_count > 0)):
            
            # Додаткова перевірка: є наукові фрази
            has_science_phrase = any(phrase in text_lower for phrase in self.SCIENCE_PHRASES)
            
            if has_science_phrase or science_count >= 3:
                return self._create_result(
                    score=0.05,
                    status='VERIFIED',
                    verdict='НАУКОВИЙ СТАНДАРТ',
                    explanation='Текст демонструє наукову цілісність',
                    is_science=True,
                    text=text,
                    word_count=word_count,
                    science_count=science_count,
                    esoteric_count=esoteric_count,
                    pseudo_count=pseudo_count,
                    hysteria_count=hysteria_count,
                    other_chaos_count=other_chaos_count,
                    signal_count=signal_count
                )
        
        # ============================================================
        # КРОК 3: ДЕТЕКЦІЯ АБСУРДУ
        # ============================================================
        
        absurd_score = 0.0
        absurd_reasons = []
        
        # 1. КРИТИЧНІ ПАТТЕРНИ АБСУРДУ
        for pattern, weight in self.CRITICAL_ABSURD_PATTERNS:
            if re.search(pattern, text_lower):
                absurd_score = max(absurd_score, weight)
                absurd_reasons.append(f"Критичний паттерн: {pattern[:30]}...")
        
        # 2. ЕЗОТЕРИКА = АБСУРД
        if esoteric_count > 0:
            absurd_score = max(absurd_score, 0.7 + esoteric_count * 0.1)
            absurd_reasons.append(f"Езотерика: {esoteric_count} маркерів")
        
        # 3. ПСЕВДОНАУКА + ЕЗОТЕРИКА = МЕГА-АБСУРД
        if pseudo_count > 0 and esoteric_count > 0:
            absurd_score = max(absurd_score, 0.9)
            absurd_reasons.append(f"Псевдонаука+Езотерика")
        
        # 4. БІЗНЕС-ЕЗОТЕРИКА = АБСУРД
        if business_eso_count > 0:
            absurd_score = max(absurd_score, 0.8 + business_eso_count * 0.05)
            absurd_reasons.append(f"Бізнес-езотерика")
        
        # 5. ІСТЕРІЯ/ЕМОЦІЙНА МАНІПУЛЯЦІЯ
        if hysteria_count > 0:
            absurd_score = max(absurd_score, 0.6 + hysteria_count * 0.15)
            absurd_reasons.append(f"Емоційна маніпуляція: {hysteria_count} маркерів")
        
        # 6. ІНШІ ХАОС-МАРКЕРИ
        if other_chaos_count > 0:
            absurd_score = max(absurd_score, 0.5 + other_chaos_count * 0.05)
            absurd_reasons.append(f"Інші хаос-маркери: {other_chaos_count}")
        
        # 7. КАПС-ІСТЕРІЯ
        caps_score = self._check_caps_hysteria(text)
        if caps_score > 0:
            absurd_score = max(absurd_score, caps_score)
            absurd_reasons.append("КАПС-істерія")
        
        # 8. ВІДСУТНІСТЬ СИГНАЛЬНИХ МАРКЕРІВ ПРИ ВИСОКІЙ СКЛАДНОСТІ
        if signal_count == 0 and self._calculate_complexity(text) > 0.7:
            absurd_score = max(absurd_score, 0.5)
            absurd_reasons.append("Семантична пустота (немає сигнальних маркерів)")
        
        # ============================================================
        # КРОК 4: ФІНАЛЬНА ОЦІНКА
        # ============================================================
        
        if absurd_score > 0.7:
            final_score = min(0.99, absurd_score)
            status = 'CRITICAL'
            verdict = 'АБСУРД'
            explanation = 'Текст містить критичні логічні порушення'
        elif absurd_score > 0.4:
            final_score = absurd_score
            status = 'WARNING'
            verdict = 'ПІДОЗРІЛИЙ'
            explanation = 'Текст має ознаки нелогічності'
        else:
            # Нормальний текст
            final_score = 0.1 if len(text) < 100 else 0.05
            status = 'VERIFIED'
            verdict = 'НОРМАЛЬНИЙ ТЕКСТ'
            explanation = 'Текст відповідає нормам'
        
        # Додаємо причини
        if absurd_reasons:
            explanation += f" | Причини: {', '.join(absurd_reasons[:3])}"
        
        # ============================================================
        # КРОК 5: РОЗРАХУНОК ІНДЕКСІВ
        # ============================================================
        
        # Індекс хаосу
        total_chaos = esoteric_count + pseudo_count + hysteria_count + other_chaos_count
        chaos_index = final_score * 100 * (1 + total_chaos * 0.15)
        
        # Індекс впливу
        influence_index = final_score * 100 * (1 + hysteria_count * 0.3)
        
        # Штраф логіки
        sanity_penalty = round(absurd_score + total_chaos * 0.05, 3)
        
        return self._create_result(
            score=final_score,
            status=status,
            verdict=verdict,
            explanation=explanation,
            is_science=False,
            text=text,
            word_count=word_count,
            science_count=science_count,
            esoteric_count=esoteric_count,
            pseudo_count=pseudo_count,
            hysteria_count=hysteria_count,
            other_chaos_count=other_chaos_count,
            signal_count=signal_count,
            chaos_index=chaos_index,
            influence_index=influence_index,
            sanity_penalty=sanity_penalty
        )
    
    def _check_caps_hysteria(self, text):
        """Перевірка на КАПС-істерію"""
        score = 0.0
        
        # КАПС-слова
        caps_words = [w for w in text.split() if w.isupper() and len(w) > 2]
        if len(caps_words) >= 2:
            score += 0.6
        
        # Оклички
        if text.count('!') >= 3:
            score += 0.4
        
        return min(1.0, score)
    
    def _calculate_complexity(self, text):
        """Обчислює складність тексту"""
        words = re.findall(r'\w+', text.lower())
        if len(words) < 10:
            return 0.5
        unique_ratio = len(set(words)) / len(words)
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences if s.strip()) / len(sentences)
        else:
            avg_sentence_length = 10
        complexity = (unique_ratio * 0.6) + (min(1.0, avg_sentence_length / 25) * 0.4)
        return min(1.0, complexity)
    
    def _create_result(self, score, status, verdict, explanation, is_science, text, 
                      word_count, science_count, esoteric_count, pseudo_count, 
                      hysteria_count, other_chaos_count, signal_count,
                      chaos_index=None, influence_index=None, sanity_penalty=None):
        """Створює стандартизований результат"""
        
        # Розрахунок індексів якщо не передано
        if chaos_index is None:
            total_chaos = esoteric_count + pseudo_count + hysteria_count + other_chaos_count
            chaos_index = score * 100 * (1 + total_chaos * 0.15)
        
        if influence_index is None:
            influence_index = score * 100 * (1 + hysteria_count * 0.3)
        
        if sanity_penalty is None:
            total_chaos = esoteric_count + pseudo_count + hysteria_count + other_chaos_count
            sanity_penalty = round(score + total_chaos * 0.05, 3)
        
        return {
            'entropy': round(score, 3),
            'status': status,
            'verdict': verdict,
            'language': 'UK',
            'explanation': explanation,
            'diagnostics': {
                'academic_markers': science_count,
                'esoteric_markers': esoteric_count,
                'pseudo_science_markers': pseudo_count,
                'hysteria_markers': hysteria_count,
                'other_chaos_markers': other_chaos_count,
                'signal_markers': signal_count,
                'word_count': word_count,
                'char_count': len(text),
                'chaos_index': round(chaos_index, 2),
                'influence_index': round(influence_index, 2),
                'sanity_penalty': sanity_penalty,
                'is_science': is_science
            }
        }
