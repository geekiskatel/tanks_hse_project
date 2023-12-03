# **Танчики на Pygame**

В рамках проектной работы ВШЭ, я воссоздал классическую 2D игру Танчики с помощью библиотеки Pygame

## Краткое описание игры:

* В неё нужно играть вдвоем. Цель каждого игрока - убить оппонента
* В ускорении процесса помогут бонусы, которые генерируются по всей карте. Они увеличивают ранг танка и его здоровье
* В левом верхнем углу есть пользовательский интерфейс, которые отображает Ранг (внутри квадрата) и Здоровье игрока. 

## Особенности:

* Логотип HSE в правом верхнем углу. В нем можно спрятаться и нельзя уничтожить
* Наличие чита, который увеличивает ранг танка до максимального
* Переделанная классическая музыка из оригинальной игры в современном стиле
* Подробно расписанный код, для быстрого понимания и редактирования под собственные нужды


## Установка:

Для запуска требуется скачать сам репозиторий и установить нужные библиотеки. 
Для начала нажмите на кнопку **"<> Code"** и выберете удобный способ скачивания, после чего введите нужную команду в свой терминал

Пример скачивания через SSH:
`git clone git@github.com:geekiskatel/tanks_hse_project.git`


## Как установить библиотеки для корректной работы кода:

Для установки нужных библиотек введите в Терминал команду:

`pip install --upgrade -r requirements.txt`

## Использование:

В случае успешной установки, запустите сам код через свой компилятор, 
либо через терминал, введя:

`python main.py` - для Windows

или 

`python3 main.py` - для Linux и MacOS


## Управление: 

### Для Синего (спавнится слева):

* W/A/S/D - вверх/вправо/вниз/влево (английская раскладка)
* Space - Выстрел
* 6 - активация читов

### Для Красного (спавнится справа):

* Стрелочки - в соответствии с направлением
* Backspace - Выстрел
* 9 - активация читов
