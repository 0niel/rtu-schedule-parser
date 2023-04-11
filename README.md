[![codecov](https://codecov.io/gh/mirea-ninja/rtu-schedule-parser/branch/main/graph/badge.svg?token=W98TXURMYZ)](https://codecov.io/gh/mirea-ninja/rtu-schedule-parser)

# rtu-schedule-parser
Простое извлечение расписания МИРЭА - Российского Технологического Университета из Excel документов.

## Почему rtu-schedule-parser?
* **Строгий формат**: Мы стремимся извлечь расписания без неожиданных итогов. Если возникают проблемы при парсинге, выводится ошибка.
* **Выходные данные**: Данные расписания легко преобразуются в формат Pandas DataFrame. Это позволяет быстро экспортировать извлеченное расписание в форматы CSV, HTML, XML, JSON и другие, а также выполнять различные операции выборки, сортировки и т.д. с данными.
* **Совместимость**: Совместим с форматами документов .xls и .xlsx. Обрабатывает большое количество случаев при парсинге.

## Примеры
Пример того, как вы можете загружать документы с расписанием и извлекать расписание для определенной группы. Вы можете увидеть больше примеров [здесь](https://github.com/mirea-ninja/rtu-schedule-parser/tree/main/examples).
```python
from rtu_schedule_parser import ExcelScheduleParser, ScheduleData
from rtu_schedule_parser.constants import Institute, Degree
from rtu_schedule_parser.downloader import ScheduleDownloader


# Initialize downloader with default directory to save files
downloader = ScheduleDownloader()

# Get documents for specified institute and degree
docs = downloader.get_documents(specific_institutes={Institute.IIT}, specific_degrees={Degree.BACHELOR})

# Download only if they are not downloaded yet.
downloaded = downloader.download_all(docs)

# Create schedule with downloaded files
schedules = None  # type: ScheduleData | None
for doc in downloaded:
    parser = ExcelScheduleParser(
        doc[1], doc[0].period, doc[0].institute, doc[0].degree
    )
    
    # The `force` argument is used to ignore exceptions during document parsing. 
    # This lets you to parse all possible groups.
    if schedules is None:
        schedules = parser.parse(force=True)
    else:
        schedules.extend(parser.parse(force=True).get_schedule())

# Get a schedule for the specified group
group_schedule = schedules.get_group_schedule("ИКБО-01-22")

# Initialize pandas dataframe
df = group_schedule.get_dataframe()

# Export dataframe to csv
df.to_csv("schedule.csv")

```

# Установка
### Из исходного кода
```bash
$ git clone https://github.com/mirea-ninja/rtu-schedule-parser
```
затем установите с помощью pip:
```console
$ cd rtu-schedule-parser
$ python -m pip install .
```
