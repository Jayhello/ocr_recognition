# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os

CREATE_PATH = 'F:/img_test/create_train_image/'
WIDTH = 700
HEIGHT = 900
# 正常字体的大小
# FONT_SIZE = 40
# FONT_SIZE = 16
# FONT_SIZE = 20
FONT_SIZE = 25
FONT_SIZE = 36
FONT_SIZE = 45
# 空格的大小，换行的时候也是要大小的不然，两行的距离太紧
FONT_BLANK_SIZE = 10
BEG_POINT = 5
BLACK_COLOR = 0 + 0 * 256 + 0 * 256 * 256

FONT_TYPE = 'C:\Windows\Fonts\FZSTK.TTF'  # 方正舒体
# FONT_TYPE = 'C:\Windows\Fonts\simsun.ttc'  # 常规简体   done 16 25
# FONT_TYPE = 'C:\Windows\Fonts\simhei.TTF'  # heiti     done 16 25
FONT_TYPE = 'C:\Windows\Fonts\STHUPO.TTF'  # 实心黑粗体  字体太大不好看有些字显示不正常
FONT_TYPE = 'C:\Windows\Fonts\simkai.TTF'  # 楷体 常规    done 16 25
FONT_TYPE = 'C:\Windows\Fonts\simfang.TTF'  # 仿宋 常规 常规  done 16 25
FONT_TYPE = 'C:\Windows\Fonts\FZYTK.TTF'    # 方正 姚体 常规
FONT_TYPE = 'C:\Windows\Fonts\STXINWEI.TTF'    # 华文新魏常规 done 25 36
FONT_TYPE = 'C:\Windows\Fonts\STCAIYUN.TTF'   #空心体
FONT_TYPE = 'F:\img_test\dahei\da_gei.TTF'    #自己下载的打黑 done  50
out_dir = 'F:/img_test/create_train_image/'
output_txt = 'output1.txt'
output_img = 'F:/img_test/create_train_image/output2.jpg'

# input_text = 'F:/img_test/create_train_image/common_word.txt'
input_text = 'F:/img_test/create_train_image/common_word2.txt'
input_text = 'F:/img_test/create_train_image/all_chinese.txt'
page_num = 47


def get_text_from_file():
    with open(input_text, 'r') as file:
        # decode('utf-8') 不行不知道为什么非要 'gbk'
        # print file.read().decode('gbk')
        return file.read().decode('gbk')


def get_page_num(text):
    textLen = len(text)
    rowLen = WIDTH / FONT_SIZE - 1
    columnLen = HEIGHT / (FONT_SIZE + FONT_BLANK_SIZE)

    if HEIGHT % (FONT_SIZE + FONT_BLANK_SIZE) > FONT_SIZE:
        columnLen += 1

    pageWordsNum = rowLen * columnLen
    pageNum = float(textLen) / (pageWordsNum)

    pageNum = int(round(pageNum + 0.499))

    textLst = str_to_strlist_by_nth(text, pageWordsNum)

    # for item in textLst:
    #     print item

    return pageNum, textLst


def do_All_Task():
    text = get_text_from_file()
    pageNum, textLst = get_page_num(text)

    baseFileName = get_filename_without_extension(input_text)
    baseFontName = get_filename_without_extension(FONT_TYPE)

    for i in range(0, pageNum):
        global output_txt, output_img, page_num
        output_txt = '%s%d%s%s%spage%d%s%s%s%d.txt' % (out_dir, page_num, '_', baseFileName, '_', i, '_', baseFontName, '_', FONT_SIZE)
        output_img = '%s%d%s%s%spage%d%s%s%s%d.jpg' % (out_dir, page_num, '_', baseFileName, '_', i, '_', baseFontName, '_', FONT_SIZE)
        print (output_txt, output_img)
        write_text2img(textLst[i])
        page_num += 1


def get_filename_without_extension(fullPath):
    base = os.path.basename(fullPath)
    return os.path.splitext(base)[0]


def process_text(text):
    # num of character in each line
    row_size = WIDTH / FONT_SIZE - 1
    # print row_len
    LEN = len(text)
    # print LEN
    count = LEN / row_size

    # for i in range(0, count):
    #     text = insert_character(text, i * row_size + i)

    textLst = str_to_strlist_by_nth(text, row_size)
    # print text
    return textLst


