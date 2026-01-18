# виртуальная модель обучения
# учитель среди методов должен уметь давать знания, опрашивать, заполняет журнал (фамилия вводится)
# некоторые характеристики: имя, предмет, опыт
# учитель дал, вывод в консоль
# пользовательский ввод + exception

class OddNumber(Exception):
    """Такая оценка должна быть от 0 до 10"""
    pass

class VoidName(Exception):
    """Имя не может быть пустым"""
    pass

class NotCorrectChoice(Exception):
    """Нет такого варианта выбора"""
    pass

class NotLetters(Exception):
    """Должно быть имя"""
    pass

class Teacher:
    def __init__(self, name, subject, experience):
        self.name = name
        self.subject = subject
        self.experience = experience
        self.journal = [] 
    
    def give_knowledge(self):
        print(f"Учитель {self.name} провёл урок по предмету '{self.subject}'")
    
    def ask_question(self):
        print(f"Учитель {self.name} задал вопрос по предмету '{self.subject}'")
    
    def fill_marks_into_journal(self):
        try:
            name_of_student = input("Введите имя ученика: ").strip()
            if not name_of_student:
                raise VoidName
            
            evaluate_student = int(input(f"Введите оценку ученика {name_of_student} (0-10): "))
            if evaluate_student < 0 or evaluate_student > 10:
                raise OddNumber
            
            self.journal.append({
                "student_name": name_of_student,
                "mark": evaluate_student,
                "subject": self.subject,
                "teacher": self.name
            })
            
            print(f"\nУчитель {self.name} поставил оценку {evaluate_student} студенту {name_of_student}")
            print(f"Всего оценок в журнале: {len(self.journal)}")
            
        except VoidName:
            print("Ошибка: Имя не может быть пустым")
        except OddNumber:
            print("Ошибка: Оценка должна быть от 0 до 10")
        except ValueError:
            print("Ошибка: Введите числовое значение для оценки")
    
    def show_journal(self):
        """Метод для отображения всего журнала"""
        if not self.journal:
            print("\nЖурнал пуст")
            return
        
        print(f"\n{'='*50}")
        print(f"Журнал учителя {self.name}")
        print(f"Предмет: {self.subject}")
        print(f"Опыт: {self.experience} лет")
        print(f"{'='*50}")
                
        for i in range(len(self.journal)):
            record = self.journal[i]
            print(f"{i+1}. {record['student_name']} | Оценка: {record['mark']}")

def main():
    print("СИСТЕМА ВИРТУАЛЬНОГО ОБУЧЕНИЯ")
    try:
        name = input("Введите имя учителя: ").strip()

        for letter in name:
            if letter.isdigit(): raise NotLetters
            break

        subject = input("Введите предмет: ").strip()

        for letter in subject:
            if letter.isdigit(): raise NotLetters

        experience = int(input("Введите ваш опыт в годах: "))

        teacher = Teacher(name, subject, experience)
    
        while True:
            print("\nВыберите действие:")
            print("1. Провести урок")
            print("2. Задать вопрос")
            print("3. Поставить оценку")
            print("4. Показать журнал")
            print("0. Выход")
            
            try:
                choice = input("\nВаш выбор (0-4): ").strip()
                
                if choice not in ["0", "1", "2", "3", "4"]:
                    raise NotCorrectChoice
                    
            except NotCorrectChoice:
                print("Ошибка: Выберите число от 0 до 4")
                continue
            
            if choice == "1":
                teacher.give_knowledge()
            elif choice == "2":
                teacher.ask_question()
            elif choice == "3":
                teacher.fill_marks_into_journal()
            elif choice == "4":
                teacher.show_journal()
            elif choice == "0":
                print("\nХорошего дня!")
                break
    except ValueError:
        print("Опыт будет установлен в 0 лет")
        experience = 0
    except NotLetters:
        print("Это должны быть буквы")

if __name__ == "__main__":
    main()