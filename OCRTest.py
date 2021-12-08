import os
import re
import shutil
from typing import Dict, List, Tuple, Union

import chardet


# 读取文件
def read_file(filepath: str) -> str:
    try:
        # 默认二进制
        content = open(filepath, "rb").read()
        content = content.decode(chardet.detect(
            content)['encoding'], errors="ignore")
        return content

    except:
        print(f'{os.path.abspath(filepath)} 编码错误')


def write_file(filepath: str, content: str, mode="w") -> None:
    dir = os.path.dirname(filepath)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(filepath, mode, encoding="utf-8") as f:
        f.write(content)


def split_module(str: str):
    pass


class Parse(object):
    def __init__(self, dlpocr_dir=None, result_dir=None) -> None:
        # super().__init__()
        if dlpocr_dir is None:
            self.dlpocr_dir = "dlpocr_dir"
        self.dlpocr_dir = dlpocr_dir
        if not os.path.exists(self.dlpocr_dir):
            os.makedirs(self.dlpocr_dir)
        print(f"将日志中采集到的文本识别结果存放在{os.path.abspath(self.dlpocr_dir)}")
        if result_dir is None:
            self.result_dir = "dlpocr_result"
        self.result_dir = result_dir
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
        print(f"将日志分析结果存放在{os.path.abspath(self.result_dir)}")
        pass

    # 对整个日志进行分析,输出每次启动的有效日志（有文件输入）
    def split_from_str(self, str_all: str) -> Union[None, List]:
        if str_all is None:
            print("日志文件没有内容")
            return None
        str_every_times = str_all.split(  # patt)
            "***********************************************TextExtractor_OCR.log started***********************************************")
        # str_every_times = re.sub("\r\n\*.*\*?\r\n", "", str_every_times)
        # patt = re.findall("^\*.*started.*\*", str_all)[0]

        str_every_times = [
            re.sub("\r\n\*.*\*?\r\n", "", i) for i in str_every_times if r"OCR(DlpOCR) $version$:" in i]
        if len(str_every_times) == 0:
            print("日志中不含组件版本信息,请检查")
            return None

        print(f"共启动{len(str_every_times)}次OCR组件")

        return str_every_times

    def split_from_file(self, filepath: str) -> Union[None, List]:
        assert os.path.exists(filepath), print(
            os.path.abspath(filepath)+"文件不存在")
        str_all = open(filepath, "rb").read().decode('utf-8')
        # str_all = read_file(filepath=filepath)
        return self.split_from_str(str_all=str_all)

    # 分析单次日志,输出识别的文件数
    def split_ocr_log(self, log: str, index=None) -> Union[None, List]:
        version = re.findall(
            r"([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}).*OCR\(DlpOCR\) \$version\$: (.*) on (.*)	, System \$version\$: (\d+.\d+)", log, re.S)
        print("\n"+"-"*50)
        print(f"第{index}次：启动时间：{version[0][0]}\t\
            组件版本：{version[0][1]}\t\
            系统版本：{version[0][3]}")
        # 获取每个输入
        input_ocr_files = log.split("Image Path:")[1:]
        if len(input_ocr_files) == 0:
            if index is not None:
                print(f"第{index}次启动未识别图片")
            else:
                print("该次启动未识别图片")
            return None

        print(f"共输入 {len(input_ocr_files)} 个文件（包含非图片）")

        return input_ocr_files

    # 分析文件，分类
    def classify_every_file(self, input_ocr_files: List) -> Tuple[Union[None, List], Union[None, List], Union[None, List]]:
        # 有效图片
        ocr_files_valid = [
            i for i in input_ocr_files if "is not a Picture" not in i]
        if len(ocr_files_valid) == 0:
            print("输入的文件都不支持")
        else:
            print(f"其中支持识别的图片数: {len(ocr_files_valid)}")
        # 求差集即可获得不支持的图片类型
        ocr_files_invalid = list(set(input_ocr_files)-set(ocr_files_valid))
        # if len(ocr_files_invalid)==0:
        #     return None,None,None

        # 识别成功
        ocr_images = [
            i for i in ocr_files_valid if "OCR Parse Failed" not in i]
        if len(ocr_images) == 0:
            print(f"支持识别的图片中全部识别失败\n")
        else:
            print(
                f"支持识别的图片中识别成功图片数: {len(ocr_images)},成功率：{len(ocr_images)/len(ocr_files_valid)}\n")
        # 求交集即可获得识别失败的图片
        ocr_images_fail = list(set(ocr_files_valid)-set(ocr_images))
        # if len(ocr_images_fail)==0:
        #     ocr_images_fail = None

        return ocr_images, ocr_files_invalid, ocr_images_fail

    # 获取单个图像的路径
    def _get_filepath(self, ocr_image: str, filename=None) -> str:
        path = re.findall(r"^ (.*)\r\n", ocr_image)[0]
        if filename is not None:
            write_file(os.path.join(self.result_dir,
                       filename), path+"\n", mode="a+")
        return path

    # 获取识别的时间
    def _get_time(self, ocr_image: str) -> float:
        return float(re.findall(r"OCR Parse Success, Cost Time: (.*?)ms", ocr_image)[0])

    # 获取识别结果
    def _get_result(self, ocr_image: str):
        str = re.findall(r": OCR Result:? \r\n(.*)\r\n\r\n",
                         ocr_image, re.S)[0]
        if "OCR Release...." in str:
            str = re.sub(
                "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} .*OCR Release....?", "", str)
        return str

    def process_ocr_images(self, ocr_images: List) -> Union[None, Tuple[List, List, List]]:
        if len(ocr_images) == 0:
            return None
        image_info = []
        for ocr_image in ocr_images:
            filepath = self._get_filepath(ocr_image, "ocr_success.txt")
            time = self._get_time(ocr_image)
            ocr_result = self._get_result(ocr_image)

            # 写入每个文件
            filename = os.path.splitext(os.path.basename(filepath))[0]
            write_file(os.path.join(self.dlpocr_dir,
                                    filename+".txt"), ocr_result)
            image_info.append([filename, time, ocr_result])
        return image_info

    def process_files_path(self, file_images: List, filename=None) -> Union[None, List]:
        if len(file_images) == 0:
            return None
        filepaths = []
        for file_image in file_images:
            filepaths.append(self._get_filepath(file_image, filename))
        return filepaths

    def task(self, filepath) -> Tuple[str, float, str]:
        ocr_infos = []
        # 获取每个日志
        ocr_logs = self.split_from_file(filepath)
        if ocr_logs is None:
            return None
        for i_log, ocr_log in enumerate(ocr_logs):
            # 第 time_i 次启动日志
            # 对日志划分为多个输入文件
            input_ocr_files = self.split_ocr_log(ocr_log, i_log)
            if input_ocr_files is None:
                print("不存在识别的文件")
                return None
            # 对输入的文件进行分析，得到有效识别，无法识别，识别错误 列表
            ocr_images, ocr_files_invalid, ocr_images_fail = self.classify_every_file(
                input_ocr_files)

            ocr_files_invalid = self.process_files_path(
                ocr_files_invalid, "ocr_invlid.txt")

            ocr_images_fail = self.process_files_path(
                ocr_images_fail, "ocr_fail.txt")

            ocr_info = self.process_ocr_images(ocr_images)
            ocr_infos.append(ocr_info)
        return ocr_infos

