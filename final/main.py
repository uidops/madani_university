#!/usr/bin/env python
# coding: utf-8

import math


numbers = ['صفر', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه',
        'ده', 'یازده', 'دوازده', 'سیزده', 'چهارده', 'پانزده', 'شانزده', 'هفده', 'هجده', 'نوزده']

excep_scales = ['بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود',
        'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد']

short_scales = ['هزار', 'میلیون', 'بیلیون', 'تریلیون', 'کوآدریلیون', 'کوینتیلیون', 'سکستیلیون',
        'سپتیلیون', 'اکتیلیون', 'نانیلیون', 'دسیلیون', 'آندسیلیون', 'دیودسیلیون',
        'تریدسیلیون', 'کواتیوردسیلیون', 'کویندسیلیون', 'سکسدسیلیون', 'سپتدسیلیون',
        'اُکتودسیلیون', 'نومدسیلیون', 'ویجینتیلیون', 'آنویجینتیلیون', 'دویجینتیلیون', 'ترسویجینتیلیون',
        'کوادرویجینتیلیون', 'کوینکاویجینتیلیون', 'سیسویجینتیلیون', 'سپتمویجینتیلیون', 'آکتوویجینتیلیون',
        'نومویجینتیلیون', 'تریویجینتیلیون', 'آنتریویجینتیلیون', 'دوتریویجینتیلیون', 'گوگول']


separator = 'و'
__currency = 'ریال'
negative = 'منفی'


def __main():
    number = int(input('num: ').strip())*10
    print(number_to_text(number) + ' ' + __currency)


def number_to_text(number=0, text='', flag=0):
    if type(number) != int or not (bool(text) or number):
        return numbers[0]

    elif number == 0:
        return text


    if number < 0:
        number = abs(number)
        text += negative + ' '

    length = math.floor(math.log10(number)) + 1

    ret = None
    if flag:
        text += ' ' + separator + ' '

    if length == 1:
        text += numbers[number//(10**(length-1))]

    elif length == 2:
        if number//(10**(length-1)) == 1:
            text += numbers[(number//(10**(length-2)))%10 + 10]

        else:
            text += excep_scales[number//(10**(length-1)) - 2]
            ret = 1

    elif length == 3:
        if number//(10**(length-1)) != '0':
            text += excep_scales[number//(10**(length-1)) + 7]

        ret = 1

    else:
        n = length%3 + (length%3+3)*(not length%3)

        text = number_to_text(number//(10**(length-n)), text)
        text += ' ' + short_scales[math.trunc(-(-(length/3)//1)) - 2]

        ret = n

    return text if ret == None else number_to_text(number%(10**(length-ret)), text, 1)


if __name__ == '__main__':
    __main()
