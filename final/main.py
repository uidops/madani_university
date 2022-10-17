from math import ceil

numbers = ['یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه',
        'ده', 'یازده', 'دوازده', 'سیزده', 'چهارده', 'پانزده', 'شانزده', 'هفده', 'هجده', 'نوزده']

excep_scales = ['بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود',
        'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد']

short_scales = ['هزار', 'میلیون', 'بیلیون', 'تریلیون', 'کوآدریلیون', 'کوینتیلیون', 'سکستیلیون',
        'سپتیلیون', 'اکتیلیون', 'نانیلیون', 'دسیلیون', 'آندسیلیون', 'دیودسیلیون',
        'تریدسیلیون', 'کواتیوردسیلیون', 'کویندسیلیون', 'سکسدسیلیون', 'سپتدسیلیون',
        'اُکتودسیلیون', 'نومدسیلیون', 'ویجینتیلیون', 'آنویجینتیلیون', 'دویجینتیلیون', 'ترسویجینتیلیون',
        'کوادرویجینتیلیون', 'کوینکاویجینتیلیون', 'سیسویجینتیلیون', 'سپتمویجینتیلیون', 'آکتوویجینتیلیون',
        'نومویجینتیلیون', 'تریویجینتیلیون', 'آنتریویجینتیلیون', 'دوتریویجینتیلیون', 'گوگول']

and_exp = ' و '
currency = ' ریال'

def main():
    the_number = input('number: ') + '0'
    print(number_to_text(the_number) + currency)


def number_to_text(number='0', text=''):
    number = strip_number(number)
    if number == None:
        return text

    if len(number) == 1:
        if number == '0':
            # print 0 only when the number's length is 1
            if text == '':
                text += 'صفر'
        else:
            text += numbers[int(number[0])-1]

    elif len(number) == 2:
        if number[0] == '1':
            # print 10-19
            text += numbers[int(number[1]) + 9]
        else:
            # print 20-99
            text += excep_scales[int(number[0]) - 2] if number[0] != '0' else ''
            text += and_exp if number[1:].replace('0', '') != '' else ''
            return number_to_text(number[1:], text)

    elif len(number) == 3:
        # print 100-999
        text += excep_scales[int(number[0]) + 7] if number[0] != '0' else ''
        text += and_exp if number[1:].replace('0', '') != '' else ''
        return number_to_text(number[1:], text)

    else:
        # calculate the multiple of the scale
        # for example, for number 12,124,291, the output is 12
        #                         1,000       the output is  1
        n = len(number)%3
        n = 3 if not n else n


        text = number_to_text(number[:n], text)

        # ceil(len(number)/3)-2 gives us the position of the scale in the short_scales list
        text += ' ' + short_scales[ceil(len(number)/3)-2] if number[0] != '0' else ''
        text += and_exp if number[n:].replace('0', '') != '' else ''

        return number_to_text(number[n:], text)

    return text


def strip_number(number):
    """
    Remove the extra zeros from the number
    """
    i = 0
    for i,j in enumerate(number):
        if j != '0':
            break
            
    return number[i:]

if __name__ == '__main__':
    main()