#########################################
# 比对
#########################################

# 读取文件所有内容，并清洗


def get_all_str(filepath: str, rmsignal: bool = False) -> str:
    # 获取所有内容
    content = read_file(filepath)
    # 清楚所有的空白
    result = re.sub(r"[\s+\n ]", "", content)
    if rmsignal:
        rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
        result = rule.sub('', result)
    return result

# 获取相同文件


def get_same_file(dir1: str, dir2: str) -> List:
    # 假设同一目录下文本名称不相同,其只有文件
    dir1_list = [i for i in os.listdir(dir1)]
    dir2_list = [i for i in os.listdir(dir2)]
    same_list = list(set(dir1_list).intersection(set(dir2_list)))

    print(f"{os.path.abspath(dir1)}\t包含文件数：{len(dir1_list)},其中无效文件：{len(dir1_list)-len(same_list)}\n{os.path.abspath(dir2)}\t包含文件数：{len(dir2_list)},其中无效文件：{len(dir2_list)-len(same_list)}")

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
    return l1, l2, acc, call


def pparse(pre_dir, label_dir, rmsignal):
    # 获取相同文件夹
    same_list = get_same_file(pre_dir, label_dir)
    res = {}
    # 获取每个文件的性能
    for file in same_list:
        pre_file = os.path.join(pre_dir, file)
        label_file = os.path.join(label_dir, file)
        pre_str, label_str = get_all_str(
            pre_file, rmsignal), get_all_str(label_file, rmsignal)
        l1, l2, acc, call = get_same_str(pre_str, label_str)
        res[file] = [l1, l2, acc, call]
    return res


