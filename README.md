# rtu-schedule-parser
Easy extraction of the MIREA - Russian Technological University schedule from Excel documents.

## Why rtu-schedule-parser?
* **Strict formatting:** We strive to extract schedules without unexpected totals. If problems are found, an error is raised and displayed.
* **Output:** Schedule data is easily converted to pandas DataFrame format. This allows you to quickly export the extracted schedule to CSV, HTML, XML, JSON and other formats, as well as perform various selecting, sorting, etc. operations on the data.
* **Compatibility:** Compatible with `.xls` and `.xlsx` document formats. Handles a large number of cases when parsing.

## Example
An example of how you can download documents with a schedule and extract a schedule for a specific group. You can see more examples [here](https://github.com/mirea-ninja/rtu-schedule-parser/tree/main/examples).
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

# Installation
### From the source code
```bash
$ git clone https://github.com/mirea-ninja/rtu-curriculum-parser
```
and then install using pip:
```console
$ cd rtu-curriculum-parser
$ python -m pip install .
```
