import math

numbers = ['Yek', 'Do', 'Seh', 'Chahar', 'Panj', 'Shish', 'Haft', 'Hasht', 'Noh']
numbers += ['Dah', 'Yazdah', 'Davazdah', 'Sizdah', 'Chahardah', 'Panzdah', 'Shanzdah', 'Hefdah', 'Hejdah', 'Nozdah']

exceptions = ['Bist', 'Si', 'Chehel', 'Panjah', 'Shast', 'Haftad', 'Hashtad', 'Navad']
exceptions += ['Sad', 'Divist', 'Sisad', 'Chahrsad', 'Pansad', 'Sheshsad', 'Haftsad', 'Hashtsad', 'Nohsad']

short_scales = ['Hezar', 'Million', 'Billion', 'Trillion', 'Quadrillion', 'Quintillion', 'Sextillion']
short_scales += ['Septillion', 'Octillion', 'Nonillion', 'Decillion', 'Undecillion', 'Duodecillion']
short_scales += ['Tredecillion', 'Quattuordecillion', 'Quindecillion', 'Sexdecillion', 'Septendecillion']
short_scales += ['Octodecillion', 'Novemdecillion', 'Vigintillion']

and_exp = 'o '

def main():
    the_number = input('gimme the number: ')
    print(number_to_text(the_number))


def number_to_text(number='0', text=''):
    number = strip_number(number)
    if number == None:
        return text

    if len(number) == 1:
        if number == '0':
            # print 0 only when the number's length is 1
            if text == '':
                text += 'Sefr'
        else:
            text += numbers[int(number[0])-1]

    elif len(number) == 2:
        if number[0] == '1':
            # print 10-19
            text += numbers[int(number[1]) + 9]
        else:
            # print 20-99
            text += exceptions[int(number[0]) - 2] if number[0] != '0' else ''
            text += and_exp if number[1:].replace('0', '') != '' else ''
            return number_to_text(number[1:], text)

    elif len(number) == 3:
        # print 100-999
        text += exceptions[int(number[0]) + 7] if number[0] != '0' else ''
        text += and_exp if number[1:].replace('0', '') != '' else ''
        return number_to_text(number[1:], text)

    else:
        # calculate the multiple of the scale
        # for example, for number 12,124,291, the output is 12
        #                         1,000       the output is  1
        n = len(number)%3
        n = 3 if not n else n


        text = number_to_text(number[:n], text)

        # math.ceil(len(number)/3)-2 gives us the position of the scale in the short_scales list
        text += ' ' + short_scales[math.ceil(len(number)/3)-2] if number[0] != '0' else ''
        text += and_exp if number[n:].replace('0', '') != '' else ''

        return number_to_text(number[n:], text)

    return text


def strip_number(number):
    """
    Remove the extra zeros from the number
    """

    for i,j in enumerate(number):
        if j != '0':
            break;
            
    return number[i:]

if __name__ == '__main__':
    main()
