#!/usr/bin/env python
# coding: utf-8

import math

numbers = ('صفر', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه',
        'ده', 'یازده', 'دوازده', 'سیزده', 'چهارده', 'پانزده', 'شانزده', 'هفده', 'هجده', 'نوزده')

excep_scales = ('بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود',
        'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد')

short_scales = ('هزار', 'میلیون', 'بیلیون', 'تریلیون', 'کوآدریلیون', 'کوینتیلیون', 'سکستیلیون',
        'سپتیلیون', 'اکتیلیون', 'نانیلیون', 'دسیلیون', 'آندسیلیون', 'دیودسیلیون',
        'تریدسیلیون', 'کواتیوردسیلیون', 'کویندسیلیون', 'سکسدسیلیون', 'سپتدسیلیون',
        'اُکتودسیلیون', 'نومدسیلیون', 'ویجینتیلیون', 'آنویجینتیلیون', 'دویجینتیلیون', 'ترسویجینتیلیون',
        'کوادرویجینتیلیون', 'کوینکاویجینتیلیون', 'سیسویجینتیلیون', 'سپتمویجینتیلیون', 'آکتوویجینتیلیون',
        'نومویجینتیلیون', 'تریویجینتیلیون', 'آنتریویجینتیلیون', 'دوتریویجینتیلیون', 'گوگول')


separator = 'و'
__currency = 'ریال'
negative = 'منفی'

x = (0, 0, -2, 7)

def __main():
    number = math.trunc(float(input('num: ').strip())*10)
    print(number_to_text(number) + ' ' + __currency)


def number_to_text(number=0, text='', flag=False):
    if not (text or number) or type(number) != int:
        return numbers[0]
    elif number == 0:
        return text

    if number < 0:
        number = ~(number - 1)
        text += negative + ' '
    elif flag:
        text += f' {separator} '

    length = math.floor(math.log10(number)) + 1
    ret = 0

    if number > 0x3e7:
        ret = length%3 or 3
        text += number_to_text(number//(10**(length-ret))) + ' ' + short_scales[math.ceil(length/3) - 2]

    elif number < 0x14:
        text += numbers[number]

    else:
        text += excep_scales[number//10**(length-1) + x[length]]
        ret = 1

    return number_to_text(number%(10**(length-ret)), text, True) if ret else text


if __name__ == '__main__':
    __main()
