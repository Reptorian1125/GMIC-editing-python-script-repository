import pyperclip as pc
import re

pos=1
u_string=""

while True:
    init_mode=input("""
    Type in the one of the two characters in the set of two character at the left to use one of those mode?
    0F. Remove Number and Period. 
    1T. Add Numbers and Period 
    Choice: """)
    if init_mode=="0" or init_mode=="F":
        mode=False
        break
    elif init_mode=="1" or init_mode=="T":
        mode=True
        break

def output_number_dots(n):
    global pos
    global u_string
    out_str=""
    new_u_string=[]
    for p in range(n):
        out_str=out_str+str(pos+p)+"."
        new_u_string.append("$"+str(pos+p))
    new_u_string=",".join(new_u_string)
    u_string+="\"{"+new_u_string+"}\"\\\n"
    pos+=n
    return out_str
def count_number_color(inp_str):
    if inp_str[1]=='#':
        if len(inp_str)==9:
            return 3
        else:
            return 4
    else:
        return inp_str.count(",")+1
def process_level_2_mode_0(inp_str):
    current_pos=0
    for c in inp_str:
        if not (c.isnumeric() or c=='.'):
            break
        current_pos+=1
    return inp_str[current_pos:]
def process_level_2_mode_1(inp_str):
    try:
        variable_equal_type_str=re.search(level_2,inp_str).groups()
    except AttributeError:
        variable_equal_type_str=re.search(level_2, inp_str)
    if variable_equal_type_str is None:
        return inp_str
    separated_info=list(variable_equal_type_str)
    if separated_info[1]=="color" or separated_info[1]=="_color":
        num_of_cols=count_number_color(separated_info[2])
        new_variable_name=output_number_dots(num_of_cols)+separated_info[0]
        separated_info[0]=new_variable_name
        separated_info[1]="="+separated_info[1]
    elif separated_info[1]=="point" or separated_info[1]=="_point":
        separated_info[0]=output_number_dots(2)+separated_info[0]
        separated_info[1] = "=" + separated_info[1]
    else:
        separated_info[0]=output_number_dots(1)+separated_info[0]
        separated_info[1] = "=" + separated_info[1]
    return "".join(separated_info)

copied_code=pc.paste()
copied_code_str=str(copied_code)
copied_code_str_line=copied_code_str.splitlines()

level_0=r'(\#@gui\s*:|\)\,(?=([A-Z]|[0-9])))(.*)=(int|float|choice|text|bool|button|point|color|folder|file|text|_int|_float|_choice|_text|_bool|_button|_point|_color|_folder|_file|_text)(\(.*\)|{.*})(.*)'
level_1=r'((?<=\)),(?=[A-Z])|(?<=\}),(?=[A-Z])|(?<=\)),(?=[0-9])|(?<=\}),(?=[0-9]))'
level_2=r'(.*)=(int|float|choice|text|bool|button|point|color|folder|file|text|_int|_float|_choice|_text|_bool|_button|_point|_color|_folder|_file|_text)(\(.*\)|{.*})(.*)'

print("\n")

for line in copied_code_str_line:
    search_result=re.search(level_0, line)
    if search_result==None:
        print(line)
    else:
        if line[:7]=="#@gui :":
            new_line=line[7:]
        else:
            new_line=line[6:]
        level_1_search_result=re.search(level_1,new_line)
        if level_1_search_result==None:
            if mode==1:
                print("#@gui:"+process_level_2_mode_1(new_line))
            else:
                print("#@gui:" + process_level_2_mode_0(new_line))
        else:
            v_level_2=re.split(level_1,new_line)
            new_level_2=[]
            for index in v_level_2:
                if mode==1:
                    new_level_2.append(process_level_2_mode_1(index))
                else:
                    new_level_2.append(process_level_2_mode_0(index))
            print("#@gui:"+"".join(new_level_2))

if mode==1:
    print("\nu "+u_string)