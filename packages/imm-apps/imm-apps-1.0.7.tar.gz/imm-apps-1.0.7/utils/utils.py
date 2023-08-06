from datetime import datetime
from enum import Enum, unique
from tabulate import tabulate
import json,readline,collections, csv
from difflib import Differ
import re
from termcolor import colored

# This function used to check a list's continuity of date. The list must have two columns as start date and end date. 
# The fromat must be "yyyy-mm-dd" or "yyy-mm".  The list has to be from most recent to past. You can force sort it by assign sort =True
# The output will be True or False, plus sorted input list and message. 
def checkContinuity(data_set:list,sort=False):
    if sort:
        data_set=sorted(data_set,key=lambda x: (x[0],x[1]),reverse=True)
    ok=[]
    errors=[]
    def difference(l1,l2):
        if bool(re.search(r'^\d{4}-\d{2}-\d{2}',l1)) and bool(re.search(r'^\d{4}-\d{2}-\d{2}',l2)):
            current_start=datetime.strptime(l1,'%Y-%m-%d')
            previous_end=datetime.strptime(l2,'%Y-%m-%d')
            return (current_start-previous_end).days,'day(s)'
        if bool(re.search(r'^\d{4}-\d{2}',l1)) and bool(re.search(r'^\d{4}-\d{2}',l2)):
            y1,m1=l1.split('-')
            y2,m2=l2.split('-')
            return (int(y1)-int(y2))*12+int(m1)-int(m2),'month(s)'
    
    for i in range(len(data_set)-1):
        diff,unit=difference(data_set[i][0],data_set[i+1][1])
        if diff>1:
            ok.append(False)
            errors.append(f"{'List sorted. ' if sort else ''}The date is not continious between line {i+1} to {i+2} (missed {diff-1} {unit})")
        elif diff<0:
            ok.append(False)
            errors.append(f"{'List sorted. ' if sort else ''}The date is not continious between line {i+1} to {i+2} (overlapped {diff} {unit})")
        else:
            ok.append(True)
    if all(ok):
        return True,data_set,"date is continious"
    else:
        return False,data_set,errors
    
#  Used to find different between two text strings. Initialize with tc=TextChanged(t1,t2), and get differences by tc.text_added or tc.text_deleted
class TextChanged():
    
    def __init__(self,text1,text2):
        self.text1=text1
        self.text2=text2

    def __get_changed(self):
    
        t1_lines=self.text1.splitlines()
        t2_lines=self.text2.splitlines()

        diff=Differ().compare(t1_lines,t2_lines)
        changed=list(diff)

        added=r'^\+\s(.+)'
        deleted=r'^\-\s(.+)'
        text_added=[ d[2:] for d in changed if re.findall(added,d)] #d[2:] delete '+ ' at the begining
        text_added='\n'.join(text_added)
        text_deleted=[ d[2:] for d in changed if re.findall(deleted,d)]
        text_deleted='\n'.join(text_deleted)

        return {'text_added':text_added,"text_deleted":text_deleted}

    @property
    def text_added(self):
        return self.__get_changed()['text_added']
    
    @property
    def text_deleted(self):
        return self.__get_changed()['text_deleted']


def age(birth_date, the_day=datetime.today()):
    # birth_date=datetime.strptime(birth_date, '%Y-%m-%d')
    return the_day.year - birth_date.year - ((the_day.month, the_day.day) < (birth_date.month, birth_date.day))

def fullname(fn,ln):
    return fn.strip().title()+" "+ln.strip().title()
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))


@unique
class Sex(Enum):
    Female = 0
    Male = 1

# 根据index，从字典里取出key
def getKeybyIndex(dict,index): 
    keylist=[]
    for k,v in dict.items():
        keylist.append(k)
    return keylist[index]

# 根据index，从字典里取出value
def getValuebyIndex(dict,index): 
    keylist=[]
    for k,v in dict.items():
        keylist.append(v)
    return keylist[index]

# 从字典里取出key，变成list
def getKeysinDict(dict): 
    keylist=[]
    for k,v in dict.items():
        keylist.append(k)
    return keylist