def write_text2img(text):
    # img = np.zeros([WIDTH, HEIGHT, 3], dtype=np.uint8)
    # img.fill(255) # or img[:] = 255
    # cv2.imwrite('F:/img_test/create_train_image/1215.jpg', img)
    # text = get_text_from_file()
    text_lst = process_text(text)

    blank = Image.new("RGB", [WIDTH, HEIGHT], "white")
    # blank = Image.new("L", [WIDTH, HEIGHT], "white")
    drawObject = ImageDraw.Draw(blank)
    # font = ImageFont.truetype()
    # Font1 = ImageFont.truetype("C:\Windows\Fonts\simsun.ttc", 36)
    Font1 = ImageFont.truetype(FONT_TYPE, FONT_SIZE)
    Font2 = ImageFont.truetype(FONT_TYPE, FONT_BLANK_SIZE)
    # text = u"我草草草草\n\n草我草草草草"
    # text = u"我草草草草草我草草草草"
    drawObject.ink = BLACK_COLOR

    lst_coord = []
    dic_word2coord = {}
    lst_word2coord = []

    size = len(text_lst)
    for i in range(0, size):
        row_text = text_lst[i]
        y = BEG_POINT + i * (FONT_SIZE + FONT_BLANK_SIZE)
        drawObject.text([BEG_POINT, y], row_text, font=Font1)
        drawObject.text([BEG_POINT, BEG_POINT + (i + 1) * FONT_SIZE + i * FONT_BLANK_SIZE], '\n', font=Font2)

        for j in range(0, len(row_text)):
            x = BEG_POINT + j * FONT_SIZE
            # drawObject.rectangle((x, y, FONT_SIZE, FONT_SIZE + 2), outline="red")
            lst_coord.append((x, y, x + FONT_SIZE, y + FONT_SIZE + 2))
            dic_word2coord[row_text[j]] = (x, y, FONT_SIZE, FONT_SIZE + 2)
            # lst_item = [row_text[j].encode('utf-8'), x, y, x + FONT_SIZE, y + FONT_SIZE + 2, 9]
            lst_item = [row_text[j].encode('utf-8'), x, HEIGHT - y - FONT_SIZE - 2, x + FONT_SIZE, HEIGHT - y, page_num]
            lst_word2coord.append(lst_item)

    blank.save(output_img)

    for j in range(0, len(lst_coord)):
        drawObject.rectangle(lst_coord[j], outline="red")
    # print dic_word2coord
    blank.show()
    # dict2txt(dic_word2coord)
    lst2txt(lst_word2coord)


def lst2txt(lst):
    filepath = output_txt
    with open(filepath, "w") as f:
        for item_lst in lst:
            # f.write(item[0].encode('utf-8') + str(item[1]) + ' ' + str(item[2]) + ' ' + str(item[3]) + '\n')
            # f.write(" ".join(item) + '\n')
            f.write(" ".join(str(item) for item in item_lst) + '\n')


def dict2txt(d):
    # txtfile = os.path.join(out_dir, output_txt)
    filepath = 'F:/img_test/create_train_image/output1.txt'
    with open(filepath, "w") as f:
        for (k, v) in d.items():
            k = k.encode('utf-8')
            # f.write(k + v[0] + v[1] + v[2] + v[3])
            f.write(k + ' ' + str(v[0]) + ' ' + str(v[1]) + ' ' + str(v[2]) + ' ' + str(v[3]) + '\n')
            # for p in d.items():
            #     f.write("%s:%s\n" % p)


def str_to_strlist_by_nth(str, nth):
    return [str[i:i + nth] for i in range(0, len(str), nth)]


def insert_character(string, index):
    return string[:index] + '\n' + string[index:]


def test():
    text = get_text_from_file()
    print process_text(text)


if __name__ == '__main__':
    do_All_Task()

    # print '%s%d%s%s.jpg' % (out_dir, 1, '_', 'abc')
    # print(os.path.splitext(FONT_TYPE)[0])
    # print(os.path.splitext(output_img)[0])
    # base = os.path.basename(FONT_TYPE)
    # print os.path.splitext(base)[0]
    # write_text2img()
    # print int(round(0.4))
    # print int(round(0.1 + 0.49))
    # test()
    # d = {u'\u7981': (205, 425, 255, 477), u'\u5c04': (5, 365, 55, 417)}
    # dict2txt(d)
    # print len(get_text_from_file())
    # str = u'1234我的5'
    # print str_to_strlist_by_nth(str, 3)
    # print len(str)
    # str = insert_character(str, 2)
    # print str
    # str = insert_character(str, 4)
    # print str
    # change(str)
    # print str
