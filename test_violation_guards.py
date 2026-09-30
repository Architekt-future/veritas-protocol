"""Регресійні тести для veritas_violation_guards (запуск: python3 test_violation_guards.py)."""
import re
import veritas_violation_guards as vg

PATS = [r'дехто каже', r'кажуть', r'говорять', r'вважають', r'вважається']

def anon(t): return vg.find_anonymous_authority(t.lower(), PATS)
def physics(t): return bool(re.search(r'\b(термодинаміка|квантовий|фізика|математика|формула|рівняння)\b',
                                      vg.neutralize_domain_metaphors('physics', t.lower())))

# хибні спрацьовування, які мають зникнути
assert anon('Що люди вважають відомим, змінила система.') is None
assert anon('Те, що вважається допустимою інформацією.') is None
assert anon('Результати покажуть, скажуть і розкажуть усе.') is None
assert not physics('Прихована ентропія інформації і політика влади.')
assert not physics('Не ентропія в термодинамічному сенсі.')

# справжні анонімні посилання, які мають лишитися
assert anon('Кажуть, що це працює.') == r'кажуть'
assert anon('Говорять, що уряд усе знає.') == r'говорять'
assert anon('Люди вважають, що ліки шкідливі.') == r'вважають'
assert anon('Вважається, що теорія доведена.') == r'вважається'
assert anon('Дехто каже, що це правда.') == r'дехто каже'

# справжня фізика лишається фізикою
assert physics('Квантовий резонанс керує виборами.')
assert physics('Термодинаміка пояснює політику.')
assert not vg.neutralize_domain_metaphors('medicine', 'ентропія') == ' '
print('ALL OK')
