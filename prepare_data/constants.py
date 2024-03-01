ARABIC_CHARS = 'دصضذطكثنتالبيسجحإأآشظمغفقةىرؤءئزوخهع'
KURDISH_CHARS = 'ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنهەوووۆیێ'
VALID_PUNCS = '\?؟\.\\\/,،«»\-:'

ARABIC_PUCTUATIONS = "،؛۔٫٪؟"
CKB_PUNCTUATIONS = "!.:;?،؛؟«»"  

NUMBERS = '٠١٢٣٤٥٦٧٨٩'
SPECIAL = ' '

NORMLIZER_MAPPER = {
    'ﻹ': 'لإ',
    'ﻷ': 'لأ',
    'ﻵ': 'لآ',
    'ﻻ': 'لا'
}
VALID_CHARS = KURDISH_CHARS + SPECIAL + NUMBERS + CKB_PUNCTUATIONS 


KEYBOARD_KEYS = [
    'قوەرتیئحۆپ',
    'اسدفگهژکل',
    'زخجڤبنم'
]
KEYBOARD_BLANK = '_'