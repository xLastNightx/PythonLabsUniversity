INCLUDED_MINUTES = 60
INCLUDED_SMS = 30
INCLUDED_MB = 1024  

BASE_PRICE = 24.99

EXTRA_MINUTE_PRICE = 0.89
EXTRA_SMS_PRICE = 0.59
EXTRA_MB_PRICE = 0.79

TAX_RATE = 0.02  

used_minutes = int(input("Минуты: "))
used_sms = int(input("SMS: "))
used_mb = int(input("МБ: "))

extra_minutes_cost = 0
extra_sms_cost = 0
extra_mb_cost = 0

if used_minutes > INCLUDED_MINUTES:
    extra_minutes = used_minutes - INCLUDED_MINUTES
    extra_minutes_cost = extra_minutes * EXTRA_MINUTE_PRICE
    print(f"Дополнительные минуты ({extra_minutes} мин.): {extra_minutes_cost:.2f} руб.")

if used_sms > INCLUDED_SMS:
    extra_sms = used_sms - INCLUDED_SMS
    extra_sms_cost = extra_sms * EXTRA_SMS_PRICE
    print(f"Дополнительные SMS ({extra_sms} шт.): {extra_sms_cost:.2f} руб.")

if used_mb > INCLUDED_MB:
    extra_mb = used_mb - INCLUDED_MB
    extra_mb_cost = extra_mb * EXTRA_MB_PRICE
    print(f"Дополнительный трафик ({extra_mb} МБ): {extra_mb_cost:.2f} руб.")

subtotal = BASE_PRICE + extra_minutes_cost + extra_sms_cost + extra_mb_cost

tax_amount = subtotal * TAX_RATE

total = subtotal + tax_amount

print("-"*50)
print(f"Сумма без налога: {subtotal:.2f} руб.")
print(f"Налог (2%): {tax_amount:.2f} руб.")
print(f"ИТОГО К ОПЛАТЕ: {total:.2f} руб.")