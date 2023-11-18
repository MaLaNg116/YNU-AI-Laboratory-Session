import pandas as pd
import jieba
import paddle
import stylecloud

# 启用paddle模式
paddle.enable_static()
jieba.enable_paddle()

# 读取数据
df = pd.read_csv('./Depression.csv', encoding='utf-8')
answer = ''.join([i for i in df['回答']])

# 加载停用词
stopwords1 = [line.rstrip() for line in open(r'stopwords\baidu_stopwords.txt', 'r',
                                             encoding='utf-8')]
stopwords2 = [line.rstrip() for line in open(r'stopwords\cn_stopwords.txt', 'r',
                                             encoding='utf-8')]
stopwords3 = [line.rstrip() for line in open(r'stopwords\hit_stopwords.txt', 'r',
                                             encoding='utf-8')]
stopwords4 = [line.rstrip() for line in open(r'stopwords\scu_stopwords.txt', 'r',
                                             encoding='utf-8')]
stopwords5 = [line.rstrip() for line in open(r'stopwords\stopwords.txt', 'r',
                                             encoding='utf-8')]

stopwords = stopwords1 + stopwords2 + stopwords3 + stopwords4 + stopwords5
meaningful_words = []

# # 加载药品名称词库,数据来源于https://github.com/xtea/chinese_medical_words
jieba.load_userdict("medicine.txt")

# 分词
seg = list(jieba.cut(answer, use_paddle=True))

# 删除停用词
for i in seg:
    if (i not in stopwords) and (len(i) != 1):
        meaningful_words.append(i)

result = " ".join(meaningful_words)

stylecloud.gen_stylecloud(text=result,
                          font_path='C:/Windows/Fonts/msyh.ttc',
                          output_name='Depression_invert.png',
                          icon_name='fas fa-heart',
                          colors='white',
                          background_color='#1A1A1A',
                          size=(1920, 1080),
                          invert_mask=True
                          )