# 从字典里取出value，变成list
def getValuesinDict(dict): 
    valve_list=[]
    for k,v in dict.items():
        valve_list.append(v)
    return valve_list

# 按给字典排序，并返回为列表
def Dict2OrderedList(dict):
    ls=[]
    for k, v in dict.items():
        ls.append([k,v])
    
    ls.sort()
    return ls

## List functions
# Remove specific elements in a list
def removeListElements(ls,element=''):
    temp=ls.copy()
    for e in ls:
        if e=='':
            temp.remove(e)
    return temp

# 去除list最后的指定字符
def remove_list_last(ls,element='\n'):
    if ls[-1]==element:
        del ls[-1]
        ls=remove_list_last(ls,element)
        return ls
    else:
        return ls

# 去除list最前的指定字符
def remove_list_first(ls,element='\n'):
    if ls[0]==element:
        del ls[0]
        ls=remove_list_first(ls,element)
        return ls
    else:
        return ls


#根据范围，从列表(2 列)中找到index，返回index
def getIndexByRange(list,data):
    index=0
    for l in list:
        if data>=l[0] and data<=l[1]:
            return index
        index+=1


# 打印1D的列表为多行
def printList(ls,index=True,sep='\t'): # 打印list，默认在前面加上index，用tab分割
    i=0
    for l in ls:
        item=f'{i}{sep}{l}' if index==True else f'{l}'
        print(item)
        i+=1

#将列表变成一行字符串    
def ListInline(ls,sep='\t'):
    item=''
    for l in ls:
        item=item+f'{l}{sep}'
    return item

# 打印2D的列表
def printList2D(ls,index=False,sep='\t'):
        i=0
        item=''
        for l in ls:
            line=ListInline(l,sep)
            item=f'{i}{sep}{line}' if index==True else f'{line}{sep}'
            print(item)
            i+=1

# 使用tabulate 打印formatted 2D的list为表格
def printFList2D(ls,index=False):
        i=0
        items=[]
        for l in ls:
            if index==True: 
               l.insert(0,i) 
               items.append(l)
                
            else:
                 items.append(l)
            i+=1
        print(tabulate(items))

