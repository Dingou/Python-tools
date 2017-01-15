#!/usr/bin/python


if __name__ == "__main__":
    str = "Aa1234bBAa"
    str.lower()
    str.upper()
    str.islower()
    str.isupper()
    str.title()  #首字母大写
    str.capitalize()  #首字母大写其他小写
    str.swapcase()  #大小写替换
    str.find('Aa')
    str.replace('a','z') #字母替换
    str.find('Aa',1) #start place
    a = ['', 'a', 'b', 'c']
    "+".join(a)
    "/".join(a)
    "1+2+3+4".split('+')
    str1 = "**** ! *** aaaa"
    str.strip(' *!') #默认为去掉空格,参数为去掉这些字符 'aaaa'


