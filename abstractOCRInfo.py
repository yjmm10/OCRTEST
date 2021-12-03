import os
import re
from typing import Dict, List, Tuple, Union

import chardet


# 读取文件
def read_file(filepath: str, mode: Union[str, None] = "rb", encoding: Union[str, None] = None) -> str:
    if encoding:
        content = open(filepath, mode, encoding=encoding).read()
    else:
        content = open(filepath, mode).read()
    encoding_type = chardet.detect(content)['encoding']
    print("编码为:", encoding_type)
    return content.decode('utf-8', errors="ignore")


def write_file(filepath: str, content: str) -> None:
    dir = os.path.dirname(filepath)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(filepath, 'w', encoding="utf-8") as f:
        f.write(content)


def parse(str="""
2021-12-03 13:32:58 [OCRFilter][Info]: OCR(DlpOCR) $version$: 1.0.0.8 on Nov 26 2021 17:25:16	, System $version$: 10.0
2021-12-03 09:25:07 [ 7176][ 6360][         DLPOCR][Info ]: Image Path: C:\DLP\Application\Repository\2021-12-03\ShareFile\SMB2_00003dcd-0099-0000-6900-000099000000_����ͼƬ.gif.lddec
2021-12-03 09:25:07 [ 7176][ 6360][         DLPOCR][Warn ]: C:\DLP\Application\Repository\2021-12-03\ShareFile\SMB2_00003dcd-0099-0000-6900-000099000000_����ͼƬ.gif.lddec is not a Picture!
2021-12-03 09:25:07 [ 7176][ 6360][         DLPOCR][Info ]: OCR Parse Failed, Cost Time: 0.197ms!
2021-12-03 09:25:07 [ 7176][ 9860][         DLPOCR][Info ]: Image Path: C:\DLP\Application\Repository\2021-12-03\ShareFile\SMB2_00003e00-0099-0000-9100-000099000000_����ͼƬ.jpg.lddec
2021-12-03 09:25:07 [ 7176][ 9860][         DLPOCR][Debug]: Image Read Success!
2021-12-03 09:25:07 [ 7176][ 9860][         DLPOCR][Debug]: Image resize: 567
2021-12-03 09:25:07 [ 7176][ 9860][         DLPOCR][Debug]: ScaleParam(src_w:  667, src_h :  255, dst_w :  640, dst_h :  224,ratio_w :  0.959520,ratio_h :  0.878431)
2021-12-03 09:25:08 [ 7176][ 9860][         DLPOCR][Info ]: Text Boxes is Empty!
2021-12-03 09:25:08 [ 7176][ 9860][         DLPOCR][Debug]: OCR Full Time: 171.266ms
2021-12-03 09:25:08 [ 7176][ 9860][         DLPOCR][Info ]: OCR Parse Failed, Cost Time: 171.512ms!
2021-12-03 09:25:08 [ 7176][ 9616][         DLPOCR][Info ]: Image Path: C:\DLP\Application\Repository\2021-12-03\ShareFile\SMB2_00003e18-0099-0000-0109-100099000000_����ͼƬ.png.lddec
2021-12-03 09:25:08 [ 7176][ 9616][         DLPOCR][Warn ]: C:\DLP\Application\Repository\2021-12-03\ShareFile\SMB2_00003e18-0099-0000-0109-100099000000_����ͼƬ.png.lddec is not a Picture!
2021-12-03 09:25:08 [ 7176][ 9616][         DLPOCR][Info ]: OCR Parse Failed, Cost Time: 0.458ms!
2021-12-03 09:25:08 [ 7176][ 6360][         DLPOCR][Info ]: Image Path: C:\DLP\Application\Repository\2021-12-03\ShareFile\SMB2_00003e30-0099-0000-9d00-000099000000_����ͼƬ.tif.lddec
2021-12-03 09:25:08 [ 7176][ 6360][         DLPOCR][Warn ]: C:\DLP\Application\Repository\2021-12-03\ShareFile\SMB2_00003e30-0099-0000-9d00-000099000000_����ͼƬ.tif.lddec is not a Picture!
2021-12-03 09:25:08 [ 7176][ 6360][         DLPOCR][Info ]: OCR Parse Failed, Cost Time: 0.392ms!
2021-12-03 09:25:11 [ 7176][ 6360][         DLPOCR][Info ]: Image Path: C:/DLP/Application/Bak/TextExtractor/20211203092511_3/image-0023.jpg
2021-12-03 09:25:11 [ 7176][ 6360][         DLPOCR][Debug]: Image Read Success!
2021-12-03 09:25:11 [ 7176][ 6360][         DLPOCR][Debug]: Image resize: 553
2021-12-03 09:25:11 [ 7176][ 6360][         DLPOCR][Debug]: ScaleParam(src_w:  653, src_h :  363, dst_w :  640, dst_h :  352,ratio_w :  0.980092,ratio_h :  0.969697)
2021-12-03 09:25:12 [ 7176][ 6360][         DLPOCR][Info ]: Text Boxes is Empty!
2021-12-03 09:25:12 [ 7176][ 6360][         DLPOCR][Debug]: OCR Full Time: 266.775ms
2021-12-03 09:25:12 [ 7176][ 6360][         DLPOCR][Info ]: OCR Parse Failed, Cost Time: 267.274ms!
2021-12-03 09:25:20 [ 7176][ 6360][         DLPOCR][Info ]: Image Path: C:/DLP/Application/Bak/TextExtractor/20211203092520_8/image-0019.jpg
2021-12-03 09:25:20 [ 7176][ 6360][         DLPOCR][Debug]: Image Read Success!
2021-12-03 09:25:20 [ 7176][ 6360][         DLPOCR][Debug]: Image resize: 553
2021-12-03 09:25:20 [ 7176][ 6360][         DLPOCR][Debug]: ScaleParam(src_w:  653, src_h :  363, dst_w :  640, dst_h :  352,ratio_w :  0.980092,ratio_h :  0.969697)
2021-12-03 09:25:20 [ 7176][ 6360][         DLPOCR][Info ]: Text Boxes is Empty!
2021-12-03 09:25:20 [ 7176][ 6360][         DLPOCR][Debug]: OCR Full Time: 237.714ms
2021-12-03 09:25:20 [ 7176][ 6360][         DLPOCR][Info ]: OCR Parse Failed, Cost Time: 237.874ms!
2021-12-03 09:25:23 [ 7176][ 9616][         DLPOCR][Info ]: Image Path: C:/DLP/Application/Bak/TextExtractor/20211203092523_10/image-0023.jpg
2021-12-03 09:25:23 [ 7176][ 9616][         DLPOCR][Debug]: Image Read Success!
2021-12-03 09:25:23 [ 7176][ 9616][         DLPOCR][Debug]: Image resize: 553
2021-12-03 09:25:23 [ 7176][ 9616][         DLPOCR][Debug]: ScaleParam(src_w:  653, src_h :  363, dst_w :  640, dst_h :  352,ratio_w :  0.980092,ratio_h :  0.969697)
2021-12-03 09:25:23 [ 7176][ 9616][         DLPOCR][Info ]: Text Boxes is Empty!
2021-12-03 09:25:23 [ 7176][ 9616][         DLPOCR][Debug]: OCR Full Time: 217.847ms
2021-12-03 09:25:23 [ 7176][ 9616][         DLPOCR][Info ]: OCR Parse Failed, Cost Time: 217.937ms!
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Info ]: Image Path: C:/DLP/Application/Bak/TextExtractor/20211202194613_9/图片 3.png
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Image Read Success!
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Image resize: 553
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: ScaleParam(src_w:  653, src_h :  363, dst_w :  640, dst_h :  352,ratio_w :  0.980092,ratio_h :  0.969697)
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Get 2 Text Boxes, Cost 184.192ms
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Text Boxes to Vectors, Cost 0.007ms
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Merge Text Boxes, Sort Boxes and Get 2 Lines, Cost 0.017ms
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Vectors to Text Boxes, Cost 0.002ms
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Get 2 Text Boxes Image, Cost 1.305ms
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Don't Get Angle, doAngle: 0.
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: Text Recognition, Cost 153.350ms
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: OCR Full Time: 344.847ms
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Info ]: OCR Parse Success, Cost Time: 345.089ms!
2021-12-02 19:46:13 [10160][12560][         DLPOCR][Debug]: OCR Result: 
成功更容易光顾磨难和限辛 
正如只有经过泥滨的道路才会留下脚印111 

""", ocr_result_dir=None):
    print(str)
