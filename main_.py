import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


f1 = '1.csv'
f2 = '2.csv'

# обрезаем первые 2 строки и сохраняем в кодировке utf-8
with open(f1, 'r', encoding='cp1251') as fin, open(f2, 'w', encoding='utf-8') as fout:
    data = fin.readlines()
    fout.writelines(data[2:])


df_events = pd.read_csv(f2, encoding='utf-8', sep=';')
columns = ['id', 'Date', 'Name', 'Value', 'reserve']
columns1 = dict(zip(df_events.columns, columns))
df_events.rename(columns=columns1, inplace=True)
df_events.drop(columns=columns[-2:], inplace=True)  # удаляем лишние столбцы
df_events.sort_values(by='id', ascending=True, inplace=True)  # сортировка по возрастанию
df_events['Date'] = pd.to_datetime(df_events['Date'],
                                   # unit='ns'  # TODO - привести к мс
                                   )
df_events.set_index('Date', inplace=True)

events_list = pd.unique(df_events['Name'])
# print(events_list)

channels_dict = {}
from grouping_widgets import App
app = App(['___'] + list(events_list) + ['reserve'], channels_dict)
app.mainloop()


# channels_dict = {
#     'LAN2':       {0: ' Ошибка LAN2',
#                    1: ' Активация LAN2'},
#     'SV-поток 2': {0: ' Ошибка SV-потока 2 (W2G_ORU2_01A1_AMU)',
#                    1: ' Прием SV-потока 2 (W2G_ORU2_01A1_AMU)'},
#     'SV-поток 3': {0: ' Ошибка SV-потока 3 (QCG_ORU3_01A1_AMU)',
#                    1: ' Прием SV-потока 3 (QCG_ORU3_01A1_AMU)'},
#     'SV-поток 4': {0: ' Ошибка SV-потока 4 (KQS_ORU4_01A1_AMU)',
#                    1: ' Прием SV-потока 4 (KQS_ORU4_01A1_AMU)'}
# }

channels = channels_dict.keys()

events_dict = {}
for ch_name, ch_dict in channels_dict.items():
    for val, event in ch_dict.items():
        events_dict[event] = {}
        events_dict[event]['channel'] = ch_name
        events_dict[event]['val'] = val

del ch_name, ch_dict

# events_dict:
# {' Активация LAN2': {'channel': 'LAN2', 'val': 1},
#  ' Ошибка LAN2': {'channel': 'LAN2', 'val': 0},
#  ' Ошибка SV-потока 2 (W2G_ORU2_01A1_AMU)': {'channel': 'SV-поток 2', 'val': 0},
#  ' Ошибка SV-потока 3 (QCG_ORU3_01A1_AMU)': {'channel': 'SV-поток 3', 'val': 0},
#  ' Ошибка SV-потока 4 (KQS_ORU4_01A1_AMU)': {'channel': 'SV-поток 4', 'val': 0},
#  ' Прием SV-потока 2 (W2G_ORU2_01A1_AMU)': {'channel': 'SV-поток 2', 'val': 1},
#  ' Прием SV-потока 3 (QCG_ORU3_01A1_AMU)': {'channel': 'SV-поток 3', 'val': 1},
#  ' Прием SV-потока 4 (KQS_ORU4_01A1_AMU)': {'channel': 'SV-поток 4', 'val': 1}}
...

# создать пустой df2 (строки - время, столбцы - каналы из словаря каналов)
df_channels_diagram = pd.DataFrame(index=df_events.index, columns=channels)

# создать Курсор
cursor = dict(zip(channels, [None] * len(channels)))
# {'LAN2': None, 'SV-поток 2': None, 'SV-поток 3': None, 'SV-поток 4': None}

# готовим начальное значение курсора (пройтись по всем каналам, найти самую раннюю запись и записать инверсное значение в Курсор)
for event in df_events['Name']:
    if not None in cursor.values():
        break
    channel = events_dict[event]['channel']
    if cursor[channel] is None:
        cursor[channel] = (events_dict[event]['val'] == 0) * 1  # присваиваем инверсное значение

# print(cursor)

# пройтись Курсором по всем записям - обновляем значения в данную метку времени для измененных каналов
            # (может быть несколько одновременно), затем записываем курсор в качестве строки по текущей метке времени
for date in df_events.index:
    # print(df_channels_diagram.loc[date])
    event = df_events.loc[date]['Name']
    channel = events_dict[event]['channel']
    value = events_dict[event]['val']
    cursor[channel] = value
    df_channels_diagram.loc[date] = cursor
    # print()

# print(df_channels_diagram)

# plt.stem(df_channels_diagram[df_channels_diagram.columns[0]])
plt.figure()
# plt.subplot(141)

for n, channel in enumerate(df_channels_diagram.columns):
    start_no = len(channels_dict)
    if start_no > 9:
        raise AssertionError  # TODO !!!
    plt.subplot(start_no * 100 + 11 + n)
    plt.step(df_channels_diagram.index,
             df_channels_diagram[df_channels_diagram.columns[n]],
             where='post')
    plt.ylabel(df_channels_diagram.columns[n], rotation=0, fontsize=6, ha='right',
               # labelpad=0,
               )
    # plt.xlabel(df_channels_diagram.index)
    plt.yticks([])
    if n != start_no - 1:
        plt.xticks([])  # убираем подписи у всех, кроме последнего


plt.show()
