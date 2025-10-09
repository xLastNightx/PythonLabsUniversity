from datetime import datetime

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

class BankAccount:
    def __init__(self, currency, clientId):
        self.currency = currency
        self.clientId = clientId
        self.balance = 0.0
        self.isActive = True
        self.transactionHistory = []

class Client:
    def __init__(self, clientId, name):
        self.clientId = clientId
        self.name = name
        self.accounts = {} # currency -> BankAccount

class Bank:
    ExchangeRates = {'BYN' : {'USD' : 0.31, 'EUR' : 0.29, 'BYN' : 1.0},
                     'USD' : {'BYN' : 3.22, 'EUR' : 0.93, 'USD' : 1.0},
                     'EUR' : {'BYN' : 3.45, 'USD' : 1.07, 'EUR' : 1.0}
                    }
    
    def __init__(self):
        self.clients = {}
        self.currentClient = None

    def _getAccountByCurrency(self, clientId, currency):
        """Получить счет клиента по валюте"""
        if clientId not in self.clients:
            raise ClientNotFound
        
        if currency not in self.clients[clientId].accounts:
            raise AccountNotFound
        
        return self.clients[clientId].accounts[currency]
    
    def registerClient(self):
        try:
            clientId = input("Введите ID клиента: ")
            name = input("Введите имя клиента: ")

            if clientId in self.clients:
                raise ClientAlreadyExists
            
            self.clients[clientId] = Client(clientId, name)
            print(f"Клиент {name} зарегистрирован")
            return clientId
        
        except ClientAlreadyExists:
            print("Ошибка: Клиент с таким ID уже существует")
            return None                 
        
    def login(self):
        try: 
            clientId = input("Введите ваш ID: ")

            if clientId not in self.clients:
                raise ClientNotFound
            
            self.currentClient = self.clients[clientId]
            print(f"Добро пожаловать, {self.currentClient.name}")
            return self.currentClient
        
        except ClientNotFound:
            print("Ошибка: Клиент не найден")
            return None             

    def logout(self):
        self.currentClient = None
        print("Вы вышли из аккаунта")
    
    def openAccount(self):
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            currency = input("Введите валюту счета (USD, EUR, BYN): ").upper()

            if currency not in self.ExchangeRates:
                raise CurrencyMismatch
            
            if currency in self.currentClient.accounts:
                raise AccountAlreadyExists
            
            account = BankAccount(currency, self.currentClient.clientId)
            self.currentClient.accounts[currency] = account

            self._addTransaction(self.currentClient.clientId, currency, "OPEN_ACCOUNT", 0, currency, f"Открытие счета в валюте {currency}")
            print(f"Счет в валюте {currency} открыт")

        except ClientNotFound: 
            print("Ошибка: Сначала войдите в систему")
        except AccountAlreadyExists:
            print("Ошибка: Счет в этой валюте уже существует")
        except CurrencyMismatch: 
            print("Ошибка: Неподдерживаемая валюта")

    def closeAccount(self):
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            currency = input("Введите валюту счета для закрытия: ").upper()

            if currency not in self.currentClient.accounts:
                raise AccountNotFound
            
            account = self.currentClient.accounts[currency]

            if account.balance > 0:
                raise InvalidAmount
            
            account.isActive = False

            self._addTransaction(self.currentClient.clientId, currency, "CLOSE_ACCOUNT", 0, currency, "Закрытие счета")

            del self.currentClient.accounts[currency]

            print(f"Счет с валютой {currency} был удален")

        except ClientNotFound:
            print("Ошибка: Сначала войдите в систему")
        except AccountNotFound:
            print("Ошибка: Счет не найден")
        except InvalidAmount:
            print("Ошибка: Нельзя закрыть счет с положительным балансом")
            
    def deposit(self):
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            currency = input("Введите валюту счета: ").upper()

            account = self._getAccountByCurrency(self.currentClient.clientId, currency)

            amount = float(input("Введите сумму для пополнения: "))

            if amount <= 0:
                raise InvalidAmount
            
            account.balance += amount

            self._addTransaction(self.currentClient.clientId, currency, "DEPOSIT", amount, currency, "Пополнение счета")
        
            print(f"Счет пополнен на {amount} {currency}. Новый баланс: {account.balance}")
        
        except ClientNotFound:
            print("Ошибка: Сначала войдите в систему")
        except AccountNotFound:
            print("Ошибка: Счет не найден")
        except InvalidAmount:
            print("Ошибка: Сумма должна быть положительной")
        except ValueError:
            print("Ошибка: Введите корректное число")

    def withdraw(self):
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            currency = input("Введите валюту счета: ").upper()
            
            account = self._getAccountByCurrency(self.currentClient.clientId, currency)
            
            amount = float(input("Введите сумму для снятия: "))
            if amount <= 0:
                raise InvalidAmount
            
            if amount > account.balance:
                raise LackOfMoney
            
            account.balance -= amount
            
            self._addTransaction(self.currentClient.clientId, currency, "WITHDRAW", -amount, currency, "Снятие со счета")
            
            print(f"Со счета снято {amount} {currency}. Новый баланс: {account.balance}")
            
        except ClientNotFound:
            print("Ошибка: Сначала войдите в систему")
        except AccountNotFound:
            print("Ошибка: Счет не найден")
        except InvalidAmount:
            print("Ошибка: Сумма должна быть положительной")
        except LackOfMoney:
            print("Ошибка: Недостаточно средств на счете")
        except ValueError:
            print("Ошибка: Введите корректное число")

    def _convertCurrency(self, amount, fromCurrency, toCurrency):
        """Конвертирует сумму из одной валюты в другую"""
        if fromCurrency == toCurrency:
            return amount
        
        return amount * self.ExchangeRates[fromCurrency][toCurrency]
    
    def transferToOwnAccount(self):
        """Перевод между своими счетами с конвертацией"""
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            fromCurrency = input("Введите валюту счета для перевода: ").upper()
            toCurrency = input("Введите валюту счета получателя: ").upper()
            
            fromAccount = self._getAccountByCurrency(self.currentClient.clientId, fromCurrency)
            toAccount = self._getAccountByCurrency(self.currentClient.clientId, toCurrency)
            
            amount = float(input("Введите сумму для перевода: "))
            if amount <= 0:
                raise InvalidAmount
            
            if amount > fromAccount.balance:
                raise LackOfMoney
            
            convertedAmount = self._convertCurrency(amount, fromCurrency, toCurrency)
            
            fromAccount.balance -= amount
            toAccount.balance += convertedAmount
            
            self._addTransaction(self.currentClient.clientId, fromCurrency, "TRANSFER_OUT", -amount, fromCurrency, 
                                f"Перевод на свой счет {toCurrency}")
            self._addTransaction(self.currentClient.clientId, toCurrency, "TRANSFER_IN", convertedAmount, toCurrency,
                                f"Перевод со своего счета {fromCurrency}")
        
            print(f"Перевод {amount} {fromCurrency} -> {convertedAmount:.2f} {toCurrency} выполнен успешно!")
            print(f"Курс: 1 {fromCurrency} = {self.ExchangeRates[fromCurrency][toCurrency]:.2f} {toCurrency}")
            
        except ClientNotFound:
            print("Ошибка: Сначала войдите в систему")
        except AccountNotFound:
            print("Ошибка: Счет не найден")
        except InvalidAmount:
            print("Ошибка: Сумма должна быть положительной")
        except LackOfMoney:
            print("Ошибка: Недостаточно средств для перевода")
        except ValueError:
            print("Ошибка: Введите корректное число")

    def transferToOtherClient(self):
        """Перевод другому клиенту (только одинаковые валюты)"""
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            fromCurrency = input("Введите валюту счета для перевода: ").upper()
            fromAccount = self._getAccountByCurrency(self.currentClient.clientId, fromCurrency)
            
            toClientId = input("Введите ID клиента-получателя: ")
            toCurrency = input("Введите валюту счета получателя: ").upper()
            toAccount = self._getAccountByCurrency(toClientId, toCurrency)
            
            if fromCurrency != toCurrency:
                raise CurrencyMismatch
            
            amount = float(input("Введите сумму для перевода: "))
            if amount <= 0:
                raise InvalidAmount
            
            if not toAccount.isActive:
                raise AccountNotFound
            
            if amount > fromAccount.balance:
                raise LackOfMoney
            
            fromAccount.balance -= amount
            toAccount.balance += amount
            
            self._addTransaction(self.currentClient.clientId, fromCurrency, "TRANSFER_OUT", -amount, fromCurrency,
                                f"Перевод клиенту {toClientId}")
            self._addTransaction(toClientId, toCurrency, "TRANSFER_IN", amount, toCurrency,
                                f"Перевод от клиента {self.currentClient.clientId}")
            
            print(f"Перевод {amount} {fromCurrency} клиенту {toClientId} выполнен успешно!")
            
        except ClientNotFound:
            print("Ошибка: Клиент не найден")
        except AccountNotFound:
            print("Ошибка: Счет не найден")
        except InvalidAmount:
            print("Ошибка: Сумма должна быть положительной")
        except LackOfMoney:
            print("Ошибка: Недостаточно средств для перевода")
        except CurrencyMismatch:
            print("Ошибка: Перевод между разными валютами другим клиентам не поддерживается")
        except ValueError:
            print("Ошибка: Введите корректное число")

    def _addTransaction(self, clientId, currency, transactionType, amount, transactionCurrency, description):
        """Добавляет запись в историю транзакций"""
        account = self._getAccountByCurrency(clientId, currency)
        transaction = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': transactionType,
            'amount': amount,
            'currency': transactionCurrency,
            'description': description,
            'balance_after': account.balance
        }
        account.transactionHistory.append(transaction)

    def generateStatement(self):
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            filename = f"statement_{self.currentClient.clientId}.txt"
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"ВЫПИСКА ПО СЧЕТАМ\n")
                file.write(f"Клиент: {self.currentClient.name} (ID: {self.currentClient.clientId})\n")
                file.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                file.write("=" * 50 + "\n")
                
                total_balance = 0
                
                for currency, account in self.currentClient.accounts.items():
                    if account.isActive:
                        file.write(f"Валюта: {currency}\n")
                        file.write(f"Баланс: {account.balance:.2f}\n")
                        file.write("-" * 30 + "\n")
                        total_balance += account.balance
                
                file.write(f"ОБЩИЙ БАЛАНС: {total_balance:.2f}\n")
            
            print(f"Выписка сохранена в файл: {filename}")
            
        except ClientNotFound:
            print("Ошибка: Сначала войдите в систему")

    def generateTransactionHistory(self):
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            currency = input("Введите валюту счета для выписки истории: ").upper()
            account = self._getAccountByCurrency(self.currentClient.clientId, currency)
            
            filename = f"history_{self.currentClient.clientId}_{currency}.txt"
            
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"ИСТОРИЯ ОПЕРАЦИЙ\n")
                file.write(f"Клиент: {self.currentClient.name} (ID: {self.currentClient.clientId})\n")
                file.write(f"Валюта: {currency}\n")
                file.write(f"Период: с момента открытия по {datetime.now().strftime('%Y-%m-%d')}\n")
                file.write("=" * 60 + "\n")
                
                for transaction in account.transactionHistory:
                    file.write(f"{transaction['timestamp']} | {transaction['type']:15} | ")
                    file.write(f"{transaction['amount']:>8.2f} {transaction['currency']} | ")
                    file.write(f"Баланс: {transaction['balance_after']:>8.2f} | ")
                    file.write(f"{transaction['description']}\n")
            
            print(f"История операций сохранена в файл: {filename}")
            
        except ClientNotFound:
            print("Ошибка: Сначала войдите в систему")
        except AccountNotFound:
            print("Ошибка: Счет не найден")

    def showAccounts(self):
        try:
            if not self.currentClient:
                raise ClientNotFound
            
            print("\nВаши счета:")
            for currency, account in self.currentClient.accounts.items():
                if account.isActive:
                    print(f"{currency}: {account.balance:.2f}")
                    
        except ClientNotFound:
            print("Ошибка: Сначала войдите в систему")