# OCR(DlpOCR) $version$: 1.0.0.8 on Nov 26 2021 17:25:16	, System $version$: 10.0
    version = re.findall(
        r"OCR\(DlpOCR\) \$version\$: (.*) on (.*)	, System \$version\$: (\d+.\d+)", str, re.S)
    print(
        f"最近重启的OCR组件版本：{version[0][0]}\t时间：{version[0][1]}\t系统版本：{version[0][2]}")
    num_failed, num_success = len(list(re.finditer(
        r"OCR Parse Failed!?", str, re.S))), len(list(re.finditer(r"OCR Parse Success?", str, re.S)))
    print(
        f"检测到{num_failed+num_success}个文件\t其中，识别失败：{num_failed}\t识别成功：{num_success}")
    result = re.findall(
        r"Image Path: (.*)\n.*?OCR Parse Success, Cost Time: (.*?)ms.*?OCR Result: \n(.*?)\n\n", str, re.S)
    print("共获取有效数据：", len(result))

    # 二次提取
    valid_info = []
    for item in result:
        temp = []
        imgpath_last = re.findall(r"Image Path: (.*)\n?", item[0])[-1]
        temp.append(os.path.splitext(os.path.basename(imgpath_last))[0])
        temp.append(item[1])
        temp.append(item[2])
        valid_info.append(temp)

    # 将结果输出
    if ocr_result_dir:
        for item in valid_info:
            write_file(os.path.join(ocr_result_dir, item[0]+".txt"), item[2])
    return valid_info