# 2D list to csv table
def List2CSVFile(ls,filename):
    with open(filename,'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for l in ls:
            wr.writerow(l)
# Dict to csv table
def dict2CSVFile(dict,filename):
    with open(filename, 'w') as f:
        for key in dict.keys():
            f.write(f"{key},{dict[key]}\n")

# Read csv fiel to list
def CSVFile2List(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# Read csv fiel to dict
def CSVFile2Dict(filename):
    with open(filename, newline='') as f:
        data={}
        reader = list(csv.reader(f))
        for line in reader:
            data[line[0]]=line[1]
    return data

# 打印dict，默认用tab分割
def printDict(dt,index=False,sep='\t'): 
    i=0
    for k,v in dt.items():
        item=f'{str(i)}{sep}{str(k)}{sep}{str(v)}' if index==True else f'{str(k)}{sep}{str(v)}'
        print(item)
        i+=1
# 使用tabulate 打印formatted dict表格
def printFDict(dt,index=False,sep='_'): 
    i=0
    items=[]
    for k,v in dt.items():
        k=str(k).replace(sep,' ').capitalize()
        items.append([i,str(k),str(v)]) if index==True else items.append([str(k),str(v)])
        i+=1
    print(tabulate(items))

# 使用tabulate 打印API json list-dict表格
def printListDict(responses,index=False,sep='_'): 
    i=0
    items=[]
    records=len(responses)
    if records==0:
        return 0
    items.append(responses[0].keys())
    for response in responses:
        items.append(response.values())
    print(colored(f"Total {records} records","green"))
    print(tabulate(items))

# 使用tabulate 打印API json list-dict表格中指定字段
def printListDictFields(responses,index=False,sep='_',fields=None,titles=None):
    if fields:
        new_list=[titles] if titles else [fields]   # setup title with given titles or just use keys 
        for res in responses:
            sub_list=[]
            for field in fields:
                sub_list.append(res[field])
            new_list.append(sub_list)
        printFList2D(new_list)
    else:
       printListDict(responses,index=index,sep=sep)


# 使用tabulate 打印formatted dict里包含另一个dict的表格
def printFDict2(dt,index=False,sep='_'): 
    i=0
    items=[]
    for k,v in dt.items():
        if not isinstance(v,dict):
            k=str(k).replace(sep,' ').capitalize()
            items.append([i,str(k),str(v)]) if index==True else items.append([str(k),str(v)])
            i+=1
        else:
            j=0
            items.append([i,str(k),'']) if index==True else items.append([str(k),''])
            i+=1
            for k1,v1 in v.items():
                    k=str(k1).replace(sep,' ').capitalize()
                    items.append([j,".   "+str(k1),str(v1)]) if index==True else items.append(['.   '+str(k1),str(v1)])
                    j+=1
    print(tabulate(items))

# 使用递归算饭，从多维列表中取出值变成一维列表
def multi_list2one(multi_D_list: list,one_list=[]):
    for ml in multi_D_list:
        if isinstance(ml,list):
            one_list=multi_list2one(ml,one_list)    #递归调用
        else:
             one_list.append(ml)
    return one_list

# 多维列表变成一维列表后做成set（去掉重复项）
def list2set(multi_D_list):
    one_list=multi_list2one(multi_D_list)
    return set(one_list)

# input list and outpout markdown table text
def markdown_table(ds:list):
    head=ds[0]
    head_str="|"
    head_sep="|"
    for col in range(0,len(ds[0])):
        head_str+=str(head[col])+"|"
        head_sep+="------------- "+"|"
    # print(head_str)
    # print(head_sep)
    output=head_str+"\n"+head_sep+"\n"

    row_data="|"
    for row in range(1,len(ds)):
        for col in range(0,len(ds[0])):
            row_data+=str(ds[row][col])+"|"
        #print(row_data)
        output+=row_data+"\n"
        row_data="|"
    
    return output

# JSON 操作
def read_json(filename):            # read json file and return a python dict 
    with open(filename) as f:       
        data=json.load(f)
    return data

def save_json(dict, filename):      # write a python dict to json file 
    with open(filename, 'w') as fp:
        json.dump(dict, fp)

# write file
def write_file(filename,text):
    with open(filename, "w") as f:
        f.write(text)
        f.close()

# Some common input functions
def multi_line_input():
    print("Ctrl-D  to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)

def edit_input(prompt='', prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()

def multi_line_edit_input(prefill=''):
    contents = []
    for l in prefill.split('\n'):
        try:
            line = edit_input('',l)
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)

def list_edit_input(prefill=''):
    contents = []
    for l in prefill:
        try:
            line = edit_input('',l)
        except EOFError:
            break
        contents.append(line)
    return contents

from datetime import datetime
from enum import Enum, unique
from tabulate import tabulate
import json,readline,collections, csv
from difflib import Differ
import re
from termcolor import colored
from datetime import date

# This function used to check a list's continuity of date. The list must have two columns as start date and end date. 
# The fromat must be "yyyy-mm-dd" or "yyy-mm".  The list has to be from most recent to past. You can force sort it by assign sort =True
# The output will be True or False, plus sorted input list and message. 
def checkContinuity(data_set:list,sort=False):
    if sort:
        data_set=sorted(data_set,key=lambda x: (x[0],x[1]),reverse=True)
    ok=[]
    errors=[]
    def difference(l1,l2):
        if bool(re.search(r'^\d{4}-\d{2}-\d{2}',l1)) and bool(re.search(r'^\d{4}-\d{2}-\d{2}',l2)):
            current_start=datetime.strptime(l1,'%Y-%m-%d')
            previous_end=datetime.strptime(l2,'%Y-%m-%d')
            return (current_start-previous_end).days,'day(s)'
        if bool(re.search(r'^\d{4}-\d{2}',l1)) and bool(re.search(r'^\d{4}-\d{2}',l2)):
            y1,m1=l1.split('-')
            y2,m2=l2.split('-')
            return (int(y1)-int(y2))*12+int(m1)-int(m2),'month(s)'
    
    for i in range(len(data_set)-1):
        date1=data_set[i][0] 
        date2=data_set[i+1][1]
        date1=date1.strftime("%Y-%m-%d") if type(date1)==date else date1
        date2=date2.strftime("%Y-%m-%d") if type(date2)==date else date2
        
        diff,unit=difference(date1,date2)
        if diff>1:
            ok.append(False)
            errors.append(f"{'List sorted. ' if sort else ''}The date is not continious between data line {i+1} to {i+2} (missed {diff-1} {unit})")
        elif diff<0:
            ok.append(False)
            errors.append(f"{'List sorted. ' if sort else ''}The date is not continious between data line {i+1} to {i+2} (overlapped {diff} {unit})")
        else:
            ok.append(True)
    if all(ok):
        return True,data_set,"date is continious"
    else:
        return False,data_set,errors
    
#  Used to find different between two text strings. Initialize with tc=TextChanged(t1,t2), and get differences by tc.text_added or tc.text_deleted
class TextChanged():
    
    def __init__(self,text1,text2):
        self.text1=text1
        self.text2=text2

    def __get_changed(self):
    
        t1_lines=self.text1.splitlines()
        t2_lines=self.text2.splitlines()

        diff=Differ().compare(t1_lines,t2_lines)
        changed=list(diff)

        added=r'^\+\s(.+)'
        deleted=r'^\-\s(.+)'
        text_added=[ d[2:] for d in changed if re.findall(added,d)] #d[2:] delete '+ ' at the begining
        text_added='\n'.join(text_added)
        text_deleted=[ d[2:] for d in changed if re.findall(deleted,d)]
        text_deleted='\n'.join(text_deleted)

        return {'text_added':text_added,"text_deleted":text_deleted}

    @property
    def text_added(self):
        return self.__get_changed()['text_added']
    
    @property
    def text_deleted(self):
        return self.__get_changed()['text_deleted']


def age(birth_date, the_day=datetime.today()):
    # birth_date=datetime.strptime(birth_date, '%Y-%m-%d')
    return the_day.year - birth_date.year - ((the_day.month, the_day.day) < (birth_date.month, birth_date.day))

def fullname(fn,ln):
    return fn.strip().title()+" "+ln.strip().title()
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))


@unique
class Sex(Enum):
    Female = 0
    Male = 1

# 根据index，从字典里取出key
def getKeybyIndex(dict,index): 
    keylist=[]
    for k,v in dict.items():
        keylist.append(k)
    return keylist[index]

# 根据index，从字典里取出value
def getValuebyIndex(dict,index): 
    keylist=[]
    for k,v in dict.items():
        keylist.append(v)
    return keylist[index]

# 从字典里取出key，变成list
def getKeysinDict(dict): 
    keylist=[]
    for k,v in dict.items():
        keylist.append(k)
    return keylist

# 从字典里取出value，变成list
def getValuesinDict(dict): 
    valve_list=[]
    for k,v in dict.items():
        valve_list.append(v)
    return valve_list

# 按给字典排序，并返回为列表
def Dict2OrderedList(dict):
    ls=[]
    for k, v in dict.items():
        ls.append([k,v])
    
    ls.sort()
    return ls

## List functions
# Remove specific elements in a list
def removeListElements(ls,element=''):
    temp=ls.copy()
    for e in ls:
        if e=='':
            temp.remove(e)
    return temp

# 去除list最后的指定字符
def remove_list_last(ls,element='\n'):
    if ls[-1]==element:
        del ls[-1]
        ls=remove_list_last(ls,element)
        return ls
    else:
        return ls

# 去除list最前的指定字符
def remove_list_first(ls,element='\n'):
    if ls[0]==element:
        del ls[0]
        ls=remove_list_first(ls,element)
        return ls
    else:
        return ls


#根据范围，从列表(2 列)中找到index，返回index
def getIndexByRange(list,data):
    index=0
    for l in list:
        if data>=l[0] and data<=l[1]:
            return index
        index+=1


# 打印1D的列表为多行
def printList(ls,index=True,sep='\t'): # 打印list，默认在前面加上index，用tab分割
    i=0
    for l in ls:
        item=f'{i}{sep}{l}' if index==True else f'{l}'
        print(item)
        i+=1

#将列表变成一行字符串    
def ListInline(ls,sep='\t'):
    item=''
    for l in ls:
        item=item+f'{l}{sep}'
    return item

# 打印2D的列表
def printList2D(ls,index=False,sep='\t'):
        i=0
        item=''
        for l in ls:
            line=ListInline(l,sep)
            item=f'{i}{sep}{line}' if index==True else f'{line}{sep}'
            print(item)
            i+=1

# 使用tabulate 打印formatted 2D的list为表格
def printFList2D(ls,index=False):
        i=0
        items=[]
        for l in ls:
            if index==True: 
               l.insert(0,i) 
               items.append(l)
                
            else:
                 items.append(l)
            i+=1
        print(tabulate(items))

# 2D list to csv table
def List2CSVFile(ls,filename):
    with open(filename,'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for l in ls:
            wr.writerow(l)
# Dict to csv table
def dict2CSVFile(dict,filename):
    with open(filename, 'w') as f:
        for key in dict.keys():
            f.write(f"{key},{dict[key]}\n")

# Read csv fiel to list
def CSVFile2List(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

# Read csv fiel to dict
def CSVFile2Dict(filename):
    with open(filename, newline='') as f:
        data={}
        reader = list(csv.reader(f))
        for line in reader:
            data[line[0]]=line[1]
    return data

# 打印dict，默认用tab分割
def printDict(dt,index=False,sep='\t'): 
    i=0
    for k,v in dt.items():
        item=f'{str(i)}{sep}{str(k)}{sep}{str(v)}' if index==True else f'{str(k)}{sep}{str(v)}'
        print(item)
        i+=1
# 使用tabulate 打印formatted dict表格
def printFDict(dt,index=False,sep='_'): 
    i=0
    items=[]
    for k,v in dt.items():
        k=str(k).replace(sep,' ').capitalize()
        items.append([i,str(k),str(v)]) if index==True else items.append([str(k),str(v)])
        i+=1
    print(tabulate(items))

# 使用tabulate 打印API json list-dict表格
def printListDict(responses,index=False,sep='_'): 
    i=0
    items=[]
    records=len(responses)
    if records==0:
        return 0
    items.append(responses[0].keys())
    for response in responses:
        items.append(response.values())
    print(colored(f"Total {records} records","green"))
    print(tabulate(items))

# 使用tabulate 打印API json list-dict表格中指定字段
def printListDictFields(responses,index=False,sep='_',fields=None,titles=None):
    if fields:
        new_list=[titles] if titles else [fields]   # setup title with given titles or just use keys 
        for res in responses:
            sub_list=[]
            for field in fields:
                sub_list.append(res[field])
            new_list.append(sub_list)
        printFList2D(new_list)
    else:
       printListDict(responses,index=index,sep=sep)


# 使用tabulate 打印formatted dict里包含另一个dict的表格
def printFDict2(dt,index=False,sep='_'): 
    i=0
    items=[]
    for k,v in dt.items():
        if not isinstance(v,dict):
            k=str(k).replace(sep,' ').capitalize()
            items.append([i,str(k),str(v)]) if index==True else items.append([str(k),str(v)])
            i+=1
        else:
            j=0
            items.append([i,str(k),'']) if index==True else items.append([str(k),''])
            i+=1
            for k1,v1 in v.items():
                    k=str(k1).replace(sep,' ').capitalize()
                    items.append([j,".   "+str(k1),str(v1)]) if index==True else items.append(['.   '+str(k1),str(v1)])
                    j+=1
    print(tabulate(items))

# 使用递归算饭，从多维列表中取出值变成一维列表
def multi_list2one(multi_D_list: list,one_list=[]):
    for ml in multi_D_list:
        if isinstance(ml,list):
            one_list=multi_list2one(ml,one_list)    #递归调用
        else:
             one_list.append(ml)
    return one_list

# 多维列表变成一维列表后做成set（去掉重复项）
def list2set(multi_D_list):
    one_list=multi_list2one(multi_D_list)
    return set(one_list)

# input list and outpout markdown table text
def markdown_table(ds:list):
    head=ds[0]
    head_str="|"
    head_sep="|"
    for col in range(0,len(ds[0])):
        head_str+=str(head[col])+"|"
        head_sep+="------------- "+"|"
    # print(head_str)
    # print(head_sep)
    output=head_str+"\n"+head_sep+"\n"

    row_data="|"
    for row in range(1,len(ds)):
        for col in range(0,len(ds[0])):
            row_data+=str(ds[row][col])+"|"
        #print(row_data)
        output+=row_data+"\n"
        row_data="|"
    
    return output

# JSON 操作
def read_json(filename):            # read json file and return a python dict 
    with open(filename) as f:       
        data=json.load(f)
    return data

def save_json(dict, filename):      # write a python dict to json file 
    with open(filename, 'w') as fp:
        json.dump(dict, fp)

# write file
def write_file(filename,text):
    with open(filename, "w") as f:
        f.write(text)
        f.close()

# Some common input functions
def multi_line_input():
    print("Ctrl-D  to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)

def edit_input(prompt='', prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)  # or raw_input in Python 2
   finally:
      readline.set_startup_hook()

def multi_line_edit_input(prefill=''):
    contents = []
    for l in prefill.split('\n'):
        try:
            line = edit_input('',l)
        except EOFError:
            break
        contents.append(line)
    return '\n'.join(contents)

def list_edit_input(prefill=''):
    contents = []
    for l in prefill:
        try:
            line = edit_input('',l)
        except EOFError:
            break
        contents.append(line)
    return contents


# Data infrastructure for NOC wage and outlook 
area_info = [
    ["Canada", "Canada", 0],
    ["Newfoundland and Labrador", "Newfoundland and Labrador", 1],
    ["Newfoundland and Labrador", "Avalon Peninsula Region", 2],
    ["Newfoundland and Labrador", "Notre Dame-Central-Bonavista Bay Region", 3],
    ["Newfoundland and Labrador", "South Coast–Burin Peninsula Region", 4],
    ["Newfoundland and Labrador", "West Coast–Northern Peninsula–Labrador Region", 5],
    ["Prince Edward Island", "Prince Edward Island", 6],
    ["Nova Scotia", "Nova Scotia", 7],
    ["Nova Scotia", "Annapolis Valley Region", 8],
    ["Nova Scotia", "Cape Breton Region", 9],
    ["Nova Scotia", "Halifax Region", 10],
    ["Nova Scotia", "North Shore Region", 11],
    ["Nova Scotia", "Southern Region", 12],
    ["New Brunswick", "New Brunswick", 13],
    ["New Brunswick", "Campbellton–Miramichi Region", 14],
    ["New Brunswick", "Edmundston–Woodstock Region", 15],
    ["New Brunswick", "Fredericton–Oromocto", 16],
    ["New Brunswick", "Moncton–Richibucto Region", 17],
    ["New Brunswick", "Saint John–St. Stephen Region", 18],
    ["Quebec", "Quebec", 19],
    ["Quebec", "Abitibi-Témiscamingue Region", 20],
    ["Quebec", "Bas-Saint-Laurent Region", 21],
    ["Quebec", "Capitale-Nationale Region", 22],
    ["Quebec", "Centre-du-Québec Region", 23],
    ["Quebec", "Chaudière-Appalaches Region", 24],
    ["Quebec", "Côte-Nord Region", 25],
    ["Quebec", "Estrie Region", 26],
    ["Quebec", "Gaspésie–Îles-de-la-Madeleine Region", 27],
    ["Quebec", "Lanaudière Region", 28],
    ["Quebec", "Laurentides Region", 29],
    ["Quebec", "Laval Region", 30],
    ["Quebec", "Mauricie Region", 31],
    ["Quebec", "Montréal Region", 32],
    ["Quebec", "Montérégie Region", 33],
    ["Quebec", "Nord-du-Québec Region", 34],
    ["Quebec", "Outaouais Region", 35],
    ["Quebec", "Saguenay–Lac-Saint-Jean Region", 36],
    ["Ontario", "Ontario", 37],
    ["Ontario", "Hamilton–Niagara Peninsula Region", 38],
    ["Ontario", "Kingston–Pembroke Region", 39],
    ["Ontario", "Kitchener–Waterloo–Barrie Region", 40],
    ["Ontario", "London Region", 41],
    ["Ontario", "Muskoka–Kawarthas Region", 42],
    ["Ontario", "Northeast Region", 43],
    ["Ontario", "Northwest Region", 44],
    ["Ontario", "Ottawa Region", 45],
    ["Ontario", "Stratford–Bruce Peninsula Region", 46],
    ["Ontario", "Toronto Region", 47],
    ["Ontario", "Windsor-Sarnia Region", 48],
    ["Manitoba", "Manitoba", 49],
    ["Manitoba", "Interlake Region", 50],
    ["Manitoba", "North Central Region", 51],
    ["Manitoba", "North Region", 52],
    ["Manitoba", "Parklands Region", 53],
    ["Manitoba", "South Central Region", 54],
    ["Manitoba", "Southeast Region", 55],
    ["Manitoba", "Southwest Region", 56],
    ["Manitoba", "Winnipeg Region", 57],
    ["Saskatchewan", "Saskatchewan", 58],
    ["Saskatchewan", "Northern Region", 59],
    ["Saskatchewan", "Prince Albert Region", 60],
    ["Saskatchewan", "Regina–Moose Mountain Region", 61],
    ["Saskatchewan", "Saskatoon–Biggar Region", 62],
    ["Saskatchewan", "Swift Current–Moose Jaw Region", 63],
    ["Saskatchewan", "Yorkton–Melville Region", 64],
    ["Alberta", "Alberta", 65],
    ["Alberta", "Athabasca–Grande Prairie–Peace River Region", 66],
    ["Alberta", "Banff–Jasper–Rocky Mountain House Region", 67],
    ["Alberta", "Calgary Region", 68],
    ["Alberta", "Camrose–Drumheller Region", 69],
    ["Alberta", "Edmonton Region", 70],
    ["Alberta", "Lethbridge–Medicine Hat Region", 71],
    ["Alberta", "Red Deer Region", 72],
    ["Alberta", "Wood Buffalo–Cold Lake Region", 73],
    ["British Columbia", "British Columbia", 74],
    ["British Columbia", "Cariboo Region", 75],
    ["British Columbia", "Kootenay Region", 76],
    ["British Columbia", "Lower Mainland–Southwest Region", 77],
    ["British Columbia", "Nechako Region", 78],
    ["British Columbia", "North Coast Region", 79],
    ["British Columbia", "Northeast Region", 80],
    ["British Columbia", "Thompson–Okanagan Region", 81],
    ["British Columbia", "Vancouver Island and Coast Region", 82],
    ["Yukon Territory", "Yukon Territory", 83],
    ["Northwest Territories", "Northwest Territories", 84],
    ["Nunavut", "Nunavut", 85]]

def getIndexByAreaName(area_name):
    index=0
    for area in area_info:
        if area_name==area[1]:
            return index
        index+=1

#col 1 is index for prince in wage/outlook search, col 2,3 is area range, 4 is index of province for provincial median wage search
prov_area=[     
    [1,2,5,4],    # Newfoundland and Labrador
    [6,6,6,9],    # Prince Edward Island
    [7,8,12,6],   # Nova Scotia
    [13,14,18,3], # New Brunswick
    [19,20,36,10], # Quebec
    [37,38,48,8], # Ontario
    [49,50,57,2], # Manitoba
    [58,59,64,11], # Saskatchewan
    [65,66,73,0], # Alberta
    [74,75,82,1], # British Columbia
    [83,83,83,12], # Yukon Territory
    [84,84,84,5], # Northwest Territories
    [85,85,85,7]  # Nunavut
]

# for wage/outlook
def get_prov_index(area_code):  
    for pa in prov_area:
        if (area_code>=pa[1]) & (area_code<=pa[2]):
            return pa[0] 

# for provincial median wage https://www.canada.ca/en/employment-social-development/services/foreign-workers/service-tables.html
def get_prov_index2(area_code):  
    for pa in prov_area:
        if (int(area_code)>=pa[1]) & (int(area_code)<=pa[2]):
            return pa[3] 

def get_prov_name(area_code):
    for ai in area_info:
        if ai[2]==int(area_code):
            return ai[0]

def get_area_name(area_code):
    for ai in area_info:
        if ai[2]==int(area_code):
            return ai[1]