def main():
    yourBank = Bank()
    while True:
        print("\n" + "=" * 40)
        print("Добро Пожаловать в Банк Your Bank!")
        print("=" * 40)
        
        if not yourBank.currentClient:
            print("1. Регистрация")
            print("2. Вход")
        else: 
            print(f"Текущий пользователь: {yourBank.currentClient.name}")
            print("1. Открыть счет")
            print("2. Закрыть счет")
            print("3. Пополнить счет")
            print("4. Снять со счета")
            print("5. Перевод между своими счетами")
            print("6. Перевод другому клиенту")
            print("7. Показать счета")
            print("8. Выписка по счетам")
            print("9. История операций")
            print("10. Выйти из системы")
        
        print("0. Завершить работу")
        
        choice = input("Ваш выбор: ")

        if choice == "0":
            print("Мы ждем вас! Хорошего дня!")
            break

        if not yourBank.currentClient:
            if choice == "1":
                clientId = yourBank.registerClient()
                if clientId:
                    yourBank.currentClient = yourBank.clients[clientId] 
                    print(f"Добро пожаловать, {yourBank.currentClient.name}!")
            elif choice == "2":
                yourBank.login()
            else:
                print("Неверный выбор!")
        else:
            if choice == "1":
                yourBank.openAccount()
            elif choice == "2":
                yourBank.closeAccount()
            elif choice == "3":
                yourBank.deposit()
            elif choice == "4":
                yourBank.withdraw()
            elif choice == "5":
                yourBank.transferToOwnAccount()
            elif choice == "6":
                yourBank.transferToOtherClient()
            elif choice == "7":
                yourBank.showAccounts()
            elif choice == "8":
                yourBank.generateStatement()
            elif choice == "9":
                yourBank.generateTransactionHistory()
            elif choice == "10":
                yourBank.logout()
            else:
                print("Неверный выбор!")

if __name__ == "__main__":
    main()