from functools import partial
import re
import pyperclip as pc

gmic_str_paste=pc.paste()
gmic_str=str(gmic_str_paste)

pattern = re.compile(r"(?<=\$)(?:\{(\d+)-(\d+)\}|(\d+)|\{(\d+)=\})")

def addfunc(m, *, n, v):
    def incif(num):
        return num + n if num >= v else num

    a, b, c , d = m[1], m[2], m[3], m[4]
    if a and b:
        a = incif(int(a))
        b = incif(int(b))
        return f'{{{a}-{b}}}'
    elif c:
        c = incif(int(c))
        return f'{c}'
    elif d:
        d = incif(int(d))
        return f'{{{d}=}}'

inc_number=input("Increment Number: ")
greater_or_equal_to_num=input("Affect only number greater or equal to: ")

add = partial(addfunc, n=int(inc_number), v=int(greater_or_equal_to_num))

out_string = pattern.sub(add, gmic_str)

print("\n"+out_string)