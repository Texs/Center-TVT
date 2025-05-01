# Licensed under GNU GPL3.0
#The GNU General Public License does not permit incorporating your program
#into proprietary programs.  If your program is a subroutine library, you
#may consider it more useful to permit linking proprietary applications with
#the library.  If this is what you want to do, use the GNU Lesser General
#Public License instead of this License.  But first, please read
#https://www.gnu.org/licenses/why-not-lgpl.html>.

import pandas as pd
from tabulate import tabulate

# Нормативы по СанПиН 2.1.4.1175-02 и ВОЗ (добавлен натрий)
standards = {
    "Показатель": ["Мутность (ЕМФ)", "Цветность (градусы)", "Запах (баллы)", 
                   "Водородный показатель (pH)", "Жесткость (мг-экв/л)", 
                   "Общее железо (мг/л)", "Марганец (мг/л)", 
                   "Фториды (мг/л)", "Нитраты (мг/л)", 
                   "Общая минерализация (мг/л)", "Хлориды (мг/л)", 
                   "Сульфаты (мг/л)", "Натрий (мг/л)"],
    "СанПиН 2.1.4.1175-02": [1.5, 20, 2, 6.5-8.5, 7, 0.3, 0.1, 1.5, 45, 1000, 350, 500, 200],
    "ВОЗ": [5, 15, 0, 6.5-8.5, -1, 0.3, 0.1, 1.5, 50, 1000, 250, 250, 200]
}

# Методы очистки для разных загрязнений (добавлен натрий)
treatment_methods = {
    "Мутность": ["Механическая фильтрация", "Коагуляция", "Ультрафильтрация"],
    "Цветность": ["Угольный фильтр", "Озонирование", "Обратный осмос"],
    "Запах": ["Угольный фильтр", "Аэрация", "Озонирование"],
    "Жесткость": ["Ионообменные смолы", "Обратный осмос", "Электродиализ"],
    "Железо": ["Аэрация + фильтрация", "Ионообмен", "Обратный осмос"],
    "Марганец": ["Окисление + фильтрация", "Ионообмен", "Обратный осмос"],
    "Фториды": ["Активированный оксид алюминия", "Обратный осмос"],
    "Нитраты": ["Ионообмен", "Обратный осмос", "Биологическая денитрификация"],
    "Минерализация": ["Обратный осмос", "Дистилляция", "Электродиализ"],
    "Хлориды": ["Обратный осмос", "Дистилляция", "Ионообмен"],
    "Сульфаты": ["Обратный осмос", "Ионообмен"],
    "Натрий": ["Обратный осмос", "Электродиализ", "Дистилляция", 
              "Ионообмен с селективными смолами"]
}

def show_standards():
    """Отобразить таблицу нормативов"""
    df = pd.DataFrame(standards)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

def analyze_water():
    """Анализ воды и подбор фильтров"""
    print("\nВведите результаты анализа воды (для пропуска параметра нажмите Enter):")
    user_data = {}
    
    for param in standards["Показатель"]:
        # Упрощаем ввод для демонстрации
        if "(" in param:
            clean_param = param.split("(")[0].strip()
        else:
            clean_param = param
            
        if clean_param in treatment_methods:
            try:
                value = input(f"{param}: ")
                if value.strip() == "":
                    continue
                user_data[clean_param] = float(value)
            except ValueError:
                print(f"Некорректное значение для {param}, пропускаем")
                continue
    
    print("\nРекомендуемые методы очистки:")
    recommendations = []
    
    for param, value in user_data.items():
        # Находим норматив СанПиН
        for i, p in enumerate(standards["Показатель"]):
            if param.lower() in p.lower():
                sanpin = standards["СанПиН 2.1.4.1175-02"][i]
                if isinstance(sanpin, str) and "-" in sanpin:
                    low, high = map(float, sanpin.split("-"))
                    is_problem = value < low or value > high
                else:
                    try:
                        sanpin_val = float(sanpin)
                        is_problem = value > sanpin_val
                    except:
                        is_problem = False
                
                if is_problem and param in treatment_methods:
                    methods = treatment_methods[param]
                    recommendations.append((param, value, sanpin, methods))
                break
    
    if not recommendations:
        print("\nВаша вода соответствует нормативам по всем проверенным параметрам!")
    else:
        rec_df = pd.DataFrame(recommendations, 
                             columns=["Параметр", "Ваше значение", "Норматив", "Методы очистки"])
        print(tabulate(rec_df, headers='keys', tablefmt='pretty', showindex=False))
        
        # Дополнительная информация по очистке натрия
        if "Натрий" in user_data and user_data["Натрий"] > 200:
            print("\nДополнительная информация по очистке натрия:")
            print("1. Обратный осмос - удаляет 85-95% натрия, наиболее эффективный бытовой метод")
            print("2. Электродиализ - используется в промышленных установках")
            print("3. Дистилляция - удаляет все соли, но требует много энергии")
            print("4. Ионообмен с селективными смолами - специализированные смолы для натрия")

def main():
    while True:
        print("\nМеню:")
        print("1 - Показать нормативы качества воды")
        print("2 - Проанализировать воду и подобрать фильтры")
        print("3 - Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            show_standards()
        elif choice == "2":
            analyze_water()
        elif choice == "3":
            print("До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте еще раз.")

if __name__ == "__main__":
    print("Программа для анализа качества воды и подбора фильтров")
    print("Версия с добавленным показателем натрия и методами его очистки")
    main()
