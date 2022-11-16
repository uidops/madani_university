#!/usr/bin/env python
# coding: utf-8

import sys

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

separator = ' و '
currency = ' ریال'
negative = 'منفی '


def main():
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} [num]')
        sys.exit(1)

    number = sys.argv[1].strip() + '0'
    try:
        number = int(number)
    except ValueError:
        print('The input is not an integer')
        sys.exit(1)

    print(number_to_text(number) + currency)


def number_to_text(number=0, text='', flag=0):
    if type(number) != int:
        return numbers[0]

    number = str(number)
    if number[0] == '-':
        number = number[1:]
        text += negative

    ret = None
    if not len(number) or number == '0':
        if not bool(text):
            text += numbers[0]

        return text

    if flag and set(number) != {'0'}:
        text += separator

    if len(number) == 1:
        text += numbers[int(number[0])]

    elif len(number) == 2:
        if number[0] == '1':
            text += numbers[int(number[1]) + 10]

        else:
            text += excep_scales[int(number[0]) - 2]
            ret = 1

    elif len(number) == 3:
        if number[0] != '0':
            text += excep_scales[int(number[0]) + 7]

        ret = 1

    else:
        n = len(number)%3
        n += (n+3)*(not n)

        text = number_to_text(int(number[:n]), text)
        if number[0] != '0':
            text += ' ' + short_scales[int(-(-(len(number)/3)//1)) - 2]

        ret = n

    return text if ret == None else number_to_text(int(number[ret:]), text, 1)


if __name__ == '__main__':
    main()