#########################################
# 比对
#########################################

# 读取文件所有内容，并清洗
def get_all_str(filepath: str) -> str:
    # 获取所有内容
    content = read_file(filepath)
    # 清楚所有的空白
    result = re.sub(r"[\s+\n ]", "", content)
    return result

# 获取相同文件
def get_same_file(dir1: str, dir2: str) -> List:
    # 假设同一目录下文本名称不相同,其只有文件
    dir1_list = [i for i in os.listdir(dir1)]
    dir2_list = [i for i in os.listdir(dir2)]
    same_list = list(set(dir1_list).intersection(set(dir2_list)))

    print(f"{os.path.abspath(dir1)}包含文件数：{len(dir1_list)},其中无效{len(dir1_list)-len(same_list)}\
            {os.path.abspath(dir2)}包含文件数：{len(dir2_list)},其中无效{len(dir2_list)-len(same_list)}")

    return same_list


def get_same_str(str1="12345678aa", str2="12345678909"):
    import copy
    list1, list2 = list(str1), list(str2)
    l1, l2 = len(list1), len(list2)
    # 并集
    same_list = list(set(list1).union(set(list2)))
    all = {}
    for i in same_list:
        all[i] = 0
    d1, d2 = copy.deepcopy(all), copy.deepcopy(all)
    for i in list1:
        d1[i] += 1
    for i in list2:
        d2[i] += 1

    more = 0
    less = 0
    for i in same_list:
        temp = d1[i]-d2[i]
        if temp > 0:
            more += temp
        else:
            less += temp
    
    # 召回率 识别正确/真实正确 - 反应识别错和多识别
    call = (l1-more)/l2
    # 准确率 识别正确/识别出的数字 - 反应识别错和漏识别
    acc = (l1-more)/l1
    return l1,l2,acc,call


def pparse(pre_dir, label_dir):
    # 获取相同文件夹
    same_list = get_same_file(pre_dir, label_dir)
    res = {}
    # 获取每个文件的性能
    for file in same_list:
        pre_file = os.path.join(pre_dir, file)
        label_file = os.path.join(label_dir, file)
        pre_str, label_str = get_all_str(pre_file), get_all_str(label_file)
        l1,l2,acc,call = get_same_str(pre_str, label_str)
        res[file]= [l1,l2,acc,call]
    return res

    #


def main():
    filepath = "TextExtractor_OCR(1).log"
    ocr_result_dir = "dlpocr_temp"
    # 真实值
    label_dir = "dlpocr_label"

    str =read_file(filepath)
    # 获取到处理后的数据,并打印文件
    valid_info = parse(str=str,ocr_result_dir=ocr_result_dir)

    data = pparse(ocr_result_dir, label_dir)

    for i in valid_info:
        if i[0]+".txt" in data.keys():
            data[i[0]+".txt"].append(float(i[1]))
    with open("result.csv","w",encoding="utf-8") as f:
        f.write("路径,预测文本长度,真实文本,召回率,准确率,耗时\n")
    with open("result.csv","a+",encoding="utf-8") as f:
        for key in data.keys():
            f.write(f"{key},{data[key][0]},{data[key][1]},{data[key][2]},{data[key][3]},{data[key][4]}\n")

if __name__ == '__main__':
    print("""
    使用说明：
    1. 本程序只针对dlplog的debug日志有效
    2. 请确保在dlpocr_temp同级目录有dlpocr_label文件夹
    3. 且2中文件夹下的文件名一一对应且不重名，如1.png-> 1.txt
    4. 生成的结果在result.csv中
    """)
    main()

