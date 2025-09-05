# pegas

Проект на Python для построения карты с результатами измерений мощности дозы в точках.

## Установка

1. Склонируйте репозиторий:
  ```shell
  $ git clone https://github.com/czertyaka/pegas.git
  ```
2. Установите зависимости:
  ```shell
  # Если используете pip:
  $ pip install -r requiremenets.txt
  # Если используете nix:
  $ nix-shell
  ```

## Описание

Программа принимает обязательный входной файл с мощностями доз в формате CSV.
Пример файла:

```csv
Долгота;Широта;МАЭД, мкЗВ/ч
73.391289;33.07328;0.091
73.391277;33.073272;0.091
73.391216;33.073276;0.093
73.39117;33.073295;0.092
73.391067;33.073313999999996;0.092
73.390983;33.073326;0.092
73.390911;33.073344999999996;0.092
73.390873;33.073348;0.093
73.390873;33.073348;0.093
...
```

Есть опциональный параметр для "профилей".
В CSV-файле должны быть координаты "профилей", которые отобразятся на карте в виде пунктирных отрезков.
Пример файла:

```csv
lon_1;lat_1;lon_2;lat_2
73.8;33.74;73.95;33.885
73.86;33.74;73.01;33.885
...
```

Список всех аргументов программы:

```shell
$ python main.py --help
usage: pegas [-h] -d DOSES_FILE [-pr PROFILES_FILE] [-c CLIP_FILE] [-t {scatter,heatmap}]
             [-o PLOT_FILE]

PEdestrian GAmma Survey (pegas) is designed to plot pedestrian gamma-ray survey results.

options:
  -h, --help            show this help message and exit
  -d DOSES_FILE, --doses-file DOSES_FILE
                        CSV file path with cooridnates and dose rates
  -pr PROFILES_FILE, --profiles-file PROFILES_FILE
                        CSV file path with profiles coordinates
  -c CLIP_FILE, --clip-file CLIP_FILE
                        Geojson file with single polygon to clip shown data
  -t {scatter,heatmap}, --plot-type {scatter,heatmap}
                        Plot type (default: scatter)
  -o PLOT_FILE, --output PLOT_FILE
                        Output image file path, open image if not given
```

## Пример

Так можно создать карту с результатами измерений из примера:

```shell
$ python main.py -d example/doses.csv
```

![plot](./example/output.png)
