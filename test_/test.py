channels_dict = {
    'LAN2':       {0: ' Ошибка LAN2',
                   1: ' Активация LAN2'},
    'SV-поток 2': {0: ' Ошибка SV-потока 2 (W2G_ORU2_01A1_AMU)',
                   1: ' Прием SV-потока 2 (W2G_ORU2_01A1_AMU)'},
    'SV-поток 3': {0: ' Ошибка SV-потока 3 (QCG_ORU3_01A1_AMU)',
                   1: ' Прием SV-потока 3 (QCG_ORU3_01A1_AMU)'},
    'SV-поток 4': {0: ' Ошибка SV-потока 4 (KQS_ORU4_01A1_AMU)',
                   1: ' Прием SV-потока 4 (KQS_ORU4_01A1_AMU)'}
}

events_dict = {}
for ch_name, ch_dict in channels_dict.items():
    for val, event in ch_dict.items():
        events_dict[event] = {}
        events_dict[event]['channel'] = ch_name
        events_dict[event]['val'] = val

import pprint
pprint.pprint(events_dict)
