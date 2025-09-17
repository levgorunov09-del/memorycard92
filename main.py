from PyQt5.QtWidgets import QApplication
from random import choice , shuffle
from time import sleep

# создаём приложение
app = QApplication([])

# главное окно
from main_window import*
from menu_window import*
# класс, описывающий вопрос и статистику
class Question():
    def __init__(self, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.question = question        # вопрос
        self.answer = answer            # правильный ответ
        self.wrong_answer1 = wrong_answer1
        self.wrong_answer2 = wrong_answer2
        self.wrong_answer3 = wrong_answer3
        self.is_active = True         
        self.count_ask = 0              # сколько раз задавался вопрос
        self.count_right = 0            # сколько раз был правильный ответ
        
    def got_right(self):                # если праывильно ответили
        self.count_ask += 1
        self.count_right += 1
    
    def got_wrong(self):                # если ошиблись
        self.count_ask += 1
        

# создаём конкретные вопросы
q1 = Question('Яблуко', 'apple', 'apply', 'pineapple', 'application')
q2 = Question('Дім', 'house', 'horse', 'hurry', 'hour')
q3 = Question('Миша', 'mouse', 'mouth', 'muse', 'museum')
q4 = Question('Число', 'number', 'digit', 'amount', 'summary')

# список всех вопросов
questions = [q1, q2, q3, q4]

# список кнопок с ответами
radio_buttons = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]


# функция для нового вопроса
def new_question():
    global cur_q
    cur_q = choice(questions)              # выбираем случайный вопрос
    lb_Question.setText(cur_q.question)    # текст вопроса
    lb_Corect.setText(cur_q.answer)        # сохраняем правильный ответ
    
    shuffle(radio_buttons)                 
    radio_buttons[0].setText(cur_q.answer)
    radio_buttons[1].setText(cur_q.wrong_answer1)
    radio_buttons[2].setText(cur_q.wrong_answer2)
    radio_buttons[3].setText(cur_q.wrong_answer3)
    
    RadioGroup.setExclusive(False)         # сбрасываем выбор
    for button in radio_buttons:
        button.setChecked(False)
    RadioGroup.setExclusive(True)

    RadioGroupBox.show()                   # показываем варианты
    AnsGroupBox.hide()                     # скрываем результаты
    btn_OK.setText('Відповісти')           # меняем текст кнопки


# функция проверки ответа
def check():
    RadioGroup.setExclusive(False)
    for button in radio_buttons:
        if button.isChecked():
            if button.text() == lb_Corect.text():   # если правильно
                cur_q.got_right()
                lb_Result.setText('Вірно!')
            else:
                cur_q.got_wrong()
                lb_Result.setText('Невірно!')
        break
    
    RadioGroup.setExclusive(True)
    RadioGroupBox.hide()              # скрываем варианты
    AnsGroupBox.show()                # показываем результат
    btn_OK.setText('Наступне питання')


# обработка клика по кнопке
def click_ok():
    if btn_OK.text() == 'Відповісти':   # если ждём ответ
        check()
    else:                               # если нужно новый вопрос
        new_question()

def rest():
    win_card.hide()
    n = box_Minutes.value() * 60
    sleep(n)
    win_card.show()
        
def menu_generation():
    if cur_q.count_ask == 0:
        c = 0
    else:
        c = (cur_q.count_right / cur_q.count_ask) * 100 
    text = f'Кількість відповідей: {cur_q.count_ask}\n'\
            f'Вірних відповідей: {cur_q.count_right}\n'\
            f'Успішність: {round(c, 2)} %'
    lb_statistic.setText(text)
    menu_win.show()
    win_card.hide()
    
def clear():
    le_question.clear()
    le_right_ans.clear()
    le_wrong_ans1.clear()
    le_wrong_ans2.clear()
    le_wrong_ans3.clear()
    
btn_clear.clicked.connect(clear)

def add_question():
    new_q = Question(le_question.text(), le_right_ans.text(),
                     le_wrong_ans1.text(), le_wrong_ans2.text(),
                     le_wrong_ans3.text())    

def back_menu():
    menu_win.hide()
    win_card.show()

btn_Sleep.clicked.connect(rest)

# привязываем кнопку к действию
btn_OK.clicked.connect(click_ok)

btn_Menu.clicked.connect(menu_generation)
btn_back.clicked.connect(back_menu)

# старт с первого
new_question()


# запускаем приложение
app.exec_()
