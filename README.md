Тестовое задание для [Aviasales](https://www.aviasales.ru/)

Задание:

> Тестовое задание в команду гейтов (Python)

> В папке два XML – это ответы на запросы, сделанные к API партнёра via.com.

>Необходимо их распарсить и вывести списком отличия между результатами двух запросов по маршрутам (тег Flights).

> * Какие рейсы входят в маршрут
> * Время начала и время конца маршрута
> * Цена маршрута
> * Что изменилось по условиям?
> * Добавился ли новый маршрут?

> Язык реализации — python3
> Используемые библиотеки и инструменты — всё на твой выбор.

> Оценивать будем умение выполнять задачу имея неполные данные о ней,
умение самостоятельно принимать решения и качество кода.


### Установка
При выполнении задания использовался python 3.7  
Для создания виртуального окружения я использовал ([pyenv](https://github.com/pyenv/pyenv) + [pipenv](https://github.com/pypa/pipenv))
```
git clone git@gitlab.com:SergeevAI/aviasales-test.git
cd aviasales-test/
pipenv install
pipenv shell
python main.py
```

### Используемые библиотеки:
```
[packages]
lxml = "*"
"beautifulsoup4" = "*"
```

### Коммиты:

596333c: Initial commit.

 - Initialize pipenv with python3
 - Create client.py for via.com class
 - Add dataclasses for Itinerary, Flight and Price

8ab0262: Develop api client for xml parsing

 - Install beautifulsoup4 and lxml
 - Add methods for parse xml and return Itineraries

3bf5e35: via.com api client
 - Add docstrings

2d23b06: via.com api client
 - Add string representation of route
 - add main.py for experiments :)

aa01dd7: Flights diff between two requests
 - Add __eq__ method to Flight class
 - Map flights to Dict
 - Calculate and print difference between two requests