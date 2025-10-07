class ClientAlreadyExists(Exception):
    """Такой клиент уже существует"""
    pass

class AccountAlreadyExists(Exception):
    """Такой счет уже открыт"""
    pass

class ClientNotFound(Exception):
    """Клиент не найден"""
    pass

class AccountNotFound(Exception):
    """Счет не найден"""
    pass

class LackOfMoney(Exception):
    """Недостаточно средств"""
    pass

class CurrencyMismatch(Exception):
    """Валюты не совпадают"""
    pass

class InvalidAmount(Exception):
    """Неверная сумма"""
    pass

class Bank:
    ExchangeRates = {'BYN' : {'USD' : 0.31, 'EUR' : 0.29, 'BYN' : 1.0},
                     'USD' : {'BYN' : 3.22, 'EUR' : 0.93, 'USD' : 1.0},
                     'EUR' : {'BYN' : 3.45, 'USD' : 1.07, 'EUR' : 1.0}
                    }
    def __init__(self):
        self.clients = {}
        self.currentClient = None


class BankAccount:
    def __init__(self, currency, clientId):
        self.currency = currency
        self.clientId = clientId
        self.balance = 0.0
        self.isActive = True
        self.historyOfTransaction = []

class Client:
    def __init__(self,  name, clientId):
        self.name = name
        self.clientId = clientId
        self.accounts = {} #bankAccount связь

def main():
    yourBank = Bank()
    while True:
        print("---" * 30)
        print("Добро Пожаловать в Банк Your Bank!")
        print("---" * 30)
        if not yourBank.currentClient:
            print("1) Регистрация")
            print("2) Вход")
        else: 
            print(f"Текущий пользователь: {yourBank.currentClient.name}")
            print("Выберите операцию: ")
            print("/n" + "1) Открыть счет")
            print("2) Закрыть счет")
            print("3) Пополнить счет")
            print("4) Снять со счета денюшки")
            print("5) Переводы между своими счетами")
            print("6) Перевод средств на чужой счет")
            print("7) Показать счета")
            print("8) Выписка по счетам")
            print("9) История операций")
            print("10) Разлогиниться")
            print("Если хотите завершить работу, нажмите 0")

            choice = input("Ваш выбор: ")

            if choice == "0":
                print("Мы ждем вас! Хорошего дня!")
                break

if "__main__": main()
