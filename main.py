import hashlib
import json
import os
import zipfile
import re
def getmd5(filename):
    file_txt = open(filename, 'rb').read()
    m = hashlib.md5(file_txt)
    return m.hexdigest()

# def zip_file(file):
#     with zipfile.ZipFile(file) as zf:
#         zf.extractall()
    # zip_name = src_dir +'.zip'
    # z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
    # for dirpath, dirnames, filenames in os.walk(src_dir):
    #     fpath = dirpath.replace(src_dir,'')
    #     fpath = fpath and fpath + os.sep or ''
    #     for filename in filenames:
    #         z.write(os.path.join(dirpath, filename),fpath+filename)
    #         print ('==压缩成功==')
    # z.close()

def main(path):
    all_md5 = []
    all_size=[]
    all_path=[]
    total_file = 0
    total_delete = 0
    # for file in os.listdir(path):
    #     if file[-1:-3] == 'zip':
    #         zip_file(file)
    for file in os.listdir(path):
        if file[-9:] == 'zip_files':
            real_path = os.path.join(path, file)
            # print(real_path,"   ",os.listdir(real_path))
            fileroot = os.listdir(real_path)    #每个文件夹下的tdb
            for tdb in fileroot:
                abs_path=os.path.join(real_path, tdb)
                if os.path.isfile(abs_path) == True:
                    total_file += 1;
                    File_Size = os.path.getsize(abs_path)  # 获取文件大小
                    if File_Size in all_size:
                        filemd5 = getmd5(abs_path)
                        if filemd5 in all_md5:
                            total_delete += 1
                            # print('删除', file)
                        else:
                            all_md5.append(filemd5)
                            all_path.append(abs_path)
                    else:
                        all_size.append(File_Size)
                        all_path.append(abs_path)
    # print('文件总数：', total_file)
    # print('删除个数：', total_delete)
    return all_path


def native_cp(str_log_open,str_new):
    import os
    import shutil
    str_log_open = str_log_open ###文件名写死！！！防止出错
    shutil.copyfile(str_log_open, str_new)

def small(line):
    line1=line.lower()
    # for i in line:
    #     if 64<i<90:
    #         line1+=chr(i+32)
    #     else:
    #         line1+=i
    return line1
def findnameandG(line,i):
    flag=0
    name=""
    line1=small(line)
    line2=line1.split()
    # print(line1)
    # print(line2)
    for j in range(len(line2)-1):
        if str(line2[j])=="b'element'" and str(line2[j+1])!="b'va'"and str(line2[j+1])!="b'/-'":
            # print(str(line2[j+1]).split("\'"))
            name=(str(line2[j+1]).split("\'"))[1]
            # print(name[3])
    # if line1.find("element")>0 and line[(line1.find("element")+8):(line1.find("element")+10)].replace(" ", "") != "VA" :
    #     name=line[(line1.find("element")+8):(line1.find("element")+10)].replace(" ", "")
    #     print(line1)
    #     print(name, i)
    if str(line).find('G('):
        flag=i
        # print("G(  ",i)
    i+=1
    return name,flag

def renameanddelet(pathof_tdb,number):
    count = 0
    num=1
    count = len(open(pathof_tdb,'rb').readlines())
    concept = open(pathof_tdb,"rb")
    namelist=[]
    # print(count)
    # print(pathof_tdb,"  ",count)
    flag_last=False
    for j in range(count):
        name,flag=findnameandG(concept.readline(),num)
        num+=1
        # print(name)
        if str(name):
            # print(name)
            namelist.append(str(name))
        if flag==1:
            flag_last= True
    name_last=namelist[0]
    for i in namelist[1:]:
        name_last=name_last+"_"+i.replace(" ", "")
    concept.close()
    name_last=name_last+str(number)
    return name_last,flag_last


#获取文件命名列表及对应地址


root=r"D:\tdbrequest"

if __name__ == '__main__':
    try:
        os.makedirs('./rename')
    except:
        print("already done")
    try:
        os.makedirs('./failrename')
    except:
        print("already done")
    j=0
    k=0
    for i in main(root):
        # print(i)
        # print(i[-3:].lower(),"aaa")
        if i[-3:].lower()=="tdb"or i[-3:].lower()=="txt":
            newname, flag = renameanddelet(i, j)
            j = j + 1
            newpath = "./rename"
            if flag == 1:
                newpath = os.path.join(newpath, newname)
                # print(newname, "   ", newpath, "  ", i)
                native_cp(i, newpath)
        else:
            newpath = "./failrename"
            print(i,"未命名")
            newpath= os.path.join(newpath,i.split("\\")[-1]+str(k))
            k=k+1
            native_cp(i, newpath)
            continue
    # for i in jsknb(): native_cp("./" + str(i), "./gophase/ve-" + str(i))
    # Root_Path = "G:\\"  # 指定根目录
    # File_Size_Dict = dict()
    # for x, y, z in os.walk(Root_Path):
    #     for s1 in z:
    #         File_Path = f"{x}\\{s1}"  # 使用OS.WALK模块枚举所有文件，并在此拼接绝对路径
    #         File_Size = os.path.getsize(File_Path)  # 获取文件大小
    #         if File_Size not in File_Size_Dict:  # 以下代码块作用是以文件大小为主键，路径列表为键值存储在字典里，逻辑是字典没主键，直接添加，已有主键，对键值的列表用append添加到列表
    #             File_Size_Dict[File_Size] = [File_Path]  # 简单说，File_Size_Dict是一个以文件大小为主键，对应包含相同大小的不同文件的不同绝对路径的列表
    #         else:
    #             File_Size_Dict.get(File_Size).append(File_Path)
    #
    # File_Hash_Info = dict()
    #
    # for y1, y2 in File_Size_Dict.items():
    #     if len(y2) >= 2:  # y2为文件路径列表，检查其长度，如大于等于2，说明相同大小的文件多于1个，有可能有重复文件，以过滤减轻hash带来的耗时
    #         for y3 in y2:
    #             with open(y3, 'rb') as e:  # 对拥有相同大小文件进行HASH生成文件指纹
    #                 a1 = hashlib.sha1()
    #                 while 1:
    #                     a2 = e.read(104857600)
    #                     a1.update(a2)
    #                     if not a2:
    #                         break
    #                 y4 = a1.hexdigest()
    #                 if y4 not in File_Hash_Info:  # 以同样方法把相同文件指纹文件及其绝对路径存到字典
    #                     File_Hash_Info[y4] = [y3]
    #                 else:
    #                     File_Hash_Info[y4].append(y3)
    #
    # with open('shadict.txt', 'w') as f:  # 用希哈值对大小一致文件再统计，列出内容相同文件，生成文件作用是通过观察思考再考虑去除重复文件的策略，因为每次哈希需时间很久，这里用JSON格式存储了数据
    #     json.dump(File_Hash_Info, f)
    #
    # for b1, b2 in File_Hash_Info.items():
    #     if len(b2) >= 2:  # 过滤具相同文件多于一个
    #         print('-----------------------')  # 输出结果进行间隔以便观察
    #         for b3 in b2:
    #             print(b3)  # 这里可以放置删除策略，懒得放上来，相信各人的需求不同吧，另代码丑陋，请原谅~