def main(root, dlpocr_dir, label_dir, result_dir):
    # 真实值

    if not os.path.exists(label_dir):
        print(f"请在{os.path.abspath(label_dir)}文件夹添加标签文件（图片对应的真实文字）")
        os.makedirs(label_dir)
        return

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    str_rmsignal = input("是否计算标点符号(默认：1) 1)是 2)否 ")
    if str_rmsignal == "1" or str_rmsignal == "":
        rmsignal = True
    if str_rmsignal == "2":
        rmsignal = False

    p = Parse(dlpocr_dir=dlpocr_dir, result_dir=result_dir)
    valid_infos = p.task(filepath)
    if valid_infos is None:
        print("请检查日志格式")

    result_path = os.path.join(result_dir, "result.csv")
    print(f"性能测试的结果文件路径：{os.path.abspath(result_path)}")
    with open(result_path, "a+", encoding="utf-8") as f:
        f.write("路径,预测文本长度,真实文本,召回率,准确率,耗时\n")
    if valid_infos is None:
        print("无有效识别文件")

    for valid_info in valid_infos:
        if valid_info is None:
            print("该次提取无有效识别文件")
            continue

        data = pparse(dlpocr_dir, label_dir, rmsignal)

        for i in valid_info:
            if i[0]+".txt" in data.keys():
                data[i[0]+".txt"].append(float(i[1]))

        with open(result_path, "a+", encoding="utf-8") as f:
            for key in data.keys():
                f.write(
                    f"{key},{data[key][0]},{data[key][1]},{data[key][2]},{data[key][3]},{data[key][4]}\n")
    print("数据提取完毕")


if __name__ == '__main__':
    print("""
    OCR_TEST: 2.4 - 修复问题
    使用说明：
    1. 本程序只针对dlplog的debug日志有效
    2. 执行工具一次，生成相应的文件结构，后根据提示添加dlpocr_label下的标签文件完毕后再执行
    3. 该标签文件与图片一一对应，如1.png-> 1.txt
    3. 生成的结果dlpocr_result目录下的result.csv中
    4. 使用日期输入，要求文件格式为TextExtractor_OCR[日期].log，该日期需要以2开头
    5. 清理程序，只清理dlpocr_dir（dlp文本识别结果）、dlpocr_result（dlp性能提取结果）
    6. 包含两种计算，一种是只计算中英文数字，一种是所有字符串，默认选第一种
    note：程序可分析多次启动，但不建议，单次启动单次分析
    """)
    mode = input("请选择模式  1)ocr性能提取, 2)清理提取数据的文件夹:")
    if mode == "1":
        print(f"两种输入形式：\n1. 输入完整路径，如：I:\Release\log\TextExtractor_OCR20211129.log\n2. 输入日期，如20211129,等同于1，但该工具路径要与日志文件同级目录")
        filepath = input("待分析日志文件路径：")
        if filepath[0] == "2":
            filepath = f"TextExtractor_OCR{filepath}.log"
            if not os.path.exists(filepath):
                print(f"{os.path.abspath(filepath)} 文件不存在，请检查")
                exit()
        filepath = os.path.abspath(filepath)
        root = os.path.splitext(filepath)[0]
        if not os.path.exists(root):
            os.makedirs(root)
            print(f"创建{os.path.abspath(root)}用来存放本次分析生成的数据")

        dlpocr_dir = os.path.join(root, "dlpocr_dir")
        label_dir = os.path.join(root, "dlpocr_label")
        result_dir = os.path.join(root, "dlpocr_result")
        main(root, dlpocr_dir, label_dir, result_dir)
    if mode == "2":
        filepath = input("请输入要清理的文件夹对应的日志文件名：")
        if filepath[0] == "2":
            filepath = f"TextExtractor_OCR{filepath}.log"
        if not os.path.exists(filepath):
            print(f"{os.path.abspath(filepath)} 文件不存在，请检查")
            exit()
        root = os.path.splitext(filepath)[0]
        label_dir = os.path.join(root, "dlpocr_dir")
        result = os.path.join(root, "dlpocr_result")

        if os.path.exists(label_dir):
            shutil.rmtree(label_dir)

            print(f"删除{label_dir}完成")
        if os.path.exists(result):
            shutil.rmtree(result)
            print(f"删除{result}完成")
        print("删除完毕")
        # task_clean()
