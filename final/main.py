#!/usr/bin/env python
# coding: utf-8

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

def main():
    number = input('number: ')
    neg = ''
    if number[0] == '-':
        number = number[1:]
        if int(number):
            neg = 'منفی '

    print(neg + number_to_text(number) + currency)


def number_to_text(number='0', text='', flag=0):
    number = number.lstrip('0')
    if not len(number):
        return text

    text += separator if flag and set(number) != {'0'} else ''
    if len(number) == 1:
        if number == '0':
            if not bool(text):
                text += numbers[0]

        else:
            text += numbers[int(number[0])]

    elif len(number) == 2:
        if number[0] == '1':
            text += numbers[int(number[1]) + 10]

        else:
            text += excep_scales[int(number[0]) - 2]
            return number_to_text(number[1:], text, 1)

    elif len(number) == 3:
        if number[0] != '0':
            text += excep_scales[int(number[0]) + 7]

        return number_to_text(number[1:], text, 1)

    else:
        n = len(number) % 3
        n += (n+3) * (not n)

        text = number_to_text(number[:n], text)
        if number[0] != '0':
            text += ' ' + short_scales[int(-(-(len(number) / 3)//1)) - 2]

        return number_to_text(number[n:], text, 1)

    return text


if __name__ == '__main__':
    main()
