#!/usr/bin/env python3
"""pateliercore mudule (under development)

This is a module for analyzing a text file.
You can provide the text lines by selecting a text file.
The text file needs to be encoded in UTF-8 or Shift-JIS.
Each control code (0x00-0x1f) in the text lines is changed to ‘▲’.
For example, a tab code in the text lines is changed to ‘▲’.
The analysis result is displayed.

This pateliercore module is still under development.

In time,
This module may be display more information by analyzing a Japanese file.
The file needs a claim written in Japanese,
    according to the Japanese patent application style.
The file is a text file or a document file,
    so its filename extention needs to be txt or docx.

This pateliercore module has patelier.
The patelier reads the file and uses Patisserie.
Patisserie employs patissier for analyzing the file.
Patisserie outputs result files.
The result files show the result of the patissier's analysis.
The result files include res-utf8.txt, patelier.html and patelierjs.js.
The res-utf8.txt is a plain text version of the patelier.html.
The patelier.html uses patelierjs.js.
The result files use Japanese language of UTF-8 encoding.

This pateliercore module also has patelier_installer.
The patelier_installer may be for installing patelier App.
In time, the patelier_installer may be able to work.

Copyright 2019-2022 K2UNIT

"""

# patelier-package-library
from patelier import __version__

# I would like to thank the developers of each of the libraries below.

# standard-library
import datetime
import os
import pickle
import shutil
import sys
import time
import threading
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import xml.sax.saxutils

# 3rd-party-library
from docx import Document
from natsort import natsorted
import regex
import win32com.client  # pywin32

mecab_flg = True
# MeCab(mecab-python3) for access to MeCab folder
# prerequisite: installed MeCab (without unidic and unidic-lite)
# Mecab: open source morphological analysis engine developed by Mr. Taku Kudo
# Mecab (with ipadic) can be installed by mecab-0.996.exe.
# If Mecab can be started, the patelier's analysis accuracy may be improved.
try:
    import MeCab
except ImportError:
    print('■Warning:MeCab(形態素解析エンジン)を起動できません。')
    mecab_flg = False

HD_CMTBLK = '■'
HD_CMT = '※'
END_STRG = '記録媒体'
NG_WDS = {
    'sub', 'sup', '複数', '数', '表', '化', '用', '以', '上', '下', '左',
    '右', '中', '内', '外', '形態'}
NG_ENDS = {
    '項', '特許', '発明', '図面', '図', '実施形態', '場合', '例', '該', '当',
    '所定', '概念', '乃至', '文献', '述', '記', '記載', '開示', '説明',
    '概要', '要旨', '適当', '適切', '明治', '大正', '昭和', '平成', '特開',
    '特表', '開平', '開昭', '表平', '表昭', '公平', '公昭', '公報', '可能',
    '自在', '必要', '平均', '最高', '最低', '最大', '最小', '同等', '同一',
    '差異', '差違', '一致', '未満', '満', '実質', '実際', '開始', '途中',
    '実施', '実行', '即座', '即時', '平時', '現在', '過去', '将来', '常時',
    '通常', '海抜', '省略', '概略', '略', '各', '的', '用', '約', '案', '々',
    '毎', '十', '百', '千', '万', '億', '兆', '第', 'pH', 'JIS', 'IEEE',
    'ISO', 'IEC', 'ANSI', 'ASME', 'MPEG', '・'}
NG_RFENDS = {
    'km', 'Km', 'cm', 'mm', 'nm', 'μm', 'um', 'kg', 'Kg', 'mg', 'KB', 'MB',
    'GB', 'TB', 'kB', 'Kb', 'Mb', 'Gb', 'Tb', 'l/', 'ml', 'dl', 'kl', 'm/',
    'mW', 'kW', 'MΩ', 'KΩ', 'kΩ', 'Ω', 'Hz', 'Å', 'π', 'ω', 'λ',
    'πf', 'dB', 'Np', 'N/', 'g/', 'Pa', 'T/', 'eV', 'J/', 'C/', 'c/', 'V/',
    'A/', 'F/', 'Wb', 'H/', 'VA', 'W/', 'μF', 'uF', 'pF', 'cd', 'lm', 'lx',
    'lm', 'mH', 'nH', 'pH'}
SP_WDS = {
    '手段', 'ステップ', '工程', '方法', '方式', 'プログラム', '処理',
    'プロセス', '情報', '信号', '画像', '画面', 'モデル', 'ツール',
    'ルーチン', 'データ', 'パターン', 'ファイル', 'ディレクトリ',
    'フォルダー', 'フォルダ', 'ドキュメント', '文書', 'プロフィール',
    'テーブル', 'データベース', 'DB', '辞書',
    'ビット', 'フラグ', 'パラメータ', '媒体', 'メモリ', 'ROM', 'RAM',
    'システム', '装置', '機器', 'ユニット', 'ブロック', '回路', '基板',
    '機構', '機械', '材料', '部材', '物体', '方向', '期間', '時間', '履歴',
    '手順', '状態', '指標', '規格', '理論', '機能', '力', '量', '層', '値',
    '数', '部', '体', '器', '機', '材', '剤', '法'}
BORE_WDS = {
    '形態', '手段', 'ステップ', '工程', '方法', '処理', 'プロセス', '媒体',
    'ユニット', '機構', '部材', '方向', '期間', '時間', '手法', '手順',
    '状態', '結果', '指標', '規格', '理論', '機能', '力', '量', '層', '値',
    '数', '部', '体', '器', '機', '材', '剤', '法'}
BORE_WDSENDS = {
    '概念', '数', '算', '番', '年', '月', '日', '週', '秒', '用', '以', '上',
    '下', '左', '右', '中', '内', '外', '目', '得', '着', '返'}
BORE_ENDS = {
    '符号', '番号', '記号', '号', '順序', '順位', '式', '角', '差', '比',
    '率', '幅', '巾', '径', '度', '圧', '温', '積', '長', '算', '時', '分',
    '等'}
PTN_HIRAWD = (
    '(＜★＞|ねじ|めっき|はかり|ばね|はんだ|びん|ふるい|おもり|ろ過|しわ|'
    'ひだ|組み合わせ|組合わせ|重なり)')
PTN_WDENDCHR = '(上|下|外|内|中|前|後)$'
PTN_AFTNAME = (
    '(?=(夫々|各々|又|若|及|並|或|即|以|上|下|外|内|中|前|後|'
    """＋|[^0-9０-９A-Za-zＡ-Ｚａ-ｚ_＿Ͱ-Ͽἀ-῾'Ⅰ-ⅿↀ-ↆ%％°ー・"""
    r'\p{Katakana}\p{Han}'
    '●いうえきくけちてみめらりるれろわんぎぐげざじずぜ]|$))')
PTN_NONEEDWD = '(前記|上記|当該|該|所謂|実質|夫々|各々|各種|各)'
PTN_NONEEDEND = (
    '(夫々|各々|自体|部分|等|又|若|及|並|或|即|毎|別|以上|以下|以外|以内|'
    '以前|以後|中|(上|下|外|内|前|後)(部|側|方)?)')
PTN_LTDHD = (
    '(第.+)?(第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]'
    '+の?|所定の?|特定の?|一定の?|一の|他の)')
PTN_B4TGT = '(備える|含む|有する)?(請求項.+記載の)?'
PTN_AFTGT = '。$'
PTN_JOINT = (
    '(と|、|＋★［[^＋]+］★＋|及び|並びに|又は|若しくは|或いは|'
    'のいずれか|$)')
JEDIC_FNAME = 'patelier.dic'
EN_CLS = 'Claims'
EN_CL = 'Claim '
EN_ABST = 'Abstract'
PTN_AFTJIWD = (
    '(?=(夫々|各々|又|若|及|並|或|即|以|上|下|外|内|中|'
    """＋|[^0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾'Ⅰ-ⅿↀ-ↆ%％°ー・"""
    r'\p{Katakana}\p{Han}]|$))')
PTN_AFTGENWD = (
    '(?=(夫々|各々|及び|並びに|又は|若しくは|或いは|'
    '即ち|つまり|のいずれか|＋★［[^＋]+］★＋|から|[はとにへをが]|$))')
PTN_CLLTDHD = (
    '(?P<head>(((第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ'
    '-ⅻIVXivx]+([,，、～]|＋★［[^＋]+］★＋))*)'
    '(第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+)'
    '|所定|特定|一定|一|他|別)(の?))')
PTN_CLGENHD = (
    '(?P<head>((([0-9０-９A-Za-zＡ-Ｚａ-ｚ一二三四五六七'
    '八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+[つ回行組個数対番目本次定列]?(以上|以下|未満|'
    '＋★［[^＋]+］★＋複数|又は複数|または複数)?)の|複数の?))?)')
STR_DFLTDESC_S = (
    '(機能/作用/動作原理/属性/形状/サイズ/材質/態様/入出力/生成関連情報等)')
STR_DFLTDESC_M = '(作用/実行機構/実行タイミング/利用手法情報等)'
STR_DFLTDESC_D = '(意義/用途/属性/サイズ/生成消滅参照更新情報等)'
AUTO_RF_MARK = 'ＸＸ'
SPC_HEADS = [
    '発明の名称', '技術分野', '背景技術', '先行技術文献', '特許文献',
    '非特許文献', '発明の概要', '発明の開示', '発明が解決しようとする課題',
    '課題を解決するための手段', '発明の効果', '図面の簡単な説明',
    '発明を実施するための形態', '発明を実施するための最良の形態', '実施例',
    '産業上の利用可能性', '符号の説明', '受託番号', '配列表フリーテキスト',
    '配列表']
SPC_NEWHEADSDIC = {
    '発明の名称': 'Title of Invention',
    '技術分野': 'Technical Field', '背景技術': 'Background Art',
    '先行技術文献': 'Citation List', '特許文献': 'Patent Literature',
    '非特許文献': 'Non Patent Literature',
    '発明の概要': 'Summary of Invention',
    '発明が解決しようとする課題': 'Technical Problem',
    '課題を解決するための手段': 'Solution to Problem',
    '発明の効果': 'Advantageous Effects of Invention',
    '図面の簡単な説明': 'Brief Description of Drawings',
    '発明を実施するための形態': 'Description of Embodiments',
    '実施例': 'Examples', '産業上の利用可能性': 'Industrial Applicability',
    '符号の説明': 'Reference Signs List',
    '受託番号': 'Reference to Deposited Biological Material',
    '配列表フリーテキスト': 'Sequence Listing Free Text',
    '配列表': 'Sequence Listing'}
ENSPCHEADS_EX = [
    'Specification', 'Description', 'Title of the Invention',
    'Background of the Invention', 'Summary of the Invention',
    'Summary of Invention', 'Brief Summary of the Invention',
    'Brief Summary of Invention', 'Detailed Description of the Invention']
SPC_HEADSNODIC = {
    '特許文献': 'PTL ', '非特許文献': 'NPL ', '実施例': 'Example '}
SPC_HEADSBRNCHDIC = {'図': 'Fig. '}
EB_HEADS = {
    '発明を実施するための形態', '発明を実施するための最良の形態', '実施例'}
STR_RFHEADS = '符号の説明'
EB_CHEMWDS = {
    '化合物', '物質', '元素', '原子', '粒子', '分子', '基', '塩', '酸',
    '触媒', '溶媒', '溶質', 'イオン'}
EB_NGWDRFS = {
    ('速度', 'm'), ('距離', 'm'), ('積', 'm'), ('積', 'm2'), ('積', 'm3'),
    ('重', 'g'), ('量', 'g'), ('重', 't'), ('量', 't'), ('量', 'B'),
    ('量', 'l'), ('電圧', 'v'), ('電位', 'v'), ('電圧', 'V'), ('力', 'N'),
    ('重量', 'N'), ('力', 'w'), ('力', 'W'), ('率', 'W'), ('電流', 'A'),
    ('容量', 'F'), ('インダクタンス', 'H'), ('率', 'H'), ('時間', 'h'),
    ('時間', 'H'), ('時間', 's'), ('量', 'J'), ('温度', 'K'), ('電荷', 'C'),
    ('磁束密度', 'B')}
PTN_EBAFTRF = (
    '((?!(以上|以下|未満|つ|号|番|個|位|日|週|月|年|時|分|秒|代|歳|才|世|台|'
    '円|度|行|列|本|巻|冊|刷|版|点|割|回|周|種|箱|順|辺|巡|票|組|杯|席|部|'
    '課|班|[0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ%％°'
    r'\p{Katakana}]))|$)')
PTN_EBHD = (
    '(?P<head>((第＃[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+'
    '([, ，、～]|＋★［[^＋]+］★＋))*)(第＃[0-9０-９一二三四五六七八九十Ⅰ'
    '-Ⅻⅰ-ⅻIVXivx]+の?)?)')
PTN_EBHD4NORF = (
    '(?P<head>((第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+([, ，、～]'
    '|＋★［[^＋]+］★＋))*)'
    '(第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+の?)?)')
PTN_EBRFAFTEN = (
    '(?P<ref>([0-9０-９Ͱ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]+)'
    '([0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]+)?'
    """(['"´‘’′“”″゛])?([-－―]"""
    '[0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]+)?)')
PTN_RF = (
    '(?P<ref>([0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]'
    '[-－―・／/0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]*)'
    """(['´‘’′"“”″゛])?"""
    '([-－―][0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]+)?)')
PTN_EBGRPRF1 = (
    '([, ，、～])([0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ'
    '-ⅿↀ-ↆ][-－―・／/0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]*'
    """['´‘’′"“”″゛]?[-－―]?"""
    '[0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]*)')
PTN_EBGRPRF = (
    '(?P<rfgrp>([, ，、～][0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ'
    '-῾Ⅰ-ⅿↀ-ↆ][-－―・／/0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]*'
    """['´‘’′"“”″゛]?[-－―]?"""
    '[0-9０-９A-Za-zＡ-Ｚａ-ｚͰ-Ͽἀ-῾Ⅰ-ⅿↀ-ↆ]*)*)')
PTN_ENWDS = (
    r'([A-Za-zＡ-Ｚａ-ｚ]+([ 　/／:：_＿\-－][A-Za-zＡ-Ｚａ-ｚ]+|'
    r'[_＿\-－][0-9０-９A-Za-zＡ-Ｚａ-ｚ]+)+)*')
STR_JEHEAD = '重要語リスト'
ZEN4RF = (
    'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
    'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ＠－―／'
    """０´１‘２’３′４“５”６″７゛８９，、～""")
HAN4RF = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@--/'
    """0'1'2'3'4"5"6"7"89,,-""")
ZEN = (
    'ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
    'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ＠．（）＿－―／'
    '０１２３４５６７８９')
HAN = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@.()_--/'
    '0123456789')
PTN_ADJ = '(?P<adjective>(＋★｛[^｛]+｝★＋)*)'
PTN_NOUN = '(?P<noun>(＋★＜[^＜]+＞★＋)*)'
ZEN_KANA = (
    '。「」、・ヲァィゥェォャュョッーアイウエオカキクケコ'
    'サシスセソタチツテトタニヌネノハヒフヘホマミムメモヤユヨ'
    'ラリルレロワン゛゜')
HAN_KANA = (
    '｡｢｣､･ｦｧｨｩｪｫｬｭｮｯｰｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖ'
    'ﾗﾘﾙﾚﾛﾜﾝﾞﾟ')  # (\uff61-\uff9f)
ZEN_NUM = '０１２３４５６７８９'
HAN_NUM = '0123456789'
NUMS = ['０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
WD_CLASSMAX = 600
prgrss = 0
prsr = None
wd_set = set()
wdlines_dic = {}
clno_max = 0
cl_nounset = set()
cl1_list = []
cl_dic = {}
cl_strdic = {}
cl_newdic = {}
cl_basedic = {}
cl_blkdic = {}
cl_jwddic = {}
cl_errjwddic = {}
cl_iwddic = {}
cl_cmtdic = {}
cl_refdic = {}
cl_tgtlinedic = {}
cl_tgtdic = {}
cl_tgtgrpdic = {}
cl_mwddic = {}
cl_eldic = {}
cl_structdic = {}
cl_tmpstructdic = {}
cl_allstructdic = {}
cl_strgdic = {}
cl_tmpstrgdic = {}
cl_allstrgdic = {}
cl_pgdic = {}
cl_tmppgdic1 = {}
cl_tmppgdic2 = {}
cl_tmppgdic3 = {}
cl_allpgdic = {}
cl_wdattrdic = {}
cl_alljwdset = set()
cl_endwdset = set()
cl_kwddic = {}
cl_onlyiwddic = {}
cl_allwddic = {}
cl_wddic = {}
cl_wdnodic = {}
cl_wdclassnodic = {}
cl_topelset = set()
cl_topmethodelset = set()
fig_dic = {}
fig_streldic = {}
je_wddic = {}
spc_basedic = {}
prev_paranum = 0
used_paranoset = set()
all_wdrefdic = {}
eb_dic = {}
eb_wdrefs = []
eb_wdrefsflg = False
eb_samerefdiffs = []
eb_norefdic = {}
eb_wdrefdic = {}
eb_wdinfodic = {}
eb_diffexpdic = {}
eb_refwdlvdic = {}
eb_refwdset = set()
eb_wdnodic = {}
imp_wdset = set()
ptn_impwd = ''
rf_refdic = {}
rf_allset = set()
rf_okset = set()
ephr_dic = {}


def patelier():
    """patelier for Command prompt

    This reads a file and gives text lines to Patisserie.
    The file needs to include a claim written in Japanese,
        according to the Japanese patent application style.
    Patisserie is a class for analyzing the text lines.

    After patelier package is installed,
    command "patelier" is available to activate this patelier function.

    """
    rt = tkinter.Tk()
    rt.attributes('-topmost', True)
    rt.withdraw()
    ftype = [('txt/docx file', '*.txt'), ('txt/docx file', '*.docx')]
    crntdir = os.getcwd()
    strs = []
    if _chk(crntdir):
        tkinter.messagebox.showinfo(
                'patelier',
                '請求項を含むファイルを選択してください。',
                parent=rt)
        srcfpath = tkinter.filedialog.askopenfilename(
                parent=rt, filetypes=ftype, initialdir=crntdir)
        rt.destroy()
        if not os.path.isfile(srcfpath):
            print(''.join((
                    '■Error:処理対象ファイルが存在しません。',
                    srcfpath)))
            print('■異常終了')
        elif 'txt' == srcfpath.rsplit('.', 1)[1].lower():
            strs = _readf(srcfpath)
            if not strs:
                strs = _readf932(srcfpath)
            if not strs:
                strs = _readfu8(srcfpath)
            if not strs:
                print('■異常終了')
        else:
            strs = _readfdx(srcfpath)
    else:  # non-under-development process
        tkinter.messagebox.showinfo(
                'patelier (under development)',
                'ファイルを選択してください', parent=rt)
        ftype = [('txt file', '*.txt')]
        srcfpath = tkinter.filedialog.askopenfilename(
                parent=rt, filetypes=ftype, initialdir=crntdir)
        rt.destroy()
        if not os.path.isfile(srcfpath):
            print(''.join((
                    '■Error:対象ファイルが存在しません。',
                    srcfpath)))
            print('■異常終了')
        else:
            strs = _readf(srcfpath)
            if not strs:
                strs = _readf932(srcfpath)
            if not strs:
                strs = _readfu8(srcfpath)
            if not strs:
                print('■異常終了')
            else:
                lineno = 1
                rgx_ngmsg = regex.compile(r'[\x00-\x1f]')
                for eatx in strs:
                    newtx = eatx.rstrip()
                    msg = rgx_ngmsg.sub('▲', newtx)
                    newmsg = ''.join((str(lineno), ' :', msg))
                    print(''.join((newmsg, '\n')))
                    lineno += 1
        return
    if strs:
        patisserie = Patisserie()
        patisserie.setting(strs, False, '', srcfpath)
        patisserie.start()
        prgrsscnt = 0
        tmp_progress = 0
        prev_progress = 0
        # prgrss:0,3,7,14,28,45,60,90,100
        range_maxset = {6, 13, 27, 44, 59, 89, 99}
        while True:
            time.sleep(2)
            progress = patisserie.get_prgrss()
            if 100 == progress:
                break
            if 0 < progress < 100:
                if prev_progress != progress:
                    prgrsscnt = 0
                tmp_progress = progress + prgrsscnt
                print(''.join((
                        '\r■原文分析中(', str(tmp_progress),
                        '%):しばらくお待ちください。')), end='')
                if tmp_progress not in range_maxset:
                    prgrsscnt += 1
            prev_progress = progress
        patisserie.join()
        if not patisserie.ret():
            print('■異常終了')
        del patisserie


class Patisserie(threading.Thread):
    """Patisserie class for analyzing text lines

    Main method of this class is 'run'.
    This gets the text lines, analyzes them, and outputs results.
    This employs the patissier function for analyzing the text lines.
    This outputs result files.
    The result files shows the result of the patissier's analysis.
    The result files include res-utf8.txt ,patelier.html and so on.
    The res-utf8.txt is a plain text version of the patelier.html.
    The patelier.html uses patelierjs.js.

    Args of method 'setting' for method 'run':
        txlines (list): This is a list of line strings of text data.
        zflg (bool): False is set by patelier function.
        outdir (string):
            This is an output folder path.
            This is needless when called by patelier function.
        srcfpath (string):
            This is a source file path.
            This is necessary only when called by patelier function.
            This is null string when called by patelier App (zero).

    Method 'set_outdir' is called by patelier App.
    Args of method 'set_outdir':
        outdir (string):
            This is an output folder path.

    Method 'readf_setting_z' is called by patelier App.
    This method reads file and makes setting for method 'run'.

    Returns of method 'get_infilename':
        string: filename of the file

    Returns of method 'get_prgrss':
        int: amount of prgrss

    Returns of method 'ret':
        bool:
            True: OK
            False: An error has ocurred.

    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.rtnval = True

    def readf_setting_z(self):
        self.rtnval = False
        strs = []
        rt = tkinter.Tk()
        rt.attributes('-topmost', True)
        rt.withdraw()
        ftype = [('txt/docx file', '*.txt'), ('txt/docx file', '*.docx')]
        rt_dir = '\\'
        srcfpath = tkinter.filedialog.askopenfilename(
                parent=rt, filetypes=ftype, initialdir=rt_dir)
        rt.destroy()
        if not os.path.isfile(srcfpath):
            print(''.join((
                    '■Error:処理対象ファイルが存在しません。',
                    srcfpath)))
            print('■異常終了')
        elif 'txt' == srcfpath.rsplit('.', 1)[1].lower():
            strs = _readf(srcfpath)
            if not strs:
                strs = _readf932(srcfpath)
            if not strs:
                strs = _readfu8(srcfpath)
            if not strs:
                print('■異常終了')
        else:
            strs = _readfdx(srcfpath)
        if strs:
            self.rtnval = True
            self.txlines = strs
            self.zflg = True
            self.srcfpath = srcfpath
            self.in_fname = os.path.basename(srcfpath)

    def set_outdir(self, outdir):
        self.outdir = outdir

    def setting(self, txlines, zflg, outdir, srcfpath):
        self.txlines = txlines
        self.zflg = zflg
        self.outdir = outdir
        self.srcfpath = srcfpath

    def run(self):
        global EN_ABST
        global EN_CLS
        global ENSPCHEADS_EX
        global HD_CMT
        global HD_CMTBLK
        global SPC_NEWHEADSDIC
        global cl_svgdic
        global prgrss
        global rgx_del
        global rgx_styledel
        global rgx_udel
        global rgx_hansp
        global rgx_headsps
        rgx_hansp = regex.compile(r'\x20')
        rgx_headsps = regex.compile(r'^[\x20\u3000\u00a0]+')
        rgx_del = regex.compile('☆［[^☆]*］☆')
        rgx_styledel = regex.compile('★［(≪|＜)[^★]*(≫|＞)］★')
        rgx_udel = regex.compile('★［≪[^★]*≫］★')
        rgx_encls = regex.compile(''.join((
                r'(^|\[)(', EN_CLS, '|', EN_CLS.upper(), ')')))
        rgx_enabst = regex.compile(''.join((
                r'(^|\[)(', EN_ABST, '|', EN_ABST.upper(), ')')))
        enspcheads = [x for x in SPC_NEWHEADSDIC.values()]
        enspcheads.extend(ENSPCHEADS_EX)
        enspcheadsup = [x.upper() for x in enspcheads]
        rgx_enspcheads = regex.compile(''.join((
                r'(^|\[)(', '|'.join((enspcheads)),
                '|',  '|'.join((enspcheadsup)), ')')))
        prgrss = 0
        efcllines = []
        efspclines = []
        eflines = []
        if self.srcfpath:
            srcfpathdiv = self.srcfpath.rsplit('.', 1)
            fextention = srcfpathdiv[1]
            efpath = ''.join((srcfpathdiv[0], '-e.', fextention))
            if os.path.isfile(efpath):
                if 'txt' == fextention.lower():
                    eflines = _readf(efpath)
                    if not eflines:
                        eflines = _readf932(efpath)
                    if not eflines:
                        eflines = _readfu8(efpath)
                else:
                    eflines = _readfdx(efpath)
        if eflines:
            eflinestat = 0
            noefclflg = True
            noefspcflg = True
            eflines = [x for x in eflines if (not x.startswith(
                    HD_CMTBLK)) and (not x.startswith(HD_CMT))]
            for efline in eflines:
                if efline:
                    if 1 != eflinestat:
                        if rgx_encls.search(efline):
                            eflinestat = 1
                            noefclflg = False
                    if 2 != eflinestat:
                        if rgx_enspcheads.search(efline):
                            eflinestat = 2
                            noefspcflg = False
                    if 0 < eflinestat:
                        if rgx_enabst.search(efline):
                            eflinestat = 0
                    if 1 == eflinestat:
                        efcllines.append(efline)
                    elif 2 == eflinestat:
                        efspclines.append(efline)
        else:
            noefclflg = True
            noefspcflg = True
        outf_mgr = _OutfMgr(self.zflg, self.outdir)
        if not outf_mgr._preparation():
            del outf_mgr
            self.rtnval = False
            prgrss = 100
            return
        cl_lines = []
        if not self.zflg:
            print(''.join(('■処理対象ファイル(原文):', self.srcfpath)))
            print(
                    '■原文分析結果ファイルは、'
                    '<patelier-result>フォルダーに格納されます。')
            starttime = datetime.datetime.now()
            print(''.join((
                '■原文分析開始:', starttime.strftime('%Y/%m/%d %H:%M'))))
        (ngline_nums, warn_lines, cl_lines, cl_elines, clel_lines,
         tr_lines, trel_lines,
         spc_lines, spc_elines, spchd_lines, spccl_lines,
         abs_lines, fig_lines, ref_lines, wd_lines, wdlist_lines,
         a_array, array_tip, array_ef) = patissier(
                self.txlines, noefclflg, efspclines)
        restxf = outf_mgr._restxf_open()
        if restxf:
            if not self.zflg:
                restxf.write(''.join(('■■原文:', self.srcfpath, '\n')))
            if self.txlines:
                _txsrc(restxf, self.txlines, ngline_nums)
            if warn_lines:
                _txwarn(restxf, warn_lines)
            if cl_lines:
                _txcl(restxf, cl_lines)
                if cl_elines:
                    _txclen(restxf, cl_lines, cl_elines)
                _txclel(restxf, clel_lines)
                _txtr(restxf, tr_lines)
                _txtrel(restxf, trel_lines)
                if spc_lines:
                    _txspc(restxf, spc_lines)
                    if spc_elines:
                        _txspcen(restxf, spc_lines, spc_elines)
                if spchd_lines:
                    _txspchd(restxf, spchd_lines)
                _txspccl(restxf, spccl_lines)
                _txabs(restxf, abs_lines)
                _txfig(restxf, fig_lines)
                _txref(restxf, ref_lines)
                _txwd(restxf, wd_lines)
                if wdlist_lines:
                    _txwdlist(restxf, wdlist_lines)
            restxf.close()
        patf = outf_mgr._patf_open()
        if patf:
            if self.zflg:
                _hxhd(patf, self.outdir, self.zflg)
            else:
                srcf_name = os.path.basename(self.srcfpath)
                _hxhd(patf, srcf_name, self.zflg)
            if cl_lines:
                if spc_lines:
                    spcflg = True
                else:
                    spcflg = False
                if spchd_lines:
                    spchdflg = True
                else:
                    spchdflg = False
                if wdlist_lines:
                    wdlistflg = True
                else:
                    wdlistflg = False
                _hxnav(patf, spcflg, spchdflg, wdlistflg)
                _hxsrcart(patf, self.txlines, ngline_nums)
                _hxwarnart(patf, warn_lines, True)
                _hxclart(patf)
                _hxclelart(patf, clel_lines)
                _hxtrart(patf, tr_lines, trel_lines)
                if spc_lines:
                    _hxspcart(patf)
                if spchd_lines:
                    _hxspchdart(patf, spchd_lines)
                _hxspcclart(patf, spccl_lines)
                _hxabsart(patf, abs_lines)
                _hxfigart(patf, fig_lines)
                svgheader = ''.join((
                        '<?xml version="1.0" encoding="UTF-8"',
                        ' standalone="no"?>\n'))
                for pageno in sorted(cl_svgdic.keys()):
                    clpictf = outf_mgr._clpictf_open(pageno)
                    if clpictf:
                        clpictf.write(''.join((
                                svgheader, cl_svgdic[pageno], '</svg>')))
                        clpictf.close()
                _hxrefart(patf, ref_lines)
                _hxwdart(patf, wd_lines)
                if wdlist_lines:
                    _hxwdlistart(patf, wdlist_lines)
                patjsf = outf_mgr._patjsf_open()
                if patjsf:
                    if noefclflg:
                        _pjsclwt(patjsf, cl_lines, cl_elines, noefclflg, '')
                    else:
                        _pjsclwt(
                                patjsf, cl_lines, efcllines,
                                noefclflg, os.path.basename(efpath))
                    if spc_lines:
                        if noefspcflg:
                            _pjsspcwt(
                                    patjsf, spc_lines, spc_elines, noefspcflg,
                                    '')
                        else:
                            _pjsspcwt(
                                    patjsf, spc_lines, efspclines, noefspcflg,
                                    os.path.basename(efpath))
                    _pjswt(patjsf, a_array, array_tip, array_ef)
                    patjsf.close()
            else:
                _hxnavlt(patf)
                _hxsrcart(patf, self.txlines, ngline_nums)
                _hxwarnart(patf, warn_lines, False)
            _hxft(patf)
            patf.close()
        del outf_mgr
        if not self.zflg:
            endtime = datetime.datetime.now()
            deltatime = endtime - starttime
            print(''.join((
                    '\r■分析終了:', endtime.strftime('%Y/%m/%d %H:%M'),
                    ' (処理時間{0}sec)'.format(deltatime.seconds))))
        self.rtnval = True
        prgrss = 100
        return

    def get_infilename(self):
        return self.in_fname

    def get_prgrss(self):
        global prgrss
        return prgrss

    def ret(self):
        return self.rtnval


def _readf(fpath):
    try:
        with open(fpath, mode='rt') as f:
            return f.read().splitlines()
    except OSError:
        print(''.join((
                '■Warning:ファイルOpen(標準文字コード)に'
                '失敗しました(Shift-JIS[CP932]指定で再試行します)。',
                fpath)))
        return []
    except Exception as e:
        print(''.join((
                '■Warning:ファイルOpen(標準文字コード)に'
                '失敗しました(Shift-JIS[CP932]指定で再試行します)。',
                fpath, ' ', str(e.args[0]))))
        return []


def _readf932(fpath):
    try:
        with open(fpath, mode='rt', encoding='cp932') as f:
            return f.read().splitlines()
    except OSError:
        print(''.join((
                '■Warning:ファイルOpen(Shift_JIS[CP932]指定)に'
                '失敗しました(UTF-8指定で再試行します)。', fpath)))
        return []
    except Exception as e:
        print(''.join((
                '■Warning:ファイルOpen(Shift_JIS[CP932]指定)に'
                '失敗しました(UTF-8指定で再試行します)。', fpath, ' ',
                str(e.args[0]))))
        return []


def _readfu8(fpath):
    try:
        with open(fpath, mode='rt', encoding='utf-8') as f:
            return f.read().splitlines()
    except OSError:
        print(''.join((
                '■Error:ファイルOpen(UTF-8指定)に失敗しました。', fpath)))
        return []
    except Exception as e:
        print(''.join((
                '■Error:ファイルOpen(UTF-8指定)に失敗しました。', fpath,
                ' ', str(e.args[0]))))
        return []


def _readfdx(fpath):
    retlines = []
    ngflg = True
    dox = Document(fpath)
    rgx_lf = regex.compile(r'\x0a')
    for paragraph in dox.paragraphs:
        doxline = ''
        for run in paragraph.runs:
            if run.underline and run.font.superscript:
                doxline = ''.join((
                        doxline, '★［≪u≫］★★［＜sup＞］★',
                        run.text, '★［＜/sup＞］★★［≪/u≫］★'))
            elif run.underline and run.font.subscript:
                doxline = ''.join((
                        doxline, '★［≪u≫］★★［＜sub＞］★',
                        run.text, '★［＜/sub＞］★★［≪/u≫］★'))
            elif run.font.superscript:
                doxline = ''.join((
                        doxline, '★［＜sup＞］★', run.text,
                        '★［＜/sup＞］★'))
            elif run.font.subscript:
                doxline = ''.join((
                        doxline, '★［＜sub＞］★', run.text,
                        '★［＜/sub＞］★'))
            elif run.underline:
                doxline = ''.join((
                        doxline, '★［≪u≫］★', run.text, '★［≪/u≫］★'))
            else:
                doxline = ''.join((doxline, run.text))
        doxline = doxline.replace('★［≪/u≫］★★［≪u≫］★', '')
        if doxline:
            ngflg = False
            mres = rgx_lf.finditer(doxline)
            lastpos = 0
            for res in sorted(mres, key=lambda x: x.span()[0], reverse=False):
                retlines.append(doxline[lastpos:res.span()[0]])
                lastpos = res.span()[1]
            if len(doxline) > lastpos:
                retlines.append(doxline[lastpos:])
        else:
            retlines.append('')
    if ngflg:
        print(''.join(('■Error:ファイル読込に失敗しました。', fpath)))
        return []
    return retlines


class _OutfMgr(object):
    def __init__(self, zflg, odir):
        self.zflg = zflg
        current_dir = os.getcwd()
        if zflg:
            self.out_rt = os.path.join(current_dir, 'zero')
            self.outpath = os.path.join(self.out_rt, odir)
            self.astspath = os.path.join(self.out_rt, 'patelier-assets')
        else:
            self.out_rt = current_dir
            self.outpath = os.path.join(self.out_rt, 'patelier-result')
            self.astspath = os.path.join(self.outpath, 'patelier-assets')
        self.restxfpath = os.path.join(self.outpath, 'res-utf8.txt')
        self.patfpath = os.path.join(self.outpath, 'patelier.html')
        self.patjsfpath = os.path.join(self.outpath, 'patelierjs.js')
        self.clpictfpath = os.path.join(self.outpath, 'res-cl-based-pict')
        return None

    def _preparation(self):
        if not self.zflg:
            path_dic = _pkg()
            if not path_dic:
                print(
                        '■Error:patelierパッケージ実体が'
                        '正しくインストールされていません。')
                return False
            if os.path.exists(self.outpath):
                if not os.path.isdir(self.outpath):
                    print('■Warning:patelier-resultファイルを削除します。')
                    try:
                        os.remove(self.outpath)
                    except OSError:
                        print(
                                '■Error:分析結果出力用フォルダーの設定'
                                '(patelier-resultファイル削除)に'
                                '失敗しました。')
                        return False
                    try:
                        os.mkdir(self.outpath)
                    except OSError:
                        print(
                                '■Error:分析結果出力用フォルダー'
                                '(patelier-result)の生成に失敗しました。')
                        return False
                else:
                    if os.path.exists(self.patjsfpath):
                        try:
                            os.remove(self.patjsfpath)
                        except OSError:
                            print(
                                    '■Error:分析結果出力用フォルダーの設定'
                                    '(残存patelierjs.jsファイル削除)に'
                                    '失敗しました。')
                            return False
                    if os.path.exists(self.clpictfpath):
                        try:
                            shutil.rmtree(self.clpictfpath)
                        except OSError:
                            print(
                                    '■Error:分析結果出力用フォルダーの'
                                    '設定(残存<res-cl-based-pict>'
                                    'フォルダー削除)に失敗しました。')
                            return False
            else:
                try:
                    os.mkdir(self.outpath)
                except OSError:
                    print(
                            '■Error:分析結果出力用フォルダー'
                            '(patelier-result)の生成に失敗しました。')
                    return False
            csspath = os.path.join(self.astspath, 'patelier.css')
            jspath = os.path.join(self.astspath, 'patelier.js')
            icopath = os.path.join(self.astspath, 'patelier.ico')
            logopath = os.path.join(self.astspath, 'patelier.png')
            gifpath = os.path.join(self.astspath, 'patelier.gif')
            if os.path.exists(self.astspath):
                if os.path.isdir(self.astspath):
                    if not os.path.isfile(csspath):
                        try:
                            shutil.copy2(path_dic['csspath'], self.astspath)
                        except OSError:
                            print(
                                    '■Error:分析結果表示用リソース'
                                    '(patelier.css)の設定に失敗しました。')
                            return False
                    if not os.path.isfile(jspath):
                        try:
                            shutil.copy2(path_dic['jspath'], self.astspath)
                        except OSError:
                            print(
                                    '■Error:分析結果表示用リソース'
                                    '(patelier.js)の設定に失敗しました。')
                            return False
                    if not os.path.isfile(icopath):
                        try:
                            shutil.copy2(path_dic['icopath'], self.astspath)
                        except OSError:
                            print(
                                    '■Error:分析結果表示用リソース'
                                    '(patelier.ico)の設定に失敗しました。')
                            return False
                    if not os.path.isfile(logopath):
                        try:
                            shutil.copy2(path_dic['logopath'], self.astspath)
                        except OSError:
                            print(
                                    '■Error:分析結果表示用リソース'
                                    '(patelier.png)の設定に失敗しました。')
                            return False
                    if not os.path.isfile(gifpath):
                        try:
                            shutil.copy2(path_dic['gifpath'], self.astspath)
                        except OSError:
                            print(
                                    '■Error:分析結果表示用リソース'
                                    '(patelier.gif)の設定に失敗しました。')
                            return False
                else:
                    print('■Warning:patelier-assetsファイルを削除します。')
                    try:
                        os.remove(self.astspath)
                    except OSError:
                        print(
                                '■Error:分析結果表示用リソースの設定'
                                '(patelier-assetsファイル削除)に'
                                '失敗しました。')
                        return False
                    try:
                        os.mkdir(self.astspath)
                        shutil.copy2(path_dic['csspath'], self.astspath)
                        shutil.copy2(path_dic['jspath'], self.astspath)
                        shutil.copy2(path_dic['icopath'], self.astspath)
                        shutil.copy2(path_dic['logopath'], self.astspath)
                        shutil.copy2(path_dic['gifpath'], self.astspath)
                    except OSError:
                        print(
                                '■Error:分析結果表示用リソース'
                                '(patelier-assetsフォルダー)の設定に'
                                '失敗しました。')
                        return False
            else:
                try:
                    os.mkdir(self.astspath)
                    shutil.copy2(path_dic['csspath'], self.astspath)
                    shutil.copy2(path_dic['jspath'], self.astspath)
                    shutil.copy2(path_dic['icopath'], self.astspath)
                    shutil.copy2(path_dic['logopath'], self.astspath)
                    shutil.copy2(path_dic['gifpath'], self.astspath)
                except OSError:
                    print(
                            '■Error:分析結果表示用リソース'
                            '(patelier-assetsフォルダー)の設定に'
                            '失敗しました。')
                    return False
        else:
            hxpath = os.path.join(self.out_rt, 'patelierzero.html')
            csspath = os.path.join(self.astspath, 'patelier.css')
            jspath = os.path.join(self.astspath, 'patelier.js')
            icopath = os.path.join(self.astspath, 'patelier.ico')
            logopath = os.path.join(self.astspath, 'patelier.png')
            gifpath = os.path.join(self.astspath, 'patelier.gif')
            tcpath = os.path.join(self.astspath, 'pateliertc.png')
            zjpath = os.path.join(self.astspath, 'patelierzero.j')
            envflg = False
            if os.path.isfile(hxpath):
                if os.path.isfile(csspath):
                    if os.path.isfile(jspath):
                        if os.path.isfile(icopath):
                            if os.path.isfile(logopath):
                                if os.path.isfile(gifpath):
                                    if os.path.isfile(tcpath):
                                        if os.path.isfile(zjpath):
                                            envflg = True
            if not envflg:
                print(
                        '■Error:分析結果表示用環境が'
                        '正しく構成されていません。')
                return False
            if os.path.exists(self.outpath):
                if not os.path.isdir(self.outpath):
                    try:
                        os.remove(self.outpath)
                    except OSError:
                        print(
                                '■Error:分析結果出力用フォルダーの設定'
                                '(同名ファイル削除)に失敗しました。')
                        return False
                    try:
                        os.mkdir(self.outpath)
                    except OSError:
                        print(
                                '■Error:分析結果出力用フォルダーの生成に'
                                '失敗しました。')
                        return False
            else:
                try:
                    os.mkdir(self.outpath)
                except OSError:
                    print(
                            '■Error:分析結果出力用フォルダーの生成に'
                            '失敗しました。')
                    return False
        return True

    def _restxf_open(self):
        try:
            restxf = open(self.restxfpath, mode='wt', encoding='utf-8')
            return restxf
        except OSError:
            print(''.join((
                    '■Error:出力ファイルOpen(UTF-8指定)に失敗しました。',
                    self.restxfpath)))
            return None
        except Exception as e:
            print(''.join((
                    '■Error:出力ファイルOpen(UTF-8指定)に失敗しました。',
                    self.restxfpath, ' ', str(e.args[0]))))
            return None

    def _patf_open(self):
        try:
            patf = open(self.patfpath, mode='wt', encoding='utf-8')
            return patf
        except OSError:
            print(''.join((
                    '■Error:出力ファイルOpen(UTF-8指定)に失敗しました。',
                    self.patfpath)))
            return None
        except Exception as e:
            print(''.join((
                    '■Error:出力ファイルOpen(UTF-8指定)に失敗しました。',
                    self.patfpath, ' ', str(e.args[0]))))
            return None

    def _patjsf_open(self):
        try:
            patjsf = open(self.patjsfpath, mode='wt', encoding='utf-8-sig')
            return patjsf
        except OSError:
            print(''.join((
                    '■Error:出力ファイルOpen(UTF-8withBOM指定)に'
                    '失敗しました。', self.patjsfpath)))
            return None
        except Exception as e:
            print(''.join((
                    '■Error:出力ファイルOpen(UTF-8withBOM指定)に'
                    '失敗しました。',
                    self.patjsfpath, ' ', str(e.args[0]))))
            return None

    def _clpictf_open(self, page_num):
        fname = ''.join(('p', str(page_num), '.svg'))
        fpath = os.path.join(self.clpictfpath, fname)
        if 1 == page_num:
            if os.path.exists(self.clpictfpath):
                if not os.path.isdir(self.clpictfpath):
                    try:
                        os.remove(self.clpictfpath)
                    except OSError:
                        print(
                                '■Error:分析結果出力用フォルダーの設定'
                                '(同名ファイル削除)に失敗しました。')
                        return None
                    try:
                        os.mkdir(self.clpictfpath)
                    except OSError:
                        print(
                                '■Error:分析結果出力用フォルダーの生成に'
                                '失敗しました。')
                        return None
                else:
                    try:
                        shutil.rmtree(self.clpictfpath)
                        os.mkdir(self.clpictfpath)
                    except OSError:
                        print(
                                '■Error:分析結果出力用フォルダーの生成に'
                                '失敗しました。')
                        return None
            else:
                try:
                    os.mkdir(self.clpictfpath)
                except OSError:
                    print(
                            '■Error:分析結果出力用フォルダーの生成に'
                            '失敗しました。')
                    return None
        try:
            clpictf = open(fpath, mode='wt', encoding='utf-8')
            return clpictf
        except OSError:
            print(''.join((
                    '■Error:出力フォルダーOpen(UTF-8指定)に失敗しました。',
                    fpath)))
            return None
        except Exception as e:
            print(''.join((
                    '■Error:出力フォルダーOpen(UTF-8指定)に失敗しました。',
                    fpath, ' ', str(e.args[0]))))
            return None


def _pkg():
    path_dic = {}
    pkg = __package__
    pkgflg = False
    if pkg:
        fdir = os.path.dirname(sys.modules[pkg].__file__)
        pkg_patpath = os.path.join(fdir, 'data')
        pkg_patzpath = os.path.join(pkg_patpath, 'patelierzero.py')
        pkg_zpath = os.path.join(pkg_patpath, 'zero')
        pkg_hxpath = os.path.join(pkg_zpath, 'patelierzero.html')
        pkg_astspath = os.path.join(pkg_zpath, 'patelier-assets')
        pkg_csspath = os.path.join(pkg_astspath, 'patelier.css')
        pkg_jspath = os.path.join(pkg_astspath, 'patelier.js')
        pkg_icopath = os.path.join(pkg_astspath, 'patelier.ico')
        pkg_logopath = os.path.join(pkg_astspath, 'patelier.png')
        pkg_gifpath = os.path.join(pkg_astspath, 'patelier.gif')
        pkg_tcpath = os.path.join(pkg_astspath, 'pateliertc.png')
        pkg_zjpath = os.path.join(pkg_astspath, 'patelierzero.j')
        if os.path.isfile(pkg_patzpath):
            if os.path.isfile(pkg_hxpath):
                if os.path.isfile(pkg_csspath):
                    if os.path.isfile(pkg_jspath):
                        if os.path.isfile(pkg_icopath):
                            if os.path.isfile(pkg_logopath):
                                if os.path.isfile(pkg_gifpath):
                                    if os.path.isfile(pkg_tcpath):
                                        if os.path.isfile(pkg_zjpath):
                                            pkgflg = True
    if pkgflg:
        path_dic['patpath'] = pkg_patpath
        path_dic['patzpath'] = pkg_patzpath
        path_dic['zpath'] = pkg_zpath
        path_dic['hxpath'] = pkg_hxpath
        path_dic['astspath'] = pkg_astspath
        path_dic['csspath'] = pkg_csspath
        path_dic['jspath'] = pkg_jspath
        path_dic['icopath'] = pkg_icopath
        path_dic['logopath'] = pkg_logopath
        path_dic['gifpath'] = pkg_gifpath
        path_dic['tcpath'] = pkg_tcpath
        path_dic['zjpath'] = pkg_zjpath
    return path_dic


def _txsrc(fobj, txlines, ngline_nums):
    global rgx_styledel
    global rgx_ctrl
    fobj.write('■■原文情報\n')
    lineno = 1
    for eatx in txlines:
        newtx = eatx.rstrip()
        newtx = rgx_styledel.sub('', newtx)
        msg = rgx_ctrl.sub('▲', newtx)
        if lineno in ngline_nums:
            newmsg = ''.join((str(lineno), '!:', msg))
        else:
            newmsg = ''.join((str(lineno), ' :', msg))
        fobj.write(''.join((newmsg, '\n')))
        lineno += 1


def _txwarn(fobj, txlines):
    global rgx_styledel
    fobj.write('\n■■Warning\n')
    rgx_ltta_b = regex.compile('★ltTA[^★]+★ltTB')
    rgx_ptta_b = regex.compile('★ptTA[^★]+★ptTB')
    rgx_ctta_b = regex.compile('★ctTA[^★]+★ctTB')
    for newmsg in txlines:
        newmsg = newmsg.replace('★eTS', '').replace('★wTS', '').replace(
                '★wTE', '').replace('★ltTC', '').replace(
                '★ptTC', '').replace('★clTS', '').replace(
                '★clTE', '').replace('★ctTC', '')
        newmsg = rgx_ltta_b.sub('', newmsg)
        newmsg = rgx_ptta_b.sub('', newmsg)
        newmsg = rgx_ctta_b.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txcl(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■CL情報\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★lTA', '☆［').replace(
                '★lTB', '').replace('★lTC', '］☆').replace(
                '★lTX', '］☆').replace('★lTD', '').replace(
                '★sTS', '').replace('★sTE', '').replace(
                '★esTS', '').replace('★cTA', '☆［').replace(
                '★cTB', '］☆').replace('★cTC', '').replace(
                '★cTX', '').replace('★cTY', '').replace(
                '★ecTX', '').replace('★cmTS', '').replace(
                '★cmTE', '').replace('★rTS', '').replace(
                '★rTE', '').replace('★rcTS', '').replace(
                '★rcTE', '').replace('★dTA', '☆［').replace(
                '★dTC', '').replace('★dTD', '］☆').replace(
                '★dTE', '').replace('★dTY', '］☆').replace(
                '★ssTS', '').replace('★ssTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txclen(fobj, txlines1, txlines2):
    global rgx_del
    global rgx_styledel
    global rgx_headsps
    fobj.write('\n■■CL情報(英語Mix)\n')
    for idx, newmsg in enumerate(txlines1):
        newmsg = newmsg.replace('★lTA', '☆［').replace(
                '★lTB', '').replace('★lTC', '］☆').replace(
                '★lTX', '］☆').replace('★lTD', '').replace(
                '★sTS', '').replace('★sTE', '').replace(
                '★esTS', '').replace('★cTA', '☆［').replace(
                '★cTB', '］☆').replace('★cTC', '').replace(
                '★cTX', '').replace('★cTY', '').replace(
                '★ecTX', '').replace('★cmTS', '').replace(
                '★cmTE', '').replace('★rTS', '').replace(
                '★rTE', '').replace('★rcTS', '').replace(
                '★rcTE', '').replace('★dTA', '☆［').replace(
                '★dTC', '').replace('★dTD', '］☆').replace(
                '★dTE', '').replace('★dTY', '］☆').replace(
                '★ssTS', '').replace('★ssTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))
        newmsg = txlines2[idx]
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★lTAC', '').replace('★lTA', '☆［').replace(
                '★lTB', '').replace('★lTC', '］☆').replace(
                '★lTX', '］☆').replace('★lTD', '').replace(
                '★sTS', '').replace('★sTE', '').replace(
                '★esTS', '').replace('★cTA', '☆［').replace(
                '★cTB', '］☆').replace('★cTC', '').replace(
                '★cTX', '').replace('★cTY', '').replace(
                '★ecTX', '').replace('★cmTS', '').replace(
                '★cmTE', '').replace('★rTS', '').replace(
                '★rTE', '').replace('★rcTS', '').replace(
                '★rcTE', '').replace('★dTA', '☆［').replace(
                '★dTC', '').replace('★dTD', '］☆').replace(
                '★dTE', '').replace('★dTY', '］☆').replace(
                '★ssTS', '').replace('★ssTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        newmsg = rgx_headsps.sub('\t', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txclel(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■CL要素関連情報\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★dTA', '☆［').replace('★dTC', '').replace(
                '★dTD', '］☆').replace('★dTE', '').replace(
                '★ssTS', '').replace('★ssTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txtr(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■CL-Tree\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★ctTA', '☆［').replace('★ctTB', '］☆').replace(
                '★ctTC', '').replace('★cmTS', '').replace('★cmTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txtrel(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■構成CL-Tree\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★ctTA', '☆［').replace('★ctTB', '］☆').replace(
                '★ctTC', '').replace('★cmTS', '').replace('★cmTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txspc(fobj, txlines):
    global rgx_del
    global rgx_styledel
    global cl_strdic
    rgx_clextag = regex.compile('★qA')
    clexflg = False
    txlines_ex = []
    fobj.write('\n■■明細情報\n')
    for newmsg in txlines:
        if not clexflg:
            if rgx_clextag.search(newmsg):
                clexflg = True
        newmsg = newmsg.replace('★lTA', '☆［').replace(
                '★lTB', '').replace('★lTC', '］☆').replace(
                '★lTX', '］☆').replace('★lTD', '').replace(
                '★sTS', '').replace('★sTE', '').replace(
                '★esTS', '').replace('★pTA', '☆［').replace(
                '★pTB', '］☆').replace('★pTC', '').replace(
                '★pTX', '').replace('★pTY', '').replace(
                '★epTX', '').replace('★dTA', '☆［').replace(
                '★dTC', '').replace('★dTD', '］☆').replace(
                '★dTE', '').replace('★dTY', '］☆')
        newmsg = rgx_styledel.sub('', newmsg)
        txlines_ex.append(newmsg)
        newmsg = newmsg.replace('★qA', '☆［').replace(
                '★qB', '］☆').replace('★qC', '')
        newmsg = rgx_del.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))
    if clexflg:
        fobj.write('\n■■明細情報(CL展開)\n')
        rgx_cl_ex = regex.compile('★qA(?P<clno>[1-9][0-9]*)★qB[^★]+★qC')
        for newmsg in txlines_ex:
            mres = rgx_cl_ex.finditer(newmsg)
            for res in sorted(mres, key=lambda x: x.span()[0], reverse=True):
                clno = int(res.group('clno'))
                if clno in cl_strdic.keys():
                    strcl = cl_strdic[clno]
                else:
                    strcl = ''.join((
                            '（■Warning：CL',
                            res.group('clno'), 'が存在しません。）'))
                newmsg = ''.join((
                        newmsg[:res.span()[0]], strcl,
                        newmsg[res.span()[1]:]))
            newmsg = rgx_del.sub('', newmsg)
            fobj.write(''.join((newmsg, '\n')))


def _txspcen(fobj, txlines1, txlines2):
    global rgx_del
    global rgx_styledel
    global rgx_headsps
    fobj.write('\n■■明細情報(英語Mix)\n')
    for idx, newmsg in enumerate(txlines1):
        newmsg = newmsg.replace('★lTA', '☆［').replace(
                '★lTB', '').replace('★lTC', '］☆').replace(
                '★lTX', '］☆').replace('★lTD', '').replace(
                '★sTS', '').replace('★sTE', '').replace(
                '★esTS', '').replace('★pTA', '☆［').replace(
                '★pTB', '］☆').replace('★pTC', '').replace(
                '★pTX', '').replace('★pTY', '').replace(
                '★epTX', '').replace('★dTA', '☆［').replace(
                '★dTC', '').replace('★dTD', '］☆').replace(
                '★dTE', '').replace('★dTY', '］☆').replace(
                '★qA', '☆［').replace('★qB', '］☆').replace('★qC', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))
        newmsg = txlines2[idx]
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★lTAC', '').replace('★lTA', '☆［').replace(
                '★lTB', '').replace('★lTC', '］☆').replace(
                '★lTX', '］☆').replace('★lTD', '').replace(
                '★sTS', '').replace('★sTE', '').replace(
                '★esTS', '').replace('★pTA', '☆［').replace(
                '★pTB', '］☆').replace('★pTC', '').replace(
                '★pTX', '').replace('★pTY', '').replace(
                '★epTX', '').replace('★dTA', '☆［').replace(
                '★dTC', '').replace('★dTD', '］☆').replace(
                '★dTE', '').replace('★dTY', '］☆')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        newmsg = rgx_headsps.sub('\t', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txspchd(fobj, txlines):
    global rgx_del
    global rgx_styledel
    rgx_ptta_b = regex.compile('★ptTA[^★]+★ptTB')
    fobj.write('\n■■明細俯瞰情報\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★sTS', '').replace('★sTE', '').replace(
                '★pTX', '').replace('★pTY', '').replace(
                '★dTA', '☆［').replace('★dTC', '').replace(
                '★dTD', '］☆').replace('★dTE', '')
        newmsg = rgx_ptta_b.sub('', newmsg)
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txspccl(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■明細情報(CLベース)\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★sTS', '').replace('★sTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txabs(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■要約情報(CLベース)\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★sTS', '').replace('★sTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txfig(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■図面情報(CLベース)\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★sTS', '').replace('★sTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txref(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■符号情報\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txwd(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■Keyword\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★kTA', '☆［').replace('★kTB', '').replace(
                '★kTC', '').replace('★kTD', '］☆').replace(
                '★kTE', '').replace('★kTO', '☆［').replace(
                '★kTP', '').replace('★kTQ', '］☆').replace(
                '★kTR', '').replace('★kTX', '☆［').replace(
                '★kTY', '］☆').replace('★kTZ', '').replace(
                '★stTS', '☆［').replace('★stTE', '］☆').replace(
                '★stTC', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _txwdlist(fobj, txlines):
    global rgx_del
    global rgx_styledel
    fobj.write('\n■■重要語List\n')
    for newmsg in txlines:
        newmsg = newmsg.replace('★hTA', '☆［').replace(
                '★hTB', '］☆').replace('★hTC', '☆［').replace(
                '★tTE', '］☆').replace('★tTC', '').replace(
                '★zTA', '☆［').replace('★zTD', '］☆').replace(
                '★zTE', '→☆［').replace('★zTF', '］☆').replace(
                '★zTZ', '］☆').replace('★zTG', '☆［').replace(
                '★zTH', '］☆').replace('★jTS', '').replace('★jTE', '')
        newmsg = rgx_del.sub('', newmsg)
        newmsg = rgx_styledel.sub('', newmsg)
        fobj.write(''.join((newmsg, '\n')))


def _hxhd(fobj, strttl, zflg):
    fobj.write(
            '<!DOCTYPE html><html lang="ja">\n<head>\n'
            '  <meta charset="utf-8">\n'
            '  <meta http-equiv="Content-Style-Type" content="text/css">\n'
            '  <meta name="description" content="patent document '
            'information">\n'
            '  <meta name="author" content="K2UNIT">\n'
            '  <meta name="viewport" content="width=device-width, '
            'initial-scale=1">\n')
    fobj.write(''.join(('  <title>', strttl, '</title>\n')))
    if zflg:
        fobj.write(
                '  <link rel="stylesheet" '
                'href="../patelier-assets/patelier.css">\n'
                '  <link rel="preload" href="../patelier-assets/patelier.gif"'
                ' as="image">\n'
                '  <link rel="icon" href="../patelier-assets/patelier.ico">\n'
                '  <script src="../patelier-assets/patelier.js"></script>\n')
        strimgsrc = '<img src="../patelier-assets/patelier.png" '
    else:
        fobj.write(
                '  <link rel="stylesheet" '
                'href="./patelier-assets/patelier.css">\n'
                '  <link rel="preload" href="./patelier-assets/patelier.gif"'
                ' as="image">\n'
                '  <link rel="icon" href="./patelier-assets/patelier.ico">\n'
                '  <script src="./patelier-assets/patelier.js"></script>\n')
        strimgsrc = '<img src="./patelier-assets/patelier.png" '
    fobj.write(
            '  <script src="./patelierjs.js" async></script>\n'
            '</head>\n<body oncontextmenu="return false;">\n'
            '<header>\n')
    strheader = ''.join((
            '  <h1 onclick="chgColor()">', strimgsrc,
            'alt="logo" height="24">patelier<span id="ver">Ver ', __version__,
            '</span><span id="src">', strttl, '</span></h1>\n'))
    fobj.write(strheader)
    fobj.write('</header>\n')


def _hxnav(fobj, spcflg, spchdflg, wdlistflg):
    fobj.write(
            '<nav>\n  <ul>\n'
            '    <li><div id="navSrc" onclick="srcActivate()">'
            '原文表示</div></li>\n'
            '    <li><div id="navWarn" onclick="warnActivate()">'
            'Warning</div></li>\n'
            '    <li><div id="navCl" onclick="clActivate()">'
            'CL情報</div></li>\n'
            '    <li><div id="navClEl" onclick="clElActivate()">'
            'CL要素関連</div></li>\n'
            '    <li><div id="navTr" onclick="trActivate()">'
            'CL-Tree</div></li>\n')
    if spcflg:
        fobj.write(
                '    <li><div id="navSpc" onclick="spcActivate()">'
                '明細情報</div></li>\n')
    if spchdflg:
        fobj.write(
                '    <li><div id="navSpcHd" onclick="spcHdActivate()">'
                '明細俯瞰情報</div></li>\n')
    fobj.write(
            '    <li><div id="navSpcCl" onclick="spcClActivate()">'
            '明細情報(CL)</div></li>\n'
            '    <li><div id="navAbs" onclick="absActivate()">'
            '要約情報(CL)</div></li>\n'
            '    <li><div id="navFig" onclick="figActivate()">'
            '図面情報(CL)</div></li>\n'
            '    <li><div id="navRef" onclick="refActivate()">'
            '符号情報</div></li>\n'
            '    <li><div id="navWd" onclick="wdActivate()">'
            'Keyword</div></li>\n')
    if wdlistflg:
        fobj.write(
                '    <li><div id="navWdList" onclick="wdListActivate()">'
                '重要語List</div></li>\n')
    fobj.write('  </ul>\n</nav>\n')


def _hxnavlt(fobj):
    fobj.write(
            '<nav>\n  <ul>\n'
            '    <li><div id="navSrc" onclick="srcActivate()">'
            '原文表示</div></li>\n'
            '    <li><div id="navWarn" onclick="warnActivate()">'
            'Warning</div></li>\n'
            '  </ul>\n</nav>\n')


def _hxft(fobj):
    fobj.write('</body>\n</html>\n')


def _hxsrcart(fobj, txlines, ng_line_nums):
    global rgx_ctrl
    global rgx_hansp
    fobj.write(
            '<article id="artSrc" class="inact">\n'
            '<section id="sctSrc" class="bright">\n')
    linenum = 1
    for eatx in txlines:
        newtx = eatx.rstrip()
        newtx = rgx_ctrl.sub('▲', newtx)
        msg = ''.join((xml.sax.saxutils.escape(newtx), '<br>'))
        newmsg = rgx_hansp.sub('&nbsp;', msg)
        newmsg = newmsg.replace('★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>').replace(
                '★［≪', '<').replace('≫］★', '>')
        if linenum in ng_line_nums:
            newmsg = ''.join((
                    '<span id="l', str(linenum), '" class="warnline">',
                    str(linenum), r'</span>:', newmsg))
        else:
            newmsg = ''.join((
                    '<span id="l', str(linenum), '" class="l">',
                    str(linenum), '</span>:', newmsg))
        fobj.write(newmsg)
        linenum += 1
    fobj.write('</section>\n</article>\n')


def _hxwarnart(fobj, txlines, flg):
    global rgx_hansp
    fobj.write(
            '<article id="artWarn" class="inact">\n'
            '<section id="sctWarn" class="bright">\n')
    rgx_ctta_b = regex.compile('★ctTA[^★]+★ctTB')
    rgx_cttc = regex.compile('★ctTC')
    rgx_ptta_b = regex.compile('★ptTA[^★]+★ptTB')
    rgx_pttc = regex.compile('★ptTC')
    for eatx in txlines:
        msg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = rgx_hansp.sub('&nbsp;', msg)
        newmsg = newmsg.replace('★eTS', '<span class="err">').replace(
                '★wTS', r'<span class="warn">').replace('★wTE', '</span>')
        if flg:
            newmsg = newmsg.replace(
                    '★ltTA', """<span class="llink" onclick="src('"""
                    ).replace('★ltTB', r"""')">""").replace(
                    '★ltTC', '</span>').replace(
                    '★ptTA', """<span class="plink" onclick="spc('"""
                    ).replace('★ptTB', """')">""").replace(
                    '★ptTC', '</span>').replace(
                    '★ctTA', """<span class="clink" onclick="cl('"""
                    ).replace('★ctTB', r"""')">""").replace(
                    '★ctTC', '</span>')
        else:
            newmsg = newmsg.replace(
                    '★ltTA', r"""<span class="llink" onclick="src('"""
                    ).replace('★ltTB', r"""')">""").replace(
                    '★ltTC', '</span>')
            newmsg = rgx_ptta_b.sub(
                    '<span class="pa">', newmsg)
            newmsg = rgx_pttc.sub(
                    '</span>', newmsg)
            newmsg = rgx_ctta_b.sub(
                    '<span class="cl">',
                    newmsg)
            newmsg = rgx_cttc.sub('</span>', newmsg)
            newmsg = newmsg.replace('★clTS', '<span class="cl">').replace(
                    '★clTE', '</span>')
        newmsg = newmsg.replace('★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxclart(fobj):
    fobj.write(
            '<article id="artCl" class="inact">\n'
            '<section id="sctCl" class="bright">\n'
            '</section>\n</article>\n')


def _hxclelart(fobj, txlines):
    global rgx_del
    fobj.write(
            '<article id="artClEl" class="inact">\n'
            '<section id="sctClEl" class="bright">\n')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', r"""<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace(
                '★dTA', '<span class="').replace(
                '★dTC',
                '''" onmouseover='tip(this)' onclick='wd("''').replace(
                '★dTD', '''")'>''').replace('★dTE', '</span>').replace(
                '★ssTS', '<span class="clgroup">').replace(
                '★ssTE', '</span>').replace('★tTC<br>', '</div>').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        newmsg = rgx_del.sub('', newmsg)
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxtrart(fobj, txlines1, txlines2):
    fobj.write(
            '<article id="artTr" class="inact">\n'
            '<section id="sctTr" class="bright">\n')
    txlines1.extend(txlines2)
    for eatx in txlines1:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace(
                '★ctTA', """<span class="clink" onclick="cl('""").replace(
                '★ctTB', """')">""").replace('★ctTC', '</span>').replace(
                '★cmTS', '<span class="cmt">').replace(
                '★cmTE', '</span>').replace('★tTC<br>', '</div>').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxspcart(fobj):
    fobj.write(
            '<article id="artSpc" class="inact">\n'
            '<section id="sctSpc" class="bright">\n'
            '</section>\n</article>\n')


def _hxspchdart(fobj, txlines):
    fobj.write(
            '<article id="artSpcHd" class="inact">\n'
            '<section id="sctSpcHd" class="bright">\n')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace(
                '★sTS', '<span class="mark">').replace(
                '★sTE', '</span>').replace(
                '★pTX', '<span class="pa">').replace(
                '★pTY', '</span>').replace(
                '★ptTA', """<span class="plink" onclick="spc('""").replace(
                '★ptTB', """')">""").replace(
                '★dTA', '<span class="').replace(
                '★dTC',
                '''" onmouseover='tip(this)' onclick='wd("''').replace(
                '★dTD', '''")'>''').replace('★dTE', '</span>').replace(
                '★tTC<br>', '</div>').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxspcclart(fobj, txlines):
    fobj.write(
            '<article id="artSpcCl" class="inact">\n'
            '<section id="sctSpcCl" class="bright">\n')
    rgx_exp = regex.compile('(■{[^}]*})')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace(
                '★sTS', '<span class="mark">').replace(
                '★sTE', '</span>').replace('★tTC<br>', '</div>')
        newmsg = rgx_exp.sub(r'<span class="description">\1</span>', newmsg)
        newmsg = newmsg.replace('★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxabsart(fobj, txlines):
    fobj.write(
            '<article id="artAbs" class="inact">\n'
            '<section id="sctAbs" class="bright">\n')
    rgx_exp = regex.compile('(■{[^}]*})')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace(
                '★sTS', '<span class="mark">').replace(
                r'★sTE', '</span>').replace('★tTC<br>', '</div>')
        newmsg = rgx_exp.sub(r'<span class="description">\1</span>', newmsg)
        newmsg = newmsg.replace('★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxfigart(fobj, txlines):
    global cl_svgdic
    global rgx_styledel
    cl_svgdic = {}
    fobj.write(
            '<article id="artFig" class="inact">\n'
            '<section id="sctFig" class="bright">\n')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace(
                '★sTS', '<span class="mark">').replace(
                '★sTE', '</span>').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>').replace(
                '★tTC<br>', '</div>')
        fobj.write(newmsg)
    htmlmsg = ''.join((
            """<h1 class="list-switch" onclick="listSwitchP('""",
            """svgfigList')">""",
            '■図面情報(CLベース/picture)</h1>',
            '<div id="prnsvgfigList" class="inactprn">'
            '<span class="prn" onclick="figPrn()">'
            'print picture</span></div>'
            '<div class="inactlist" id="svgfigList">',
            '<span class="mark">【書類名】</span>'
            '<span class="fig-title">図面</span>'))
    fobj.write(htmlmsg)
    rgx_fig = regex.compile('★sTS【図(?P<fig_num>[１-９][０-９]*)】★sTE')
    rgx_figel = regex.compile(
            '^　(?P<indent>　*)(?P<element>[^　]+)(　+)(?P<ref>[^　]+)$')
    indent = 0
    figelcnt = 0
    prevfigno = '0'
    figno = '0'
    figeldic = {}
    for ealine in txlines:
        ealine = rgx_styledel.sub('', ealine)
        res = rgx_fig.search(ealine)
        if res:
            figno = res.group('fig_num')
            if '0' != prevfigno and prevfigno != figno:
                if 0 < indent:
                    for i in reversed(range(indent)):
                        figeldic[(prevfigno, figelcnt, i)] = ['', '', 0, 1]
                        figelcnt += 1
            prevfigno = figno
            figelcnt = 0
            prev_indent = 0
            continue
        if '★' not in ealine:
            res = rgx_figel.search(ealine)
            if res:
                indent = len(res.group('indent'))
                if prev_indent > indent:
                    for i in reversed(range(indent, prev_indent)):
                        figeldic[(figno, figelcnt, i)] = ['', '', 0, 1]
                        figelcnt += 1
                prev_indent = indent
                element = res.group('element')
                lenel = len(element)
                ref = res.group('ref')
                figeldic[(figno, figelcnt, indent)] = [
                        element, ref, lenel + 2, 1]
                figelcnt += 1
    if 0 < indent:
        for i in reversed(range(indent)):
            figeldic[(figno, figelcnt, i)] = ['', '', 0, 1]
            figelcnt += 1
    prevfigno = '0'
    figsizedic = {}
    figorder = 0
    svgbeginflg = True
    figwmax = 0
    fighmax = 0
    fignorefwmax = 0
    for (figno, figelcnt, indent) in natsorted(figeldic.keys()):
        if '0' != prevfigno and prevfigno != figno:
            if fighmax > 0:
                if figno not in figsizedic.keys():
                    figsizedic[prevfigno] = [
                            figorder, figwmax, fighmax, fignorefwmax]
                    figorder += 1
            figwmax = 0
            fighmax = 0
            fignorefwmax = 0
        prevfigno = figno
        maxw = figeldic[(figno, figelcnt, indent)][2]
        prev_figelcnt2 = figelcnt
        dh = 0
        for (figno2, figelcnt2, indent2) in natsorted([
                (p1, p2, p3) for (p1, p2, p3) in figeldic.keys() if
                p1 == figno and p2 > figelcnt and p3 > indent]):
            if figelcnt2 == (prev_figelcnt2 + 1):
                prev_figelcnt2 = figelcnt2
                w = figeldic[(figno2, figelcnt2, indent2)][2]
                w += (indent2 - indent) * 2
                if w > maxw:
                    maxw = w
                dh += 1
            else:
                break
        figeldic[(figno, figelcnt, indent)][2] = maxw
        if dh:
            figeldic[(figno, figelcnt, indent)][3] += dh + 1
        tmpfigwmax = maxw + len(figeldic[(figno, figelcnt, indent)][1])
        if tmpfigwmax > figwmax:
            figwmax = tmpfigwmax
        if maxw > fignorefwmax:
            fignorefwmax = maxw
        fighmax += 1
    if fighmax > 0:
        if figno not in figsizedic.keys():
            figsizedic[figno] = [figorder, figwmax, fighmax, fignorefwmax]
            figorder += 1
    tmargin = 200
    lmargin = 200
    refinterval = 100
    rmargin = 50
    wscale = 50
    hscale = 100
    linemargin = 40
    svgfigdic = {}
    svgbeginflg = True
    for figno, figval in sorted(figsizedic.items(), key=lambda x: x[1][0]):
        figwarn = ''
        widthunit = figval[1]
        width = lmargin + widthunit * wscale + rmargin
        heightunit = figval[2]
        height = tmargin + heightunit * hscale
        norefwidthunit = figval[3]
        norefwidth = lmargin + norefwidthunit * wscale
        if height > 2550:
            if width > 1700:
                figwarn = ''.join((
                        '※図面が不適切かもしれません'
                        '（縦255mm/横170mm基準超過）'))
            else:
                width = 1700
                figwarn = ''.join((
                        '※図面が不適切かもしれません'
                        '（縦255mm基準超過）'))
        else:
            if width > 1700:
                figwarn = ''.join((
                        '※図面が不適切かもしれません'
                        '（※横170mm基準超過）'))
            else:
                width = 1700
        if width > 2100:
            wsvg = width
        else:
            wsvg = 2100
        hsvg = height
        tpos = 0
        svgfigdic[figval[0]] = [
                figno, figwarn, width, height, norefwidth, svgbeginflg,
                wsvg, hsvg, tpos]
    for figorder in sorted(svgfigdic.keys()):
        if svgfigdic[figorder][5]:
            totalh = svgfigdic[figorder][3]
            tpos = svgfigdic[figorder][8]
            figorder_n = figorder
            while 2770 > totalh:
                figorder_n += 1
                if figorder_n in svgfigdic.keys():
                    tpos = totalh
                    height = svgfigdic[figorder_n][3]
                    totalh += height
                    if 2770 > totalh:
                        wsvg = svgfigdic[figorder_n][6]
                        if svgfigdic[figorder][6] > wsvg:
                            break
                        svgfigdic[figorder_n][5] = False
                        svgfigdic[figorder_n][8] = tpos
                        svgfigdic[figorder][7] = totalh
                    else:
                        break
                else:
                    break
    pageno = 0
    outputfigorder = set()
    for figorder in svgfigdic.keys():
        figno = svgfigdic[figorder][0]
        figwarn = svgfigdic[figorder][1]
        width = svgfigdic[figorder][2]
        height = svgfigdic[figorder][3]
        norefwidth = svgfigdic[figorder][4]
        tpos = svgfigdic[figorder][8]
        if svgfigdic[figorder][5]:
            pageno += 1
            wsvg = svgfigdic[figorder][6]
            hsvg = svgfigdic[figorder][7]
            tmpsvg = ''.join((
                    '<svg class="fig" version="1.1" viewBox="0 0 ',
                    str(wsvg), ' ', str(hsvg),
                    '" xmlns="http://www.w3.org/2000/svg">'
                    '<text font-size="40" text-anchor="start" fill="#000"'
                    ' dominant-baseline="middle" x="0" y="100">【図',
                    figno, '】', figwarn, '</text>'))
            if outputfigorder:
                svgend = '</svg>'
            else:
                svgend = ''
            htmlmsg = ''.join((svgend, tmpsvg))
            fobj.write(htmlmsg)
            cl_svgdic[pageno] = tmpsvg
        else:
            tmpsvg = ''.join((
                    '<text font-size="40" text-anchor="start" '
                    'fill="#000" dominant-baseline="middle" x="0" y="',
                    str(tpos + tmargin - 100), '">【図',
                    figno, '】', figwarn, '</text>'))
            htmlmsg = tmpsvg
            fobj.write(htmlmsg)
            cl_svgdic[pageno] = ''.join((cl_svgdic[pageno], tmpsvg))
        mthdflg = False
        outputfigorder.add(figorder)
        for (fig_n, figelcnt, indent) in natsorted([
                (p1, p2, p3) for (p1, p2, p3) in figeldic.keys()
                if p1 == figno]):
            element = figeldic[(figno, figelcnt, indent)][0]
            if mthdflg:
                if 0 == indent:
                    if not element:
                        element = '終了'
            if element:
                ref = figeldic[(figno, figelcnt, indent)][1]
                if not mthdflg:
                    if 0 == indent:
                        if ref:
                            if _hanref(ref).upper().startswith('S'):
                                mthdflg = True
                if mthdflg:
                    elposx = lmargin + int((norefwidth - lmargin) / 2)
                    tmpelposx = 1050 + int(lmargin / 2)
                    if tmpelposx < elposx:
                        elposx = tmpelposx
                    posy = tpos + tmargin + figelcnt * hscale
                    rectposy = posy - linemargin
                    if 0 == indent:
                        hunit = 1
                    else:
                        hunit = figeldic[(figno, figelcnt, indent)][3]
                    recth = (hunit - 1) * hscale + linemargin * 2
                    if 0 == indent:
                        wunit = len(element) + 2
                    else:
                        wunit = figeldic[(figno, figelcnt, indent)][2]
                    rectw = (wunit - 2) * wscale + linemargin * 2
                    rectposx = elposx - int(rectw / 2)
                    if 0 == indent:
                        rounded = ''.join(('" rx="', str(linemargin)))
                    else:
                        rounded = ''
                    if 0 == figelcnt or 1 < indent:
                        vline = ''
                    else:
                        vline = ''.join((
                                '<line x1="', str(elposx), '" y1="',
                                str(posy - hscale + linemargin), '" x2="',
                                str(elposx), '" y2="', str(posy - linemargin),
                                '" stroke-width="4"/>'))
                    if ref:
                        lenref = len(ref)
                        refposx = width - lenref * wscale - rmargin
                        tmprefposx = norefwidth + refinterval
                        if tmprefposx < refposx:
                            refposx = tmprefposx
                        jx1 = rectposx + rectw
                        jx3 = refposx
                        jx2 = int((jx1 + jx3) / 2)
                        jxq = int((jx1 + jx2) / 2)
                        jyq = posy - linemargin
                        tmpsvg = ''.join((
                                '<g font-size="50" fill="#000" '
                                'dominant-baseline="middle">'
                                '<text text-anchor="middle" x="', str(elposx),
                                '" y="', str(posy), '">', element,
                                '</text><text text-anchor="start" x="',
                                str(refposx), '" y="', str(posy), '">', ref,
                                '</text></g>'
                                '<g fill="transparent" fill-opacity="0" '
                                'stroke="#000"><rect x="', str(rectposx),
                                '" y="', str(rectposy), '" width="',
                                str(rectw), '" height="', str(recth), rounded,
                                '" stroke-width="4"/>', vline,
                                '<path d="M ', str(jx1), ' ', str(posy),
                                ' Q ', str(jxq), ' ', str(jyq), ', ',
                                str(jx2), ' ', str(posy), ' T ', str(jx3),
                                ' ', str(posy), '" stroke-width="2"/></g>'))
                    else:
                        tmpsvg = ''.join((
                                '<g font-size="50" text-anchor="middle" '
                                'fill="#000" dominant-baseline="middle">'
                                '<text x="', str(elposx), '" y="', str(posy),
                                '">', element, '</text></g>'
                                '<g fill="transparent" fill-opacity="0" '
                                'stroke="#000"><rect x="', str(rectposx),
                                '" y="', str(rectposy), '" width="',
                                str(rectw), '" height="', str(recth), rounded,
                                '" stroke-width="4"/>', vline, '</g>'))
                else:
                    elposx = lmargin + indent * wscale
                    posy = tpos + tmargin + figelcnt * hscale
                    rectposx = elposx - linemargin
                    rectposy = posy - linemargin
                    wunit = figeldic[(figno, figelcnt, indent)][2]
                    rectw = (wunit - 2) * wscale + linemargin * 2
                    hunit = figeldic[(figno, figelcnt, indent)][3]
                    recth = (hunit - 1) * hscale + linemargin * 2
                    if ref:
                        lenref = len(ref)
                        refposx = width - lenref * wscale - rmargin
                        tmprefposx = norefwidth + refinterval
                        if tmprefposx < refposx:
                            refposx = tmprefposx
                        jx1 = rectposx + rectw
                        jx3 = refposx
                        jx2 = int((jx1 + jx3) / 2)
                        jxq = int((jx1 + jx2) / 2)
                        jyq = posy - linemargin
                        tmpsvg = ''.join((
                                '<g font-size="50" text-anchor="start" '
                                'fill="#000" dominant-baseline="middle">'
                                '<text x="', str(elposx), '" y="', str(posy),
                                '">', element, '</text><text x="',
                                str(refposx), '" y="', str(posy), '">', ref,
                                '</text></g>'
                                '<g fill="transparent" fill-opacity="0" '
                                'stroke="#000"><rect x="', str(rectposx),
                                '" y="', str(rectposy), '" width="',
                                str(rectw), '" height="', str(recth),
                                '" stroke-width="4"/><path d="M ',
                                str(jx1), ' ', str(posy), ' Q ', str(jxq),
                                ' ', str(jyq), ', ', str(jx2), ' ', str(posy),
                                ' T ', str(jx3), ' ',
                                str(posy), '" stroke-width="2"/></g>'))
                    else:
                        tmpsvg = ''.join((
                                '<g font-size="50" text-anchor="start" '
                                'fill="#000" dominant-baseline="middle">'
                                '<text x="', str(elposx), '" y="', str(posy),
                                '">', element, '</text></g>'
                                '<g fill="transparent" fill-opacity="0" '
                                'stroke="#000"><rect x="', str(rectposx),
                                '" y="', str(rectposy), '" width="',
                                str(rectw), '" height="', str(recth),
                                '" stroke-width="4"/></g>'))
                htmlmsg = tmpsvg
                fobj.write(htmlmsg)
                cl_svgdic[pageno] = ''.join((cl_svgdic[pageno], tmpsvg))
    fobj.write('</svg></div></section></article>')


def _hxrefart(fobj, txlines):
    fobj.write(
            '<article id="artRef" class="inact">\n'
            '<section id="sctRef" class="bright">\n')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace('★tTC<br>', '</div>').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxwdart(fobj, txlines):
    fobj.write(
            '<article id="artWd" class="inact">\n'
            '<section id="sctWd" class="bright">\n')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace('★kTA', '<span id="').replace(
                '★kTB', '" class="').replace(
                '★kTC', """ r"  onclick="wdListSwitchP('""").replace(
                '★kTD', """')">""").replace('★kTE', '</span>').replace(
                '★kTO', '<span  class="').replace(
                '★kTP', """ r"  onclick="wdListSwitchP('""").replace(
                '★kTQ', """')">""").replace('★kTR', '</span>').replace(
                '★kTX', '<span class="').replace('★kTY', ' f">').replace(
                '★kTZ', '</span>').replace(
                '★stTS', '''<div class="inactlist" id="''').replace(
                '★stTE', '">').replace('★stTC', '</div>').replace(
                '★tTC<br>', '</div>').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _hxwdlistart(fobj, txlines):
    fobj.write(
            '<article id="artWdList" class="inact">\n'
            '<section id="sctWdList" class="bright">\n')
    for eatx in txlines:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★hTA', """<h1 class="list-switch" onclick="listSwitch('"""
                ).replace('★hTB', """')">""").replace(
                '★hTC', """</h1><div id='cpyF""").replace(
                '★hTD', """' class="inactcpy"><span class="cpy" """
                """onclick="listCpy(this)">copy plain text"""
                '</span></div>').replace(
                '★tTS', '<div class="inactlist" id="').replace(
                '★tTE<br>', '">').replace(
                '★jTS', '<span class="imp-wd">').replace(
                '★jTE', '</span>').replace('★zTA', '<span id="').replace(
                '★zTB', '" class="').replace(
                '★zTC', """ b r" onclick="wdListListSwitch('L""").replace(
                '★zTD', """')">""").replace(
                '★zTE', '</span>→<span id="E').replace(
                '★zTF', '">').replace('★zTZ', '" class="p">').replace(
                '★zTG',
                """</span><div class="inactlist" id="L""").replace(
                '★zTH', '"></div>').replace(
                '★zTX', '"'
                """ class="w y r" onclick="wdListListSwitch('L""").replace(
                '★tTC<br>', '</div>')
        fobj.write(newmsg)
    fobj.write('</section>\n</article>\n')


def _pjswt(fobj, dataset1, dataset2, dataset3):
    arrayset = ','.join(dataset1)
    strarray = ''.join(('const A_ARRAY = {', arrayset, '};\n'))
    fobj.write(strarray)
    arrayset = ','.join(dataset2)
    strarray = ''.join(('const ARRAY_TIP = {', arrayset, '};\n'))
    fobj.write(strarray)
    arrayset = ','.join(dataset3)
    strarray = ''.join(('const ARRAY_EF = {', arrayset, '};\n'))
    fobj.write(strarray)
    fobj.write(
            'function wdListSwitchP(listId){\n'
            '  let wdId = listId.split("Z")[1];\n'
            '  let linkLines = A_ARRAY[wdId];\n'
            '  wdListSwitch(listId, linkLines);\n}\n')


def _pjsclwt(fobj, txlines1, txlines2, noefcl, efname):
    global HD_CMTBLK
    global rgx_styledel
    rgx_spansps = regex.compile('(<span[^>]*>)[ 　]+')
    fobj.write(
            'const INNER_SC_CL = `<h1 class="list-switch" '
            """onclick="listSwitch('clJpList')">"""
            '■CL情報</h1><div id="cpyFclJpList" '
            'class="inactcpy"><span class="cpy" '
            """onclick="listCpy(this)">copy plain text</span></div>"""
            '<div class="inactlist" id="clJpList"></div>')
    if txlines2:
        fobj.write(
                '<h1 class="list-switch" '
                """onclick="listSwitchE('clJEList')">""")
        if noefcl:
            fobj.write('■CL情報(英語Mix)</h1>')
        else:
            fobj.write(''.join(('■CL情報(英語:', efname, ')</h1>')))
        fobj.write(
                '<div id="cpyFclJEList" '
                'class="inactcpy"><span class="cpy" '
                """onclick="listCpy(this)">copy plain text</span></div>"""
                '<div class="inactlist" id="clJEList"></div>')
    fobj.write('`;\nconst INNER_CL_JPLIST = `')
    for eatx in txlines1:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★lTA', '<span id="').replace(
                '★lTB', '" title="').replace(
                '★lTC', '">').replace(
                '★lTD<br>', '<br></span>').replace(
                '★sTS', '<span class="mark">').replace(
                '★esTS', '<span class="emark">').replace(
                '★sTE', '</span>').replace(
                '★cTA', '<span id="').replace(
                '★cTB', '" class="cl">').replace(
                '★cTC', '</span>').replace(
                '★cTX', '<span class="cl">').replace(
                '★ecTX', '<span class="ecl">').replace(
                '★cTY', '</span>').replace(
                '★cmTS', '<span class="cmt">').replace(
                '★cmTE', '</span>').replace(
                '★rTS', '<span class="refwd">').replace(
                '★rTE', '</span>').replace(
                '★rcTS', '<span class="refcl">').replace(
                '★rcTE', '</span>').replace(
                '★dTA', '<span class="').replace(
                '★dTC',
                '''" onmouseover='tip(this)' onclick='wd("''').replace(
                '★dTD', '''")'>''').replace(
                '★dTE', '</span>').replace('`', r'\`').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('`;\n')
    if txlines2:
        if not noefcl:
            cmtblk = ''.join(('★lTC★cmTS', HD_CMTBLK))
            txlines1 = [x for x in txlines1 if not (cmtblk in x)]
        fobj.write('const INNER_CL_JELIST = `')
        rgx_lta_b = regex.compile('★lTA[^★]+★lTB')
        idx = 0
        idxnum = len(txlines1)
        idx2 = 0
        idx2num = len(txlines2)
        rgx_eclstart = regex.compile(
                r'(^[1-9][0-9]*\.[ \u00a0]|\[Claim[ \u00a0][1-9][0-9]*\])')
        rgx_eclstartsb1 = regex.compile(
                r'(\[Claim([\u00a0]|&nbsp;)[1-9][0-9]*\])')
        rgx_eclstartsb2 = regex.compile(r'>([1-9][0-9]*\.([\u00a0]|&nbsp;))')
        clsync = False
        if not noefcl:
            for etx in txlines2:
                etx = rgx_styledel.sub('', etx)
                if rgx_eclstart.search(etx):
                    clsync = True
                    break
        eclstart = False
        clstart = False
        clwt = False
        while (idx < idxnum) or (idx2 < idx2num):
            if idx < idxnum:
                if not clstart:
                    eatx = txlines1[idx]
                    if clsync:
                        if '★cTB' in eatx:
                            clstart = True
                        else:
                            clstart = False
                    newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
                    newmsg = rgx_lta_b.sub('★lTAB', newmsg)
                    newmsg = newmsg.replace(
                            '★lTAB', '<span class="j" title="').replace(
                            '★lTC', '">').replace(
                            '★lTD<br>', '<br></span>').replace(
                            '★sTS', '<span class="mark">').replace(
                            '★esTS', '<span class="emark">').replace(
                            '★sTE', '</span>').replace(
                            '★cTA', '<span id="').replace(
                            '★cTB', '" class="cl">').replace(
                            '★cTC', '</span>').replace(
                            '★cTX', '<span class="cl">').replace(
                            '★ecTX', '<span class="ecl">').replace(
                            '★cTY', '</span>').replace(
                            '★cmTS', '<span class="cmt">').replace(
                            '★cmTE', '</span>').replace(
                            '★rTS', '<span class="refwd">').replace(
                            '★rTE', '</span>').replace(
                            '★rcTS', '<span class="refcl">').replace(
                            '★rcTE', '</span>').replace(
                            '★dTA', '<span class="').replace(
                            '★dTC',
                            '''" onmouseover='tip(this)' onclick='wd("'''
                            ).replace(
                            '★dTD', '''")'>''').replace(
                            '★dTE', '</span>').replace('`', r'\`').replace(
                            '★［＜sub＞］★', '<span><sub>').replace(
                            '★［＜/sub＞］★', '</sub></span>').replace(
                            '★［＜sup＞］★', '<span><sup>').replace(
                            '★［＜/sup＞］★', '</sup></span>')
                    if clstart:
                        if idx2 < idx2num:
                            etx = rgx_styledel.sub('', txlines2[idx2])
                            if rgx_eclstart.search(etx):
                                fobj.write(newmsg)
                                idx += 1
                                clstart = False
                                clwt = True
                            else:
                                fobj.write('<span class="j"><br></span>')
                        else:
                            fobj.write(newmsg)
                            idx += 1
                            clstart = False
                            clwt = True
                    else:
                        fobj.write(newmsg)
                        idx += 1
                else:
                    if idx2 < idx2num:
                        etx = rgx_styledel.sub('', txlines2[idx2])
                        if rgx_eclstart.search(etx):
                            fobj.write(newmsg)
                            idx += 1
                            clstart = False
                            clwt = True
                        else:
                            fobj.write('<span class="j"><br></span>')
                    else:
                        fobj.write(newmsg)
                        idx += 1
                        clstart = False
                        clwt = True
            else:
                fobj.write('<span class="j"><br></span>')
            if idx2 < idx2num:
                if not eclstart:
                    eatx2 = txlines2[idx2]
                    if clsync:
                        etx = rgx_styledel.sub('', eatx2)
                        if rgx_eclstart.search(etx):
                            eclstart = True
                        else:
                            eclstart = False
                    newmsg2 = ''.join((
                            xml.sax.saxutils.escape(eatx2), '<br>'))
                    newmsg2 = newmsg2.replace('`', r'\`')
                    if noefcl:
                        newmsg2 = newmsg2.replace(
                                '★lTAC', '<span class="e">').replace(
                                '★lTD<br>', '<br></span><hr>').replace(
                                '★sTS', '<span class="mark">').replace(
                                '★esTS', '<span class="emark">').replace(
                                '★sTE', '</span>').replace(
                                '★cTA', '<span id="').replace(
                                '★cTB', '" class="cl">').replace(
                                '★cTC', '</span>').replace(
                                '★cTX', '<span class="cl">').replace(
                                '★ecTX', '<span class="ecl">').replace(
                                '★cTY', '</span>').replace(
                                '★cmTS', '<span class="cmt">').replace(
                                '★cmTE', '</span>').replace(
                                '★rTS', '<span class="refwd">').replace(
                                '★rTE', '</span>').replace(
                                '★rcTS', '<span class="refcl">').replace(
                                '★rcTE', '</span>').replace(
                                '★dTA', '<span class="').replace(
                                '★dTC',
                                '''" onmouseover='tip(this)' '''
                                '''onclick='wd("''').replace(
                                '★dTD', '''")'>''').replace(
                                '★dTY', '">').replace(
                                '★dTE', '</span>')
                        newmsg2 = rgx_spansps.sub(
                                r'\1&nbsp;&nbsp;&nbsp;&nbsp;', newmsg2)
                    else:
                        newmsg2 = newmsg2.replace(' ', '&nbsp;')
                        newmsg2 = newmsg2.replace(
                                '★［≪', '<').replace('≫］★', '>')
                        newmsg2 = ''.join((
                                '<span class="e">', newmsg2, '</span><hr>'))
                    newmsg2 = newmsg2.replace(
                            '★［＜sub＞］★', '<span><sub>').replace(
                            '★［＜/sub＞］★', '</sub></span>').replace(
                            '★［＜sup＞］★', '<span><sup>').replace(
                            '★［＜/sup＞］★', '</sup></span>')
                    if eclstart:
                        if rgx_eclstartsb1.search(newmsg2):
                            newmsg2 = rgx_eclstartsb1.sub(
                                    r'<span class="ecl">\1</span>', newmsg2)
                        else:
                            newmsg2 = rgx_eclstartsb2.sub(
                                r'><span class="ecl">\1</span>', newmsg2)
                        if idx < idxnum:
                            if clwt:
                                fobj.write(newmsg2)
                                idx2 += 1
                                eclstart = False
                                clwt = False
                            else:
                                fobj.write(
                                        '<span class="e dm"><br></span><hr>')
                        else:
                            fobj.write(newmsg2)
                            idx2 += 1
                            eclstart = False
                            clwt = False
                    else:
                        fobj.write(newmsg2)
                        idx2 += 1
                else:
                    if idx < idxnum:
                        if clwt:
                            fobj.write(newmsg2)
                            idx2 += 1
                            eclstart = False
                            clwt = False
                        else:
                            fobj.write('<span class="e dm"><br></span><hr>')
                    else:
                        fobj.write(newmsg2)
                        idx2 += 1
                        eclstart = False
                        clwt = False
            else:
                fobj.write('<span class="e dm"><br></span><hr>')
        fobj.write('`;\n')
    fobj.write(
            'function setSectionCl(){\n'
            '  let scClList;\n  let scCl;\n'
            '  scCl = document.getElementById("sctCl");\n'
            '  if (scCl){\n    scCl.insertAdjacentHTML'
            '("beforeend", INNER_SC_CL);\n  }\n'
            '  scClList = document.getElementById("clJpList");\n'
            '  if (scClList){\n    scClList.insertAdjacentHTML'
            '("beforeend", INNER_CL_JPLIST);\n  }\n')
    if txlines2:
        fobj.write(
            '  scClList = document.getElementById("clJEList");\n'
            '  if (scClList){\n    scClList.insertAdjacentHTML'
            '("beforeend", INNER_CL_JELIST);\n  }\n')
    fobj.write('}\nwindow.addEventListener("load", setSectionCl, false);\n')


def _pjsspcwt(fobj, txlines1, txlines2, noefspc, efname):
    global rgx_styledel
    global cl_strdic
    global rf_allset
    hanrefs = [_hanref(x) for x in rf_allset]
    rgx_hanref = regex.compile(''.join((
            r'([ \-\u00a0])(',
            '|'.join((hanrefs)), r')(?=[ \.,:;\-\u00a0])')))
    rgx_spansps = regex.compile('(<span[^>]*>)[ 　]+')
    fobj.write('let a_array_cl_abbr = {};')
    clstrset = set()
    for clno in cl_strdic.keys():
        clstrline = cl_strdic[clno]
        clstrline = clstrline.replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        clstrset.add(''.join(("CL", str(clno), ":'", clstrline, "'")))
    strarraycl = ''.join((
            'const ARRAY_CL = {', ','.join((clstrset)), '};\n'))
    fobj.write(strarraycl)
    fobj.write('const INNER_SPC_JPLIST = `')
    for eatx in txlines1:
        newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
        newmsg = newmsg.replace(
                '★sTS', '<span class="mark">').replace(
                '★sTE', '</span>').replace(
                '★esTS', '<span class="emark">').replace(
                '★epTX', '<span class="epa">').replace(
                '★dTA', '<span class="').replace(
                '★dTC',
                '''" onmouseover='tip(this)' onclick='wd("''').replace(
                '★dTD', '''")'>''').replace(
                '★dTE', '</span>').replace('`', r'\`').replace(
                '★lTA', '<span id="').replace(
                '★lTB', '" title="').replace('★lTC', '">').replace(
                '★lTD<br>', '<br></span>').replace(
                '★pTA', '<span id="').replace(
                '★pTB', '" class="pa">').replace(
                '★pTC', '</span>').replace(
                '★pTX', '<span class="pa">').replace(
                '★pTY', '</span>').replace(
                '★qA',
                """<span class="clabbr" onclick='transformCl()' title='CL"""
                ).replace(
                '★qB', """'">""").replace('★qC', '</span>').replace(
                '★［＜sub＞］★', '<span><sub>').replace(
                '★［＜/sub＞］★', '</sub></span>').replace(
                '★［＜sup＞］★', '<span><sup>').replace(
                '★［＜/sup＞］★', '</sup></span>')
        fobj.write(newmsg)
    fobj.write('`;\n')
    if txlines2:
        rgx_lta_b = regex.compile('★lTA[^★]+★lTB')
        fobj.write('const INNER_SPC_JELIST = `')
        idx = 0
        idxnum = len(txlines1)
        idx2 = 0
        idx2num = len(txlines2)
        rgx_eparastart = regex.compile(r'\[[0-9]{4}[0-9]?\]$')
        rgx_eparastartsb = regex.compile(r'(\[[0-9]{4}[0-9]?\])')
        parasync = False
        if not noefspc:
            tmp_parasync = False
            for text in txlines1:
                if ('★pTB' in text) or ('★pTX' in text):
                    tmp_parasync = True
                    break
            if tmp_parasync:
                for etx in txlines2:
                    etx = rgx_styledel.sub('', etx)
                    if rgx_eparastart.search(etx.rstrip()):
                        parasync = True
                        break
        eparastart = False
        parastart = False
        parawt = False
        while (idx < idxnum) or (idx2 < idx2num):
            if idx < idxnum:
                if not parastart:
                    eatx = txlines1[idx]
                    if parasync:
                        if ('★pTB' in eatx) or ('★pTX' in eatx):
                            parastart = True
                        else:
                            parastart = False
                    newmsg = ''.join((xml.sax.saxutils.escape(eatx), '<br>'))
                    newmsg = rgx_lta_b.sub('★lTAB', newmsg)
                    newmsg = newmsg.replace(
                            '★lTAB', '<span class="j" title="').replace(
                            '★lTC', '">').replace(
                            '★lTD<br>', '<br></span>').replace(
                            '★sTS', '<span class="mark">').replace(
                            '★sTE', '</span>').replace(
                            '★esTS', '<span class="emark">').replace(
                            '★pTA', '<span id="').replace(
                            '★pTB', '" class="pa">').replace(
                            '★pTC', '</span>').replace(
                            '★pTX', '<span class="pa">').replace(
                            '★pTY', '</span>').replace(
                            '★epTX', '<span class="epa">').replace(
                            '★dTA', '<span class="').replace(
                            '★dTC',
                            '''" onmouseover='tip(this)' onclick='wd("'''
                            ).replace(
                            '★dTD', '''")'>''').replace(
                            '★dTE', '</span>').replace(
                            '★qA',
                            """<span class="clink" onclick="cl('cl"""
                            ).replace(
                            '★qB', """')">""").replace(
                            '★qC', '</span>').replace('`', r'\`').replace(
                            '★［＜sub＞］★', '<span><sub>').replace(
                            '★［＜/sub＞］★', '</sub></span>').replace(
                            '★［＜sup＞］★', '<span><sup>').replace(
                            '★［＜/sup＞］★', '</sup></span>')
                    if parastart:
                        if idx2 < idx2num:
                            etx = rgx_styledel.sub('', txlines2[idx2])
                            if rgx_eparastart.search(etx.rstrip()):
                                fobj.write(newmsg)
                                idx += 1
                                parastart = False
                                parawt = True
                            else:
                                fobj.write('<span class="j"><br></span>')
                        else:
                            fobj.write(newmsg)
                            idx += 1
                            parastart = False
                            parawt = True
                    else:
                        fobj.write(newmsg)
                        idx += 1
                else:
                    if idx2 < idx2num:
                        etx = rgx_styledel.sub('', txlines2[idx2])
                        if rgx_eparastart.search(etx.rstrip()):
                            fobj.write(newmsg)
                            idx += 1
                            parastart = False
                            parawt = True
                        else:
                            fobj.write('<span class="j"><br></span>')
                    else:
                        fobj.write(newmsg)
                        idx += 1
                        parastart = False
                        parawt = True
            else:
                fobj.write('<span class="j"><br></span>')
            if idx2 < idx2num:
                if not eparastart:
                    eatx2 = txlines2[idx2]
                    if parasync:
                        etx = rgx_styledel.sub('', eatx2)
                        if rgx_eparastart.search(etx.rstrip()):
                            eparastart = True
                        else:
                            eparastart = False
                    newmsg2 = ''.join((
                            xml.sax.saxutils.escape(eatx2), '<br>'))
                    newmsg2 = newmsg2.replace('`', r'\`')
                    if noefspc:
                        newmsg2 = newmsg2.replace(
                                '★lTAC', '<span class="e">').replace(
                                '★lTD<br>', '<br></span><hr>').replace(
                                '★sTS', '<span class="mark">').replace(
                                '★sTE', '</span>').replace(
                                '★esTS', '<span class="emark">').replace(
                                '★pTA', '<span id="').replace(
                                '★pTB', '" class="pa">').replace(
                                '★pTC', '</span>').replace(
                                '★pTX', '<span class="pa">').replace(
                                '★pTY', '</span>').replace(
                                '★epTX', '<span class="epa">').replace(
                                '★dTA', '<span class="').replace(
                                '★dTB', ' r" title="').replace(
                                '★dTX', ' f" title="').replace(
                                '★dTC',
                                '''" onmouseover='tip(this)' '''
                                '''onclick='wd("''').replace(
                                '★dTD', '''")'>''').replace(
                                '★dTY', '''">''').replace(
                                '★dTE', '</span>')
                        newmsg2 = rgx_spansps.sub(
                                r'\1&nbsp;&nbsp;&nbsp;&nbsp;', newmsg2)
                    else:
                        newmsg2 = rgx_hanref.sub(r'\1<b>\2</b>', newmsg2)
                        newmsg2 = newmsg2.replace(' ', '&nbsp;').replace(
                                '★［≪', '<').replace('≫］★', '>')
                        newmsg2 = ''.join((
                                '<span id="en', str(idx), '" class="e">',
                                newmsg2, '</span><hr>'))
                    newmsg2 = newmsg2.replace(
                            '★［＜sub＞］★', '<span><sub>').replace(
                            '★［＜/sub＞］★', '</sub></span>').replace(
                            '★［＜sup＞］★', '<span><sup>').replace(
                            '★［＜/sup＞］★', '</sup></span>')
                    if eparastart:
                        newmsg2 = rgx_eparastartsb.sub(
                                r'<span class="epa">\1</span>', newmsg2)
                        if idx < idxnum:
                            if parawt:
                                fobj.write(newmsg2)
                                idx2 += 1
                                eparastart = False
                                parawt = False
                            else:
                                fobj.write(
                                        '<span class="e dm"><br></span><hr>')
                        else:
                            fobj.write(newmsg2)
                            idx2 += 1
                            eparastart = False
                            parawt = False
                    else:
                        fobj.write(newmsg2)
                        idx2 += 1
                else:
                    if idx < idxnum:
                        if parawt:
                            fobj.write(newmsg2)
                            idx2 += 1
                            eparastart = False
                            parawt = False
                        else:
                            fobj.write('<span class="e dm"><br></span><hr>')
                    else:
                        fobj.write(newmsg2)
                        idx2 += 1
                        eparastart = False
                        parawt = False
            else:
                fobj.write('<span class="e dm"><br></span><hr>')
        fobj.write('`;\n')
    fobj.write(
            'const INNER_SC_SPC = `<h1 class="list-switch" '
            """onclick="listSwitch('spcJpList')">"""
            '■明細情報</h1><div id="cpyFspcJpList" '
            'class="inactcpy"><span class="cpy" '
            """onclick="listCpy(this)">copy plain text</span></div>"""
            '<div class="inactlist" id="spcJpList"></div>')
    if txlines2:
        fobj.write(
                '<h1 class="list-switch" '
                """onclick="listSwitchE('spcJEList')">""")
        if noefspc:
            fobj.write('■明細情報(英語Mix)</h1>')
        else:
            fobj.write(''.join(('■明細情報(英語:', efname, ')</h1>')))
        fobj.write(
                '<div id="cpyFspcJEList" class="inactcpy">'
                '<span class="cpy" '
                """onclick="listCpy(this)">copy plain text</span></div>"""
                '<div class="inactlist" id="spcJEList"></div>')
    fobj.write('`;\n')
    fobj.write(
            'function setSectionSpc(){\n'
            '  let scSpcList;\n  let scSpc;\n'
            '  scSpc = document.getElementById("sctSpc");\n'
            '  if (scSpc){\n    scSpc.insertAdjacentHTML'
            '("beforeend", INNER_SC_SPC);\n  }\n'
            '  scSpcList = document.getElementById("spcJpList");\n'
            '  if (scSpcList){\n    scSpcList.insertAdjacentHTML'
            '("beforeend", INNER_SPC_JPLIST);\n  }\n')
    if txlines2:
        fobj.write(
                '  scSpcList = document.getElementById("spcJEList");\n'
                '  if (scSpcList){\n    scSpcList.insertAdjacentHTML'
                '("beforeend", INNER_SPC_JELIST);\n  }\n')
    fobj.write('}\nwindow.addEventListener("load", setSectionSpc, false);\n')


class _Parser(object):
    def __init__(self, flg, ptnexwd):
        self.mcbflg = flg
        if self.mcbflg:
            try:
                self.mecab = MeCab.Tagger('-Ochasen2')  # non ignoring space
                self.nonverbset = set()
                self.ptnexceptionwd = ptnexwd
            except Exception as e:
                print(
                    '■Warning:MeCab(形態素解析エンジン)が'
                    '起動できませんでした。', str(e.args[0]))
                self.mcbflg = False
        return None

    def _set_nonverbs(self, wds):
        if self.mcbflg:
            try:
                hdauxiliaryverb = '助動詞'
                hdverb = '動詞'
                for wd in wds:
                    reslist = self.mecab.parse(wd).splitlines()
                    for chunk in reslist[:-1]:
                        wddat = chunk.split('\t')
                        feat = wddat[3]
                        if feat.startswith(hdauxiliaryverb):
                            self.nonverbset.add(wd)
                        elif feat.startswith(hdverb):
                            self.nonverbset.add(wd)
            except Exception as e:
                print(
                        '■Warning:MeCab形態素解析失敗(処理続行します)。',
                        str(e.args[0]))
                self.mcbflg = False

    def _clr_nonverbset(self):
        self.nonverbset = set()

    def _transform_tx(self, text):
        if self.mcbflg:
            try:
                jyoshi = '助詞'
                newtx = ''
                parsetgt = text
                reslist = self.mecab.parse(parsetgt).splitlines()
                for chunk in reslist[:-1]:
                    wddat = chunk.split('\t')
                    surf = wddat[0]
                    feat = wddat[3]
                    if '接続詞' == feat:
                        newtx = ''.join((newtx, '＋★［', surf, '］★＋'))
                    elif 'は' == surf:
                        if feat.startswith(jyoshi):
                            newtx = ''.join((newtx, surf, '、'))
                        else:
                            newtx = ''.join((newtx, surf))
                    else:
                        newtx = ''.join((newtx, surf))
                return newtx
            except Exception as e:
                print(
                        '■Warning:MeCab形態素解析失敗(処理続行します)。',
                        str(e.args[0]))
                self.mcbflg = False
                return text
        else:
            return text

    def _transform_clnoun(self, text):
        if self.mcbflg:
            try:
                hdnoun = '名詞'
                newtx = ''
                parsetgt = text
                reslist = self.mecab.parse(parsetgt).splitlines()
                for chunk in reslist[:-1]:
                    wddat = chunk.split('\t')
                    surf = wddat[0]
                    feat = wddat[3]
                    if feat.startswith(hdnoun):
                        newtx = ''.join((newtx, '＋★＜', surf, '＞★＋'))
                    else:
                        newtx = ''.join((newtx, surf))
                return newtx
            except Exception as e:
                print(
                        '■Warning:MeCab形態素解析失敗(処理続行します)。',
                        str(e.args[0]))
                self.mcbflg = False
                return text
        else:
            return text

    def _transform_cladj(self, text):
        if self.mcbflg:
            try:
                hdadj = '形容詞'
                hdadnominal = '連体詞'
                rgx_exceptwd = regex.compile(''.join((
                        self.ptnexceptionwd, '$')))
                newtx = ''
                parsetgt = text
                reslist = self.mecab.parse(parsetgt).splitlines()
                for chunk in reslist[:-1]:
                    wddat = chunk.split('\t')
                    surf = wddat[0]
                    feat = wddat[3]
                    if (feat.startswith(hdadj) or
                            feat.startswith(hdadnominal)):
                        if not rgx_exceptwd.search(surf):
                            if 1 < len(surf):
                                newtx = ''.join((
                                        newtx, '＋★｛', surf, '｝★＋'))
                            else:
                                newtx = ''.join((newtx, surf))
                        else:
                            newtx = ''.join((newtx, surf))
                    else:
                        newtx = ''.join((newtx, surf))
                return newtx
            except Exception as e:
                print(
                        '■Warning:MeCab形態素解析失敗(処理続行します)。',
                        str(e.args[0]))
                self.mcbflg = False
                return text
        else:
            return text

    def _transformcl4onewd(self, text):
        if self.mcbflg:
            try:
                hdauxiliaryverb = '助動詞'
                hdverb = '動詞'
                hdadverb = '副詞'
                hdadj = '形容詞'
                rgx_exceptwd = regex.compile(''.join((
                        self.ptnexceptionwd, '$')))
                rgx_kanji = regex.compile(r'^\p{Han}')
                newtx = ''
                # auxiliary verb exclusion
                parsetgt = text.replace('であ', '★●')
                reslist = self.mecab.parse(parsetgt).splitlines()
                for chunk in reslist[:-1]:
                    wddat = chunk.split('\t')
                    surf = wddat[0]
                    feat = wddat[3]
                    conj = wddat[5]
                    if feat.startswith(hdauxiliaryverb):
                        newtx = ''.join((newtx, '●'))
                    elif feat.startswith(hdverb):
                        if '連用形' == conj and rgx_kanji.search(surf):
                            newtx = ''.join((newtx, surf))
                        else:
                            if not rgx_exceptwd.search(surf):
                                newtx = ''.join((newtx, '●'))
                            else:
                                newtx = ''.join((newtx, surf))
                    elif feat.startswith(hdadverb):
                        newtx = ''.join((newtx, '●'))
                    elif feat.startswith(hdadj):
                        if not rgx_exceptwd.search(surf):
                            newtx = ''.join((newtx, '●'))
                        else:
                            newtx = ''.join((newtx, surf))
                    else:
                        newtx = ''.join((newtx, surf))
                return newtx
            except Exception as e:
                print(
                        '■Warning:MeCab形態素解析失敗(処理続行します)。',
                        str(e.args[0]))
                self.mcbflg = False
                return text
        else:
            return text

    def _transform_clverb(self, text):
        if self.mcbflg:
            try:
                newtx = ''
                if self.nonverbset:
                    ptn = ''.join(('(', '|'.join(self.nonverbset), ')'))
                    strblks = regex.split(ptn, text)
                else:
                    strblks = [text]
                for strblk in strblks:
                    if strblk in self.nonverbset:
                        newtx = ''.join((newtx, strblk))
                    else:
                        hdauxiliaryverb = '助動詞'
                        hdverb = '動詞'
                        reslist = self.mecab.parse(strblk).splitlines()
                        for chunk in reslist[:-1]:
                            wddat = chunk.split('\t')
                            surf = wddat[0]
                            feat = wddat[3]
                            if feat.startswith(hdauxiliaryverb):
                                newtx = ''.join((newtx, '●', surf))
                            elif feat.startswith(hdverb):
                                newtx = ''.join((newtx, '●', surf))
                            else:
                                newtx = ''.join((newtx, surf))
                return newtx
            except Exception as e:
                print(
                        '■Warning:MeCab形態素解析失敗(処理続行します)。',
                        str(e.args[0]))
                self.mcbflg = False
                return text
        else:
            return text

    def _transform_spc(self, text):
        if self.mcbflg:
            try:
                hdauxiliaryverb = '助動詞'
                hdverb = '動詞'
                hdadverb = '副詞'
                hdadj = '形容詞'
                rgx_exceptwd = regex.compile(''.join((
                        self.ptnexceptionwd, '$')))
                rgx_kanji = regex.compile(r'^\p{Han}')
                newtx = ''
                # auxiliary verb exclusion
                parsetgt = text.replace('であ', '★●')
                reslist = self.mecab.parse(parsetgt).splitlines()
                for chunk in reslist[:-1]:
                    wddat = chunk.split('\t')
                    surf = wddat[0]
                    feat = wddat[3]
                    conj = wddat[5]
                    if feat.startswith(hdauxiliaryverb):
                        newtx = ''.join((newtx, '●'*len(surf)))
                    elif feat.startswith(hdverb):
                        if '連用形' == conj and rgx_kanji.search(surf):
                            newtx = ''.join((newtx, surf))
                        else:
                            if not rgx_exceptwd.search(surf):
                                newtx = ''.join((newtx, '●'*len(surf)))
                            else:
                                newtx = ''.join((newtx, surf))
                    elif feat.startswith(hdadverb):
                        newtx = ''.join((newtx, '●'*len(surf)))
                    elif feat.startswith(hdadj):
                        if not rgx_exceptwd.search(surf):
                            newtx = ''.join((newtx, '●'*len(surf)))
                        else:
                            newtx = ''.join((newtx, surf))
                    else:
                        newtx = ''.join((newtx, surf))
                return newtx
            except Exception as e:
                print(
                        '■Warning:MeCab形態素解析失敗(処理続行します)。',
                        str(e.args[0]))
                self.mcbflg = False
                return text
        else:
            return text


def patissier(txlines, noefclflg, efspclines):
    """patissier function for analyzing text data

    This returns results of analyzing input text data.
    This function is called by run method in Patisserie class.

    Args:
        txlines (list): a list of line strings of text data
        noefclflg(bool): True: CL in English-file does not exist.
        efspclines(list): a list of English Specification lines
    Returns:
        data-set1: p_ngline_nums : NG line numbers
        list1: p_warn_lines : Warning text lines
        list2: p_cl_lines : Claim text lines (No header)
        list3: p_cl_elines : English-mixed claim lines (No header)
        list4: p_clel_lines : Claim element lines
        list5: p_tr_lines : Claim tree text lines
        list6: p_trel_lines : Claim tree of claim elements
        list7: p_spc_lines : Specification text lines (No header)
        list8: p_spc_elines : English-mixed specification lines (No header)
        list9: p_spchd_lines : Headlines of specification
        list10: p_spccl_lines : Claim-base specification text lines
        list11: p_abs_lines : Claim-base abstract text lines
        list12: p_fig_lines : Claim-base figure text lines
        list13: p_ref_lines : Reference lines
        list14: p_wd_lines : Keyword lines
        list15: p_wdlist_lines : Important keyword lines
        data-set2: p_a_array : data for patelierjs.js
        data-set3: p_array_tip : data tip for patelierjs.js
        data-set4: p_array_ef : data of English file for patelierjs.js

    """
    global noefcl_flg
    global noefspc_flg
    global ef_spclines
    global prgrss
    global mecab_flg
    global prsr
    global wd_set
    global wdlines_dic
    global clno_max
    global cl_nounset
    global cl1_list
    global cl_dic
    global cl_newdic
    global cl_basedic
    global cl_strdic
    global cl_blkdic
    global cl_jwddic
    global cl_errjwddic
    global cl_iwddic
    global cl_cmtdic
    global cl_refdic
    global cl_tgtlinedic
    global cl_tgtdic
    global cl_tgtgrpdic
    global cl_mwddic
    global cl_eldic
    global cl_structdic
    global cl_tmpstructdic
    global cl_allstructdic
    global cl_strgdic
    global cl_tmpstrgdic
    global cl_allstrgdic
    global cl_pgdic
    global cl_tmppgdic1
    global cl_tmppgdic2
    global cl_tmppgdic3
    global cl_allpgdic
    global cl_wdattrdic
    global cl_alljwdset
    global cl_endwdset
    global cl_kwddic
    global cl_onlyiwddic
    global cl_allwddic
    global cl_wddic
    global cl_wdnodic
    global cl_wdclassnodic
    global cl_topelset
    global cl_topmethodelset
    global fig_dic
    global fig_streldic
    global je_wddic
    global spc_basedic
    global prev_paranum
    global used_paranoset
    global all_wdrefdic
    global eb_dic
    global eb_wdrefs
    global eb_wdrefsflg
    global eb_samerefdiffs
    global eb_wdinfodic
    global eb_wdnodic
    global imp_wdset
    global ptn_impwd
    global rf_refdic
    global rf_allset
    global rf_okset
    global ephr_dic
    global SPC_HEADSNODIC
    global SPC_HEADSBRNCHDIC
    global NG_ENDS
    global BORE_WDSENDS
    global NG_RFENDS
    global SP_WDS
    global EB_CHEMWDS
    global HD_CMTBLK
    global HD_CMT
    global PTN_NOUN
    global PTN_ENWDS
    global PTN_HIRAWD
    global PTN_ADJ
    global PTN_RF
    global PTN_EBGRPRF
    global PTN_B4TGT
    global PTN_AFTGT
    global PTN_CLLTDHD
    global PTN_CLGENHD
    global PTN_AFTNAME
    global PTN_EBHD
    global PTN_EBRFAFTEN
    global PTN_EBAFTRF
    global PTN_EBGRPRF
    global PTN_EBGRPRF1
    global PTN_NONEEDWD
    global PTN_NONEEDEND
    global PTN_EBHD4NORF
    global rgx_parentheses
    global rgx_ctrl
    global rgx_nosps
    global rgx_2typesp
    global rgx_linehdok
    global rgx_nbsp
    global rgx_mspace
    global rgx_mcomma
    global rgx_mperiod
    global rgx_ngcircle
    global rgx_nghan
    global rgx_ngchr
    global rgx_ngmarunum
    global rgx_hdmk
    global rgx_hd
    global rgx_para
    global rgx_hdbasic
    global rgx_spchdno
    global rgx_spchdnobr
    global rgx_quote1, rgx_quote2, rgx_quote3
    global rgx_spcend
    global rgx_ebhdno
    global rgx_refwd
    global rgx_chkref
    global rgx_clhd
    global rgx_clcmt
    global rgx_clend
    global rgx_hannum
    global rgx_noun
    global rgx_mhira
    global rgx_ovrhira
    global rgx_impxa
    global rgx_11xa, rgx_12xa, rgx_13xa
    global rgx_21xa, rgx_22xa, rgx_23xa
    global rgx_31xa, rgx_32xa
    global rgx_40xa
    global rgx_50xa
    global rgx_90xa
    global rgx_95xa
    global rgx_refcl
    global rgx_refnum
    global rgx_refnumgrp
    global rgx_iclngwd
    global rgx_refjwd
    global rgx_noneedclwds
    global rgx_noneedclwdend
    global rgx_string
    global rgx_impa, rgx_impb
    global rgx_11a, rgx_11b, rgx_12a, rgx_12b, rgx_13a, rgx_13b
    global rgx_21a, rgx_21b, rgx_22a, rgx_22b, rgx_23a, rgx_23b
    global rgx_31a, rgx_31b, rgx_32a, rgx_32b
    global rgx_40a, rgx_40b
    global rgx_50a, rgx_50b
    global rgx_90a, rgx_90b
    global rgx_chkrefwd
    global rgx_impia, rgx_impib, rgx_impic
    global rgx_11ia, rgx_11ib, rgx_11ic
    global rgx_12ia, rgx_12ib, rgx_12ic
    global rgx_13ia, rgx_13ib, rgx_13ic
    global rgx_21ia, rgx_21ib, rgx_21ic
    global rgx_22ia, rgx_22ib, rgx_22ic
    global rgx_24ia, rgx_24ib, rgx_24ic
    global rgx_31ia, rgx_31ib, rgx_31ic
    global rgx_32ia, rgx_32ib, rgx_32ic
    global rgx_40ia, rgx_40ib, rgx_40ic
    global rgx_50ia, rgx_50ib, rgx_50ic
    global rgx_ngend
    global rgx_alpha1
    global rgx_borewdend
    global rgx_ngrefend
    global rgx_spwd
    global rgx_clendwd
    global rgx_pgcl
    global rgx_methodcl
    global rgx_pg11, rgx_pg12, rgx_pg21, rgx_pg22, rgx_pg31, rgx_pg32
    global rgx_funccl
    global rgx_meanscl
    global rgx_struct
    global rgx_datcl
    global rgx_verbmk
    global rgx_strg1, rgx_strg2, rgx_strg3
    global rgx_g
    global rgx_va1, rgx_va2, rgx_va3
    global rgx_ebwdhd
    global rgx_ebnum
    global rgx_imprefenend
    global rgx_imprefjpend
    global rgx_11eb, rgx_12eb, rgx_13eb
    global rgx_21eb, rgx_22eb, rgx_23eb
    global rgx_31eb, rgx_32eb
    global rgx_40eb
    global rgx_50eb
    global rgx_englishend
    global rgx_ebgrpref1
    global rgx_noneedwds
    global rgx_noneedend
    global rgx_refchk01, rgx_refchk02, rgx_refchk03, rgx_refchk04
    global rgx_chemwd
    global rgx_impex
    global rgx_11ex, rgx_12ex, rgx_13ex
    global rgx_21ex, rgx_22ex, rgx_24ex
    global rgx_31ex, rgx_32ex
    global rgx_40ex
    global rgx_50ex
    global rgx_udel
    global p_ngline_nums
    global p_warn_lines
    global p_cl_lines
    global p_cl_elines
    global p_clel_lines
    global p_tr_lines
    global p_trel_lines
    global p_spc_lines
    global p_spc_elines
    global p_spchd_lines
    global p_spccl_lines
    global p_abs_lines
    global p_fig_lines
    global p_ref_lines
    global p_wd_lines
    global p_wdlist_lines
    global p_a_array
    global p_array_tip
    global p_array_ef
    noefcl_flg = noefclflg
    if efspclines:
        noefspc_flg = False
    else:
        noefspc_flg = True
    ef_spclines = efspclines
    p_ngline_nums = set()
    p_warn_lines = []
    p_cl_lines = []  # no header
    p_cl_elines = []  # no header
    p_clel_lines = []
    p_tr_lines = []
    p_trel_lines = []
    p_spc_lines = []  # no header
    p_spc_elines = []  # no header
    p_spchd_lines = []
    p_spccl_lines = []
    p_abs_lines = []
    p_fig_lines = []
    p_ref_lines = []
    p_wd_lines = []
    p_wdlist_lines = []
    p_a_array = set()
    p_array_tip = set()
    p_array_ef = set()
    wd_set = set()
    wdlines_dic = {}
    clno_max = 0
    cl_nounset = set()
    cl1_list = []
    cl_dic = {}
    cl_strdic = {}
    cl_newdic = {}
    cl_basedic = {}
    cl_blkdic = {}
    cl_jwddic = {}
    cl_errjwddic = {}
    cl_iwddic = {}
    cl_cmtdic = {}
    cl_refdic = {}
    cl_tgtlinedic = {}
    cl_tgtdic = {}
    cl_tgtgrpdic = {}
    cl_mwddic = {}
    cl_eldic = {}
    cl_structdic = {}
    cl_tmpstructdic = {}
    cl_allstructdic = {}
    cl_strgdic = {}
    cl_tmpstrgdic = {}
    cl_allstrgdic = {}
    cl_pgdic = {}
    cl_tmppgdic1 = {}
    cl_tmppgdic2 = {}
    cl_tmppgdic3 = {}
    cl_allpgdic = {}
    cl_wdattrdic = {}
    cl_alljwdset = set()
    cl_endwdset = set()
    cl_kwddic = {}
    cl_onlyiwddic = {}
    cl_allwddic = {}
    cl_wddic = {}
    cl_wdnodic = {}
    cl_wdclassnodic = {}
    cl_topelset = set()
    cl_topmethodelset = set()
    fig_dic = {}
    fig_streldic = {}
    je_wddic = {}
    spc_basedic = {}
    prev_paranum = 0
    used_paranoset = set()
    all_wdrefdic = {}
    eb_dic = {}
    eb_wdrefs = []
    eb_wdrefsflg = False
    eb_samerefdiffs = []
    eb_wdinfodic = {}
    eb_wdnodic = {}
    imp_wdset = set()
    ptn_impwd = ''
    rf_refdic = {}
    rf_allset = set()
    rf_okset = set()
    ephr_dic = {}
    if prsr is None:
        prsr = _Parser(mecab_flg, PTN_HIRAWD)
    else:
        prsr._clr_nonverbset()
    rgx_parentheses = regex.compile(
            '(?<parentheses>[(（]([^()（）]+|(?&parentheses))*[)）])')
    rgx_ctrl = regex.compile(r'[\x00-\x1f]')
    rgx_nosps = regex.compile(r'[^\x20\u3000\u00a0]+')
    rgx_2typesp = regex.compile(r'[\x20\u00a0]')
    rgx_linehdok = regex.compile(r'^[\u3000■※【]')
    rgx_nbsp = regex.compile(r'[\u00a0]')
    rgx_mspace = regex.compile(r'\x20{2,}')
    rgx_mcomma = regex.compile('、{2,}')
    rgx_mperiod = regex.compile('。{2,}')
    rgx_ngcircle = regex.compile('◯')
    rgx_nghan = regex.compile(r'[\uff61-\uff9f]+')
    rgx_ngchr = regex.compile(
            '[①-⑳㉑-㉟㊱-㊿Ⅰ-Ⅹ'
            '㍉㌔㌢㍍㌘㌧㌃㌶㍑㍗㌍㌦㌣㌫㍊㌻㎜㎝㎞㎎㎏㏄㎡㍻〝〟№㏍℡'
            '㊤㊥㊦㊧㊨㈱㈲㈹㍾㍽㍼∮∑∟⊿]+')
    rgx_ngmarunum = regex.compile('[㉑-㉟㊱-㊿]')
    rgx_hdmk = regex.compile('【.*】')
    rgx_hd = regex.compile('【(?P<heading>.+)】')
    rgx_hdbasic = regex.compile('【(?P<heading>[^数表化].+)】')
    rgx_para = regex.compile('^(?P<paranum>[0-9０-９]{4}[0-9０-９]?)$')
    rgx_spchdno = regex.compile(
            '^('+'|'.join(SPC_HEADSNODIC.keys())+')'
            '(?P<number>([1-9１-９][0-9０-９]*)?)$')
    rgx_spchdnobr = regex.compile(
            '^('+'|'.join(SPC_HEADSBRNCHDIC.keys())+')'
            '(?P<number_br>[1-9１-９][0-9０-９]*'
            r'([\-－\.．]?[0-9０-９A-Za-zＡ-Ｚａ-ｚ]+|'
            r'[\(（][0-9０-９A-Za-zＡ-Ｚａ-ｚ]+[\)）])?)$')
    rgx_quote1 = regex.compile('「[^「」]+」')
    rgx_quote2 = regex.compile('『[^『』]+』')
    rgx_quote3 = regex.compile('“[^“”]+”')
    rgx_spcend = regex.compile('^(書類名|請求項|要約)')
    rgx_ebhdno = regex.compile('^実施例([1-9１-９][0-9０-９]*)?$')
    rgx_refwd = regex.compile('(?P<ref>[^ 　]+)[ 　]+(?P<word>[^ 　].*)')
    rgx_chkref = regex.compile(''.join(('^', PTN_RF, PTN_EBGRPRF, '$')))
    rgx_clhd = regex.compile('【請求項(?P<clno>[1-9１-９][0-9０-９]*)】')
    rgx_clcmt = regex.compile(r'^.*【請求項.+】[\x20\u3000]*')
    rgx_clend = regex.compile('【[^数表化請].+】')
    rgx_hannum = regex.compile('[0-9]')
    rgx_noun = regex.compile(PTN_NOUN)
    rgx_mhira = regex.compile(r'[\p{Hiragana}]{2,}')
    rgx_ovrhira = regex.compile(r'[\p{Hiragana}]{7,}')
    rgx_refcl = regex.compile('請求項(?P<refstr>[^記]+)記載')
    rgx_refnum = regex.compile('[1-9１-９][0-9０-９]*')
    rgx_refnumgrp = regex.compile(
            '(?P<from_rfno>[1-9１-９][0-9０-９]*)(-|~|－|～|乃至|ないし|から)'
            '(?P<to_rfno>[1-9１-９][0-9０-９]*)')
    rgx_iclngwd = regex.compile('(?P<ngwd>のみ|だけ)')
    rgx_refjwd = regex.compile(
            '([0-9０-９]記載の|項記載の|に記載の|前記の|'
            '上記の|前記|上記|当該|該(?!当))')
    rgx_noneedclwds = regex.compile('^(各種|各)')
    rgx_noneedclwdend = regex.compile(
            '(の?それぞれ.*|の?おのおの.*|'
            'の?夫々.*|の?各々.*|自体|部分|又|若|及|並|或|毎|別|'
            '(の|以)?(上|下|外|内|前|後)|'
            'の?(上|下|外|内|前|後)(部|側|方)|'
            'の?中)$')
    rgx_chkrefwd = regex.compile(
            '([0-9０-９]記載の|項記載の|に記載の|'
            '前記|上記|当該|該(?!当)|、|【)')
    ptn_11i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけすせちつてねひみむめりるれぎげじぜぢびべ]'
            r'[\p{Han}]'
            '[いうえきくけすせちつてねひみむめりるれぎげじぜぢびべ]'
            r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
            '[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_11ia = ''.join((PTN_CLLTDHD, ptn_11i, PTN_AFTNAME))
    rgx_11ia = regex.compile(ptn_11ia)
    ptn_11ib = ''.join((PTN_CLGENHD, ptn_11i, PTN_AFTGENWD))
    rgx_11ib = regex.compile(ptn_11ib)
    ptn_11ic = ''.join((PTN_CLGENHD, ptn_11i, PTN_AFTNAME))
    rgx_11ic = regex.compile(ptn_11ic)
    ptn_12i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけすせちつてねひみむめりるれぎげじぜぢびべ]'
            r'[\p{Han}]'
            '[いうえきくけすせちつてねひみむめりるれぎげじぜぢびべ]'
            r'[A-Za-zＡ-Ｚａ-ｚ]*[ー・\p{Katakana}\p{Han}]+)'))
    ptn_12ia = ''.join((PTN_CLLTDHD, ptn_12i, PTN_AFTNAME))
    rgx_12ia = regex.compile(ptn_12ia)
    ptn_12ib = ''.join((PTN_CLGENHD, ptn_12i, PTN_AFTGENWD))
    rgx_12ib = regex.compile(ptn_12ib)
    ptn_12ic = ''.join((PTN_CLGENHD, ptn_12i, PTN_AFTNAME))
    rgx_12ic = regex.compile(ptn_12ic)
    ptn_13i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけすせちつてねひみむめりるれぎげじぜぢびべ]'
            r'[\p{Han}]+[いえきけせちてねみめりれぎげじぜび])'))
    ptn_13ia = ''.join((PTN_CLLTDHD, ptn_13i, PTN_AFTNAME))
    rgx_13ia = regex.compile(ptn_13ia)
    ptn_13ib = ''.join((PTN_CLGENHD, ptn_13i, PTN_AFTGENWD))
    rgx_13ib = regex.compile(ptn_13ib)
    ptn_13ic = ''.join((PTN_CLGENHD, ptn_13i, PTN_AFTNAME))
    rgx_13ic = regex.compile(ptn_13ic)
    ptn_21i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけすせちつてねひみむめりるれぎげじぜぢびべ]'
            r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
            '[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_21ia = ''.join((PTN_CLLTDHD, ptn_21i, PTN_AFTNAME))
    rgx_21ia = regex.compile(ptn_21ia)
    ptn_21ib = ''.join((PTN_CLGENHD, ptn_21i, PTN_AFTGENWD))
    rgx_21ib = regex.compile(ptn_21ib)
    ptn_21ic = ''.join((PTN_CLGENHD, ptn_21i, PTN_AFTNAME))
    rgx_21ic = regex.compile(ptn_21ic)
    ptn_22i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけすせちつてねひみむめりるれぎげじぜぢびべ]'
            r'[A-Za-zＡ-Ｚａ-ｚ]*[ー・\p{Katakana}\p{Han}]+)'))
    ptn_22ia = ''.join((PTN_CLLTDHD, ptn_22i, PTN_AFTNAME))
    rgx_22ia = regex.compile(ptn_22ia)
    ptn_22ib = ''.join((PTN_CLGENHD, ptn_22i, PTN_AFTGENWD))
    rgx_22ib = regex.compile(ptn_22ib)
    ptn_22ic = ''.join((PTN_CLGENHD, ptn_22i, PTN_AFTNAME))
    rgx_22ic = regex.compile(ptn_22ic)
    ptn_24i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*',
            PTN_HIRAWD,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*|'
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]+)[\p{Han}]'
            '[いえきけしせちてねみめりれぎげじぜび])'))
    ptn_24ia = ''.join((PTN_CLLTDHD, ptn_24i, PTN_AFTNAME))
    rgx_24ia = regex.compile(ptn_24ia)
    ptn_24ib = ''.join((PTN_CLGENHD, ptn_24i, PTN_AFTGENWD))
    rgx_24ib = regex.compile(ptn_24ib)
    ptn_24ic = ''.join((PTN_CLGENHD, ptn_24i, PTN_AFTNAME))
    rgx_24ic = regex.compile(ptn_24ic)
    ptn_31i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
            '[A-Za-zＡ-Ｚａ-ｚ]*[-－―・／/]?[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_31ia = ''.join((PTN_CLLTDHD, ptn_31i, PTN_AFTNAME))
    rgx_31ia = regex.compile(ptn_31ia)
    ptn_31ib = ''.join((PTN_CLGENHD, ptn_31i, PTN_AFTGENWD))
    rgx_31ib = regex.compile(ptn_31ib)
    ptn_31ic = ''.join((PTN_CLGENHD, ptn_31i, PTN_AFTNAME))
    rgx_31ic = regex.compile(ptn_31ic)
    ptn_32i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
            r'[ー・\p{Katakana}\p{Han}]+)'))
    ptn_32ia = ''.join((PTN_CLLTDHD, ptn_32i, PTN_AFTNAME))
    rgx_32ia = regex.compile(ptn_32ia)
    ptn_32ib = ''.join((PTN_CLGENHD, ptn_32i, PTN_AFTGENWD))
    rgx_32ib = regex.compile(ptn_32ib)
    ptn_32ic = ''.join((PTN_CLGENHD, ptn_32i, PTN_AFTNAME))
    rgx_32ic = regex.compile(ptn_32ic)
    ptn_40i = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*)', PTN_HIRAWD,
            r'([ー・\p{Katakana}\p{Han}]*))'))
    ptn_40ia = ''.join((PTN_CLLTDHD, ptn_40i, PTN_AFTNAME))
    rgx_40ia = regex.compile(ptn_40ia)
    ptn_40ib = ''.join((PTN_CLGENHD, ptn_40i, PTN_AFTGENWD))
    rgx_40ib = regex.compile(ptn_40ib)
    ptn_40ic = ''.join((PTN_CLGENHD, ptn_40i, PTN_AFTNAME))
    rgx_40ic = regex.compile(ptn_40ic)
    ptn_50i = ''.join(('(?P<name>', PTN_ENWDS, ')'))
    ptn_50ia = ''.join((PTN_CLLTDHD, ptn_50i, PTN_AFTNAME))
    rgx_50ia = regex.compile(ptn_50ia)
    ptn_50ib = ''.join((PTN_CLGENHD, ptn_50i, PTN_AFTGENWD))
    rgx_50ib = regex.compile(ptn_50ib)
    ptn_50ic = ''.join((PTN_CLGENHD, ptn_50i, PTN_AFTNAME))
    rgx_50ic = regex.compile(ptn_50ic)
    rgx_ngend = regex.compile(''.join(('(', '|'.join(NG_ENDS), ')$')))
    rgx_alpha1 = regex.compile('^[A-Za-z]$')
    rgx_borewdend = regex.compile(''.join((
            '(', '|'.join(BORE_WDSENDS), ')$')))
    rgx_ngrefend = regex.compile(''.join((
            '^(', '|'.join(NG_RFENDS), ')[A-Za-z]*')))
    rgx_spwd = regex.compile(''.join((
            '(', '|'.join(SP_WDS), ')([A-Za-z]+)?$')))
    rgx_pgcl = regex.compile('プログラム([A-Za-zＡ-Ｚａ-ｚ]+)?$')
    rgx_methodcl = regex.compile(
            '(ステップ|工程|法|処理|プロセス|ルーチン|手順)'
            '([A-Za-zＡ-Ｚａ-ｚ]+)?$')
    rgx_pg11 = regex.compile(
            '(?P<verb>(((前記の|上記の|前記|上記|当該|該)?コンピュータに、?)?'
            '(実行さ|行わ|行なわ)せ|実行する|行う|行なう))')
    rgx_pg12 = regex.compile(
            '^(?P<str_e>.+)(?P<verb>(を、?((前記の|上記の|前記|上記|当該|該)?'
            'コンピュータに、?)?'
            '(実行さ|行わ|行なわ)せ|を、?(実行する|行う|行なう)))')
    rgx_pg21 = regex.compile(
            '(?P<verb>(((前記の|上記の|前記|上記|当該|該)?コンピュータに、?)?'
            '実現させ|実現する))')
    rgx_pg22 = regex.compile(
            '^(?P<str_e>.+)(?P<verb>(を、?((前記の|上記の|前記|上記|当該|該)?'
            'コンピュータに、?)?実現させ|を、?実現する))')
    rgx_pg31 = regex.compile(
            '(?P<verb>(((前記の|上記の|前記|上記|当該|該)?コンピュータを、?)?'
            '機能させ))')
    rgx_pg32 = regex.compile(
            '^(?P<str_e>.+)(?P<verb>(として、?'
            '((前記の|上記の|前記|上記|当該|該)?コンピュータを、?)?'
            '機能させ))')
    rgx_funccl = regex.compile('機能([A-Za-zＡ-Ｚａ-ｚ]+)?$')
    rgx_meanscl = regex.compile(
            '(手段|システム|装置|機器|ユニット|ブロック)'
            '([A-Za-zＡ-Ｚａ-ｚ]+)?$')
    rgx_struct = regex.compile(
            '^(?P<str_e>.+)(とを?|＋★［[^＋]+］★＋|及び|並びに|又は|'
            '若しくは|或いは|のいずれかを?)、?$')
    rgx_datcl = regex.compile(
            '(データ|情報|信号|画像|画面|モデル|ツール|パターン|ファイル|'
            'ディレクトリ|フォルダー|フォルダ|ドキュメント|文書|'
            'プロフィール|テーブル|データベース|DB|辞書|ビット|フラグ|'
            'ルーチン|プログラム|パラメータ|期間|時間|履歴|状態|結果|指標|'
            '規格|力|量|値|数)([A-Za-zＡ-Ｚａ-ｚ]+)?$')
    rgx_verbmk = regex.compile('^.+●')
    rgx_strg1 = regex.compile(
            '(記録し|記録しており|記録する|記録した|記録している|'
            '登録し|登録しており|登録する|登録した|登録している|'
            '格納し|格納しており|格納する|格納した|格納している|記憶し|'
            '記憶しており|記憶する|記憶した|記憶している|保持し|保持しており|'
            '保持する|保持した|保持している|保存し|保存しており|保存する|'
            '保存した|保存している|蓄積し|蓄積しており|蓄積する|蓄積した|'
            '蓄積している|記録内容とし|記録内容としており|記録内容とする|'
            '記録内容とした|記録内容としている|登録内容とし|'
            '登録内容としており|登録内容とする|登録内容とした|'
            '登録内容としている|格納内容とし|格納内容としており|'
            '格納内容とする|格納内容とした|格納内容としている|記憶内容とし|'
            '記憶内容としており|記憶内容とする|記憶内容とした|'
            '記憶内容としている|保持内容とし|保持内容としており|'
            '保持内容とする|保持内容とした|保持内容としている|保存内容とし|'
            '保存内容としており|保存内容とする|保存内容とした|'
            '保存内容としている|蓄積内容とし|蓄積内容としており|'
            '蓄積内容とする|蓄積内容とした|蓄積内容としている|内容とし|'
            '内容としており|内容とする|内容とした|内容としている|一内容とし|'
            '一内容としており|一内容とする|一内容とした|一内容としている)')
    rgx_strg2 = regex.compile(
            '^(?P<str_e>.+)(?P<verb>(を、?(記録し|記録しており|記録する|'
            '記録した|記録している|登録し|登録しており|登録する|登録した|'
            '登録している|格納し|格納しており|格納する|格納した|格納している|'
            '記憶し|記憶しており|記憶する|記憶した|記憶している|保持し|'
            '保持しており|保持する|保持した|保持している|保存し|'
            '保存しており|保存する|保存した|保存している|蓄積し|'
            '蓄積しており|蓄積する|蓄積した|蓄積している|記録内容とし|'
            '記録内容としており|記録内容とする|記録内容とした|'
            '記録内容としている|登録内容とし|登録内容としており|'
            '登録内容とする|登録内容とした|登録内容としている|'
            '格納内容とし|格納内容としており|格納内容とする|'
            '格納内容とした|格納内容としている|記憶内容とし|'
            '記憶内容としており|記憶内容とする|記憶内容とした|'
            '記憶内容としている|保持内容とし|保持内容としており|'
            '保持内容とする|保持内容とした|保持内容としている|'
            '保存内容とし|保存内容としており|保存内容とする|'
            '保存内容とした|保存内容としている|蓄積内容とし|'
            '蓄積内容としており|蓄積内容とする|蓄積内容とした|'
            '蓄積内容としている|内容とし|内容としており|内容とする|'
            '内容とした|内容としている|一内容とし|一内容としており|'
            '一内容とする|一内容とした|一内容としている)|(が、?'
            '(記録される|記録された|記録されている|登録される|登録された|'
            '登録されている|格納される|格納された|格納されている|'
            '記憶される|記憶された|記憶されている|保持される|保持された|'
            '保持されている|保存される|保存された|保存されている|'
            '蓄積される|蓄積された|蓄積されている))))(、|$|こと(を特徴)?|'
            '請求項)')
    rgx_strg3 = regex.compile(
            '^(?P<str_e>.+)(?P<verb>(に、?'
            '(記録され|記録されており|記録される|記録された|'
            '記録されている|登録され|登録されており|登録される|登録された|'
            '登録されている|格納され|格納されており|格納される|格納された|'
            '格納されている|記憶され|記憶されており|記憶される|記憶された|'
            '記憶されている|保持され|保持されており|保持される|保持された|'
            '保持されている|保存され|保存されており|保存される|保存された|'
            '保存されている|蓄積され|蓄積されており|蓄積される|蓄積された|'
            '蓄積されている)|(の、?(記録内容であり|記録内容である|'
            '記録内容であって|登録内容であり|登録内容である|'
            '登録内容であって|格納内容であり|格納内容である|'
            '格納内容であって|記憶内容であり|記憶内容である|'
            '記憶内容であって|保持内容であり|保持内容である|'
            '保持内容であって|保存内容であり|保存内容である|'
            '保存内容であって|蓄積内容であり|蓄積内容である|'
            '蓄積内容であって|内容であり|内容である|内容であって|'
            '一内容であり|一内容である|一内容であって))))'
            '(、|$|こと(を特徴)?|請求項)')
    rgx_g = regex.compile(
            '^(([0-9０-９A-Za-zＡ-Ｚａ-ｚ'
            '一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+'
            '[つ回行組個数対番目本次定列]?以上)の|複数の?)(?P<word2>.+)$')
    rgx_va1 = regex.compile(
            '(備え|備えており|備える|備えた|備えている|'
            '有し|有しており|有す|有する|有している|含み|含んでおり|含む|'
            '含んだ|含んでいる|含んで構成され|含んで構成される|具備し|'
            '具備しており|具備する|具備した|具備している|包含し|'
            '包含しており|包含する|包含した|包含している|構成要素とし|'
            '構成要素としており|構成要素とする|構成要素とした|'
            '構成要素としている|構成され|構成されており|構成される|'
            '構成された|構成されている|形成され|形成されており|形成される|'
            '形成された|形成されている|成り|成っており|成る|成った|'
            '成っている|なり|なっており|なる|なった|なっている)')
    rgx_va2 = regex.compile(
            '^(?P<str_e>.+)(?P<verb>(を、?'
            '((更|さら)に、?)?(備え|備えており|備える|備えた|備えている|'
            '有し|有しており|有す|有する|有している|含み|含んでおり|含む|'
            '含んだ|含んでいる|含んで構成され|含んで構成される|具備し|'
            '具備しており|具備する|具備した|具備している|包含し|'
            '包含しており|包含する|包含した|包含している|構成要素とし|'
            '構成要素としており|構成要素とする|構成要素とした|'
            '構成要素としている)|((により|で|から)、?(構成され|'
            '構成されており|構成される|構成された|構成されている|形成され|'
            '形成されており|形成される|形成された|形成されている|成り|'
            '成っており|成る|成った|成っている|なり|なっており|なる|なった|'
            'なっている))))(、|$|こと(を特徴)?|請求項)')
    rgx_va3 = regex.compile(
            '^(?P<str_e>.+)(?P<verb>(に、?(備えられ|'
            '備えられており|備えられる|備えられた|備えられている|有され|'
            '有されており|有される|有されている|含まれ|含まれており|含まれる|'
            '含まれた|含まれている|具備され|具備されており|具備される|'
            '具備された|具備されている|包含され|包含されており|包含される|'
            '包含された|包含されている)|(の、?(構成要素であり|'
            '構成要素である|構成要素であって|一部であり|一部である|'
            '一部であって|一部分であり|一部分である|一部分であって|'
            '部分であり|部分である|部分であって|部品であり|部品である|'
            '部品であって|要素であり|要素である|要素であって))))(、|$|こと'
            '(を特徴)?|請求項)')
    rgx_englishend = regex.compile('[A-Za-zＡ-Ｚａ-ｚ]$')
    para_num = 0
    lineno = 1
    claim_num = 0
    last_line = ''
    spc_num = 0
    impjenum = 0
    prgrss = 3
    for txline in txlines:
        txline = rgx_udel.sub('', txline)
        newtxline = txline.rstrip()
        if 3 == spc_num or 1 == impjenum:
            newtxline = _cchk(
                    newtxline, lineno, claim_num, spc_num, para_num, False)
        else:
            newtxline = _cchk(
                    newtxline, lineno, claim_num, spc_num, para_num, True)
        if not newtxline:
            last_line = newtxline
            lineno += 1
            continue
        if (not newtxline.startswith(HD_CMTBLK)) and (
                not newtxline.startswith(HD_CMT)):
            if -1 < claim_num:
                c_flg, claim_num = _claimextr(
                        newtxline, lineno, claim_num, last_line)
                if not c_flg:
                    return (p_ngline_nums, p_warn_lines, p_cl_lines,
                            p_cl_elines, p_clel_lines, p_tr_lines,
                            p_trel_lines, p_spc_lines, p_spc_elines,
                            p_spchd_lines, p_spccl_lines, p_abs_lines,
                            p_fig_lines, p_ref_lines, p_wd_lines,
                            p_wdlist_lines, p_a_array, p_array_tip,
                            p_array_ef)
            if 1 > claim_num:
                if -1 < impjenum:
                    impjenum = _jeextr(newtxline, impjenum)
                if -1 < spc_num:
                    spc_num, para_num = _spcextr(
                            newtxline, lineno, spc_num, para_num)
        last_line = newtxline
        lineno += 1
    if 0 == claim_num:
        p_warn_lines.append('★eTS■請求項がありません★wTE')
        p_warn_lines.append('★eTS■分析を中止します★wTE')
        return (p_ngline_nums, p_warn_lines, p_cl_lines, p_cl_elines,
                p_clel_lines, p_tr_lines, p_trel_lines, p_spc_lines,
                p_spc_elines, p_spchd_lines, p_spccl_lines, p_abs_lines,
                p_fig_lines, p_ref_lines, p_wd_lines, p_wdlist_lines,
                p_a_array, p_array_tip, p_array_ef)
    imp_wdset = rf_refdic.keys() | je_wddic.keys()
    ptn_impwd = ''.join(('(', '|'.join(imp_wdset), ')'))
    if imp_wdset:
        rgx_impxa = regex.compile(''.join((
                PTN_B4TGT, PTN_ADJ, '(?P<name>', ptn_impwd, ')',
                PTN_AFTGT)))
    else:
        rgx_impxa = None
    rgx_string = regex.compile(''.join((
            '^', PTN_CLGENHD, PTN_ADJ, '(?P<name>「[^「」]+」)',
            PTN_AFTNAME)))
    rgx_impa = regex.compile(''.join((
            '^', PTN_CLLTDHD, PTN_ADJ, '(?P<name>', ptn_impwd, ')',
            PTN_AFTNAME)))
    rgx_impb = regex.compile(''.join((
            '^', PTN_CLGENHD, PTN_ADJ, '(?P<name>', ptn_impwd, ')',
            PTN_AFTNAME)))
    rgx_impia = regex.compile(''.join((
            PTN_CLLTDHD, '(?P<name>', ptn_impwd, ')', PTN_AFTNAME)))
    rgx_impib = regex.compile(''.join((
            PTN_CLGENHD, '(?P<name>', ptn_impwd, ')', PTN_AFTGENWD)))
    rgx_impic = regex.compile(''.join((
            PTN_CLGENHD, '(?P<name>', ptn_impwd, ')', PTN_AFTNAME)))
    clno_max = len(cl_dic.keys())
    for eacl in cl_dic.keys():
        if eacl not in cl_tgtlinedic.keys():
            p_warn_lines.append(''.join((
                    '★eTS■★clTS請求項', str(eacl),
                    '★clTEに文尾の全角句点「。」がありません★wTE')))
            p_warn_lines.append('★eTS■分析を中止します★wTE')
            return (p_ngline_nums, p_warn_lines, p_cl_lines, p_cl_elines,
                    p_clel_lines, p_tr_lines, p_trel_lines, p_spc_lines,
                    p_spc_elines, p_spchd_lines, p_spccl_lines,
                    p_abs_lines, p_fig_lines, p_ref_lines, p_wd_lines,
                    p_wdlist_lines, p_a_array, p_array_tip, p_array_ef)
    if cl_nounset:
        tmp_ptnnounphr = '|'.join(cl_nounset)
        tmp_ptnhirawd = regex.sub('＜★＞', tmp_ptnnounphr, PTN_HIRAWD)
    else:
        tmp_ptnhirawd = PTN_HIRAWD
    ptn_11x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            r'[いえきけしせちてねみめりれぎげじぜび][\p{Han}]'
            '[いえきけしせちてねみめりれぎげじぜび]'
            r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
            '[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_11xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_11x, PTN_AFTGT))
    rgx_11xa = regex.compile(ptn_11xa)
    ptn_12x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            r'[いえきけしせちてねみめりれぎげじぜび][\p{Han}]'
            '[いえきけしせちてねみめりれぎげじぜび][A-Za-zＡ-Ｚａ-ｚ]*'
            r'[ー・\p{Katakana}\p{Han}]+)'))
    ptn_12xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_12x, PTN_AFTGT))
    rgx_12xa = regex.compile(ptn_12xa)
    ptn_13x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            r'[いえきけしせちてねみめりれぎげじぜび][\p{Han}]+'
            '[いえきけしせちてねみめりれぎげじぜび])'))
    ptn_13xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_13x, PTN_AFTGT))
    rgx_13xa = regex.compile(ptn_13xa)
    ptn_21x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いえきけしせちてねみめりれぎげじぜび]'
            r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
            '[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_21xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_21x, PTN_AFTGT))
    rgx_21xa = regex.compile(ptn_21xa)
    ptn_22x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いえきけしせちてねみめりれぎげじぜび][A-Za-zＡ-Ｚａ-ｚ]*'
            r'[ー・\p{Katakana}\p{Han}]+)'))
    ptn_22xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_22x, PTN_AFTGT))
    rgx_22xa = regex.compile(ptn_22xa)
    ptn_23x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*)',
            tmp_ptnhirawd,
            r'?([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いえきけしせちてねみめりれぎげじぜび]))'))
    ptn_23xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_23x, PTN_AFTGT))
    rgx_23xa = regex.compile(ptn_23xa)
    ptn_31x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
            '[A-Za-zＡ-Ｚａ-ｚ]*[-－―・／/]?[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_31xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_31x, PTN_AFTGT))
    rgx_31xa = regex.compile(ptn_31xa)
    ptn_32x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
            r'[ー・\p{Katakana}\p{Han}]+)'))
    ptn_32xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_32x, PTN_AFTGT))
    rgx_32xa = regex.compile(ptn_32xa)
    ptn_40x = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*)',
            tmp_ptnhirawd, r'([ー・\p{Katakana}\p{Han}]*))'))
    ptn_40xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_40x, PTN_AFTGT))
    rgx_40xa = regex.compile(ptn_40xa)
    ptn_50x = ''.join(('(?P<name>', PTN_ENWDS, ')'))
    ptn_50xa = ''.join((PTN_B4TGT, PTN_ADJ, ptn_50x, PTN_AFTGT))
    rgx_50xa = regex.compile(ptn_50xa)
    ptn_90xa = ''.join((PTN_B4TGT, PTN_ADJ, PTN_NOUN, PTN_AFTGT))
    rgx_90xa = regex.compile(ptn_90xa)
    ptn_95x = '[^のたる]*[のたる](?P<name>[^のたる]+)'
    ptn_95xa = ''.join((ptn_95x, PTN_AFTGT))
    rgx_95xa = regex.compile(ptn_95xa)
    ptn_11 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけさしすせちつてなねひみむめりるれぎげじぜぢびべ]'
            r'[\p{Han}]'
            '[いうえきくけさしすせちつてなねひみむめりるれぎげじぜぢびべ]'
            r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
            '[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_11a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_11, PTN_AFTNAME))
    rgx_11a = regex.compile(ptn_11a)
    ptn_11b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_11, PTN_AFTNAME))
    rgx_11b = regex.compile(ptn_11b)
    ptn_12 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけさしすせちつてなねひみむめりるれぎげじぜぢびべ]'
            r'[\p{Han}]'
            '[いうえきくけさしすせちつてなねひみむめりるれぎげじぜぢびべ]'
            r'[A-Za-zＡ-Ｚａ-ｚ]*[ー・\p{Katakana}\p{Han}]+)'))
    ptn_12a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_12, PTN_AFTNAME))
    rgx_12a = regex.compile(ptn_12a)
    ptn_12b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_12, PTN_AFTNAME))
    rgx_12b = regex.compile(ptn_12b)
    ptn_13 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけさしすせちつてなねひみむめりるれぎげじぜぢびべ]'
            r'[\p{Han}]+[いえきけしせちてねみめりれぎげじぜび])'))
    ptn_13a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_13, PTN_AFTNAME))
    rgx_13a = regex.compile(ptn_13a)
    ptn_13b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_13, PTN_AFTNAME))
    rgx_13b = regex.compile(ptn_13b)
    ptn_21 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけさしすせちつてなねひみむめりるれぎげじぜぢびべ]'
            r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
            '[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_21a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_21, PTN_AFTNAME))
    rgx_21a = regex.compile(ptn_21a)
    ptn_21b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_21, PTN_AFTNAME))
    rgx_21b = regex.compile(ptn_21b)
    ptn_22 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いうえきくけさしすせちつてなねひみむめりるれぎげじぜぢびべ]'
            r'[A-Za-zＡ-Ｚａ-ｚ]*[ー・\p{Katakana}\p{Han}]+)'))
    ptn_22a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_22, PTN_AFTNAME))
    rgx_22a = regex.compile(ptn_22a)
    ptn_22b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_22, PTN_AFTNAME))
    rgx_22b = regex.compile(ptn_22b)
    ptn_23 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*)',
            tmp_ptnhirawd,
            r'?([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
            '[いえきけしせちてねみめりれぎげじぜび]))'))
    ptn_23a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_23, PTN_AFTNAME))
    rgx_23a = regex.compile(ptn_23a)
    ptn_23b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_23, PTN_AFTNAME))
    rgx_23b = regex.compile(ptn_23b)
    ptn_31 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
            '[A-Za-zＡ-Ｚａ-ｚ]*[-－―・／/]?[A-Za-zＡ-Ｚａ-ｚ]+)'))
    ptn_31a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_31, PTN_AFTNAME))
    rgx_31a = regex.compile(ptn_31a)
    ptn_31b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_31, PTN_AFTNAME))
    rgx_31b = regex.compile(ptn_31b)
    ptn_32 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
            r'[ー・\p{Katakana}\p{Han}]+)'))
    ptn_32a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_32, PTN_AFTNAME))
    rgx_32a = regex.compile(ptn_32a)
    ptn_32b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_32, PTN_AFTNAME))
    rgx_32b = regex.compile(ptn_32b)
    ptn_40 = ''.join((
            '(?P<name>', PTN_ENWDS,
            r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*)',
            tmp_ptnhirawd, r'([ー・\p{Katakana}\p{Han}]*))'))
    ptn_40a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_40, PTN_AFTNAME))
    rgx_40a = regex.compile(ptn_40a)
    ptn_40b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_40, PTN_AFTNAME))
    rgx_40b = regex.compile(ptn_40b)
    ptn_50 = ''.join(('(?P<name>', PTN_ENWDS, ')'))
    ptn_50a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, ptn_50, PTN_AFTNAME))
    rgx_50a = regex.compile(ptn_50a)
    ptn_50b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, ptn_50, PTN_AFTNAME))
    rgx_50b = regex.compile(ptn_50b)
    ptn_90a = ''.join(('^', PTN_CLLTDHD, PTN_ADJ, PTN_NOUN))
    rgx_90a = regex.compile(ptn_90a)
    ptn_90b = ''.join(('^', PTN_CLGENHD, PTN_ADJ, PTN_NOUN))
    rgx_90b = regex.compile(ptn_90b)
    for eacl in cl_tgtlinedic.keys():
        _cltgtextr(eacl, cl_tgtlinedic[eacl])
    for eacl in cl_dic.keys():
        claim_ref = _clrefextr(eacl)
        cl_refdic[eacl] = sorted(claim_ref)
    for eacl in cl_refdic.keys():
        if not cl_refdic[eacl]:
            _cliclwdchk(eacl)
    _clstrdicmod()
    for eacl in cl_dic.keys():
        clblks, cljwds, clerrjwds = _cljwdextr(eacl)
        cl_blkdic[eacl] = clblks
        cl_jwddic[eacl] = cljwds
        cl_errjwddic[eacl] = clerrjwds
        for jwd in cljwds:
            cl_alljwdset.add(jwd)
    rgx_ptn = regex.compile(
            r'([^A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]+)'
            r'(?P<word>[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]+)$')
    for strtgt in cl_alljwdset:
        mres = rgx_ptn.search(strtgt)
        if mres:
            endword = mres.group('word')
            cl_endwdset.add(endword)
    prntflg = False
    for eacl in sorted(cl_errjwddic.keys()):
        if cl_errjwddic[eacl]:
            if not prntflg:
                prntflg = True
                p_warn_lines.append(
                        '★eTS■全参照範囲に同一用語がない参照的記載が'
                        'あります★wTE')
            errInfo = ', '.join(cl_errjwddic[eacl])
            p_warn_lines.append(''.join((
                    '・★ctTAcl', str(eacl), '★ctTB請求項',
                    str(eacl), '★ctTC:', errInfo)))
    rgx_clendwd = regex.compile(''.join(('(', '|'.join(cl_endwdset), ')$')))
    for eacl in cl_dic.keys():
        cliwds = _cliwdextr(eacl)
        cl_iwddic[eacl] = cliwds
    for eacl in cl_tgtdic.keys():
        cltgtwd = cl_tgtdic[eacl]
        if '？' == cltgtwd:
            p_warn_lines.append(''.join((
                    '★wTS■請求対象の記載が不適切な可能性があります'
                    '★wTE:★ctTAcl', str(eacl), '★ctTB請求項',
                    str(eacl), '★ctTC')))
        cl_iwddic[eacl].add(cltgtwd)
    for eacl in cl_dic.keys():
        cl_mwddic[eacl] = cl_iwddic[eacl] | cl_jwddic[eacl]
    for key in cl_alljwdset:
        key00 = _delmrkconj(key)
        cl_kwddic[key00] = []
        for eacl in sorted(cl_iwddic.keys()):
            if key in cl_iwddic[eacl]:
                cl_kwddic[key00].append(eacl)
        for eacl in sorted(cl_jwddic.keys()):
            if key in cl_jwddic[eacl]:
                cl_kwddic[key00].append(-eacl)
    for eacl in sorted(cl_iwddic.keys()):
        for wd in cl_iwddic[eacl]:
            if wd not in cl_alljwdset:
                wd00 = _delmrkconj(wd)
                if wd00 not in cl_onlyiwddic:
                    cl_onlyiwddic[wd00] = [eacl]
                else:
                    cl_onlyiwddic[wd00].append(eacl)
    _clwdsetgen()
    _clnonverbs()
    prgrss = 7
    _clpgana()
    _clstrgana()
    _clstructana()
    _cldicintgr()
    _clwdprichg()
    _clelextr()
    misspeltwds = _clwdsetchk()
    if misspeltwds:
        p_warn_lines.append(
                '★wTS■全角文字/半角文字について不統一な用語があります★wTE')
        for (word1, word2) in misspeltwds:
            p_warn_lines.append(''.join(('・', word1, '←→', word2)))
    if eb_dic:
        ptnwdhd1 = ''.join(('^', PTN_CLLTDHD, '用?'))
        rgx_wdhd1 = regex.compile(ptnwdhd1)
        ptnwdhd2 = ''.join(('^', PTN_CLGENHD))
        rgx_wdhd2 = regex.compile(ptnwdhd2)
        wordbody_set = set()
        for wd in wd_set:
            if rgx_wdhd1.search(wd):
                tmp_wd = rgx_wdhd1.sub('', wd)
                if tmp_wd:
                    wordbody_set.add(tmp_wd)
            if rgx_wdhd2.search(wd):
                tmp_wd = rgx_wdhd1.sub('', wd)
                if tmp_wd:
                    wordbody_set.add(tmp_wd)
        if wordbody_set:
            wd_set = wd_set | wordbody_set
        imp_wdset = wd_set | rf_refdic.keys() | je_wddic.keys()
        imp_wd_enend_set = set()
        imp_wd_jpend_set = set()
        for wd in imp_wdset:
            if rgx_englishend.search(wd):
                imp_wd_enend_set.add(wd)
            else:
                imp_wd_jpend_set.add(wd)
        ptnimpwdenend = ''.join(('(', '|'.join(imp_wd_enend_set), ')'))
        ptnimpwdjpend = ''.join(('(', '|'.join(imp_wd_jpend_set), ')'))
        rgx_ebwdhd = regex.compile(
            '^(第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+'
            '([,，、～]|＋★［[^＋]+］★＋))*'
            '第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+の?')
        rgx_ebnum = regex.compile(
                '^第[0-9０-９一二三四五六七八九十Ⅰ-Ⅻⅰ-ⅻIVXivx]+'
                '[,，、～＋]')
        rgx_ebgrpref1 = regex.compile(PTN_EBGRPRF1)
        rgx_imprefenend = regex.compile(''.join((
                r'(^|[^A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}])',
                PTN_EBHD, '(?P<name>', PTN_NONEEDWD, '?',
                ptnimpwdenend, ')', PTN_EBRFAFTEN,
                PTN_EBGRPRF, PTN_EBAFTRF)))
        rgx_imprefjpend = regex.compile(''.join((
                r'(^|[^A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}])',
                PTN_EBHD, '(?P<name>', PTN_NONEEDWD, '?',
                ptnimpwdjpend, ')', PTN_RF, PTN_EBGRPRF,
                PTN_EBAFTRF)))
        ptn_11eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                r'[いえきけせちてねみめりれぎげじぜび][\p{Han}]'
                '[いえきけせちてねみめりれぎげじぜび]'
                r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
                '[A-Za-zＡ-Ｚａ-ｚ]+)', PTN_EBRFAFTEN, PTN_EBGRPRF,
                PTN_EBAFTRF))
        rgx_11eb = regex.compile(ptn_11eb)
        ptn_12eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                r'[いえきけせちてねみめりれぎげじぜび][\p{Han}]'
                '[いえきけせちてねみめりれぎげじぜび][A-Za-zＡ-Ｚａ-ｚ]*'
                r'[ー・\p{Katakana}\p{Han}]+)', PTN_RF, PTN_EBGRPRF,
                PTN_EBAFTRF))
        rgx_12eb = regex.compile(ptn_12eb)
        ptn_13eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                r'[いえきけせちてねみめりれぎげじぜび][\p{Han}]+'
                '[いえきけせちてねみめりれぎげじぜび])', PTN_RF,
                PTN_EBGRPRF, PTN_EBAFTRF))
        rgx_13eb = regex.compile(ptn_13eb)
        ptn_21eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                '[いえきけせちてねみめりれぎげじぜび]'
                r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+'
                '[-－―・／/]?[A-Za-zＡ-Ｚａ-ｚ]+)', PTN_EBRFAFTEN,
                PTN_EBGRPRF, PTN_EBAFTRF))
        rgx_21eb = regex.compile(ptn_21eb)
        ptn_22eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                '[いえきけしせちてねみめりれぎげじぜび][A-Za-zＡ-Ｚａ-ｚ]*'
                r'[ー・\p{Katakana}\p{Han}]+)', PTN_RF, PTN_EBGRPRF,
                PTN_EBAFTRF))
        rgx_22eb = regex.compile(ptn_22eb)
        ptn_23eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*)',
                PTN_HIRAWD,
                r'?([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                '[いえきけせちてねみめりれぎげじぜび]))', PTN_RF,
                PTN_EBGRPRF, PTN_EBAFTRF))
        rgx_23eb = regex.compile(ptn_23eb)
        ptn_31eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
                '[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?[A-Za-zＡ-Ｚａ-ｚ]+)',
                PTN_EBRFAFTEN, PTN_EBGRPRF, PTN_EBAFTRF))
        rgx_31eb = regex.compile(ptn_31eb)
        ptn_32eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
                r'[ー・\p{Katakana}\p{Han}]+)',
                PTN_RF, PTN_EBGRPRF, PTN_EBAFTRF))
        rgx_32eb = regex.compile(ptn_32eb)
        ptn_40eb = ''.join((
                PTN_EBHD, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*',
                PTN_HIRAWD, r'[ー・\p{Katakana}\p{Han}]*)',
                PTN_RF, PTN_EBGRPRF, PTN_EBAFTRF))
        rgx_40eb = regex.compile(ptn_40eb)
        ptn_50eb = ''.join((
            PTN_EBHD, '(?P<name>', PTN_ENWDS, ')',
            PTN_EBRFAFTEN, PTN_EBGRPRF, PTN_EBAFTRF))
        rgx_50eb = regex.compile(ptn_50eb)
        rgx_noneedwds = regex.compile(''.join(('^', PTN_NONEEDWD)))
        rgx_refchk01 = regex.compile('^[A-Za-z][/A-Za-z]{2,}')
        rgx_refchk02 = regex.compile('^([A-Z][a-z]|[a-z][A-Z]|[A-Z]{2})')
        rgx_refchk03 = regex.compile('^[A-Z]')
        rgx_refchk04 = regex.compile('^([0-9]+)(?P<unitword>[^0-9]{1,2})')
        rgx_chemwd = regex.compile(''.join(('(', '|'.join(EB_CHEMWDS), ')$')))
        rgx_noneedend = regex.compile(''.join((PTN_NONEEDEND, '$')))
        rgx_impex = regex.compile(''.join((
                r'(^|[^A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}])',
                PTN_EBHD4NORF, '(?P<name>', PTN_NONEEDWD,
                '?', ptn_impwd, ')', PTN_AFTNAME)))
        ptn_11ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                r'[いえきけせちてねみめりれぎげじぜび][\p{Han}]'
                '[いえきけせちてねみめりれぎげじぜび]'
                r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
                '[A-Za-zＡ-Ｚａ-ｚ]+)', PTN_AFTNAME))
        rgx_11ex = regex.compile(ptn_11ex)
        ptn_12ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                r'[いえきけせちてねみめりれぎげじぜび][\p{Han}]'
                '[いえきけせちてねみめりれぎげじぜび][A-Za-zＡ-Ｚａ-ｚ]*'
                r'[ー・\p{Katakana}\p{Han}]+)', PTN_AFTNAME))
        rgx_12ex = regex.compile(ptn_12ex)
        ptn_13ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                r'[いえきけせちてねみめりれぎげじぜび][\p{Han}]+'
                '[いえきけせちてねみめりれぎげじぜび])', PTN_AFTNAME))
        rgx_13ex = regex.compile(ptn_13ex)
        ptn_21ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                '[いえきけせちてねみめりれぎげじぜび]'
                r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?'
                '[A-Za-zＡ-Ｚａ-ｚ]+)', PTN_AFTNAME))
        rgx_21ex = regex.compile(ptn_21ex)
        ptn_22ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*[\p{Han}]+'
                '[いえきけせちてねみめりれぎげじぜび][A-Za-zＡ-Ｚａ-ｚ]*'
                r'[ー・\p{Katakana}\p{Han}]+)', PTN_AFTNAME))
        rgx_22ex = regex.compile(ptn_22ex)
        ptn_24ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'([A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*',
                PTN_HIRAWD,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*|'
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]+)[\p{Han}]'
                '[いえきけしせちてねみめりれぎげじぜび])', PTN_AFTNAME))
        rgx_24ex = regex.compile(ptn_24ex)
        ptn_31ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
                '[A-Za-zＡ-Ｚａ-ｚ]+[-－―・／/]?[A-Za-zＡ-Ｚａ-ｚ]+)',
                PTN_AFTNAME))
        rgx_31ex = regex.compile(ptn_31ex)
        ptn_32ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*'
                r'[ー・\p{Katakana}\p{Han}]+)', PTN_AFTNAME))
        rgx_32ex = regex.compile(ptn_32ex)
        ptn_40ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS,
                r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*',
                PTN_HIRAWD, r'[ー・\p{Katakana}\p{Han}]*)', PTN_AFTNAME))
        rgx_40ex = regex.compile(ptn_40ex)
        ptn_50ex = ''.join((
                PTN_EBHD4NORF, '(?P<name>', PTN_ENWDS, ')', PTN_AFTNAME))
        rgx_50ex = regex.compile(ptn_50ex)
        for key in rf_refdic.keys():
            for earef in rf_refdic[key]:
                rf_okset.add(earef)
        prgrss = 14
        _ebana()
    _clkwdprc()
    if eb_wdinfodic:
        _ebkwdprc()
    _clinfogen()
    _cleltr()
    _cltr()
    _clstructtr()
    _refgen()
    _figgen()
    _abstgen()
    prgrss = 60
    if spc_basedic:
        _spczinfogen()
    prgrss = 90
    _spcgen()
    _tipdicgen()
    if ef_spclines:
        _efspcphrextr()
    _impkwdjegen()
    _clwdarraygen()
    _clkwdsetgen()
    if eb_wdinfodic:
        _ebwdarraygen()
        _ebkwdsetgen()
    tmp_lines = p_warn_lines.copy()
    p_warn_lines = [_delmrkconj(eastr) for eastr in tmp_lines]
    if not p_warn_lines:
        p_warn_lines.append('★wTS■Warningなし★wTE')
    prgrss = 100
    return (
            p_ngline_nums, p_warn_lines, p_cl_lines, p_cl_elines,
            p_clel_lines, p_tr_lines, p_trel_lines, p_spc_lines,
            p_spc_elines, p_spchd_lines, p_spccl_lines, p_abs_lines,
            p_fig_lines, p_ref_lines, p_wd_lines, p_wdlist_lines,
            p_a_array, p_array_tip, p_array_ef)


def _delmrkconj(msg):
    newmsg = msg.replace('＋★［', '').replace('］★＋', '')
    return newmsg


def _wtag(lineno, clnum, spcnum, paranum):
    global p_ngline_nums
    if lineno not in p_ngline_nums:
        p_ngline_nums.add(lineno)
    linelnk = ''.join((
            '★ltTAl', str(lineno), '★ltTB原文line', str(lineno), '★ltTC'))
    cllnk = ''
    if 0 < clnum:
        cllnk = ''.join((
                '(★ctTAcl', str(clnum), '★ctTB請求項', str(clnum),
                '★ctTC)'))
    paralnk = ''
    if 0 < spcnum:
        if 0 < paranum:
            paralnk = ''.join((
                    '(★ptTApa', str(paranum), '★ptTB段落', str(paranum),
                    '★ptTC)'))
    mixlnk = ''.join((linelnk, cllnk, paralnk))
    return mixlnk


def _cchk(srctxline, lineno, clnum, spcnum, paranum, hdspchkflg):
    global HAN_KANA
    global ZEN_KANA
    global p_warn_lines
    global rgx_ctrl
    global rgx_nosps
    global rgx_headsps
    global rgx_2typesp
    global rgx_linehdok
    global rgx_nbsp
    global rgx_mspace
    global rgx_mcomma
    global rgx_mperiod
    global rgx_ngcircle
    global rgx_nghan
    global rgx_ngchr
    global rgx_ngmarunum
    newtxline = srctxline
    mres = rgx_ctrl.findall(newtxline)
    reslist = []
    for res in mres:
        reslist.append(res.encode('utf-8').hex())
    if reslist:
        srctxline = rgx_ctrl.sub('▲', newtxline)
        mixlnk = _wtag(lineno, clnum, spcnum, paranum)
        p_warn_lines.append(''.join((
                '★wTS■不正制御文字(tab等)がありました'
                '(削除して分析を行います)★wTE:x', ', x'.join(reslist),
                '(16進:原文中▲表記) in ', mixlnk, '「', srctxline, '」')))
        newtxline = rgx_ctrl.sub('', newtxline)
    res = rgx_nosps.search(newtxline)
    if not res:
        newtxline = ''
        mixlnk = _wtag(lineno, clnum, spcnum, paranum)
        p_warn_lines.append(''.join((
                '★wTS■空行があります'
                '(空白のみ又は改頁の場合もあります)★wTE:', mixlnk)))
    else:
        if hdspchkflg:
            res = rgx_headsps.search(newtxline)
            if res:
                if rgx_2typesp.search(res.group()):
                    tmp_zensp = rgx_2typesp.sub('', res.group())
                    if not tmp_zensp:
                        tmp_zensp = '　'
                        newtxline = ''.join((
                                tmp_zensp, newtxline[res.span()[1]:]))
                        mixlnk = _wtag(lineno, clnum, spcnum, paranum)
                        p_warn_lines.append(''.join((
                                '★wTS■行頭部分に半角空白がありました'
                                '(１つの全角空白にして分析を行います)★wTE:',
                                mixlnk, '「', srctxline, '」')))
                    else:
                        newtxline = ''.join((
                                tmp_zensp, newtxline[res.span()[1]:]))
                        mixlnk = _wtag(lineno, clnum, spcnum, paranum)
                        p_warn_lines.append(''.join((
                                '★wTS■行頭部分に半角空白がありました'
                                '(削除して分析を行います)★wTE:', mixlnk,
                                '「', srctxline, '」')))
            res = rgx_linehdok.search(newtxline)
            if not res:
                mixlnk = _wtag(lineno, clnum, spcnum, paranum)
                p_warn_lines.append(''.join((
                        '★wTS■文頭に空白がありません★wTE:', mixlnk,
                        '「', srctxline, '」')))
        if rgx_nbsp.search(newtxline):
            newtxline = rgx_nbsp.sub(r'\x20', newtxline)
            mixlnk = _wtag(lineno, clnum, spcnum, paranum)
            p_warn_lines.append(''.join((
                    '★wTS■特別な半角空白(NO-BREAK SPACE)がありました'
                    '(普通の半角空白にして分析を行います)★wTE:',
                    mixlnk, '「', srctxline, '」')))
        if rgx_mspace.search(newtxline):
            newtxline = rgx_mspace.sub(r'\x20', newtxline)
            mixlnk = _wtag(lineno, clnum, spcnum, paranum)
            p_warn_lines.append(''.join((
                    '★wTS■連続した半角空白がありました'
                    '(半角空白を１つにして分析を行います)★wTE:',
                    mixlnk, '「', srctxline, '」')))
        if rgx_mcomma.search(newtxline):
            newtxline = rgx_mcomma.sub('、', newtxline)
            mixlnk = _wtag(lineno, clnum, spcnum, paranum)
            p_warn_lines.append(''.join((
                    '★wTS■連続した読点がありました'
                    '(読点を１つにして分析を行います)★wTE:', mixlnk,
                    '「', srctxline, '」')))
        if rgx_mperiod.search(newtxline):
            newtxline = rgx_mperiod.sub('。', newtxline)
            mixlnk = _wtag(lineno, clnum, spcnum, paranum)
            p_warn_lines.append(''.join((
                    '★wTS■連続した句点がありました'
                    '(句点を１つにして分析を行います)★wTE:', mixlnk,
                    '「', srctxline, '」')))
        if rgx_ngcircle.search(newtxline):
            newtxline = rgx_ngcircle.sub('○', newtxline)
            mixlnk = _wtag(lineno, clnum, spcnum, paranum)
            p_warn_lines.append(''.join((
                    '★wTS■不正文字(合成丸◯)がありました'
                    '(○記号に置換して分析を行います)★wTE:', mixlnk,
                    '「', srctxline, '」')))
        mres = rgx_nghan.findall(newtxline)
        reslist = []
        for res in mres:
            reslist.append(res)
        if reslist:
            newtxline = newtxline.translate(newtxline.maketrans(
                    HAN_KANA, ZEN_KANA))
            mixlnk = _wtag(lineno, clnum, spcnum, paranum)
            p_warn_lines.append(''.join((
                    '★wTS■不正文字(半角カナ記号/半角カナ)がありました'
                    '(全角文字に置換して分析を行います)★wTE:',
                    ','.join(reslist), ' in ', mixlnk, '「',
                    srctxline, '」')))
        mres = rgx_ngchr.findall(newtxline)
        reslist = []
        for res in mres:
            reslist.append(res)
        if reslist:
            mixlnk = _wtag(lineno, clnum, spcnum, paranum)
            p_warn_lines.append(''.join((
                    '★eTS■不正文字(丸付き数字/ローマ数字/環境依存文字等)が'
                    'あります★wTE:', ','.join(reslist), ' in ', mixlnk,
                    '「', newtxline, '」')))
        res = rgx_ngmarunum.search(newtxline)
        if not res:
            try:
                newtxline.encode('cp932', 'strict')
            except UnicodeEncodeError:
                mixlnk = _wtag(lineno, clnum, spcnum, paranum)
                p_warn_lines.append(''.join((
                        '★eTS■不正文字(所定Shift_JISコード以外)があります'
                        '★wTE:', mixlnk, '「', newtxline, '」')))
    return newtxline


def _jeextr(txline, impjenum):
    global STR_JEHEAD
    global p_warn_lines
    global je_wddic
    global rgx_hdmk
    global rgx_hd
    global rgx_styledel
    txline = rgx_styledel.sub('', txline)
    res = rgx_hd.search(txline)
    if res:
        heading = res.group('heading')
        if 0 < impjenum:
            impjenum = -1
        else:
            if STR_JEHEAD == heading:
                impjenum = 1
    if 0 < impjenum:
        if not rgx_hdmk.search(txline):
            newtxline = txline.lstrip()
            words = newtxline.split('→')
            jpwd = words[0].strip()
            enwds = words[1:]
            if enwds:
                strenwd = '/'.join(enwds)
                strenwd = strenwd.strip()
            else:
                strenwd = ''
            if jpwd not in je_wddic.keys():
                je_wddic[jpwd] = strenwd
    return impjenum


def _spcextr(txline, lineno, spcnum, paranum):
    global SPC_HEADS
    global STR_RFHEADS
    global eb_dic
    global p_warn_lines
    global prsr
    global prev_paranum
    global rgx_hdmk
    global rgx_quote1, rgx_quote2, rgx_quote3
    global rgx_para
    global rgx_hdbasic
    global rgx_spcend
    global rgx_ebhdno
    global rgx_spchdno
    global spc_basedic
    res = rgx_hdbasic.search(txline)
    if res:
        heading = res.group('heading')
        if 0 < spcnum:
            res1 = rgx_para.search(heading)
            if res1:
                paranum = int(res1.group('paranum'))
                if (prev_paranum+1) != paranum:
                    mixlnk = _wtag(lineno, 0, spcnum, paranum)
                    if 0 == prev_paranum:
                        p_warn_lines.append(''.join((
                                '★wTS■段落番号が適切でないかもしれません'
                                '★wTE:', mixlnk, '「', txline, '」')))
                    else:
                        p_warn_lines.append(''.join((
                                '★eTS■段落番号が連続していません★wTE:',
                                mixlnk, '「', txline, '」')))
                prev_paranum = paranum
            elif rgx_spcend.search(heading):
                spcnum = -1
            else:
                if 2 == spcnum:
                    if STR_RFHEADS == heading:
                        spcnum = 3
                    else:
                        ebendflg = True
                        for heading_eb in EB_HEADS:
                            if heading == heading_eb:
                                ebendflg = False
                                break
                        if ebendflg:
                            if rgx_ebhdno.search(heading):
                                ebendflg = False
                        if ebendflg:
                            spcnum = 1
                elif 3 == spcnum:
                    ebstartflg = False
                    for heading_eb in EB_HEADS:
                        if heading == heading_eb:
                            ebstartflg = True
                            break
                    if not ebstartflg:
                        if rgx_ebhdno.search(heading):
                            ebstartflg = True
                    if ebstartflg:
                        spcnum = 2
                    else:
                        spcnum = 1
                else:
                    if STR_RFHEADS == heading:
                        spcnum = 3
                    else:
                        for heading_eb in EB_HEADS:
                            if heading == heading_eb:
                                spcnum = 2
                                break
                        if 2 != spcnum:
                            if rgx_ebhdno.search(heading):
                                spcnum = 2
                if 0 != paranum:
                    for spcheading in SPC_HEADS:
                        if heading == spcheading:
                            paranum = 0
                            break
                if 0 != paranum:
                    if rgx_spchdno.search(heading):
                        paranum = 0
        else:
            if STR_RFHEADS == heading:
                spcnum = 3
            else:
                for heading_eb in EB_HEADS:
                    if heading == heading_eb:
                        spcnum = 2
                        break
                if 2 != spcnum:
                    if rgx_ebhdno.search(heading):
                        spcnum = 2
            if 2 > spcnum:
                for spcheading in SPC_HEADS:
                    if heading == spcheading:
                        spcnum = 1
                        break
                if 1 != spcnum:
                    if rgx_spchdno.search(heading):
                        spcnum = 1
    if 0 < spcnum:
        spc_basedic[lineno] = txline
        if 2 == spcnum:
            if not rgx_hdmk.search(txline):
                newtxline = txline.lstrip()
                newtxline = rgx_quote1.sub('＊', newtxline)
                newtxline = rgx_quote2.sub('＊', newtxline)
                newtxline = rgx_quote3.sub('＊', newtxline)
                blk = prsr._transform_tx(newtxline)
                blk = regex.sub('、、', '、', blk)
                eb_dic[lineno] = blk
        if 3 == spcnum:
            if not rgx_hdmk.search(txline):
                newtxline = txline.lstrip()
                _ref_ana(newtxline, lineno)
    return spcnum, paranum


def _ref_ana(strline, lineno):
    global p_warn_lines
    global rf_refdic
    global rgx_parentheses
    global rgx_refwd
    global rgx_chkref
    res = rgx_refwd.search(strline)
    if res:
        references = res.group('ref')
        tmp_reflist = natsorted(regex.split('[、，,]', references))
        reflist = []
        for earef in tmp_reflist:
            if rgx_chkref.search(earef):
                reflist.append(earef)
            else:
                mixlnk = _wtag(lineno, 0, 0, 0)
                p_warn_lines.append(''.join((
                        '★wTS■【符号の説明】の「', earef, '」が符号'
                        'として適切ではありません★wTE:', mixlnk, '「',
                        strline, '」')))
        if reflist:
            strwd = res.group('word')
            strwd = strwd.strip()
            if strwd:
                resw = rgx_parentheses.search(strwd)
                if resw:
                    firstname = rgx_parentheses.sub('', strwd)
                    if firstname not in rf_refdic.keys():
                        rf_refdic[firstname] = reflist
                    if regex.search(r'[\)）]$', strwd):
                        second_name = regex.sub(r'[\(（\)）]', '', resw[0])
                        if second_name not in rf_refdic.keys():
                            rf_refdic[second_name] = reflist
                else:
                    if strwd not in rf_refdic.keys():
                        rf_refdic[strwd] = reflist


def _claimextr(txline, lineno, claimno, lastline):
    global ZEN_NUM
    global HAN_NUM
    global HD_CMTBLK
    global p_warn_lines
    global prsr
    global cl1_list
    global cl_dic
    global cl_basedic
    global cl_strdic
    global cl_cmtdic
    global cl_tgtlinedic
    global rgx_clhd
    global rgx_clcmt
    global rgx_clend
    global rgx_hannum
    lastclaimno = claimno
    res0 = regex.search('【請求項.*】', txline)
    if res0:
        if regex.search('[^ 　]', txline[:res0.span()[0]]):
            mixlnk = _wtag(lineno, 0, 0, 0)
            p_warn_lines.append(''.join((
                    '★eTS■請求項の表記が正しくありません★wTE:',
                    mixlnk, '「', txline, '」')))
            p_warn_lines.append('★eTS■分析を中止します★wTE')
            return False, claimno
        res = rgx_clhd.search(txline)
        if res:
            strclno = res.group('clno')
            clno = int(strclno)
            if 1 == clno:
                cl1_list = []
            if claimno == clno:
                mixlnk = _wtag(lineno, claimno, 0, 0)
                p_warn_lines.append(''.join((
                        '★wTS■請求項の番号が重複しています(先行の請求項',
                        str(claimno), 'を無視して分析を行います)★wTE:',
                        mixlnk, '「', txline, '」')))
            else:
                claimno = clno
            cl_dic[claimno] = []
            cl_basedic[claimno] = []
            cl_strdic[claimno] = ''
            cl_cmtdic[claimno] = ''
            newtxline = txline
            resc = rgx_hannum.search(strclno)
            if resc:
                strnewclno = strclno.translate(
                        strclno.maketrans(HAN_NUM, ZEN_NUM))
                mixlnk = _wtag(lineno, claimno, 0, 0)
                p_warn_lines.append(''.join((
                        '★wTS■請求項番中に半角数字がありました'
                        '(全角数字にして分析を行います)★wTE:', mixlnk, '「',
                        res.group(), '」→「【請求項', strnewclno, '】」')))
                newtxline = txline.replace(''.join((
                        '【請求項', strclno, '】')),
                        ''.join(('【請求項', strnewclno, '】')))
            if lastline.startswith(HD_CMTBLK):
                cl_basedic[claimno].append(lastline)
                cl_cmtdic[claimno] = lastline[len(HD_CMTBLK):]
            else:
                tmp_txline = rgx_clcmt.sub('', newtxline)
                cl_cmtdic[claimno] = tmp_txline.replace(
                        '（', '').replace('）', '')
            cl_basedic[claimno].append(newtxline)
        else:
            mixlnk = _wtag(lineno, 0, 0, 0)
            p_warn_lines.append(''.join((
                    '★eTS■請求項の表記が正しくありません★wTE:',
                    mixlnk, '「', txline, '」')))
            p_warn_lines.append('★eTS■分析を中止します★wTE')
            return False, claimno
    else:
        if 0 < claimno:
            res = rgx_clend.search(txline)
            if res:
                claimno = -1
            else:
                stripped_txline = txline.lstrip()
                if stripped_txline:
                    newtxline = txline
                    stripped_new_txline = newtxline.lstrip()
                    if 1 == claimno:
                        cl1_list.append(stripped_new_txline)
                    blk = prsr._transform_tx(stripped_new_txline)
                    blk = regex.sub('、、', '、', blk)
                    cl_dic[claimno].append(blk)
                    _clnounextr(blk)
                    cl_basedic[claimno].append(newtxline)
                    if stripped_new_txline.endswith('。'):
                        cl_tgtlinedic[claimno] = stripped_new_txline
                    cl_strdic[claimno] = ''.join((
                            cl_strdic[claimno], newtxline))
    if 0 < claimno:
        if (lastclaimno+1) != claimno:
            if lastclaimno != claimno:
                if 0 != lastclaimno:
                    p_warn_lines.append(
                            '★eTS■請求項が連番ではありません★wTE')
                    p_warn_lines.append(''.join((
                            '・★clTS請求項', str(lastclaimno),
                            '★clTE→★clTS請求項', str(claimno),
                            '★clTE')))
                else:
                    p_warn_lines.append(
                            '★eTS■★clTS請求項１★clTEがありません★wTE')
                p_warn_lines.append('★eTS■分析を中止します★wTE')
                return False, claimno
    return True, claimno


def _clnounextr(blk):
    global cl_nounset
    global rgx_noun
    global rgx_mhira
    global rgx_ovrhira
    newblk = prsr._transform_clnoun(blk)
    mres = rgx_noun.finditer(newblk)
    for res in mres:
        noun_phr = regex.sub('(＋★＜|＞★＋)', '', res.group('noun'))
        if 1 < len(noun_phr):
            if rgx_mhira.search(noun_phr):
                if not rgx_ovrhira.search(noun_phr):
                    cl_nounset.add(noun_phr)


def _cltgtextr(clnum, target_line):
    global cl_tgtdic
    global rgx_parentheses
    global rgx_11xa, rgx_12xa, rgx_13xa
    global rgx_21xa, rgx_22xa, rgx_23xa
    global rgx_31xa, rgx_32xa
    global rgx_40xa
    global rgx_50xa
    global rgx_90xa
    global rgx_95xa
    global rgx_impxa
    global rgx_ovrhira
    tgtwds = set()
    blk = rgx_parentheses.sub('', target_line)
    blka = prsr._transform_cladj(blk)
    if rgx_impxa is not None:
        res = rgx_impxa.search(blka)
        if res:
            nameadj = res.group('adjective')
            namebody = res.group('name')
            if namebody:
                name = ''.join((nameadj, namebody))
                tgtwds.add(name)
    res = rgx_11xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_12xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_13xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_21xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_22xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_23xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_31xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_32xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_40xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    res = rgx_50xa.search(blka)
    if res:
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((nameadj, namebody))
            tgtwds.add(name)
    blkn = prsr._transform_clnoun(blka)
    res = rgx_90xa.search(blkn)
    if res:
        nameadj = res.group('adjective')
        namebody = regex.sub('(＋★＜|＞★＋)', '', res.group('noun'))
        if namebody:
            name = ''.join((nameadj, namebody))
            if not rgx_ovrhira.search(name):
                tgtwds.add(name)
    if not tgtwds:
        res = rgx_95xa.search(blk)
        if res:
            name = res.group('name')
            if name:
                tgtwds.add(name)
    if tgtwds:
        longwd = sorted(tgtwds, key=len, reverse=True)[0]
        longwdn = regex.sub('(＋★｛|｝★＋)', '', longwd)
        if '記載' != longwdn:
            ptn_tgtr = ''.join((
                    PTN_B4TGT, '(?P<tgtr>',
                    r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]+の',
                    longwdn, ')', PTN_AFTGT))
            res = regex.search(ptn_tgtr, blk)
            if res:
                tgtreal = res.group('tgtr')
                res = regex.search('記載の', tgtreal)
                if res:
                    tgtreal = tgtreal[res.span()[1]:]
            else:
                tgtreal = longwdn
            cl_tgtdic[clnum] = tgtreal
        else:
            cl_tgtdic[clnum] = '？'
    else:
        cl_tgtdic[clnum] = '？'


def _clstrdicmod():
    global cl_tgtdic
    global cl_refdic
    global cl_strdic
    cltgt_set = set(cl_tgtdic.values())
    rgx_verbend = regex.compile('[うくすつぬむるぐぶ]$')
    rgx_refclstrend = regex.compile(''.join((
            r'、?請求項[^記]+記載[\p{Hiragana}]{1,5}(?P<target>(',
            '|'.join((cltgt_set)), '))$')))
    rgx_refclstr = regex.compile(''.join((
            r'、?請求項[^記]+記載[\p{Hiragana}]{1,5}(?P<target>(',
            '|'.join((cltgt_set)), '))')))
    rgx_tgtstrend = regex.compile(''.join((
            r'、?(?P<target>(', '|'.join((cltgt_set)), '))$')))
    for eacl in cl_strdic.keys():
        strcl = cl_strdic[eacl].replace(' ', '').replace(
                '　', '').replace('。', '')
        if cl_refdic[eacl]:
            res = rgx_refclstrend.search(strcl)
            if res:
                strcl = strcl[:res.span()[0]]
            else:
                res = rgx_refclstr.search(strcl)
                if res:
                    res_tgt = res.group('target')
                    strcl = ''.join((
                            strcl[:res.span()[0]], '上述の',
                            res_tgt, strcl[res.span()[1]:]))
                res = rgx_tgtstrend.search(strcl)
                if res:
                    strcl = strcl[:res.span()[0]]
        else:
            res = rgx_tgtstrend.search(strcl)
            if res:
                strcl = strcl[:res.span()[0]]
        res = rgx_verbend.search(strcl)
        if not res:
            strcl = ''.join((strcl, 'ものである'))
        cl_strdic[eacl] = strcl


def _clrefextr(clnum):
    global p_warn_lines
    global cl_dic
    global rgx_refcl
    global rgx_refnum
    global rgx_refnumgrp
    global rgx_hannum
    refclnums = []
    for eastr in cl_dic[clnum]:
        res = rgx_refcl.search(str(eastr))
        if res:
            strrefclaim = res.group('refstr').replace(
                    '１項', '').replace('1項', '').replace(
                    '１つ', '').replace('1つ', '')
            resc = rgx_hannum.search(strrefclaim)
            if resc:
                p_warn_lines.append(''.join((
                        '★wTS■引用先項番中に半角数字があります'
                        '★wTE:★ctTAcl', str(clnum), '★ctTB請求項',
                        str(clnum), '★ctTC「', str(eastr), '」')))
            strrefnums = rgx_refnum.findall(strrefclaim)
            for strrefnum in strrefnums:
                int_num = int(strrefnum)
                if int_num not in refclnums:
                    refclnums.append(int_num)
            refnumgrps = rgx_refnumgrp.finditer(strrefclaim)
            icnt = 0
            for refnumgrp in refnumgrps:
                for i in range(
                        int(refnumgrp.group('from_rfno'))+1,
                        int(refnumgrp.group('to_rfno'))):
                    if i not in refclnums:
                        refclnums.append(i)
                icnt += 1
            if icnt:
                if not regex.search('いずれか', str(eastr)):
                    p_warn_lines.append(''.join((
                            '★wTS■請求項引用が択一的でない可能性があります'
                            '★wTE:★ctTAcl', str(clnum), '★ctTB請求項',
                            str(clnum), '★ctTC「', str(eastr), '」')))
    return refclnums


def _cliclwdchk(clnum):
    global p_warn_lines
    global cl_dic
    global rgx_iclngwd
    for eastr in cl_dic[clnum]:
        mres = rgx_iclngwd.finditer(eastr)
        for res in mres:
            newstr = ''.join((
                    eastr[:res.span()[0]], '『', res.group('ngwd'), '』',
                    eastr[res.span()[1]:]))
            p_warn_lines.append(''.join((
                    '★wTS■独立請求項中に限定的な表現が含まれている可能性が'
                    'あります★wTE:★ctTAcl', str(clnum), '★ctTB請求項',
                    str(clnum), '★ctTC「', newstr, '」')))


def _cljwdextr(clnum):
    global cl_dic
    global rgx_refjwd
    clblks = []
    cljwds = set()
    clerrjwds = set()
    for eastr in cl_dic[clnum]:
        tmpblks = rgx_refjwd.split(eastr)
        lastblk = ''
        for tmpblk in tmpblks:
            if (not regex.search('記載の$', tmpblk) and '前記の' != tmpblk
                    and '上記の' != tmpblk and '前記' != tmpblk
                    and '上記' != tmpblk and '当該' != tmpblk
                    and '該' != tmpblk and '' != tmpblk):
                if (regex.search('記載の$', lastblk) or '前記の' == lastblk
                        or '上記の' == lastblk or '前記' == lastblk
                        or '上記' == lastblk or '当該' == lastblk
                        or '該' == lastblk):
                    if regex.search('記載の$', lastblk):
                        clonly = True
                    else:
                        clonly = False
                    jwd, notjwd, flgok = _cljwdchk(
                            clnum, tmpblk, clblks, clonly)
                    clblks.append(''.join((lastblk, jwd)))
                    if notjwd:
                        clblks.append(notjwd)
                    if flgok:
                        cljwds.add(jwd)
                    else:
                        thejwd = ''.join((lastblk, jwd))
                        clerrjwds.add(thejwd)
                else:
                    clblks.append(tmpblk)
            lastblk = tmpblk
    return clblks, cljwds, clerrjwds


def _cljwdchk(clnum, tgtblk, preblklist, clonly):
    global PTN_WDENDCHR
    global rgx_parentheses
    global rgx_noneedclwds
    global rgx_noneedclwdend
    global rgx_11a, rgx_11b, rgx_12a, rgx_12b, rgx_13a, rgx_13b
    global rgx_21a, rgx_21b, rgx_22a, rgx_22b, rgx_23a, rgx_23b
    global rgx_31a, rgx_31b, rgx_32a, rgx_32b
    global rgx_40a, rgx_40b
    global rgx_50a, rgx_50b
    global rgx_90a, rgx_90b
    global rgx_string
    global rgx_impa, rgx_impb
    okflg = False
    wdcands = set()
    jwd = tgtblk
    blk = rgx_parentheses.sub('', tgtblk)
    blk = prsr._transform_cladj(blk)
    res = rgx_string.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_impa.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_impb.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_11a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_11b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_12a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_12b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_13a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_13b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_21a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_21b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_22a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_22b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_23a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_23b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_31a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_31b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_32a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_32b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_40a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_40b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_50a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_50b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    blk = prsr._transform_clnoun(blk)
    res = rgx_90a.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = regex.sub('(＋★＜|＞★＋)', '', res.group('noun'))
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    res = rgx_90b.search(blk)
    if res:
        namehd = res.group('head')
        nameadj = res.group('adjective')
        namebody = regex.sub('(＋★＜|＞★＋)', '', res.group('noun'))
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, nameadj, namebody))
            wdcands.add(name)
    if wdcands:
        sortedwdcandidates = sorted(wdcands, key=len, reverse=True)
        jwd = sortedwdcandidates[0]
        jwd = regex.sub('(＋★｛|｝★＋)', '', jwd)
        for word in sortedwdcandidates:
            word = regex.sub('(＋★｛|｝★＋)', '', word)
            if not clonly:
                for preblk in preblklist:
                    if word in preblk:
                        okflg = True
                        break
                    elif ('第' in word and 'の' in word
                            and '第' in preblk and 'の' in preblk):
                        res = regex.search(''.join((
                                word.rsplit('の', 1)[0],
                                '(([,，、～]|＋★［[^＋]+］★＋)'
                                '第[0-9０-９一二三四五六七八九十'
                                'Ⅰ-Ⅻⅰ-ⅻIVXivx]+)+の',
                                word.rsplit('の', 1)[1])), preblk)
                        if res:
                            okflg = True
                            break
                if okflg:
                    break
            okflg = _clpathwdsrch(word, clnum)
            if okflg:
                break
        if okflg:
            jwd = word
        else:
            for word in sortedwdcandidates:
                word = regex.sub('(＋★｛|｝★＋)', '', word)
                if 1 < len(word):
                    if regex.search(PTN_WDENDCHR, word):
                        word = word[:-1]
                        if not clonly:
                            for preblk in preblklist:
                                if word in preblk:
                                    okflg = True
                                    break
                            if okflg:
                                break
                        okflg = _clpathwdsrch(word, clnum)
                        if okflg:
                            break
            if okflg:
                jwd = word
    notjwd = tgtblk[len(jwd):]
    return jwd, notjwd, okflg


def _clpathwdsrch(word, clnum):
    global cl_dic
    global cl_refdic
    okflg = False
    pathnum = len(cl_refdic[clnum])
    if 0 != pathnum:
        pathokcnt = 0
        for clrefnum in cl_refdic[clnum]:
            pathokflg = False
            for strline in cl_dic[clrefnum]:
                if word in strline:
                    pathokflg = True
                    break
                elif ('第' in word and 'の' in word
                        and '第' in strline and 'の' in strline):
                    res = regex.search(''.join((
                            word.rsplit('の', 1)[0],
                            '(([,，、～]|＋★［[^＋]+］★＋)'
                            '第[0-9０-９一二三四五六七八九十'
                            'Ⅰ-Ⅻⅰ-ⅻIVXivx]+)+の',
                            word.rsplit('の', 1)[1])), strline)
                    if res:
                        pathokflg = True
                        break
            if pathokflg:
                pathokcnt += 1
            else:
                pathokflg = _clpathwdsrch(word, clrefnum)
                if pathokflg:
                    pathokcnt += 1
        if pathnum == pathokcnt:
            okflg = True
    return okflg


def _cliwdextr(clnum):
    global cl_blkdic
    global rgx_chkrefwd
    cliwds = set()
    for tmpblk in cl_blkdic[clnum]:
        if not rgx_chkrefwd.match(tmpblk):
            if tmpblk:
                iwds = _cliwdchk(tmpblk)
                if iwds:
                    for iwd in iwds:
                        cliwds.add(iwd)
    return cliwds


def _cliwdchk(tgtblk):
    global PTN_AFTJIWD
    global prsr
    global cl_alljwdset
    global rgx_parentheses
    global rgx_noneedclwds
    global rgx_noneedclwdend
    global rgx_11ia, rgx_11ib, rgx_11ic
    global rgx_12ia, rgx_12ib, rgx_12ic
    global rgx_13ia, rgx_13ib, rgx_13ic
    global rgx_21ia, rgx_21ib, rgx_21ic
    global rgx_22ia, rgx_22ib, rgx_22ic
    global rgx_24ia, rgx_24ib, rgx_24ic
    global rgx_31ia, rgx_31ib, rgx_31ic
    global rgx_32ia, rgx_32ib, rgx_32ic
    global rgx_40ia, rgx_40ib, rgx_40ic
    global rgx_50ia, rgx_50ib, rgx_50ic
    global rgx_impia, rgx_impib, rgx_impic
    wdcands = set()
    blk = rgx_parentheses.sub('', tgtblk)
    for jwd in cl_alljwdset:
        res = regex.search(''.join((
                r'(^|[^A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}])',
                '{0}'.format(jwd), PTN_AFTJIWD)), blk)
        if res:
            wdcands.add(jwd)
    matchinfoset = set()
    blk = prsr._transformcl4onewd(blk)
    okwds = set()
    for jwd in cl_alljwdset:
        mres = regex.finditer('(?P<name>{0})'.format(jwd), blk)
        for res in mres:
            name = res.group('name')
            matchinfoset.add((res.span(), name))
    mres = rgx_impia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        if namebody:
            name = ''.join((namehd, namebody))
            matchinfoset.add((res.span(), name))
    mres = rgx_impib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        if namebody:
            name = namebody
            matchinfoset.add((res.span(), name))
    mres = rgx_impic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        if namebody:
            name = namebody
            matchinfoset.add((res.span(), name))
    mres = rgx_11ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_12ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_13ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_21ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_22ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_24ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_31ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_32ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_40ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_50ia.finditer(blk)
    for res in mres:
        namehd = res.group('head')
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = ''.join((namehd, namebody))
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    okwds = set()
    mres = rgx_11ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_12ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_13ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_21ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_22ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_24ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_31ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_32ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_40ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_50ib.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, False)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    okwds = set()
    mres = rgx_11ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_12ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_13ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_21ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_22ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_24ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_31ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_32ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_40ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    mres = rgx_50ic.finditer(blk)
    for res in mres:
        namebody = res.group('name')
        namebody = rgx_noneedclwds.sub('', namebody)
        namebody = rgx_noneedclwdend.sub('', namebody)
        if namebody:
            name = namebody
            if namebody not in okwds:
                chkres = _clkwdchk(namebody, True)
                if chkres:
                    okwds.add(namebody)
                    matchinfoset.add((res.span(), name))
            else:
                matchinfoset.add((res.span(), name))
    deltgtmatchinfoset = {
            (span, name) for (span, name) in matchinfoset
            for (span2, name2) in matchinfoset if span != span2
            and span2[0] <= span[0] and span[1] <= span2[1]}
    matchinfoset = matchinfoset.difference(deltgtmatchinfoset)
    for (span, name) in matchinfoset:
        wdcands.add(name)
    return wdcands


def _clkwdchk(name, special_chk_flg):
    global ZEN
    global HAN
    global NG_WDS
    global BORE_WDS
    global BORE_ENDS
    global rgx_alpha1
    global rgx_ngend
    global rgx_borewdend
    global rgx_ngrefend
    global rgx_spwd
    global rgx_clendwd
    namehan = name.translate(name.maketrans(ZEN, HAN))
    if namehan in NG_WDS:
        return False
    if namehan in BORE_WDS:
        return False
    if namehan in BORE_ENDS:
        return False
    if rgx_alpha1.search(namehan):
        return False
    if rgx_ngend.search(namehan):
        return False
    if rgx_borewdend.search(namehan):
        return False
    if rgx_ngrefend.search(namehan):
        return False
    if special_chk_flg:
        if 1 < len(name) and rgx_spwd.search(namehan):
            return True
        if rgx_clendwd.search(namehan):
            return True
        return False
    else:
        if 2 > len(name):
            return False
    return True


def _clwdsetgen():
    global cl_mwddic
    global wd_set
    for eacl in cl_mwddic.keys():
        for word in cl_mwddic[eacl]:
            wd_set.add(word)


def _clnonverbs():
    global prsr
    global wd_set
    prsr._set_nonverbs(wd_set)


def _clpgana():
    global cl_mwddic
    global cl_dic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global rgx_parentheses
    global rgx_pgcl
    for eacl in sorted(cl_dic.keys()):
        strblks = []
        for idx, strline in enumerate(cl_dic[eacl]):
            if not regex.search('【', strline):
                tmp_strline = rgx_parentheses.sub('', strline)
                strblks = regex.split('(は、)', tmp_strline)
                for strblk in strblks:
                    if 'は、' != strblk:
                        _clpgchk(eacl, idx, strblk)
        subj = cl_tgtdic[eacl]
        for idx, newline in enumerate(cl_dic[eacl]):
            tmpnewline = regex.sub('は、', 'は、●', newline)
            strblks = regex.split('●', tmpnewline)
            for strblk in strblks:
                if rgx_pgcl.search(subj):
                    _clpgsubjchk(eacl, idx, subj, strblk)
                tmpsubj = ''
                for word in sorted(cl_mwddic[eacl], key=len, reverse=True):
                    if rgx_pgcl.search(word):
                        tmpsrchwd = ''.join((word, 'は、'))
                        if strblk.endswith(tmpsrchwd):
                            tmpsubj = word
                            break
                if tmpsubj:
                    subj = tmpsubj
                    subj00 = _delmrkconj(subj)
                    wdpri = eacl * 100 + idx
                    if subj00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if subj00 not in cl_wdattrdic.keys():
                        mthdflg = False
                        cl_wdattrdic[subj00] = [
                                eacl, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[subj00][4]:
                        cl_wdattrdic[subj00][0] = eacl
                        cl_wdattrdic[subj00][1] = idx
                        cl_wdattrdic[subj00][4] = wdpri


def _clpgchk(clno, idx, strblk):
    global cl_mwddic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_pgdic
    global rgx_pgcl
    global rgx_methodcl
    global rgx_funccl
    global rgx_meanscl
    ptnverbpg1 = (
            '(?P<verb>(を、?((前記の|上記の|前記|上記|当該|該)?'
            'コンピュータに、?)?(実行さ|行わ|行なわ)せる(ための)?、?|'
            'を、?(実行する|行う|行なう)(ための)?、?))')
    ptnverbpg2 = (
            '(?P<verb>(を、?((前記の|上記の|前記|上記|当該|該)?'
            'コンピュータに、?)?実現させる(ための)?、?|を、?'
            '実現する(ための)?、?))')
    ptnverbpg3 = (
            '(?P<verb>(として、?((前記の|上記の|前記|上記|当該|該)?'
            'コンピュータを、?)?機能させる(ための)?、?))')
    brkflg = False
    sortedclwds = sorted(cl_mwddic[clno], key=len, reverse=True)
    for pgwd in sortedclwds:
        if rgx_pgcl.search(pgwd):
            res1 = regex.search(''.join((
                    '(?P<str_e>.+)', ptnverbpg1, '{0}'.format(pgwd),
                    r'(＋★［[^＋]+］★＋|及び|並びに|又は|若しくは|或いは|'
                    r'[\p{Hiragana}]|、|。|$)')), strblk)
            if res1:
                str_e = res1.group('str_e')
                newstr_e = regex.sub('^.+に、', '', str_e)
                resset = set()
                for word in cl_mwddic[clno]:
                    if rgx_methodcl.search(word):
                        mres = regex.finditer(''.join((
                                '{0}'.format(word), PTN_JOINT)), newstr_e)
                        for res in mres:
                            resset.add((word, res.span()))
                deltgtmatchinfoset = {
                        (word, span) for (word, span) in resset
                        for (word2, span2) in resset if span != span2
                        and span2[0] <= span[0] and span[1] <= span2[1]}
                resset = resset.difference(deltgtmatchinfoset)
                for (word, span) in resset:
                    brkflg = True
                    pgwd00 = _delmrkconj(pgwd)
                    word00 = _delmrkconj(word)
                    if (clno, pgwd00) not in cl_pgdic.keys():
                        cl_pgdic[(clno, pgwd00)] = [(clno, word00)]
                    else:
                        if (clno, word00) not in cl_pgdic[(clno, pgwd00)]:
                            cl_pgdic[(clno, pgwd00)].append((clno, word00))
                    wdpri = clno * 100 + idx
                    if pgwd00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if pgwd00 not in cl_wdattrdic.keys():
                        mthdflg = False
                        cl_wdattrdic[pgwd00] = [
                                clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[pgwd00][4]:
                        cl_wdattrdic[pgwd00][0] = clno
                        cl_wdattrdic[pgwd00][1] = idx
                        cl_wdattrdic[pgwd00][4] = wdpri
                    wdpri = clno * 100 + idx
                    if word00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if word00 not in cl_wdattrdic.keys():
                        mthdflg = True
                        cl_wdattrdic[word00] = [
                                clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[word00][4]:
                        cl_wdattrdic[word00][0] = clno
                        cl_wdattrdic[word00][1] = idx
                        cl_wdattrdic[word00][4] = wdpri
                if brkflg:
                    break
    if brkflg:
        return
    for pgwd in sortedclwds:
        if rgx_pgcl.search(pgwd):
            res2 = regex.search(''.join((
                    '(?P<str_e>.+)', ptnverbpg2, '{0}'.format(pgwd),
                    '(＋★［[^＋]+］★＋|及び|並びに|又は|若しくは|或いは|'
                    r'[\p{Hiragana}]|、|。|$)')), strblk)
            if res2:
                str_e = res2.group('str_e')
                newstr_e = regex.sub('^.+に、', '', str_e)
                resset = set()
                for word in cl_mwddic[clno]:
                    if rgx_funccl.search(word):
                        mres = regex.finditer(''.join((
                                '{0}'.format(word), PTN_JOINT)), newstr_e)
                        for res in mres:
                            resset.add((word, res.span()))
                deltgtmatchinfoset = {
                        (word, span) for (word, span) in resset
                        for (word2, span2) in resset if span != span2
                        and span2[0] <= span[0] and span[1] <= span2[1]}
                resset = resset.difference(deltgtmatchinfoset)
                for (word, span) in resset:
                    brkflg = True
                    pgwd00 = _delmrkconj(pgwd)
                    word00 = _delmrkconj(word)
                    if (clno, pgwd00) not in cl_pgdic.keys():
                        cl_pgdic[(clno, pgwd00)] = [(clno, word00)]
                    else:
                        if (clno, word00) not in cl_pgdic[(clno, pgwd00)]:
                            cl_pgdic[(clno, pgwd00)].append((clno, word00))
                    wdpri = clno * 100 + idx
                    if pgwd00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if pgwd00 not in cl_wdattrdic.keys():
                        mthdflg = False
                        cl_wdattrdic[pgwd00] = [
                                clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[pgwd00][4]:
                        cl_wdattrdic[pgwd00][0] = clno
                        cl_wdattrdic[pgwd00][1] = idx
                        cl_wdattrdic[pgwd00][4] = wdpri
                    wdpri = clno * 100 + idx
                    if word00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if word00 not in cl_wdattrdic.keys():
                        mthdflg = False
                        cl_wdattrdic[word00] = [
                                clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[word00][4]:
                        cl_wdattrdic[word00][0] = clno
                        cl_wdattrdic[word00][1] = idx
                        cl_wdattrdic[word00][4] = wdpri
                if brkflg:
                    break
    if brkflg:
        return
    for pgwd in sortedclwds:
        if rgx_pgcl.search(pgwd):
            res3 = regex.search(''.join((
                    '(?P<str_e>.+)', ptnverbpg3, '{0}'.format(pgwd),
                    '(＋★［[^＋]+］★＋|及び|並びに|又は|若しくは|或いは|'
                    r'[\p{Hiragana}]|、|。|$)')), strblk)
            if res3:
                str_e = res3.group('str_e')
                newstr_e = regex.sub('^.+を、', '', str_e)
                resset = set()
                for word in cl_mwddic[clno]:
                    if rgx_meanscl.search(word):
                        mres = regex.finditer(''.join((
                                '{0}'.format(word), PTN_JOINT)), newstr_e)
                        for res in mres:
                            resset.add((word, res.span()))
                deltgtmatchinfoset = {
                        (word, span) for (word, span) in resset
                        for (word2, span2) in resset if span != span2
                        and span2[0] <= span[0] and span[1] <= span2[1]}
                resset = resset.difference(deltgtmatchinfoset)
                for (word, span) in resset:
                    brkflg = True
                    pgwd00 = _delmrkconj(pgwd)
                    word00 = _delmrkconj(word)
                    if (clno, pgwd00) not in cl_pgdic.keys():
                        cl_pgdic[(clno, pgwd00)] = [(clno, word00)]
                    else:
                        if (clno, word00) not in cl_pgdic[(clno, pgwd00)]:
                            cl_pgdic[(clno, pgwd00)].append((clno, word00))
                    wdpri = clno * 100 + idx
                    if pgwd00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if pgwd00 not in cl_wdattrdic.keys():
                        mthdflg = False
                        cl_wdattrdic[pgwd00] = [
                                clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[pgwd00][4]:
                        cl_wdattrdic[pgwd00][0] = clno
                        cl_wdattrdic[pgwd00][1] = idx
                        cl_wdattrdic[pgwd00][4] = wdpri
                    wdpri = clno * 100 + idx
                    if word00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if word00 not in cl_wdattrdic.keys():
                        mthdflg = False
                        cl_wdattrdic[word00] = [
                                clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[word00][4]:
                        cl_wdattrdic[word00][0] = clno
                        cl_wdattrdic[word00][1] = idx
                        cl_wdattrdic[word00][4] = wdpri
                if brkflg:
                    break


def _clpgsubjchk(clno, idx, subj, strblk):
    global cl_mwddic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_pgdic
    global cl_tmppgdic1, cl_tmppgdic2, cl_tmppgdic3
    global rgx_methodcl
    global rgx_funccl
    global rgx_meanscl
    global rgx_pg11, rgx_pg12, rgx_pg21, rgx_pg22, rgx_pg31, rgx_pg32
    global rgx_struct
    subj00 = _delmrkconj(subj)
    res = rgx_pg11.search(strblk)
    if res:
        if (clno, subj00) in cl_tmppgdic1.keys():
            if (clno, subj00) in cl_pgdic.keys():
                tmplist = cl_pgdic[
                        (clno, subj00)] + cl_tmppgdic1[(clno, subj00)]
                cl_pgdic[(clno, subj00)] = list(set(tmplist))
            else:
                cl_pgdic[(clno, subj00)] = cl_tmppgdic1[(clno, subj00)].copy()
            cl_tmppgdic1.pop((clno, subj00), None)
    res = rgx_pg21.search(strblk)
    if res:
        if (clno, subj00) in cl_tmppgdic2.keys():
            if (clno, subj00) in cl_pgdic.keys():
                tmplist = cl_pgdic[
                        (clno, subj00)] + cl_tmppgdic2[(clno, subj00)]
                cl_pgdic[(clno, subj00)] = list(set(tmplist))
            else:
                cl_pgdic[(clno, subj00)] = cl_tmppgdic2[(clno, subj00)].copy()
            cl_tmppgdic2.pop((clno, subj00), None)
    res = rgx_pg31.search(strblk)
    if res:
        if (clno, subj00) in cl_tmppgdic3.keys():
            if (clno, subj00) in cl_pgdic.keys():
                tmplist = cl_pgdic[
                        (clno, subj00)] + cl_tmppgdic3[(clno, subj00)]
                cl_pgdic[(clno, subj00)] = list(set(tmplist))
            else:
                cl_pgdic[(clno, subj00)] = cl_tmppgdic3[(clno, subj00)].copy()
            cl_tmppgdic3.pop((clno, subj00), None)
    res = rgx_pg12.search(strblk)
    if res:
        str_e = res.group('str_e')
        newstr_e = regex.sub('^.+に、', '', str_e)
        resset = set()
        for word in cl_mwddic[clno]:
            if rgx_methodcl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), newstr_e)
                for res in mres:
                    resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_pgdic.keys():
                cl_pgdic[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_pgdic[(clno, subj00)]:
                    cl_pgdic[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = True
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
    res = rgx_pg22.search(strblk)
    if res:
        str_e = res.group('str_e')
        newstr_e = regex.sub('^.+に、', '', str_e)
        resset = set()
        for word in cl_mwddic[clno]:
            if rgx_funccl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), newstr_e)
                for res in mres:
                    resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_pgdic.keys():
                cl_pgdic[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_pgdic[(clno, subj00)]:
                    cl_pgdic[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
    res = rgx_pg32.search(strblk)
    if res:
        str_e = res.group('str_e')
        newstr_e = regex.sub('^.+に、', '', str_e)
        resset = set()
        for word in cl_mwddic[clno]:
            if rgx_meanscl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), newstr_e)
                for res in mres:
                    resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_pgdic.keys():
                cl_pgdic[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_pgdic[(clno, subj00)]:
                    cl_pgdic[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
    res = rgx_struct.search(strblk)
    if res:
        str_e = res.group('str_e')
        newstr_e = regex.sub('^.+に、', '', str_e)
        resset1 = set()
        resset2 = set()
        resset3 = set()
        for word in cl_mwddic[clno]:
            if rgx_methodcl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), newstr_e)
                for res in mres:
                    resset1.add((word, res.span()))
            elif rgx_funccl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), newstr_e)
                for res in mres:
                    resset2.add((word, res.span()))
            elif rgx_meanscl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), newstr_e)
                for res in mres:
                    resset3.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset1
                for (word2, span2) in resset1 if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset1 = resset1.difference(deltgtmatchinfoset)
        for (word, span) in resset1:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_tmppgdic1.keys():
                cl_tmppgdic1[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_tmppgdic1[(clno, subj00)]:
                    cl_tmppgdic1[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = True
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset2
                for (word2, span2) in resset2 if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset2 = resset2.difference(deltgtmatchinfoset)
        for (word, span) in resset2:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_tmppgdic2.keys():
                cl_tmppgdic2[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_tmppgdic2[(clno, subj00)]:
                    cl_tmppgdic2[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset3
                for (word2, span2) in resset3 if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset3 = resset3.difference(deltgtmatchinfoset)
        for (word, span) in resset3:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_tmppgdic3.keys():
                cl_tmppgdic3[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_tmppgdic3[(clno, subj00)]:
                    cl_tmppgdic3[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri


def _clstrgana():
    global cl_mwddic
    global cl_dic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_newdic
    global rgx_parentheses
    global rgx_methodcl
    for eacl in sorted(cl_dic.keys()):
        cl_newdic[eacl] = []
        strblks = []
        for idx, strline in enumerate(cl_dic[eacl]):
            if not regex.search('【', strline):
                tmp_strline = rgx_parentheses.sub('', strline)
                strblks = regex.split('(は、)', tmp_strline)
                newline = ''
                for strblk in strblks:
                    if 'は、' == strblk:
                        newline = ''.join((newline, strblk))
                    else:
                        newline = ''.join((
                                newline, _clstrgchk(eacl, idx, strblk)))
                cl_newdic[eacl].append(newline)
        subj = cl_tgtdic[eacl]
        for idx, newline in enumerate(cl_newdic[eacl]):
            tmpnewline = regex.sub('は、', 'は、●', newline)
            strblks = regex.split('●', tmpnewline)
            for strblk in strblks:
                _clstrgsubjchk(eacl, idx, subj, strblk)
                tmpsubj = ''
                for word in sorted(cl_mwddic[eacl], key=len, reverse=True):
                    tmpsrchwd = ''.join((word, 'は、'))
                    if strblk.endswith(tmpsrchwd):
                        tmpsubj = word
                        break
                if tmpsubj:
                    subj = tmpsubj
                    wdpri = eacl * 100 + idx
                    subj00 = _delmrkconj(subj)
                    if subj00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if subj00 not in cl_wdattrdic.keys():
                        if rgx_methodcl.search(subj00):
                            mthdflg = True
                        else:
                            mthdflg = False
                        cl_wdattrdic[subj00] = [
                                eacl, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[subj00][4]:
                        cl_wdattrdic[subj00][0] = eacl
                        cl_wdattrdic[subj00][1] = idx
                        cl_wdattrdic[subj00][4] = wdpri
    cl_newdic.clear()


def _clstrgchk(clno, idx, strblk):
    global cl_mwddic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_strgdic
    global rgx_methodcl
    global rgx_datcl
    ptnverbstrg = (
            '(?P<verb>(を、?(記録する|記録した|記録している|登録する|登録した|'
            '登録している|格納する|格納した|格納している|記憶する|記憶した|'
            '記憶している|保持する|保持した|保持している|保存する|保存した|'
            '保存している|蓄積する|蓄積した|蓄積している)|(が、?(記録される|'
            '記録された|記録されている|登録される|登録された|登録されている|'
            '格納される|格納された|格納されている|記憶される|記憶された|'
            '記憶されている|保持される|保持された|保持されている|保存される|'
            '保存された|保存されている|蓄積される|蓄積された|'
            '蓄積されている)))(コンピュータ(で|により)?'
            '(読み取り|読取り|読取)可能な)?)')
    ptnvostrg1 = (
            '(?P<object1>を、?((記録|登録|格納|保存|蓄積)'
            '(し|する)|(記憶|保持)させ))')
    ptnostrg = (
            '(?P<object2>(を、?)(前記の|上記の|前記|上記|当該|該)?'
            '(コンピュータ(で|により)?(読み取り|読取り|読取)可能な)?'
            '(前記の|上記の|前記|上記|当該|該)?)')
    ptnvostrg2 = (
            '(各々|夫々)?に、?((記録|登録|格納|保存|蓄積)'
            '(し|する)|(記憶|保持)させ)')
    newblk = strblk
    brkflg = False
    sortedclwds = sorted(cl_mwddic[clno], key=len, reverse=True)
    for strgwd in sortedclwds:
        res1 = regex.search(''.join((
                '{0}'.format(strgwd), '(各々|夫々)?に、(?P<str_e>.+)',
                ptnvostrg1)), strblk)
        if res1:
            str_e = res1.group('str_e')
            resset = set()
            for word in cl_mwddic[clno]:
                if rgx_datcl.search(word):
                    mres = regex.finditer(''.join((
                            '{0}'.format(word), PTN_JOINT)), str_e)
                    for res in mres:
                        resset.add((word, res.span()))
            deltgtmatchinfoset = {
                    (word, span) for (word, span) in resset
                    for (word2, span2) in resset
                    if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            resset = resset.difference(deltgtmatchinfoset)
            for (word, span) in resset:
                brkflg = True
                strgwd00 = _delmrkconj(strgwd)
                word00 = _delmrkconj(word)
                if (clno, strgwd00) not in cl_strgdic.keys():
                    cl_strgdic[(clno, strgwd00)] = [(clno, word00)]
                else:
                    if (clno, word00) not in cl_strgdic[(clno, strgwd00)]:
                        cl_strgdic[(clno, strgwd00)].append((clno, word00))
                wdpri = clno * 100 + idx
                if strgwd00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if strgwd00 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(strgwd00):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[strgwd00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[strgwd00][4]:
                    cl_wdattrdic[strgwd00][0] = clno
                    cl_wdattrdic[strgwd00][1] = idx
                    cl_wdattrdic[strgwd00][4] = wdpri
                wdpri = clno * 100 + idx
                if word00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if word00 not in cl_wdattrdic.keys():
                    mthdflg = False
                    cl_wdattrdic[word00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[word00][4]:
                    cl_wdattrdic[word00][0] = clno
                    cl_wdattrdic[word00][1] = idx
                    cl_wdattrdic[word00][4] = wdpri
            if brkflg:
                break
    if brkflg:
        newblk = regex.sub(res1.group(), '', strblk)
        return newblk
    for strgwd in sortedclwds:
        res2 = regex.search(''.join((
                '^(?P<str_e>.+)', ptnostrg, '{0}'.format(strgwd),
                ptnvostrg2)), strblk)
        if res2:
            str_e = res2.group('str_e')
            resset = set()
            for word in cl_mwddic[clno]:
                if rgx_datcl.search(word):
                    mres = regex.finditer(''.join((
                            '{0}'.format(word), PTN_JOINT)), str_e)
                    for res in mres:
                        resset.add((word, res.span()))
            deltgtmatchinfoset = {
                    (word, span) for (word, span) in resset
                    for (word2, span2) in resset if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            resset = resset.difference(deltgtmatchinfoset)
            for (word, span) in resset:
                brkflg = True
                strgwd00 = _delmrkconj(strgwd)
                word00 = _delmrkconj(word)
                if (clno, strgwd00) not in cl_strgdic.keys():
                    cl_strgdic[(clno, strgwd00)] = [(clno, word00)]
                else:
                    if (clno, word00) not in cl_strgdic[(clno, strgwd00)]:
                        cl_strgdic[(clno, strgwd00)].append((clno, word00))
                wdpri = clno * 100 + idx
                if strgwd00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if strgwd00 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(strgwd00):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[strgwd00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[strgwd00][4]:
                    cl_wdattrdic[strgwd00][0] = clno
                    cl_wdattrdic[strgwd00][1] = idx
                    cl_wdattrdic[strgwd00][4] = wdpri
                wdpri = clno * 100 + idx
                if word00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if word00 not in cl_wdattrdic.keys():
                    mthdflg = False
                    cl_wdattrdic[word00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[word00][4]:
                    cl_wdattrdic[word00][0] = clno
                    cl_wdattrdic[word00][1] = idx
                    cl_wdattrdic[word00][4] = wdpri
            if brkflg:
                break
    if brkflg:
        newblk = regex.sub(res2.group(), '', strblk)
        return newblk
    for strgwd in sortedclwds:
        res3 = regex.search(''.join((
                '^(?P<str_e>.+)', ptnverbstrg,
                '{0}'.format(strgwd), (
                    '(各々|夫々)?(＋★［[^＋]+］★＋|及び|並びに|又は|'
                    r'若しくは|或いは|[\p{Hiragana}]|、|。|$)'))), strblk)
        if res3:
            str_e = res3.group('str_e')
            resset = set()
            for word in cl_mwddic[clno]:
                if rgx_datcl.search(word):
                    mres = regex.finditer(''.join((
                            '{0}'.format(word), PTN_JOINT)), str_e)
                    for res in mres:
                        resset.add((word, res.span()))
            deltgtmatchinfoset = {
                    (word, span) for (word, span) in resset
                    for (word2, span2) in resset if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            resset = resset.difference(deltgtmatchinfoset)
            for (word, span) in resset:
                brkflg = True
                strgwd00 = _delmrkconj(strgwd)
                word00 = _delmrkconj(word)
                if (clno, strgwd00) not in cl_strgdic.keys():
                    cl_strgdic[(clno, strgwd00)] = [(clno, word00)]
                else:
                    if (clno, word00) not in cl_strgdic[(clno, strgwd00)]:
                        cl_strgdic[(clno, strgwd00)].append((clno, word00))
                wdpri = clno * 100 + idx
                if strgwd00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if strgwd00 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(strgwd00):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[strgwd00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[strgwd00][4]:
                    cl_wdattrdic[strgwd00][0] = clno
                    cl_wdattrdic[strgwd00][1] = idx
                    cl_wdattrdic[strgwd00][4] = wdpri
                wdpri = clno * 100 + idx
                if word00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if word00 not in cl_wdattrdic.keys():
                    mthdflg = False
                    cl_wdattrdic[word00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[word00][4]:
                    cl_wdattrdic[word00][0] = clno
                    cl_wdattrdic[word00][1] = idx
                    cl_wdattrdic[word00][4] = wdpri
            if brkflg:
                break
    if brkflg:
        newblk = regex.sub(res3.group(), '', strblk)
        return newblk
    return newblk


def _clstrgsubjchk(clno, idx, subj, strblk):
    global prsr
    global cl_mwddic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_strgdic
    global cl_tmpstrgdic
    global rgx_methodcl
    global rgx_struct
    global rgx_datcl
    global rgx_strg1, rgx_strg2, rgx_strg3
    global rgx_verbmk
    subj00 = _delmrkconj(subj)
    if rgx_datcl.search(subj):
        res = rgx_strg3.search(strblk)
        if res:
            str_e = res.group('str_e')
            tmpstr = prsr._transform_clverb(str_e)
            str_e = rgx_verbmk.sub('', tmpstr)
            resset = set()
            for word in cl_mwddic[clno]:
                mres = regex.finditer(''.join((
                        '{0}'.format(word), '$')), str_e)
                for res in mres:
                    resset.add((word, res.span()))
            deltgtmatchinfoset = {
                    (word, span) for (word, span) in resset
                    for (word2, span2) in resset if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            resset = resset.difference(deltgtmatchinfoset)
            for (word, span) in resset:
                word00 = _delmrkconj(word)
                if (clno, word00) not in cl_strgdic.keys():
                    cl_strgdic[(clno, word00)] = [(clno, subj00)]
                else:
                    if (clno, subj00) not in cl_strgdic[(clno, word00)]:
                        cl_strgdic[(clno, word00)].append((clno, subj00))
                wdpri = clno * 100 + idx
                if word00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if word00 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(word00):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[word00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[word00][4]:
                    cl_wdattrdic[word00][0] = clno
                    cl_wdattrdic[word00][1] = idx
                    cl_wdattrdic[word00][4] = wdpri
            return
    res = rgx_strg1.search(strblk)
    if res:
        if (clno, subj00) in cl_tmpstrgdic.keys():
            if (clno, subj00) in cl_strgdic.keys():
                tmplist = cl_strgdic[
                        (clno, subj00)] + cl_tmpstrgdic[(clno, subj00)]
                cl_strgdic[(clno, subj00)] = list(set(tmplist))
            else:
                cl_strgdic[(clno, subj00)] = cl_tmpstrgdic[
                        (clno, subj00)].copy()
            cl_tmpstrgdic.pop((clno, subj00), None)
    res = rgx_strg2.search(strblk)
    if res:
        str_e = res.group('str_e')
        resset = set()
        for word in cl_mwddic[clno]:
            if rgx_datcl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), str_e)
                for res in mres:
                    resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_strgdic.keys():
                cl_strgdic[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_strgdic[(clno, subj00)]:
                    cl_strgdic[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
    res = rgx_struct.search(strblk)
    if res:
        str_e = res.group('str_e')
        resset = set()
        for word in cl_mwddic[clno]:
            if rgx_datcl.search(word):
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), str_e)
                for res in mres:
                    resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_tmpstrgdic.keys():
                cl_tmpstrgdic[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_tmpstrgdic[(clno, subj00)]:
                    cl_tmpstrgdic[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri


def _clstructana():
    global cl_mwddic
    global clno_max
    global cl_wdattrdic
    global cl_dic
    global cl_tgtdic
    global cl_newdic
    global rgx_methodcl
    global rgx_parentheses
    for eacl in sorted(cl_dic.keys()):
        cl_newdic[eacl] = []
        strblks = []
        for idx, strline in enumerate(cl_dic[eacl]):
            if not regex.search('【', strline):
                tmp_strline = rgx_parentheses.sub('', strline)
                strblks = regex.split('(は、)', tmp_strline)
                newline = ''
                for strblk in strblks:
                    if 'は、' == strblk:
                        newline = ''.join((newline, strblk))
                    else:
                        newline = ''.join((
                                newline, _clstructchk(eacl, idx, strblk)))
                cl_newdic[eacl].append(newline)
        subj = cl_tgtdic[eacl]
        for idx, newline in enumerate(cl_newdic[eacl]):
            tmpnewline = regex.sub('は、', 'は、●', newline)
            strblks = regex.split('●', tmpnewline)
            for strblk in strblks:
                _clstructsubjchk(eacl, idx, subj, strblk)
                tmpsubj = ''
                for word in sorted(cl_mwddic[eacl], key=len, reverse=True):
                    tmpsrchwd = ''.join((word, 'は、'))
                    if strblk.endswith(tmpsrchwd):
                        tmpsubj = word
                        break
                if tmpsubj:
                    subj = tmpsubj
                    wdpri = eacl * 100 + idx
                    subj00 = _delmrkconj(subj)
                    if subj00 in cl_tgtdic.values():
                        cltgtflg = True
                    else:
                        cltgtflg = False
                        wdpri += (clno_max+1) * 100
                    if subj00 not in cl_wdattrdic.keys():
                        if rgx_methodcl.search(subj00):
                            mthdflg = True
                        else:
                            mthdflg = False
                        cl_wdattrdic[subj00] = [
                                eacl, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                    elif wdpri < cl_wdattrdic[subj00][4]:
                        cl_wdattrdic[subj00][0] = eacl
                        cl_wdattrdic[subj00][1] = idx
                        cl_wdattrdic[subj00][4] = wdpri
    for eacl in sorted(cl_tgtdic.keys()):
        idx = 0
        claimtgt = cl_tgtdic[eacl]
        wdpri = eacl * 100 + idx
        cltgtflg = True
        if rgx_methodcl.search(claimtgt):
            mthdflg = True
        else:
            mthdflg = False
        if claimtgt not in cl_wdattrdic.keys():
            cl_wdattrdic[claimtgt] = [
                    eacl, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
        else:
            if wdpri < cl_wdattrdic[claimtgt][4]:
                cl_wdattrdic[claimtgt] = [
                        eacl, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
    cl_newdic.clear()


def _clstructchk(clno, idx, strblk):
    global prsr
    global cl_mwddic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_structdic
    global rgx_methodcl
    global rgx_verbmk
    newblk = strblk
    reslist = []
    ptn_va0 = (
            '(?P<verb>(を、?((更|さら)に、?)?(備える|備えた|備えている|有す|'
            '有する|有している|含む|含んだ|含んでいる|含んで構成される|'
            '具備する|具備した|具備している|包含する|包含した|包含している|'
            '構成要素とする|構成要素とした|構成要素としている)|'
            '((により|で|から)、?(構成される|構成された|構成されている|'
            '形成される|形成された|形成されている|成る|成った|成っている|'
            'なる|なった|なっている))))')
    for word in cl_mwddic[clno]:
        res = regex.search(''.join((
                '^(?P<str_e>.+)', ptn_va0, '{0}'.format(word), (
                    '(各々|夫々)?(＋★［[^＋]+］★＋|及び|並びに|又は|'
                    r'若しくは|或いは|[\p{Hiragana}]|、|。|$)'))), strblk)
        if res:
            reslist.append((
                    word, res.group('str_e'), res.group('verb'), res.group()))
    if reslist:
        reslist.sort(key=lambda x: len(x[3]))
        newblk = regex.sub(''.join((
                '^', reslist[-1][1], reslist[-1][2])), '', strblk)
        prevstrpart = '●'
        prevframewd = '●'
        for (framewd, str_e, verb, allstr) in reslist:
            newstr_e = regex.sub(''.join((
                    '^', prevstrpart)), prevframewd, str_e)
            tmpstr = prsr._transform_clverb(newstr_e)
            newstr_e = rgx_verbmk.sub('', tmpstr)
            prevstrpart = ''.join((str_e, verb, framewd))
            prevframewd = framewd
            resset = set()
            for word in cl_mwddic[clno]:
                mres = regex.finditer(''.join((
                        '{0}'.format(word), PTN_JOINT)), newstr_e)
                for res in mres:
                    resset.add((word, res.span()))
            deltgtmatchinfoset = {
                    (word, span) for (word, span) in resset
                    for (word2, span2) in resset if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            resset = resset.difference(deltgtmatchinfoset)
            for (word, span) in resset:
                framewd00 = _delmrkconj(framewd)
                word00 = _delmrkconj(word)
                if (clno, framewd00) not in cl_structdic.keys():
                    cl_structdic[(clno, framewd00)] = [(clno, word00)]
                else:
                    if (clno, word00) not in cl_structdic[(clno, framewd00)]:
                        cl_structdic[(clno, framewd00)].append((clno, word00))
                wdpri = clno * 100 + idx
                if framewd00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if framewd00 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(framewd00):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[framewd00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[framewd00][4]:
                    cl_wdattrdic[framewd00][0] = clno
                    cl_wdattrdic[framewd00][1] = idx
                    cl_wdattrdic[framewd00][4] = wdpri
                wdpri = clno * 100 + idx
                if word00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if word00 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(word00):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[word00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[word00][4]:
                    cl_wdattrdic[word00][0] = clno
                    cl_wdattrdic[word00][1] = idx
                    cl_wdattrdic[word00][4] = wdpri
    return newblk


def _clstructsubjchk(clno, idx, subj, strblk):
    global prsr
    global cl_mwddic
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_structdic
    global cl_tmpstructdic
    global rgx_methodcl
    global rgx_struct
    global rgx_g
    global rgx_va1, rgx_va2, rgx_va3
    global rgx_verbmk
    subj00 = _delmrkconj(subj)
    for word in cl_mwddic[clno]:
        res = rgx_g.search(word)
        if res:
            word2 = res.group('word2')
            if regex.search(word, strblk):
                word00 = _delmrkconj(word)
                word200 = _delmrkconj(word2)
                if (clno, word00) not in cl_structdic.keys():
                    cl_structdic[(clno, word00)] = [(clno, word200)]
                else:
                    if (clno, word200) not in cl_structdic[(clno, word00)]:
                        cl_structdic[(clno, word00)].append((clno, word200))
                wdpri = clno * 100 + idx
                if word00 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if word00 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(word00):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[word00] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[word00][4]:
                    cl_wdattrdic[word00][0] = clno
                    cl_wdattrdic[word00][1] = idx
                    cl_wdattrdic[word00][4] = wdpri
                wdpri = clno * 100 + idx
                if word200 in cl_tgtdic.values():
                    cltgtflg = True
                else:
                    cltgtflg = False
                    wdpri += (clno_max+1) * 100
                if word200 not in cl_wdattrdic.keys():
                    if rgx_methodcl.search(word200):
                        mthdflg = True
                    else:
                        mthdflg = False
                    cl_wdattrdic[word200] = [
                            clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
                elif wdpri < cl_wdattrdic[word200][4]:
                    cl_wdattrdic[word200][0] = clno
                    cl_wdattrdic[word200][1] = idx
                    cl_wdattrdic[word200][4] = wdpri
    res = rgx_va3.search(strblk)
    if res:
        str_e = res.group('str_e')
        tmpstr = prsr._transform_clverb(str_e)
        str_e = rgx_verbmk.sub('', tmpstr)
        resset = set()
        for word in cl_mwddic[clno]:
            mres = regex.finditer(''.join(('{0}'.format(word), '$')), str_e)
            for res in mres:
                resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, word00) not in cl_structdic.keys():
                cl_structdic[(clno, word00)] = [(clno, subj00)]
            else:
                if (clno, subj00) not in cl_structdic[(clno, word00)]:
                    cl_structdic[(clno, word00)].append((clno, subj00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                if rgx_methodcl.search(word00):
                    mthdflg = True
                else:
                    mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
        return
    res = rgx_va1.search(strblk)
    if res:
        if (clno, subj00) in cl_tmpstructdic.keys():
            if (clno, subj00) in cl_structdic.keys():
                tmplist = cl_structdic[
                        (clno, subj00)] + cl_tmpstructdic[(clno, subj00)]
                cl_structdic[(clno, subj00)] = list(set(tmplist))
            else:
                cl_structdic[(clno, subj00)] = cl_tmpstructdic[
                        (clno, subj00)].copy()
            cl_tmpstructdic.pop((clno, subj00), None)
    res = rgx_va2.search(strblk)
    if res:
        str_e = res.group('str_e')
        tmpstr = prsr._transform_clverb(str_e)
        str_e = rgx_verbmk.sub('', tmpstr)
        resset = set()
        for word in cl_mwddic[clno]:
            mres = regex.finditer(''.join((
                    '{0}'.format(word), PTN_JOINT)), str_e)
            for res in mres:
                resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_structdic.keys():
                cl_structdic[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_structdic[(clno, subj00)]:
                    cl_structdic[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                if rgx_methodcl.search(word00):
                    mthdflg = True
                else:
                    mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri
    res = rgx_struct.search(strblk)
    if res:
        str_e = res.group('str_e')
        tmpstr = prsr._transform_clverb(str_e)
        str_e = rgx_verbmk.sub('', tmpstr)
        resset = set()
        for word in cl_mwddic[clno]:
            mres = regex.finditer(''.join((
                    '{0}'.format(word), PTN_JOINT)), str_e)
            for res in mres:
                resset.add((word, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        for (word, span) in resset:
            word00 = _delmrkconj(word)
            if (clno, subj00) not in cl_tmpstructdic.keys():
                cl_tmpstructdic[(clno, subj00)] = [(clno, word00)]
            else:
                if (clno, word00) not in cl_tmpstructdic[(clno, subj00)]:
                    cl_tmpstructdic[(clno, subj00)].append((clno, word00))
            wdpri = clno * 100 + idx
            if word00 in cl_tgtdic.values():
                cltgtflg = True
            else:
                cltgtflg = False
                wdpri += (clno_max+1) * 100
            if word00 not in cl_wdattrdic.keys():
                if rgx_methodcl.search(word00):
                    mthdflg = True
                else:
                    mthdflg = False
                cl_wdattrdic[word00] = [
                        clno, idx, cltgtflg, mthdflg, wdpri, 0, '', 0]
            elif wdpri < cl_wdattrdic[word00][4]:
                cl_wdattrdic[word00][0] = clno
                cl_wdattrdic[word00][1] = idx
                cl_wdattrdic[word00][4] = wdpri


def _cldicintgr():
    global cl_pgdic
    global cl_allpgdic
    global cl_strgdic
    global cl_allstrgdic
    global cl_structdic
    global cl_allstructdic
    for (cl, wd) in sorted(cl_pgdic.keys(), key=lambda x: x[0]):
        if wd not in cl_allpgdic.keys():
            cl_allpgdic[wd] = []
        for (cl1, wd1) in cl_pgdic[(cl, wd)]:
            if wd1 not in cl_allpgdic[wd]:
                cl_allpgdic[wd].append(wd1)
    for (cl, wd) in sorted(cl_strgdic.keys(), key=lambda x: x[0]):
        if wd not in cl_allstrgdic.keys():
            cl_allstrgdic[wd] = []
        for (cl1, wd1) in cl_strgdic[(cl, wd)]:
            if wd1 not in cl_allstrgdic[wd]:
                cl_allstrgdic[wd].append(wd1)
    for (cl, wd) in sorted(cl_structdic.keys(), key=lambda x: x[0]):
        if wd not in cl_allstructdic.keys():
            cl_allstructdic[wd] = []
        for (cl1, wd1) in cl_structdic[(cl, wd)]:
            if wd1 not in cl_allstructdic[wd]:
                cl_allstructdic[wd].append(wd1)


def _clwdprichg():
    global cl_tgtdic
    global clno_max
    global cl_wdattrdic
    global cl_allpgdic
    global cl_allstrgdic
    global rgx_pgcl
    borderpri = (clno_max+1) * 100
    pglist = []
    for wd in cl_allstrgdic.keys():
        if wd in cl_tgtdic.values():
            for wd1 in cl_allstrgdic[wd]:
                wdpri = cl_wdattrdic[wd1][4]
                if borderpri < wdpri:
                    cl_wdattrdic[wd1][4] = wdpri - borderpri
                if rgx_pgcl.search(wd1):
                    if wd1 not in pglist:
                        pglist.append(wd1)
    for wd in cl_allpgdic.keys():
        if wd in cl_tgtdic.values() or wd in pglist:
            for wd1 in cl_allpgdic[wd]:
                wdpri = cl_wdattrdic[wd1][4]
                if borderpri < wdpri:
                    cl_wdattrdic[wd1][4] = wdpri - borderpri


def _clelextr():
    global cl_refdic
    global cl_tgtdic
    global cl_tgtgrpdic
    global cl_structdic
    global cl_eldic
    indwddic = {}
    for eacl in sorted(cl_refdic.keys()):
        chkclflg = False
        numref = len(cl_refdic[eacl])
        if 0 == numref:
            chkclflg = True
        else:
            for cl in cl_refdic[eacl]:
                if cl_tgtdic[eacl] != cl_tgtdic[cl]:
                    numref -= 1
            if 0 == numref:
                chkclflg = True
        if chkclflg:
            cl_tgtgrpdic[eacl] = [eacl]
            for eacl_r in sorted(cl_refdic.keys()):
                if eacl_r > eacl:
                    if _clrefchainchk(eacl, eacl_r):
                        cl_tgtgrpdic[eacl].append(eacl_r)
                elif eacl_r < eacl:
                    if _clrefchainchk(eacl_r, eacl):
                        cl_tgtgrpdic[eacl].append(eacl_r)
    for eacl in cl_tgtdic.keys():
        claimtgt = cl_tgtdic[eacl]
        if (eacl, claimtgt) not in cl_structdic.keys():
            cl_structdic[(eacl, claimtgt)] = []
    for eacl in cl_tgtgrpdic.keys():
        claimtgt = cl_tgtdic[eacl]
        cl_eldic[(eacl, '')] = []
        clnumlist = []
        for (cl, framewd) in cl_structdic.keys():
            if cl in cl_tgtgrpdic[eacl]:
                if framewd == claimtgt:
                    clnumlist.append(cl)
        newclnumlist = sorted(list(set(clnumlist)))
        cl_eldic[(eacl, '')].append([claimtgt, newclnumlist])
    for eacl in cl_tgtgrpdic.keys():
        for (cl, framewd) in cl_structdic.keys():
            if cl in cl_tgtgrpdic[eacl]:
                if (eacl, framewd) in cl_eldic.keys():
                    for (clno, wd) in cl_structdic[(cl, framewd)]:
                        wdidx = -1
                        for idx, wd_cl in enumerate(cl_eldic[
                                (eacl, framewd)]):
                            if wd == wd_cl[0]:
                                wdidx = idx
                                break
                        if -1 != wdidx:
                            clnumlist = [clno]
                            for clno0 in cl_eldic[
                                    (eacl, framewd)][wdidx][1]:
                                clnumlist.append(clno0)
                            for (clno0, wd0) in cl_structdic.keys():
                                if clno0 in cl_tgtgrpdic[eacl]:
                                    if wd == wd0:
                                        clnumlist.append(clno0)
                            newclnumlist = sorted(list(set(clnumlist)))
                            cl_eldic[(eacl, framewd)][wdidx] = [
                                    wd, newclnumlist]
                        else:
                            clnumlist = [clno]
                            for (clno0, wd0) in cl_structdic.keys():
                                if clno0 in cl_tgtgrpdic[eacl]:
                                    if wd == wd0:
                                        clnumlist.append(clno0)
                            newclnumlist = sorted(list(set(clnumlist)))
                            cl_eldic[(eacl, framewd)].append(
                                    [wd, newclnumlist])
                else:
                    cl_eldic[(eacl, framewd)] = []
                    for (clno, wd) in cl_structdic[(cl, framewd)]:
                        wdidx = -1
                        for idx, wd_cl in enumerate(cl_eldic[
                                (eacl, framewd)]):
                            if wd == wd_cl[0]:
                                wdidx = idx
                                break
                        if -1 != wdidx:
                            clnumlist = [clno]
                            for clno0 in cl_eldic[(eacl, framewd)][wdidx][1]:
                                clnumlist.append(clno0)
                            for (clno0, wd0) in cl_structdic.keys():
                                if clno0 in cl_tgtgrpdic[eacl]:
                                    if wd == wd0:
                                        clnumlist.append(clno0)
                            newclnumlist = sorted(list(set(clnumlist)))
                            cl_eldic[(eacl, framewd)][wdidx] = [
                                    wd, newclnumlist]
                        else:
                            clnumlist = [clno]
                            for (clno0, wd0) in cl_structdic.keys():
                                if clno0 in cl_tgtgrpdic[eacl]:
                                    if wd == wd0:
                                        clnumlist.append(clno0)
                            newclnumlist = sorted(list(set(clnumlist)))
                            cl_eldic[(eacl, framewd)].append(
                                    [wd, newclnumlist])
    for eacl in cl_tgtgrpdic.keys():
        claimtgt = cl_tgtdic[eacl]
        for (cl, framewd) in cl_structdic.keys():
            if cl in cl_tgtgrpdic[eacl]:
                if framewd != claimtgt:
                    independent_flg = True
                    for (cl0, wd0), wdlist in cl_eldic.items():
                        if cl0 == eacl:
                            for wd_cl00 in wdlist:
                                wd00 = wd_cl00[0]
                                if wd00 == framewd:
                                    independent_flg = False
                    if independent_flg:
                        if eacl not in indwddic.keys():
                            indwddic[eacl] = [framewd]
                        else:
                            if framewd not in indwddic[eacl]:
                                indwddic[eacl].append(framewd)
    for eacl in indwddic.keys():
        for indwd in indwddic[eacl]:
            clnumlist = []
            for (cl, framewd) in cl_structdic.keys():
                if cl in cl_tgtgrpdic[eacl]:
                    if framewd == indwd:
                        clnumlist.append(cl)
            newclnumlist = sorted(list(set(clnumlist)))
            cl_eldic[(eacl, '')].append([indwd, newclnumlist])


def _clrefchainchk(rtclno, tgtclno):
    global cl_refdic
    retflg = False
    if rtclno in cl_refdic[tgtclno]:
        retflg = True
    else:
        for eacl in cl_refdic[tgtclno]:
            if _clrefchainchk(rtclno, eacl):
                retflg = True
                break
    return retflg


def _clwdsetchk():
    global ZEN
    global HAN
    global wd_set
    misspeltwds = set()
    for word1 in wd_set:
        for word2 in wd_set:
            if word1 != word2:
                if regex.search('[0-9A-Za-z]', word1):
                    if regex.search('[０-９Ａ-Ｚａ-ｚ]', word2):
                        word1r = word1.translate(word1.maketrans(ZEN, HAN))
                        word2r = word2.translate(word2.maketrans(ZEN, HAN))
                        if word1r == word2r:
                            if (word2, word1) not in misspeltwds:
                                misspeltwds.add((word1, word2))
    return misspeltwds


def _ebana():
    global prgrss
    global PTN_RF
    global PTN_EBGRPRF1
    global eb_dic
    global eb_wdrefs
    global eb_wdrefsflg
    global eb_samerefdiffs
    global eb_wdinfodic
    global eb_norefdic
    global eb_wdrefdic
    global eb_diffexpdic
    global eb_refwdlvdic
    global eb_refwdset
    global rf_allset
    global rgx_parentheses
    global rgx_ebwdhd
    global rgx_ebnum
    eb_norefdic = {}
    eb_wdrefdic = {}
    eb_diffexpdic = {}
    eb_refwdlvdic = {}
    eb_refwdset = set()
    for key in eb_dic.keys():
        _ebrefwdsrch(key)
    poptgts = set()
    eb_nameset = set()
    for (name, ref) in eb_wdrefdic.keys():
        eb_nameset.add(name)
    for (name, ref) in eb_wdrefdic.keys():
        for namex in eb_nameset:
            res = regex.search(r'^\(?{0}'.format(namex), ref)
            if res:
                poptgts.add((name, ref))
                break
    for pop_tgt in poptgts:
        eb_wdrefdic.pop(pop_tgt, None)
    poptgts = set()
    for (name, ref) in eb_wdrefdic.keys():
        rf_allset.add(ref)
    for (name, ref) in eb_wdrefdic.keys():
        nameref = ''.join((name, ref))
        for ref in rf_allset:
            if nameref in ref:
                poptgts.add((name, ref))
                break
    for pop_tgt in poptgts:
        eb_wdrefdic.pop(pop_tgt, None)
    refnamedic = {}
    for (name, ref) in eb_wdrefdic.keys():
        if ref not in refnamedic.keys():
            refnamedic[ref] = [name]
        else:
            refnamedic[ref].append(name)
    for ref in refnamedic.keys():
        if 1 < len(refnamedic[ref]):
            samerefnames = refnamedic[ref].copy()
            tgtnameset = set()
            for name1 in samerefnames:
                name1_body = rgx_ebwdhd.sub('', name1)
                for name2 in samerefnames:
                    name2_body = rgx_ebwdhd.sub('', name2)
                    if name1 != name2 and name1_body != name2_body:
                        if name2.endswith(name1):
                            tgtnameset.add((name2, name1))
            for tgtname in tgtnameset:
                expression_list = []
                if (tgtname[0], ref) in eb_diffexpdic.keys():
                    expression_list = eb_diffexpdic[(tgtname[0], ref)]
                    eb_diffexpdic.pop((tgtname[0], ref), None)
                expression_list.append(tgtname[0])
                if (tgtname[1], ref) not in eb_diffexpdic.keys():
                    eb_diffexpdic[(tgtname[1], ref)] = sorted(
                            expression_list, key=len)
                else:
                    tmplist = eb_diffexpdic[(tgtname[1], ref)]
                    tmplist.extend(expression_list)
                    eb_diffexpdic[(tgtname[1], ref)] = sorted(
                            set(tmplist), key=len)
    for (name, ref) in eb_wdrefdic.keys():
        level = eb_wdrefdic[(name, ref)]
        eb_refwdlvdic[name] = level
        if rgx_ebwdhd.search(name):
            headless_name = rgx_ebwdhd.sub('', name)
            if headless_name not in eb_refwdlvdic.keys():
                eb_refwdlvdic[headless_name] = level
        eb_refwdset.add(''.join((name, ref)))
    prgrss = 28
    for key in eb_norefdic.keys():
        _ebwdsrch(key)
    prgrss = 45
    noref_eb_wd_set = {name for (name, ref) in eb_wdrefdic.keys() if not ref}
    ref_eb_wd_set = {
            (name, ref) for (name, ref) in eb_wdrefdic.keys() if ref}
    uptgtnameset = set()
    for name1 in noref_eb_wd_set:
        for name2 in {n2 for n2 in noref_eb_wd_set if n2 != name1}:
            name1_body = rgx_ebwdhd.sub('', name1)
            name2_body = rgx_ebwdhd.sub('', name2)
            if name1_body != name2_body:
                if name2.endswith(name1):
                    uptgtnameset.add(name2)
    for name in uptgtnameset:
        if 4 > eb_wdrefdic[(name, '')]:
            eb_wdrefdic[(name, '')] += 1
    for (name, ref) in eb_wdrefdic.keys():
        lvupflg = False
        if not ref:
            ptn_subj = ''.join((
                    '{0}'.format(name),
                    '(の?(各々|夫々|おのおの|それぞれ))?は'))
        else:
            ptn_subj = ''.join((
                    '{0}'.format(name), PTN_RF, '?(', PTN_EBGRPRF1,
                    ')*[, ，、～]?', '{0}'.format(ref), '(',
                    PTN_EBGRPRF1,
                    ')*(の?(各々|夫々|おのおの|それぞれ))?は'))
        rgx_subj = regex.compile(ptn_subj)
        for key in eb_norefdic.keys():
            eb_line_rev = eb_norefdic[key]
            if name in eb_line_rev:
                blk = rgx_parentheses.sub('', eb_line_rev)
                if rgx_subj.search(blk):
                    lvupflg = True
                    break
        if lvupflg:
            eb_wdrefdic[(name, ref)] += 1
    rfdic = {}
    tmpsamerefdic = {}
    samerefdic = {}
    for (name, ref) in ref_eb_wd_set:
        level = eb_wdrefdic[(name, ref)]
        if name not in rfdic.keys():
            rfdic[name] = [level, [ref]]
        else:
            rfdic[name][1].append(ref)
        if rgx_ebnum.search(name):
            name = ''.join(('(', name, ')'))
        if ref not in tmpsamerefdic.keys():
            tmpsamerefdic[ref] = [name]
        else:
            tmpsamerefdic[ref].append(name)
    for (name, ref) in eb_diffexpdic.keys():
        if ref not in tmpsamerefdic.keys():
            tmpsamerefdic[ref] = [name, '★']
        else:
            if name not in tmpsamerefdic[ref]:
                tmpsamerefdic[ref].append(name)
            if 2 > len(tmpsamerefdic[ref]):
                tmpsamerefdic[ref].append('★')
    for ref in tmpsamerefdic.keys():
        if 1 < len(tmpsamerefdic[ref]):
            samerefdic[ref] = natsorted(tmpsamerefdic[ref])
    for name in rfdic.keys():
        rfdic[name][1] = natsorted(rfdic[name][1])
    for wdinf in natsorted(rfdic.items(), key=lambda x: x[1][1][0]):
        strref = '，'.join(wdinf[1][1])
        if 1 == wdinf[1][0]:
            eb_wdrefsflg = True
            if rgx_ebnum.search(wdinf[0]):
                eb_wdrefs.append((strref, ''.join((
                        '(', _delmrkconj(wdinf[0]), ')▲'))))
            else:
                eb_wdrefs.append((strref, ''.join((
                        _delmrkconj(wdinf[0]), '▲'))))
        else:
            if rgx_ebnum.search(wdinf[0]):
                eb_wdrefs.append((strref, ''.join((
                        '(', _delmrkconj(wdinf[0]), ')'))))
            else:
                eb_wdrefs.append((strref, _delmrkconj(wdinf[0])))
    for ref in natsorted(samerefdic.keys()):
        names = []
        for name in samerefdic[ref]:
            if '★' == name:
                continue
            if (name, ref) in eb_diffexpdic.keys():
                tmp_name = ''.join((
                        name, '(', ','.join(eb_diffexpdic[(name, ref)]), ')'))
                names.append(tmp_name)
            else:
                names.append(name)
        strname = _delmrkconj('，'.join(names))
        eb_samerefdiffs.append((ref, strname))
    for (name, ref) in eb_wdrefdic.keys():
        newwdlv = eb_wdrefdic[(name, ref)]
        if ref:
            if name in noref_eb_wd_set:
                newrefflg = 2
            else:
                newrefflg = 1
            newreflist = [ref]
        else:
            newrefflg = 0
            newreflist = []
        real_name = _delmrkconj(name)
        if real_name not in eb_wdinfodic.keys():
            eb_wdinfodic[real_name] = [newwdlv, newrefflg, newreflist, 0]
        else:
            tmpwdlv = eb_wdinfodic[real_name][0]
            if newwdlv < tmpwdlv:
                newwdlv = tmpwdlv
            tmprefflg = eb_wdinfodic[real_name][1]
            if 2 == tmprefflg:
                newrefflg = 2
            elif 1 == tmprefflg:
                if 0 == newrefflg:
                    newrefflg = 2
            else:
                if 1 == newrefflg:
                    newrefflg = 2
            tmpreflist = eb_wdinfodic[real_name][2]
            if ref:
                tmpreflist.append(ref)
                newreflist = [x for x in tmpreflist]
            else:
                newreflist = [x for x in tmpreflist]
            eb_wdinfodic[real_name] = [newwdlv, newrefflg, newreflist, 0]


def _ebrefwdsrch(key):
    global PTN_ENWDS
    global PTN_HIRAWD
    global eb_dic
    global eb_norefdic
    global eb_wdrefdic
    global imp_wdset
    global ptn_impwd
    global rgx_parentheses
    global rgx_11eb, rgx_12eb, rgx_13eb
    global rgx_21eb, rgx_22eb, rgx_23eb
    global rgx_31eb, rgx_32eb
    global rgx_40eb
    global rgx_50eb
    global rgx_englishend
    global rgx_ebgrpref1
    global rgx_noneedwds
    global rgx_imprefenend
    global rgx_imprefjpend
    ptn00 = '【'
    ptninparen = ''.join((
            r'(?P<pparen>[\(（](?P<pinparen>',
            PTN_ENWDS, r'[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*',
            PTN_HIRAWD, (
                    r'?[A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}]*([\p{Han}]'
                    '[いえきけしせちてねみめりれぎげじぜび]){0, 2}'
                    r'(|[\p{Han}]+[いえきけしせちてねみめりれぎげじぜび]|'
                    r'[ー・\p{Katakana}\p{Han}]*[A-Za-zＡ-Ｚａ-ｚ]+'
                    '[-－―・／/]?[A-Za-zＡ-Ｚａ-ｚ]+|[A-Za-zＡ-Ｚａ-ｚ]*'
                    r'[ー・\p{Katakana}\p{Han}]+))[\)）])')))
    blk = eb_dic[key]
    blkr = blk
    linestrnamerefs = set()
    linestrnameparenrefs = set()
    blk = blk.replace('第', '第＃')
    if not regex.search(ptn00, blk):
        resp = rgx_parentheses.findall(blk)
        for innerwd in resp:
            matchinfolvs = set()
            innerblk = innerwd[0]
            mres = rgx_imprefenend.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_imprefjpend.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            innerblk = prsr._transform_spc(innerblk)
            mres = rgx_11eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_12eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_13eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_21eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_22eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_23eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_31eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_32eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_40eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            mres = rgx_50eb.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namehd = namehd.replace('第＃', '第')
                namebody = res.group('name')
                reference = res.group('ref')
                rfgrp = res.group('rfgrp')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, reference)
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebrefchk(namebody, reference)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, rfgrp, level))
            deltgtmatchinfoset = {
                    (span, nameref, rfgrp, level)
                    for (span, nameref, rfgrp, level) in matchinfolvs
                    for (span2, nameref2, rfgrp2, level2)
                    in matchinfolvs if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            matchinfolvs = matchinfolvs.difference(deltgtmatchinfoset)
            for (span, nameref, rfgrp, level) in matchinfolvs:
                strnameref = ''.join((nameref[0], nameref[1], rfgrp))
                linestrnamerefs.add(strnameref)
                if nameref not in eb_wdrefdic.keys():
                    eb_wdrefdic[nameref] = level
                if rfgrp:
                    last_ref = nameref[1]
                    ref_strs = rgx_ebgrpref1.findall(rfgrp)
                    for ref_string in ref_strs:
                        if ((nameref[0], ref_string[1])
                                not in eb_wdrefdic.keys()):
                            eb_wdrefdic[(nameref[0], ref_string[1])] = level
                        if '～' == ref_string[0]:
                            ref_str = ''.join((
                                    '(', last_ref, '～', ref_string[1], ')'))
                            if ((nameref[0], ref_str)
                                    not in eb_wdrefdic.keys()):
                                eb_wdrefdic[(nameref[0], ref_str)] = level
                        last_ref = ref_string[1]
        blk = rgx_parentheses.sub('', blk)
        matchinfolvs = set()
        mres = rgx_imprefenend.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_imprefjpend.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        blk = prsr._transform_spc(blk)
        mres = rgx_11eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_12eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_13eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_21eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_22eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_23eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_31eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_32eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_40eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        mres = rgx_50eb.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namehd = namehd.replace('第＃', '第')
            namebody = res.group('name')
            reference = res.group('ref')
            rfgrp = res.group('rfgrp')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, reference)
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebrefchk(namebody, reference)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, rfgrp, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, rfgrp, level))
        deltgtmatchinfoset = {
                (span, nameref, rfgrp, level)
                for (span, nameref, rfgrp, level) in matchinfolvs
                for (span2, nameref2, rfgrp2, level2)
                in matchinfolvs if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        matchinfolvs = matchinfolvs.difference(deltgtmatchinfoset)
        for (span, nameref, rfgrp, level) in matchinfolvs:
            strnameref = ''.join((nameref[0], nameref[1], rfgrp))
            linestrnamerefs.add(strnameref)
            eb_wdrefdic[nameref] = level
            ptnnameparenref = ''.join((
                    nameref[0], '(?P<pparen>[(（](?P<pinparen>',
                    ptn_impwd, ')[)）])', nameref[1]))
            mres = regex.finditer(ptnnameparenref, blkr)
            for res in mres:
                if 2 > level:
                    level = 2
                    eb_wdrefdic[nameref] = level
                inner_parentheses = res.group('pinparen')
                newnameref = (inner_parentheses, nameref[1])
                if newnameref not in eb_wdrefdic.keys():
                    eb_wdrefdic[newnameref] = level
                strparen = res.group('pparen')
                strnameparenref = ''.join((
                        nameref[0], strparen, nameref[1], rfgrp))
                linestrnameparenrefs.add(strnameparenref)
            ptnnameparenref = ''.join((nameref[0], ptninparen, nameref[1]))
            mres = regex.finditer(ptnnameparenref, blkr)
            for res in mres:
                inner_parentheses = res.group('pinparen')
                if inner_parentheses not in imp_wdset:
                    newnameref = (inner_parentheses, nameref[1])
                    if newnameref not in eb_wdrefdic.keys():
                        eb_wdrefdic[newnameref] = level
                    strparen = res.group('pparen')
                    strnameparenref = ''.join((
                            nameref[0], strparen, nameref[1], rfgrp))
                    linestrnameparenrefs.add(strnameparenref)
            if rfgrp:
                last_ref = nameref[1]
                ref_strs = rgx_ebgrpref1.findall(rfgrp)
                for ref_string in ref_strs:
                    if (nameref[0], ref_string[1]) not in eb_wdrefdic.keys():
                        eb_wdrefdic[(nameref[0], ref_string[1])] = level
                    if '～' == ref_string[0]:
                        ref_str = ''.join((
                                '(', last_ref, '～', ref_string[1], ')'))
                        if (nameref[0], ref_str) not in eb_wdrefdic.keys():
                            eb_wdrefdic[(nameref[0], ref_str)] = level
                    last_ref = ref_string[1]
    for strnameparenref in sorted(
            linestrnameparenrefs, key=len, reverse=True):
        blkr = blkr.replace(strnameparenref, '●')
    tmpblkr = ''
    resp = rgx_parentheses.findall(blkr)
    for innerwd in resp:
        innerblk = ''.join((innerwd[0], '★'))
        tmpblkr = ''.join((tmpblkr, innerblk))
    blkr = ''.join((tmpblkr, rgx_parentheses.sub('', blkr)))
    for strnameref in sorted(linestrnamerefs, key=len, reverse=True):
        blkr = blkr.replace(strnameref, '●')
    eb_norefdic[key] = blkr


def _ebrefchk(name, reference):
    global NG_WDS
    global NG_ENDS
    global BORE_WDS
    global BORE_WDSENDS
    global BORE_ENDS
    global EB_CHEMWDS
    global PTN_EBAFTRF
    global NG_RFENDS
    global EB_NGWDRFS
    global ZEN
    global HAN
    global rf_okset
    global imp_wdset
    global rgx_refchk01, rgx_refchk02, rgx_refchk03, rgx_refchk04
    global rgx_ngend
    global rgx_chemwd
    namehan = name.translate(name.maketrans(ZEN, HAN))
    reference_han = reference.translate(reference.maketrans(ZEN, HAN))
    if namehan in NG_WDS:
        return 0
    jmpflg = False
    if rgx_ngend.search(namehan):
        return 0
    if reference not in rf_okset:
        if rgx_refchk01.search(reference_han):
            return 0
        if rgx_refchk02.search(reference_han):
            return 0
        if rgx_refchk03.search(reference_han):
            if rgx_chemwd.search(namehan):
                return 0
        res = rgx_refchk04.search(reference_han)
        if res:
            unitwd = res.group('unitword')
            if unitwd in NG_RFENDS:
                return 0
            for (nameend, ref_ending) in EB_NGWDRFS:
                if unitwd.endswith(ref_ending):
                    if namehan.endswith(nameend):
                        jmpflg = True
                        break
            if jmpflg:
                return 0
    if name in imp_wdset:
        return 4
    if namehan in BORE_WDS:
        return 1
    for wd in BORE_WDSENDS:
        if namehan.endswith(wd):
            jmpflg = True
            break
    if jmpflg:
        return 1
    for wd in BORE_ENDS:
        if namehan.endswith(wd):
            jmpflg = True
            break
    if jmpflg:
        return 1
    return 4


def _ebwdsrch(key):
    global eb_norefdic
    global eb_wdrefdic
    global rgx_parentheses
    global rgx_noneedwds
    global rgx_noneedend
    global rgx_11ex, rgx_12ex, rgx_13ex
    global rgx_21ex, rgx_22ex, rgx_24ex
    global rgx_31ex, rgx_32ex
    global rgx_40ex
    global rgx_50ex
    global rgx_impex
    ptn00 = '【'
    blk = eb_norefdic[key]
    if not regex.search(ptn00, blk):
        resp = rgx_parentheses.findall(blk)
        for innerwd in resp:
            matchinfolvs = set()
            innerblk = innerwd[0]
            mres = rgx_impex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            innerblk = prsr._transform_spc(innerblk)
            mres = rgx_11ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_12ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_13ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_21ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_22ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_24ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_31ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_32ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_40ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            mres = rgx_50ex.finditer(innerblk)
            for res in mres:
                namehd = res.group('head')
                namebody = res.group('name')
                namebody = rgx_noneedwds.sub('', namebody)
                namebody = rgx_noneedend.sub('', namebody)
                if not namebody:
                    continue
                name = ''.join((namehd, namebody))
                nameref = (name, '')
                if nameref not in eb_wdrefdic.keys():
                    chkres = _ebwdchk(namebody)
                    if 0 != chkres:
                        matchinfolvs.add((res.span(), nameref, chkres))
                else:
                    level = eb_wdrefdic[nameref]
                    matchinfolvs.add((res.span(), nameref, level))
            deltgtmatchinfoset = {
                    (span, nameref, level)
                    for (span, nameref, level) in matchinfolvs
                    for (span2, nameref2, level2)
                    in matchinfolvs if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            matchinfolvs = matchinfolvs.difference(deltgtmatchinfoset)
            for (span, nameref, level) in matchinfolvs:
                if nameref not in eb_wdrefdic.keys():
                    eb_wdrefdic[nameref] = level
        blk = rgx_parentheses.sub('', blk)
        matchinfolvs = set()
        mres = rgx_impex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        blk = prsr._transform_spc(blk)
        mres = rgx_11ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_12ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_13ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_21ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_22ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_24ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_31ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_32ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_40ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        mres = rgx_50ex.finditer(blk)
        for res in mres:
            namehd = res.group('head')
            namebody = res.group('name')
            namebody = rgx_noneedwds.sub('', namebody)
            namebody = rgx_noneedend.sub('', namebody)
            if not namebody:
                continue
            name = ''.join((namehd, namebody))
            nameref = (name, '')
            if nameref not in eb_wdrefdic.keys():
                chkres = _ebwdchk(namebody)
                if 0 != chkres:
                    matchinfolvs.add((res.span(), nameref, chkres))
            else:
                level = eb_wdrefdic[nameref]
                matchinfolvs.add((res.span(), nameref, level))
        deltgtmatchinfoset = {
                (span, nameref, level)
                for (span, nameref, level) in matchinfolvs
                for (span2, nameref2, level2)
                in matchinfolvs if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        matchinfolvs = matchinfolvs.difference(deltgtmatchinfoset)
        for (span, nameref, level) in matchinfolvs:
            if nameref not in eb_wdrefdic.keys():
                eb_wdrefdic[nameref] = level


def _ebwdchk(name):
    global SP_WDS
    global NG_WDS
    global NG_ENDS
    global BORE_WDS
    global BORE_WDSENDS
    global BORE_ENDS
    global NG_RFENDS
    global ZEN
    global HAN
    global eb_refwdlvdic
    global eb_refwdset
    global imp_wdset
    global rgx_englishend
    namehan = name.translate(name.maketrans(ZEN, HAN))
    if name in eb_refwdlvdic.keys():
        return eb_refwdlvdic[name]
    if namehan in NG_WDS:
        return 0
    if namehan in BORE_WDS:
        return 0
    if namehan in BORE_ENDS:
        return 0
    jmpflg = False
    for wd in NG_ENDS:
        if namehan.endswith(wd):
            if len(namehan) == len(wd):
                jmpflg = True
                break
            res = regex.search('[^A-Za-z_]{0}$'.format(wd), namehan)
            if res:
                jmpflg = True
                break
    if jmpflg:
        return 0
    for wd in BORE_WDSENDS:
        if namehan.endswith(wd):
            jmpflg = True
            break
    if jmpflg:
        return 0
    for wd in NG_RFENDS:
        ptn = '^{0}[A-Za-z]*'.format(wd)
        if regex.search(ptn, namehan):
            jmpflg = True
            break
    if jmpflg:
        return 0
    res = rgx_englishend.search(name)
    if res:
        nameref = (name[:res.start()], name[res.start():])
        if nameref in eb_refwdset:
            return 0
    for wd in SP_WDS:
        ptn = ''.join(('.{2, }', '{0}$'.format(wd)))
        if regex.search(ptn, namehan):
            jmpflg = True
            break
    if jmpflg:
        return 2
    if name in imp_wdset:
        return 2
    if 2 < len(name):
        return 2
    if 2 > len(name):
        return 0
    return 1  # this may be a mis-extraction


def _clkwdprc():
    global WD_CLASSMAX
    global cl_basedic
    global cl_mwddic
    global cl_wdattrdic
    global cl_wddic
    global cl_wdnodic
    global cl_wdclassnodic
    global cl_kwddic
    global cl_onlyiwddic
    global cl_allwddic
    wdnum = 1
    for eacl in cl_basedic.keys():
        tmpwdlist = []
        for word in cl_mwddic[eacl]:
            if word not in cl_wddic.values():
                word00 = _delmrkconj(word)
                if word00 in cl_wdattrdic.keys():
                    tmpwdlist.append((word, cl_wdattrdic[word00][1]))
                else:
                    tmpwdlist.append((word, 100))
        for (word, lineidx) in sorted(tmpwdlist, key=lambda x: x[1]):
            cl_wddic[wdnum] = word
            word00 = _delmrkconj(word)
            if word00 not in cl_wdnodic.keys():
                cl_wdnodic[word00] = wdnum
            if word00 not in cl_wdclassnodic.keys():
                if WD_CLASSMAX < wdnum:
                    cl_wdclassnodic[word00] = 0
                else:
                    cl_wdclassnodic[word00] = wdnum
            wdnum += 1
    for wdnum in cl_wddic.keys():
        word = _delmrkconj(cl_wddic[wdnum])
        if word in cl_kwddic.keys():
            cllist = cl_kwddic[word]
        else:
            cllist = cl_onlyiwddic[word]
        cl_allwddic[wdnum] = [word, cllist]


def _ebkwdprc():
    global eb_wdinfodic
    global eb_wdnodic
    global cl_wdnodic
    ebwdnum = 1
    for (word, val) in natsorted(eb_wdinfodic.items(), key=lambda x: x[0]):
        if word not in cl_wdnodic.keys():
            if 1 < val[0]:
                eb_wdnodic[word] = ebwdnum
                ebwdnum += 1


def _clinfogen():
    global PTN_NONEEDWD
    global PTN_NONEEDEND
    global PTN_LTDHD
    global EN_CLS
    global EN_CL
    global HD_CMTBLK
    global p_cl_lines
    global p_cl_elines
    global noefcl_flg
    global cl_basedic
    global cl_wdnodic
    global cl_wdclassnodic
    global cl_allwddic
    global wdlines_dic
    global je_wddic
    global rgx_clhd
    global rgx_del
    rfwds = ['前記の', '上記の', '前記', '上記', '当該', '該']
    rgx_refclaim = regex.compile('請求項[1-9１-９][^記]*記載')
    rgx_cltag = regex.compile(
            '★cTX【請求項(?P<number>[1-9１-９][0-9０-９]*)】★cTY')
    rgx_wdtag = regex.compile(
            '(?P<color>(b|y)) r★dTC'
            '(?P<c_d>[^★]+)★dTD(?P<jpword>[^★]+)★dTE')
    rgx_ltdhd = regex.compile(PTN_LTDHD)
    enlistflg = False
    linecnt = 1
    hdline = '★sTS【書類名】★sTE特許請求の範囲'
    hdline = ''.join((
            '★lTAc', str(linecnt), '★lTBCL-line', str(linecnt),
            '★lTC', hdline, '★lTD'))
    p_cl_lines.append(hdline)
    if je_wddic and noefcl_flg:
        enline = ''.join(('★esTS[', EN_CLS, ']★sTE'))
        enline = ''.join(('★lTAC', enline, '★lTD'))
        p_cl_elines.append(enline)
    for eacl in sorted(cl_basedic.keys()):
        for ealine in cl_basedic[eacl]:
            linecnt += 1
            rescl = rgx_clhd.search(ealine)
            if ealine.startswith(HD_CMTBLK):
                newline = ''.join(('★cmTS', ealine, '★cmTE'))
            elif rescl:
                clno = int(rescl.group('clno'))
                spancl = rescl.span()
                newline = ''.join((
                        ealine[:spancl[0]], '★cTAcl', str(clno),
                        '★cTB【請求項', rescl.group('clno'),
                        '】★cTC★cmTS', ealine[spancl[1]:], '★cmTE'))
            else:
                resset = set()
                for word in [w for w in cl_wdnodic.keys() if w in ealine]:
                    wdnum = cl_wdnodic[word]
                    ptnkwd = ''.join((
                            '(', PTN_NONEEDWD, (
                                '|^|[^0-9０-９A-Za-zＡ-Ｚａ-ｚー・'
                                r'\p{Katakana}\p{Han}])'),
                            '(?P<wd>{0})'.format(word), '(', PTN_NONEEDEND,
                            r'|$|[^A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}])'
                            ))
                    mres = regex.finditer(ptnkwd, ealine)
                    for res in mres:
                        resset.add((wdnum, word, res.span('wd')))
                deltgtmatchinfoset = {
                        (wdnum, word, span)
                        for (wdnum, word, span) in resset
                        for (wdnum2, word2, span2) in resset if span != span2
                        and span2[0] <= span[0] and span[1] <= span2[1]}
                resset = resset.difference(deltgtmatchinfoset)
                newline = ealine
                linewds = set()
                for (wdnum, word, span) in sorted(
                        resset, key=lambda x: x[2][0], reverse=True):
                    linewds.add(word)
                    if word in cl_wdclassnodic.keys():
                        strkwdclassno = str(cl_wdclassnodic[word])
                    else:
                        strkwdclassno = ''.join((' k', str(wdnum)))
                    newline = ''.join((
                            ealine[:span[1]], '★dTE', newline[span[1]:]))
                    newline = ''.join((
                            ealine[:span[0]], '★dTAk', strkwdclassno,
                            ' b r★dTCk', str(wdnum), '★dTD',
                            newline[span[0]:]))
                for refwd in rfwds:
                    newline = regex.sub(
                            ''.join((refwd, '★dTA')),
                            ''.join(('★rTS', refwd, '★rTE★dTA')),
                            newline)
                mres = rgx_refclaim.finditer(newline)
                for res in mres:
                    strrefclaim = res.group()
                    newline = newline.replace(strrefclaim, ''.join((
                            '★rcTS', strrefclaim, '★rcTE')))
                for linewd in linewds:
                    strwdline = ''.join((
                            'c', str(linecnt), '/', str(eacl), '/0'))
                    if linewd not in wdlines_dic.keys():
                        wdlines_dic[linewd] = [strwdline]
                    else:
                        wdlines_dic[linewd].append(strwdline)
            jeline = newline
            newline = ''.join((
                    '★lTAc', str(linecnt), '★lTBCL-line',
                    str(linecnt), '★lTC', newline, '★lTD'))
            p_cl_lines.append(newline)
            if je_wddic and noefcl_flg:
                enline = jeline.replace(
                        '★cTA', '☆［').replace(
                        '★cTB', '］☆★cTX').replace('★cTC', '★cTY')
                enline = rgx_del.sub('', enline)
                resnum = rgx_cltag.search(enline)
                if resnum:
                    jpnum = resnum.group('number')
                    ennum = str(int(jpnum))
                    enhd = ''.join((EN_CL, ennum))
                    enline = enline.replace(''.join((
                            '★cTX【請求項', jpnum, '】★cTY')),
                            ''.join(('★ecTX[', enhd, ']★cTY')))
                mres = rgx_wdtag.finditer(enline)
                for res in mres:
                    noreplace = True
                    bgcolor = res.group('color')
                    strctod = res.group('c_d')
                    jpwd = res.group('jpword')
                    if jpwd in je_wddic.keys():
                        if je_wddic[jpwd]:
                            enlistflg = True
                            enline = enline.replace(
                                    ''.join((
                                        bgcolor, ' r★dTC', strctod, '★dTD',
                                        jpwd, '★dTE')),
                                    ''.join((
                                        'ew', strctod, ' p f★dTY',
                                        je_wddic[jpwd], '★dTE')))
                            noreplace = False
                        else:
                            resltd = rgx_ltdhd.search(jpwd)
                            if resltd:
                                srchwd = jpwd[resltd.span()[1]:]
                                hdwd = jpwd[:resltd.span()[1]]
                                if srchwd in je_wddic.keys():
                                    if je_wddic[srchwd]:
                                        enlistflg = True
                                        enline = enline.replace(
                                                ''.join((
                                                    bgcolor, ' r★dTC',
                                                    strctod, '★dTD',
                                                    jpwd, '★dTE')),
                                                ''.join((
                                                    'ew', strctod,
                                                    ' p f★dTY', hdwd,
                                                    je_wddic[srchwd],
                                                    '★dTE')))
                                        noreplace = False
                    else:
                        resltd = rgx_ltdhd.search(jpwd)
                        if resltd:
                            srchwd = jpwd[resltd.span()[1]:]
                            hdwd = jpwd[:resltd.span()[1]]
                            if srchwd in je_wddic.keys():
                                if je_wddic[srchwd]:
                                    enlistflg = True
                                    enline = enline.replace(
                                            ''.join((
                                                bgcolor, ' r★dTC', strctod,
                                                '★dTD', jpwd, '★dTE')),
                                            ''.join((
                                                'ew', strctod, ' p f★dTY',
                                                hdwd, je_wddic[srchwd],
                                                '★dTE')))
                                    noreplace = False
                    if noreplace:
                        enline = enline.replace(
                                ''.join((
                                    bgcolor, ' r★dTC',
                                    strctod, '★dTD', jpwd, '★dTE')),
                                ''.join((
                                    'ew', strctod, ' ', bgcolor, ' f★dTY',
                                    jpwd, '★dTE')))
                enline = ''.join(('★lTAC', enline, '★lTD'))
                p_cl_elines.append(enline)
    if not enlistflg:
        p_cl_elines = []


def _hanref(strsrc):
    global ZEN4RF
    global HAN4RF
    return strsrc.translate(strsrc.maketrans(ZEN4RF, HAN4RF))


def _cleltr():
    global p_clel_lines
    global cl_tgtgrpdic
    global cl_tgtdic
    global cl_eldic
    global cl_wdclassnodic
    global cl_wdnodic
    wrtntopelset = set()
    p_clel_lines.append(
            '★hTAclElList★hTB■請求対象グループ毎のCL要素関連情報:'
            '●請求対象・関連要素 (関係記述CL番号)★hTCclElList'
            '★hTD★tTSclElList★tTE')
    grpcnt = 1
    for eacl in sorted(cl_tgtgrpdic.keys()):
        claimtgt = cl_tgtdic[eacl]
        for wdclaim in cl_eldic[(eacl, '')]:
            wd = wdclaim[0]
            wdnum = cl_wdnodic[wd]
            if claimtgt == wd:
                p_clel_lines.append(''.join((
                        '★ssTS■グループ', str(grpcnt), '［CL',
                        ','.join(map(str, cl_tgtgrpdic[eacl])),
                        '］★ssTE')))
                grpcnt += 1
                wrtntopelset = set()
                if wd in cl_wdclassnodic.keys():
                    strkwdclassno = str(cl_wdclassnodic[wd])
                else:
                    strkwdclassno = ''.join((' k', str(wdnum)))
                p_clel_lines.append(''.join((
                        '●★dTAk', strkwdclassno, ' b r★dTCk', str(wdnum),
                        '★dTD', wd, '★dTE(',
                        ','.join(map(str, wdclaim[1])), ')')))
                wrtntopelset.add(wd)
                break
        for (clno, keyword) in natsorted(
                cl_eldic.keys(), key=lambda x: (x[0], _delmrkconj(x[1]))):
            if eacl == clno and claimtgt == keyword:
                _cleltrsb(1, clno, keyword, wrtntopelset)
        for wdclaim in cl_eldic[(eacl, '')]:
            wd = wdclaim[0]
            wdnum = cl_wdnodic[wd]
            if claimtgt != wd:
                if wd in cl_wdclassnodic.keys():
                    strkwdclassno = str(cl_wdclassnodic[wd])
                else:
                    strkwdclassno = ''.join((' k', str(wdnum)))
                p_clel_lines.append(''.join((
                        '・★dTAk', strkwdclassno, ' b r★dTCk', str(wdnum),
                        '★dTD', wd, '★dTE(', ','.join(map(str, wdclaim[1])),
                        ')')))
                wrtntopelset.add(wd)
                for (clno, keyword) in natsorted(
                        cl_eldic.keys(), key=lambda x: (x[0], x[1])):
                    if eacl == clno and wd == keyword:
                        _cleltrsb(1, clno, keyword, wrtntopelset)
        p_clel_lines.append('')
    p_clel_lines.append('★tTC')


def _cleltrsb(cnt, clno, pre_wd, wrtntopelset):
    global p_clel_lines
    global cl_eldic
    global cl_wdclassnodic
    global cl_wdnodic
    for wdcl_n in natsorted(cl_eldic[(clno, pre_wd)], key=lambda x: x[0]):
        wd_n = wdcl_n[0]
        if wd_n in cl_wdnodic.keys():
            wdnum = cl_wdnodic[wd_n]
            if wd_n in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[wd_n])
            else:
                strkwdclassno = ''.join((' k', str(wdnum)))
            p_clel_lines.append(''.join((
                    '　', '→' * cnt, '★dTAk', strkwdclassno,
                    ' b r★dTCk', str(wdnum), '★dTD', wd_n,
                    '★dTE(', ','.join(map(str, wdcl_n[1])), ')')))
        else:
            p_clel_lines.append(''.join((
                    '　', '→' * cnt, wd_n, '(',
                    ','.join(map(str, wdcl_n[1])), ')')))
        if 10 > cnt:
            if wd_n in wrtntopelset:
                break
            if (clno, wd_n) in cl_eldic.keys():
                _cleltrsb(cnt+1, clno, wd_n, wrtntopelset)


def _cltr():
    global NUMS
    global p_tr_lines
    global cl_tgtdic
    global cl_cmtdic
    global cl_refdic
    lastclaimtgt = ''
    p_tr_lines.append(
            '★hTAtrList★hTB■クレームツリー'
            '★hTCtrList★hTD★tTStrList★tTE')
    for eacl in sorted(cl_refdic.keys()):
        refmark = ''
        lastnum = 0
        for i in cl_refdic[eacl]:
            refmark = ''.join((refmark, '－'*(i-lastnum-1), '〇'))
            lastnum = i
        refmark = ''.join((refmark, '－'*(eacl-lastnum-1)))
        claimtgt = cl_tgtdic[eacl]
        if lastclaimtgt != claimtgt:
            p_tr_lines.append(''.join(('［', claimtgt, '］')))
        lastclaimtgt = claimtgt
        comment = cl_cmtdic[eacl]
        if not comment:
            comment = _clcmt(eacl)
        if 10 > eacl:
            p_tr_lines.append(''.join((
                    refmark, '★ctTAcl', str(eacl), '★ctTB',
                    NUMS[eacl], '★ctTC．★cmTS', comment, '★cmTE')))
        else:
            p_tr_lines.append(''.join((
                    refmark, '★ctTAcl', str(eacl), '★ctTB',
                    str(eacl), '★ctTC．★cmTS', comment, '★cmTE')))
    p_tr_lines.append('★tTC')


def _clcmt(clno):
    global cl_alljwdset
    global cl_iwddic
    global cl_structdic
    global cl_tgtdic
    cmtlist = []
    claimtgt = cl_tgtdic[clno]
    if claimtgt:
        for (cl, wd) in cl_structdic.keys():
            if cl == clno and wd == claimtgt:
                for (cl1, wd1) in cl_structdic[(cl, wd)]:
                    if wd1 not in cmtlist:
                        cmtlist.append(wd1)
        if cmtlist:
            strcom = ''.join((
                    claimtgt, '(', ','.join(natsorted(cmtlist)), ')'))
            return strcom
    allsblist = []
    for (cl, wd) in cl_structdic.keys():
        if cl == clno:
            for jwd in cl_alljwdset:
                jwd00 = _delmrkconj(jwd)
                if jwd00 == wd:
                    for (cl1, wd1) in cl_structdic[(cl, wd)]:
                        if wd1 not in allsblist:
                            allsblist.append(wd1)
    for (cl, wd) in cl_structdic.keys():
        if cl == clno:
            for jwd in cl_alljwdset:
                jwd00 = _delmrkconj(jwd)
                if jwd00 == wd:
                    if wd not in allsblist:
                        sblist = []
                        for (cl1, wd1) in cl_structdic[(cl, wd)]:
                            if wd1 not in sblist:
                                sblist.append(wd1)
                        if sblist:
                            strpart = ''.join((
                                    jwd00, '(',
                                    ','.join(natsorted(sblist)), ')'))
                            if strpart not in cmtlist:
                                cmtlist.append(strpart)
    if cmtlist:
        strcom = ','.join(natsorted(cmtlist))
        return strcom
    onlyiwdset = set()
    for iwd in cl_iwddic[clno]:
        if iwd not in cl_alljwdset:
            onlyiwdset.add(iwd)
    if onlyiwdset:
        allsblist = []
        for (cl, wd) in cl_structdic.keys():
            if cl == clno:
                for (cl1, wd1) in cl_structdic[(cl, wd)]:
                    for onlyiwd in onlyiwdset:
                        onlyiwd00 = _delmrkconj(onlyiwd)
                        if wd1 == onlyiwd00:
                            if wd1 not in allsblist:
                                allsblist.append(wd1)
        for (cl, wd) in cl_structdic.keys():
            if cl == clno:
                if wd not in allsblist:
                    for (cl1, wd1) in cl_structdic[(cl, wd)]:
                        sblist = []
                        for onlyiwd in onlyiwdset:
                            onlyiwd00 = _delmrkconj(onlyiwd)
                            if wd1 == onlyiwd00:
                                if wd1 not in sblist:
                                    sblist.append(wd1)
                        if sblist:
                            strpart = ''.join((
                                    wd, '(', ','.join(natsorted(sblist)),
                                    ')'))
                            if strpart not in cmtlist:
                                cmtlist.append(strpart)
    if cmtlist:
        strcom = ','.join(natsorted(cmtlist))
        return strcom
    for onlyiwd in onlyiwdset:
        onlyiwd00 = _delmrkconj(onlyiwd)
        if onlyiwd00 not in cmtlist:
            cmtlist.append(onlyiwd00)
    if cmtlist:
        strcom = ','.join(natsorted(cmtlist))
        return strcom
    allsblist = []
    for (cl, wd) in cl_structdic.keys():
        if cl == clno:
            for (cl1, wd1) in cl_structdic[(cl, wd)]:
                for iwd in cl_iwddic[clno]:
                    iwd00 = _delmrkconj(iwd)
                    if wd1 == iwd00:
                        if wd1 not in allsblist:
                            allsblist.append(wd1)
    for (cl, wd) in cl_structdic.keys():
        if cl == clno:
            if wd not in allsblist:
                for (cl1, wd1) in cl_structdic[(cl, wd)]:
                    sblist = []
                    for iwd in cl_iwddic[clno]:
                        iwd00 = _delmrkconj(iwd)
                        if wd1 == iwd00:
                            if wd1 not in sblist:
                                sblist.append(wd1)
                        if sblist:
                            strpart = ''.join((
                                    wd, '(', ','.join(natsorted(sblist)),
                                    ')'))
                            if strpart not in cmtlist:
                                cmtlist.append(strpart)
    if cmtlist:
        strcom = ','.join(natsorted(cmtlist))
        return strcom
    allsblist = []
    for (cl, wd) in cl_structdic.keys():
        if cl == clno:
            for (cl1, wd1) in cl_structdic[(cl, wd)]:
                if wd1 not in allsblist:
                    allsblist.append(wd1)
    for (cl, wd) in cl_structdic.keys():
        if cl == clno:
            if wd not in allsblist:
                sblist = []
                for (cl1, wd1) in cl_structdic[(cl, wd)]:
                    if wd1 not in sblist:
                        sblist.append(wd1)
                if sblist:
                    strpart = ''.join((
                            wd, '(', ','.join(natsorted(sblist)), ')'))
                    if strpart not in cmtlist:
                        cmtlist.append(strpart)
    if cmtlist:
        strcom = ','.join(natsorted(cmtlist))
        return strcom
    for iwd in cl_iwddic[clno]:
        iwd00 = _delmrkconj(iwd)
        if iwd00 not in cmtlist:
            cmtlist.append(iwd00)
    if cmtlist:
        strcom = ','.join(natsorted(cmtlist))
        return strcom
    strcom = ''
    return strcom


def _clstructtr():
    global NUMS
    global p_trel_lines
    global cl_tgtdic
    global cl_refdic
    lastclaimtgt = ''
    p_trel_lines.append(
            '★hTAtrElList★hTB■構成クレームツリー'
            '★hTCtrElList★hTD★tTStrElList★tTE')
    for eacl in sorted(cl_refdic.keys()):
        refmark = ''
        lastnum = 0
        for i in cl_refdic[eacl]:
            refmark = ''.join((refmark, '－'*(i-lastnum-1), '〇'))
            lastnum = i
        refmark = ''.join((refmark, '－'*(eacl-lastnum-1)))
        claimtgt = cl_tgtdic[eacl]
        if lastclaimtgt != claimtgt:
            p_trel_lines.append(''.join(('［', claimtgt, '］')))
        lastclaimtgt = claimtgt
        comment = _clstructcmt(eacl)
        if 10 > eacl:
            p_trel_lines.append(''.join((
                    refmark, '★ctTAcl', str(eacl), '★ctTB',
                    NUMS[eacl], '★ctTC．★cmTS', comment, '★cmTE')))
        else:
            p_trel_lines.append(''.join((
                    refmark, '★ctTAcl', str(eacl), '★ctTB',
                    str(eacl), '★ctTC．★cmTS', comment, '★cmTE')))
    p_trel_lines.append('★tTC')


def _clstructcmt(clno):
    global cl_structdic
    global cl_tgtdic
    strcom = ''
    chklist = []
    claimtgt = cl_tgtdic[clno]
    if claimtgt:
        if (clno, claimtgt) in cl_structdic.keys():
            tmplist1 = []
            for (cl1, wd1) in cl_structdic[(clno, claimtgt)]:
                if wd1 not in chklist:
                    chklist.append(wd1)
                if (cl1, wd1) in cl_structdic.keys():
                    wd1 = _clstructcmtsba(2, cl1, wd1, chklist)
                if wd1 not in tmplist1:
                    tmplist1.append(wd1)
            if tmplist1:
                strcom = ''.join((
                        strcom, claimtgt, '(', ','.join(natsorted(tmplist1)),
                        ')'))
    chklist2 = []
    for (cl, wd0) in cl_structdic.keys():
        if cl == clno and wd0 != claimtgt and wd0 not in chklist:
            _clstructcmtsbb(1, cl, wd0, chklist2)
    tmplist = chklist + chklist2
    chklist = list(set(tmplist))
    tmplist0 = []
    for (cl, wd0) in cl_structdic.keys():
        if cl == clno and wd0 != claimtgt and wd0 not in chklist:
            tmplist1 = []
            for (cl1, wd1) in cl_structdic[(cl, wd0)]:
                if (cl1, wd1) in cl_structdic.keys():
                    wd1 = _clstructcmtsbc(2, cl1, wd1)
                if wd1 not in tmplist1:
                    tmplist1.append(wd1)
            if tmplist1:
                wd0 = ''.join((wd0, '(', ','.join(natsorted(tmplist1)), ')'))
            if wd0 not in tmplist0:
                tmplist0.append(wd0)
    if tmplist0:
        if not strcom:
            strcom = ','.join(natsorted(tmplist0))
        else:
            strcom = ''.join((strcom, ',', ','.join(natsorted(tmplist0))))
    return strcom


def _clstructcmtsba(cnt, precln, prewdn, chklist):
    global cl_structdic
    tmplistn = []
    for (cl_n, wd_n) in cl_structdic[(precln, prewdn)]:
        if wd_n not in chklist:
            chklist.append(wd_n)
        if 10 > cnt:
            if (cl_n, wd_n) in cl_structdic.keys():
                wd_n = _clstructcmtsba(cnt+1, cl_n, wd_n, chklist)
        if wd_n not in tmplistn:
            tmplistn.append(wd_n)
    if tmplistn:
        prewdn = ''.join((prewdn, '(', ','.join(natsorted(tmplistn)), ')'))
    return prewdn


def _clstructcmtsbb(cnt, precln, prewdn, chklist):
    global cl_structdic
    for (cl_n, wd_n) in cl_structdic[(precln, prewdn)]:
        if wd_n not in chklist:
            chklist.append(wd_n)
        if 10 > cnt:
            if (cl_n, wd_n) in cl_structdic.keys():
                _clstructcmtsbb(cnt+1, precln, prewdn, chklist)


def _clstructcmtsbc(cnt, precln, prewdn):
    global cl_structdic
    tmplistn = []
    for (cl_n, wd_n) in cl_structdic[(precln, prewdn)]:
        if 10 > cnt:
            if (cl_n, wd_n) in cl_structdic.keys():
                wd_n = _clstructcmtsbc(cnt+1, cl_n, wd_n)
        if wd_n not in tmplistn:
            tmplistn.append(wd_n)
    if tmplistn:
        prewdn = ''.join((prewdn, '(', ','.join(natsorted(tmplistn)), ')'))
    return prewdn


def _refgen():
    global AUTO_RF_MARK
    global ZEN
    global HAN
    global p_warn_lines
    global p_ref_lines
    global cl_wdattrdic
    global cl_topelset
    global cl_topmethodelset
    global cl_allstructdic
    global eb_wdinfodic
    global eb_wdrefs
    global eb_wdrefsflg
    global eb_samerefdiffs
    global rf_refdic
    global rgx_pgcl
    cl_topelset = set()
    for element in cl_allstructdic.keys():
        cl_topelset.add(element)
    for element in cl_allstructdic.keys():
        for element2 in cl_allstructdic[element]:
            cl_topelset.discard(element2)
    for element in cl_topelset:
        _refgensba(1, element)
    cl_topmethodelset = set()
    for element in cl_topelset:
        if cl_wdattrdic[element][3]:
            cl_topmethodelset.add(element)
    for element in cl_topmethodelset:
        cl_topelset.discard(element)
    delete_tgt_set = set()
    for element in cl_topelset:
        okflg = False
        if element in cl_allstructdic.keys():
            if cl_allstructdic[element]:
                okflg = True
        if element in cl_allstrgdic.keys():
            for element2 in cl_allstrgdic[element]:
                if not rgx_pgcl.search(element2):
                    okflg = True
        if not okflg:
            delete_tgt_set.add(element)
    for element in delete_tgt_set:
        cl_topelset.discard(element)
    num = len(cl_topelset)
    if 10 > num:
        refno = 1
    elif 91 > num:
        refno = 10
    else:
        refno = 100
    for element in natsorted(
            cl_topelset, key=lambda x: (cl_wdattrdic[x][4], x)):
        if 0 == cl_wdattrdic[element][5]:
            cl_wdattrdic[element][5] = refno
            if element in cl_allstructdic.keys():
                if 10 > len(cl_allstructdic[element]):
                    refno1 = refno * 10 + 1
                else:
                    refno1 = refno * 100 + 1
                _refgensbb(1, element, refno1, True)
            refno += 1
    num = len(cl_topmethodelset)
    if 10 > num:
        refno = 1
    elif 91 > num:
        refno = 10
    else:
        refno = 100
    for element in natsorted(
            cl_topmethodelset, key=lambda x: (cl_wdattrdic[x][4], x)):
        if 0 == cl_wdattrdic[element][5]:
            cl_wdattrdic[element][5] = refno
            if element in cl_allstructdic.keys():
                if 10 > len(cl_allstructdic[element]):
                    refno1 = refno * 10 + 1
                else:
                    refno1 = refno * 100 + 1
                _refgensbb(1, element, refno1, False)
            refno += 1
    figallrefauto = True
    for element, attrs in cl_wdattrdic.items():
        if 0 != attrs[5]:
            if element in rf_refdic.keys():
                figallrefauto = False
                tmp_refs = rf_refdic[element][0].split('～')
                tmpstrref = tmp_refs[0]
                cl_wdattrdic[element][6] = tmpstrref.translate(
                        tmpstrref.maketrans(HAN, ZEN))
            elif element in eb_wdinfodic.keys():
                if 0 < eb_wdinfodic[element][1]:
                    figallrefauto = False
                    tmp_eb_ref_list = eb_wdinfodic[element][2]
                    eb_ref_list = natsorted(
                            [ref for ref in tmp_eb_ref_list
                                if not regex.search('～', ref)])
                    eb_ref = eb_ref_list[0]
                    cl_wdattrdic[element][6] = eb_ref.translate(
                            eb_ref.maketrans(HAN, ZEN))
    if figallrefauto:
        for element, attrs in cl_wdattrdic.items():
            if 0 != attrs[5]:
                str_reference = _zeno(attrs[5])
                if attrs[3]:
                    str_reference = ''.join(('Ｓ', str_reference))
                cl_wdattrdic[element][6] = str_reference
    else:
        for element, attrs in cl_wdattrdic.items():
            if 0 != attrs[5]:
                if not attrs[6]:
                    str_reference = ''.join((_zeno(attrs[5]), AUTO_RF_MARK))
                    if attrs[3]:
                        str_reference = ''.join(('Ｓ', str_reference))
                    cl_wdattrdic[element][6] = str_reference
    p_ref_lines.append(
            '★hTArefClList1★hTB■CL構成要素関連の符号情報'
            '★hTCrefClList1★hTD★tTSrefClList1★tTE')
    flg_exsist_info = False
    for element, attrs in natsorted(
            cl_wdattrdic.items(), key=lambda x: x[1][6]):
        if 0 != attrs[5]:
            p_ref_lines.append(''.join(('　', attrs[6], '　', element)))
            flg_exsist_info = True
    if not flg_exsist_info:
        p_ref_lines.append('　なし')
        p_ref_lines.append('★tTC')
    else:
        p_ref_lines.append('★tTC')
        if figallrefauto:
            p_ref_lines.append(
                    '★hTArefClList2★hTB'
                    '■CL構成要素関連の符号情報(関連順)'
                    '★hTCrefClList2★hTD★tTSrefClList2★tTE')
            for element, attrs in sorted(
                    cl_wdattrdic.items(), key=lambda x: _zeno(x[1][5])):
                if 0 != attrs[5] and (not attrs[3]):
                    p_ref_lines.append(''.join((
                            '　', attrs[6], '　', element)))
            for element, attrs in sorted(
                    cl_wdattrdic.items(),
                    key=lambda x: _zeno(x[1][5])):
                if 0 != attrs[5] and (attrs[3]):
                    p_ref_lines.append(''.join((
                            '　', attrs[6], '　', element)))
            p_ref_lines.append('★tTC')
    if eb_wdrefs:
        if eb_wdrefsflg:
            p_ref_lines.append(
                    '★hTArefEbList1★hTB■原文実施形態(EB)要素の符号情報'
                    '(▲:有用性疑問有)★hTCrefEbList1★hTD'
                    '★tTSrefEbList1★tTE')
        else:
            p_ref_lines.append(
                    '★hTArefEbList1★hTB■原文実施形態(EB)要素の符号情報'
                    '★hTCrefEbList1★hTD★tTSrefEbList1★tTE')
        for (str_ref, strel) in eb_wdrefs:
            p_ref_lines.append(''.join(('　', str_ref, '　', strel)))
        p_ref_lines.append('★tTC')
    if eb_samerefdiffs:
        p_ref_lines.append(
                '★hTArefEbList2★hTB■原文実施形態(EB)の同一符号複数要素'
                '(異表現)情報★hTCrefEbList2★hTD★tTSrefEbList2★tTE')
        for (str_ref, strel) in eb_samerefdiffs:
            p_ref_lines.append(''.join(('　', str_ref, '　', strel)))
        p_ref_lines.append('★tTC')


def _refgensba(cnt, preel_n):
    global cl_wdattrdic
    global cl_allstructdic
    for eln in cl_allstructdic[preel_n]:
        if 10 > cnt:
            if eln in cl_allstructdic.keys():
                _refgensba(cnt+1, eln)
        if cl_wdattrdic[preel_n][4] > cl_wdattrdic[eln][4]:
            cl_wdattrdic[preel_n][4] = cl_wdattrdic[eln][4]


def _refgensbb(cnt, preel_n, refno_n, flg):
    global p_warn_lines
    global cl_wdattrdic
    global cl_allstructdic
    for eln in natsorted(
            cl_allstructdic[preel_n], key=lambda x: (cl_wdattrdic[x][4], x)):
        if flg == cl_wdattrdic[eln][3]:
            p_warn_lines.append(''.join((
                    '★wTS■包含関係が不適切かもしれない用語があります★wTE:',
                    eln, ' in ', preel_n)))
        if 0 == cl_wdattrdic[eln][5]:
            cl_wdattrdic[eln][5] = refno_n
            if 10 > cnt:
                if eln in cl_allstructdic.keys():
                    if 10 > len(cl_allstructdic[eln]):
                        nex_refno = refno_n * 10 + 1
                    else:
                        nex_refno = refno_n * 100 + 1
                    _refgensbb(cnt+1, eln, nex_refno, flg)
            refno_n += 1


def _zeno(number):
    global ZEN_NUM
    global HAN_NUM
    str_num = str(number)
    return str_num.translate(str_num.maketrans(HAN_NUM, ZEN_NUM))


def _figgen():
    global END_STRG
    global STR_DFLTDESC_S, STR_DFLTDESC_M, STR_DFLTDESC_D
    global p_fig_lines
    global cl_wdattrdic
    global cl_topelset
    global cl_topmethodelset
    global cl_allpgdic
    global cl_allstrgdic
    global cl_allstructdic
    global cl_tgtdic
    global fig_dic
    global fig_streldic
    global rgx_datcl
    global rgx_pgcl
    p_fig_lines.append(
            '★hTAfigList★hTB■図面情報(CLベース/text)★hTCfigList★hTD'
            '★tTSfigList★tTE')
    p_fig_lines.append('★sTS【書類名】★sTE図面')
    index = 1
    writtenellist = []
    ellist = []
    cl1target = cl_tgtdic[1]
    element = cl1target
    ellist.append(element)
    if element in cl_allstructdic.keys():
        if cl_allstructdic[element]:
            figno = _zeno(index)
            p_fig_lines.append(''.join(('★sTS【図', figno, '】★sTE')))
            strsel0 = []
            strel0, strelwithsp = _figelstr(index, element)
            p_fig_lines.append(''.join(('　', strelwithsp)))
            if rgx_datcl.search(element):
                strdesc = STR_DFLTDESC_D
            elif cl_wdattrdic[element][3]:
                strdesc = STR_DFLTDESC_M
            else:
                strdesc = STR_DFLTDESC_S
            strsel0.append(''.join((
                    strel0, 'は、■{', strel0, 'の説明', strdesc, '}。')))
            strdesc = ''
            includetgt = _figstructel(
                    1, element, strel0, strsel0, ellist, [], index, cl1target)
            fig_streldic[index] = strsel0
            if rgx_datcl.search(element):
                strfig = ''.join((
                        '図', figno, 'は', element, 'の一例を示す図である。'))
                strfigref = ''.join((
                        '図', figno, 'は、', strel0,
                        'の一例を示す図である。'))
            elif cl_wdattrdic[element][3]:
                strfig = ''.join((
                        '図', figno, 'は', element,
                        'の一例を示すフローチャートである。'))
                strfigref = ''.join((
                        '図', figno, 'は、', strel0,
                        'の一例を示すフローチャートである。'))
            else:
                strfig = ''.join((
                        '図', figno, 'は', element,
                        'の構成の一例を示す図である。'))
                strfigref = ''.join((
                        '図', figno, 'は、', strel0,
                        'の構成の一例を示す図である。'))
            fig_dic[index] = [element, '', 1, strfig, strfigref]
            index += 1
    if 1 < index:
        ellist2 = ellist.copy()
        for element in ellist:
            if element in cl_allstrgdic.keys():
                if cl_allstrgdic[element]:
                    figno = _zeno(index)
                    p_fig_lines.append(
                            ''.join(('★sTS【図', figno, '】★sTE')))
                    strsel0 = []
                    strel0, strelwithsp = (_figelstr(index, element))
                    p_fig_lines.append(''.join((
                            '　（', strel0, 'における記録内容例）')))
                    strel1list = []
                    strsel1 = []
                    for element1 in natsorted(
                            cl_allstrgdic[element],
                            key=lambda x: (cl_wdattrdic[x][4], x)):
                        if element1 not in ellist2:
                            ellist2.append(element1)
                        strel1, strelwithsp = (_figelstr(index, element1))
                        p_fig_lines.append(''.join((
                                '　', '　'*1, strelwithsp)))
                        if rgx_datcl.search(element1):
                            strdesc = STR_DFLTDESC_D
                        elif cl_wdattrdic[element1][3]:
                            strdesc = STR_DFLTDESC_M
                        else:
                            strdesc = STR_DFLTDESC_S
                        strsel1.append(''.join((
                                strel1, 'は、■{', strel1, 'の説明', strdesc,
                                '}。')))
                        strdesc = ''
                        if element1 in cl_allstructdic.keys():
                            includetgt = _figstructel(
                                    2, element1, strel1, strsel1, ellist2, [],
                                    index, cl1target)
                        strel1list.append(strel1)
                    if strel1list:
                        if 1 == len(strel1list):
                            strsel0 += [''.join((
                                    strel0, 'は、', strel1list[0],
                                    'である。'))]
                        else:
                            strsel0 += [''.join((
                                    strel0, 'は、',
                                    '、'.join(strel1list[:-1]), '及び',
                                    strel1list[-1], 'である。'))]
                        strsel0 += strsel1
                    fig_streldic[index] = strsel0
                    if cl_wdattrdic[element][3]:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'における記録内容の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'の一例を示す図である。'))
                    else:  # may change expression in the future
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'における記録内容の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'の一例を示す図である。'))
                    fig_dic[index] = [element, '', 2, strfig, strfigref]
                    index += 1
        writtenellist = ellist2.copy()
        for element in ellist2:
            if element in cl_allpgdic.keys():
                if cl_allpgdic[element]:
                    figno = _zeno(index)
                    p_fig_lines.append(''.join((
                            '★sTS【図', figno, '】★sTE')))
                    strsel0 = []
                    strel0 = element
                    p_fig_lines.append(''.join((
                            '　（', element,
                            'により実現される処理/機能/構成例）')))
                    strel1list = []
                    strsel1 = []
                    for element1 in natsorted(
                            cl_allpgdic[element],
                            key=lambda x: (cl_wdattrdic[x][4], x)):
                        if element1 not in writtenellist:
                            writtenellist.append(element1)
                        strel1, strelwithsp = (_figelstr(index, element1))
                        p_fig_lines.append(''.join((
                                '　', '　'*1, strelwithsp)))
                        if rgx_datcl.search(element1):
                            strdesc = STR_DFLTDESC_D
                        elif cl_wdattrdic[element1][3]:
                            strdesc = STR_DFLTDESC_M
                        else:
                            strdesc = STR_DFLTDESC_S
                        strsel1.append(''.join((
                                strel1, 'は、■{', strel1, 'の説明', strdesc,
                                '}。')))
                        strdesc = ''
                        if element1 in cl_allstructdic.keys():
                            includetgt = _figstructel(
                                    2, element1, strel1, strsel1,
                                    writtenellist, [], index, cl1target)
                        strel1list.append(strel1)
                    if strel1list:
                        if 1 == len(strel1list):
                            strsel0 += [''.join((
                                    strel0, 'により、', strel1list[0],
                                    'が実現される。'))]
                        else:
                            strsel0 += [''.join((
                                    strel0, 'により、',
                                    '、'.join(strel1list[:-1]), '及び',
                                    strel1list[-1], 'が実現される。'))]
                        strsel0 += strsel1
                    fig_streldic[index] = strsel0
                    numsbel = len(cl_allpgdic[element])
                    if 1 == numsbel:
                        sbel = cl_allpgdic[element][0]
                    else:
                        sbel = ''.join((
                                '、'.join(cl_allpgdic[element][:-1]),
                                '及び', cl_allpgdic[element][-1]))
                    if cl_wdattrdic[cl_allpgdic[element][0]][3]:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'により実現される', sbel,
                                'の一例を示すフローチャートである。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'により実現される', sbel,
                                'の一例を示すフローチャートである。'))
                    else:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'により実現される', sbel,
                                'の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'により実現される', sbel,
                                'の一例を示す図である。'))
                    fig_dic[index] = [element, '', 3, strfig, strfigref]
                    index += 1
    else:
        pgelset = set()
        dataelset = set()
        if rgx_pgcl.search(element) and element in cl_allpgdic.keys():
            pgelset.add(element)
        elif (END_STRG == element[-len(END_STRG):]
                and (1, element) in cl_strgdic.keys()):
            for (clno, content) in cl_strgdic[(1, element)]:
                if 1 == clno:
                    if rgx_pgcl.search(content):
                        if content in cl_allpgdic.keys():
                            pgelset.add(content)
                    else:
                        if content in cl_allstructdic.keys():
                            dataelset.add(content)
        for pgel in pgelset:
            if cl_allpgdic[pgel]:
                figno = _zeno(index)
                p_fig_lines.append(''.join(('★sTS【図', figno, '】★sTE')))
                strsel0 = []
                strel0 = pgel
                p_fig_lines.append(''.join((
                        '　（', pgel, 'により実現される処理/機能/構成例）')))
                strel1list = []
                strsel1 = []
                for element1 in natsorted(
                        cl_allpgdic[pgel],
                        key=lambda x: (cl_wdattrdic[x][4], x)):
                    if element1 not in writtenellist:
                        writtenellist.append(element1)
                    strel1, strelwithsp = (_figelstr(index, element1))
                    p_fig_lines.append(''.join(('　', '　'*1, strelwithsp)))
                    if rgx_datcl.search(element1):
                        strdesc = STR_DFLTDESC_D
                    elif cl_wdattrdic[element1][3]:
                        strdesc = STR_DFLTDESC_M
                    else:
                        strdesc = STR_DFLTDESC_S
                    strsel1 += [''.join((
                            strel1, 'は、■{', strel1, 'の説明', strdesc,
                            '}。'))]
                    strdesc = ''
                    if element1 in cl_allstructdic.keys():
                        includetgt = _figstructel(
                                2, element1, strel1, strsel1,
                                writtenellist, [], index, cl1target)
                    strel1list.append(strel1)
                if strel1list:
                    if 1 == len(strel1list):
                        strsel0 += [''.join((
                                strel0, 'により、', strel1list[0],
                                'が実現される。'))]
                    else:
                        strsel0 += [''.join((
                                strel0, 'により、',
                                '、'.join(strel1list[:-1]), '及び',
                                strel1list[-1], 'が実現される。'))]
                    strsel0 += strsel1
                fig_streldic[index] = strsel0
                numsbel = len(cl_allpgdic[pgel])
                if 1 == numsbel:
                    sbel = cl_allpgdic[pgel][0]
                else:
                    sbel = ''.join((
                            '、'.join(
                                cl_allpgdic[pgel][:-1]),
                            '及び', cl_allpgdic[pgel][-1]))
                if cl_wdattrdic[cl_allpgdic[pgel][0]][3]:
                    strfig = ''.join((
                            '図', _zeno(index), 'は', pgel,
                            'により実現される', sbel,
                            'の一例を示すフローチャートである。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、', strel0,
                            'により実現される', sbel,
                            'の一例を示すフローチャートである。'))
                else:
                    strfig = ''.join((
                            '図', _zeno(index), 'は', pgel,
                            'により実現される', sbel,
                            'の一例を示す図である。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、', strel0,
                            'により実現される', sbel,
                            'の一例を示す図である。'))
                fig_dic[index] = [pgel, '', 3, strfig, strfigref]
                index += 1
        for datael in dataelset:
            if cl_allstructdic[datael]:
                if datael not in writtenellist:
                    writtenellist.append(datael)
                figno = _zeno(index)
                p_fig_lines.append(''.join(('★sTS【図', figno, '】★sTE')))
                strsel0 = []
                strel0, strelwithsp = (_figelstr(index, datael))
                p_fig_lines.append(''.join(('　（', strel0, 'の構成例）')))
                if rgx_datcl.search(datael):
                    strdesc = STR_DFLTDESC_D
                elif cl_wdattrdic[datael][3]:
                    strdesc = STR_DFLTDESC_M
                else:
                    strdesc = STR_DFLTDESC_S
                strsel0 += [''.join((
                        strel0, 'は、■{', strel0, 'の説明', strdesc, '}。'))]
                strdesc = ''
                includetgt = _figstructel(
                        1, datael, strel0, strsel0, writtenellist, [], index,
                        cl1target)
                fig_streldic[index] = strsel0
                strfig = ''.join((
                        '図', _zeno(index), 'は', datael,
                        'の構成の一例を示す図である。'))
                strfigref = ''.join((
                        '図', _zeno(index), 'は、', strel0,
                        'の構成の一例を示す図である。'))
                fig_dic[index] = [datael, '', 4, strfig, strfigref]
                index += 1
    for element in writtenellist:
        cl_topelset.discard(element)
        cl_topmethodelset.discard(element)
    for element in natsorted(
            cl_topelset,
            key=lambda x: (cl_wdattrdic[x][4], cl_wdattrdic[x][0])):
        ellist = []
        if element in cl_allstructdic.keys():
            if cl_allstructdic[element]:
                figno = _zeno(index)
                p_fig_lines.append(''.join(('★sTS【図', figno, '】★sTE')))
                strsel0 = []
                strel0, strelwithsp = _figelstr(index, element)
                p_fig_lines.append(''.join(('　', strelwithsp)))
                if rgx_datcl.search(element):
                    strdesc = STR_DFLTDESC_D
                elif cl_wdattrdic[element][3]:
                    strdesc = STR_DFLTDESC_M
                else:
                    strdesc = STR_DFLTDESC_S
                strsel0 += [''.join((
                        strel0, 'は、■{', strel0, 'の説明', strdesc, '}。'))]
                strdesc = ''
                includetgt = ''
                ellist.append(element)
                includetgt = _figstructel(
                        1, element, strel0, strsel0, ellist, writtenellist,
                        index, cl1target)
                fig_streldic[index] = strsel0
                if rgx_datcl.search(element):
                    strfig = ''.join((
                            '図', _zeno(index), 'は', element,
                            'の一例を示す図である。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、',
                            strel0, 'の一例を示す図である。'))
                elif cl_wdattrdic[element][3]:
                    strfig = ''.join((
                            '図', _zeno(index), 'は', element,
                            'の一例を示すフローチャートである。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、',
                            strel0,
                            'の一例を示すフローチャートである。'))
                else:
                    strfig = ''.join((
                            '図', _zeno(index), 'は', element,
                            'の構成の一例を示す図である。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、',
                            strel0, 'の構成の一例を示す図である。'))
                fig_dic[index] = [element, includetgt, 1, strfig, strfigref]
                index += 1
        for element in ellist:
            if element not in writtenellist:
                writtenellist.append(element)
        ellist2 = ellist.copy()
        for element in ellist:
            if element in cl_allstrgdic.keys():
                if cl_allstrgdic[element]:
                    figno = _zeno(index)
                    p_fig_lines.append(''.join((
                            '★sTS【図', figno, '】★sTE')))
                    strsel0 = []
                    strel0, strelwithsp = (_figelstr(index, element))
                    p_fig_lines.append(''.join((
                            '　（', strel0, 'における記録内容例）')))
                    strel1list = []
                    strsel1 = []
                    for element1 in natsorted(
                            cl_allstrgdic[element],
                            key=lambda x: (cl_wdattrdic[x][4], x)):
                        if element1 not in ellist2:
                            ellist2.append(element1)
                        strel1, strelwithsp = (_figelstr(index, element1))
                        p_fig_lines.append(''.join((
                                '　', '　'*1, strelwithsp)))
                        if element1 not in writtenellist:
                            if rgx_datcl.search(element1):
                                strdesc = STR_DFLTDESC_D
                            elif cl_wdattrdic[element1][3]:
                                strdesc = STR_DFLTDESC_M
                            else:
                                strdesc = STR_DFLTDESC_S
                            strsel1 += [''.join((
                                    strel1, 'は、■{', strel1,
                                    'の説明', strdesc, '}。'))]
                            strdesc = ''
                            if element1 in cl_allstructdic.keys():
                                includetgt = _figstructel(
                                        2, element1, strel1, strsel1, ellist2,
                                        writtenellist, index, '')
                        strel1list.append(strel1)
                    if strel1list:
                        if 1 == len(strel1list):
                            strsel0 += [''.join((
                                    strel0, 'は、',
                                    strel1list[0], 'である。'))]
                        else:
                            strsel0 += [''.join((
                                    strel0, 'は、',
                                    '、'.join(strel1list[:-1]), '及び',
                                    strel1list[-1], 'である。'))]
                        strsel0 += strsel1
                    fig_streldic[index] = strsel0
                    if cl_wdattrdic[element][3]:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'における記録内容の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'の一例を示す図である。'))
                    else:  # may change expression in the future
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'における記録内容の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'の一例を示す図である。'))
                    fig_dic[index] = [element, '', 2, strfig, strfigref]
                    index += 1
        for element in ellist2:
            if element not in writtenellist:
                writtenellist.append(element)
        ellist3 = []
        for element in ellist2:
            if element in cl_allpgdic.keys():
                if cl_allpgdic[element]:
                    figno = _zeno(index)
                    p_fig_lines.append(''.join((
                            '★sTS【図', figno, '】★sTE')))
                    strsel0 = []
                    strel0 = element
                    p_fig_lines.append(''.join((
                            '　（', element,
                            'により実現される処理/機能/構成例）')))
                    strel1list = []
                    strsel1 = []
                    for element1 in natsorted(
                            cl_allpgdic[element],
                            key=lambda x: (cl_wdattrdic[x][4], x)):
                        if element1 not in ellist3:
                            ellist3.append(element1)
                        strel1, strelwithsp = (_figelstr(index, element1))
                        p_fig_lines.append(''.join((
                                '　', '　'*1, strelwithsp)))
                        if element1 not in writtenellist:
                            if rgx_datcl.search(element1):
                                strdesc = STR_DFLTDESC_D
                            elif cl_wdattrdic[element1][3]:
                                strdesc = STR_DFLTDESC_M
                            else:
                                strdesc = STR_DFLTDESC_S
                            strsel1 += [''.join((
                                    strel1, 'は、■{', strel1,
                                    'の説明', strdesc, '}。'))]
                            strdesc = ''
                            if element1 in cl_allstructdic.keys():
                                includetgt = _figstructel(
                                        2, element1, strel1, strsel1, ellist3,
                                        writtenellist, index, '')
                        strel1list.append(strel1)
                    if strel1list:
                        if 1 == len(strel1list):
                            strsel0 += [''.join((
                                    strel0, 'により、',
                                    strel1list[0], 'が実現される。'))]
                        else:
                            strsel0 += [''.join((
                                    strel0, 'により、',
                                    '、'.join(strel1list[:-1]), '及び',
                                    strel1list[-1], 'が実現される。'))]
                        strsel0 += strsel1
                    fig_streldic[index] = strsel0
                    numsbel = len(cl_allpgdic[element])
                    if 1 == numsbel:
                        sbel = cl_allpgdic[element][0]
                    else:
                        sbel = ''.join((
                                '、'.join(cl_allpgdic[element][:-1]),
                                '及び', cl_allpgdic[element][-1]))
                    if cl_wdattrdic[cl_allpgdic[element][0]][3]:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'により実現される', sbel,
                                'の一例を示すフローチャートである。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'により実現される', sbel,
                                'の一例を示すフローチャートである。'))
                    else:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'により実現される', sbel,
                                'の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'により実現される', sbel,
                                'の一例を示す図である。'))
                    fig_dic[index] = [element, '', 3, strfig, strfigref]
                    index += 1
        for element in ellist3:
            if element not in writtenellist:
                writtenellist.append(element)
    for element in natsorted(
            cl_topmethodelset,
            key=lambda x: (cl_wdattrdic[x][4], cl_wdattrdic[x][0])):
        ellist = []
        if element in cl_allstructdic.keys():
            if cl_allstructdic[element]:
                figno = _zeno(index)
                p_fig_lines.append(''.join(('★sTS【図', figno, '】★sTE')))
                strsel0 = []
                strel0, strelwithsp = _figelstr(index, element)
                p_fig_lines.append(''.join(('　', strelwithsp)))
                if rgx_datcl.search(element):
                    strdesc = STR_DFLTDESC_D
                elif cl_wdattrdic[element][3]:
                    strdesc = STR_DFLTDESC_M
                else:
                    strdesc = STR_DFLTDESC_S
                strsel0 += [''.join((
                        strel0, 'は、■{', strel0, 'の説明',
                        strdesc, '}。'))]
                strdesc = ''
                includetgt = ''
                ellist.append(element)
                includetgt = _figstructel(
                        1, element, strel0, strsel0, ellist,
                        writtenellist, index, cl1target)
                fig_streldic[index] = strsel0
                if rgx_datcl.search(element):
                    strfig = ''.join((
                            '図', _zeno(index), 'は', element,
                            'の一例を示す図である。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、',
                            strel0, 'の一例を示す図である。'))
                elif cl_wdattrdic[element][3]:
                    strfig = ''.join((
                            '図', _zeno(index), 'は', element,
                            'の一例を示すフローチャートである。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、',
                            strel0,
                            'の一例を示すフローチャートである。'))
                else:
                    strfig = ''.join((
                            '図', _zeno(index), 'は', element,
                            'の構成の一例を示す図である。'))
                    strfigref = ''.join((
                            '図', _zeno(index), 'は、',
                            strel0, 'の構成の一例を示す図である。'))
                fig_dic[index] = [element, includetgt, 1, strfig, strfigref]
                index += 1
        for element in ellist:
            if element not in writtenellist:
                writtenellist.append(element)
        ellist2 = ellist.copy()
        for element in ellist:
            if element in cl_allstrgdic.keys():
                if cl_allstrgdic[element]:
                    figno = _zeno(index)
                    p_fig_lines.append(''.join((
                            '★sTS【図', figno, '】★sTE')))
                    strsel0 = []
                    strel0, strelwithsp = (_figelstr(index, element))
                    p_fig_lines.append(''.join((
                            '　（', strel0, 'における記録内容例）')))
                    strel1list = []
                    strsel1 = []
                    for element1 in natsorted(
                            cl_allstrgdic[element],
                            key=lambda x: (cl_wdattrdic[x][4], x)):
                        if element1 not in ellist2:
                            ellist2.append(element1)
                        strel1, strelwithsp = (_figelstr(index, element1))
                        p_fig_lines.append(''.join((
                                '　', '　'*1, strelwithsp)))
                        if element1 not in writtenellist:
                            if rgx_datcl.search(element1):
                                strdesc = STR_DFLTDESC_D
                            elif cl_wdattrdic[element1][3]:
                                strdesc = STR_DFLTDESC_M
                            else:
                                strdesc = STR_DFLTDESC_S
                            strsel1 += [''.join((
                                    strel1, 'は、■{', strel1,
                                    'の説明', strdesc, '}。'))]
                            strdesc = ''
                            if element1 in cl_allstructdic.keys():
                                includetgt = _figstructel(
                                        2, element1, strel1, strsel1, ellist2,
                                        writtenellist, index, '')
                        strel1list.append(strel1)
                    if strel1list:
                        if 1 == len(strel1list):
                            strsel0 += [''.join((
                                    strel0, 'は、',
                                    strel1list[0], 'である。'))]
                        else:
                            strsel0 += [''.join((
                                    strel0, 'は、',
                                    '、'.join(strel1list[:-1]), '及び',
                                    strel1list[-1], 'である。'))]
                        strsel0 += strsel1
                    fig_streldic[index] = strsel0
                    if cl_wdattrdic[element][3]:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'における記録内容の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'の一例を示す図である。'))
                    else:  # may change expression in the future
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'における記録内容の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'の一例を示す図である。'))
                    fig_dic[index] = [element, '', 2, strfig, strfigref]
                    index += 1
        for element in ellist2:
            if element not in writtenellist:
                writtenellist.append(element)
        ellist3 = []
        for element in ellist2:
            if element in cl_allpgdic.keys():
                if cl_allpgdic[element]:
                    figno = _zeno(index)
                    p_fig_lines.append(''.join((
                            '★sTS【図', figno, '】★sTE')))
                    strsel0 = []
                    strel0 = element
                    p_fig_lines.append(''.join((
                            '　（', element,
                            'により実現される処理/機能/構成例）')))
                    strel1list = []
                    strsel1 = []
                    for element1 in natsorted(
                            cl_allpgdic[element],
                            key=lambda x: (cl_wdattrdic[x][4], x)):
                        if element1 not in ellist3:
                            ellist3.append(element1)
                        strel1, strelwithsp = (_figelstr(index, element1))
                        p_fig_lines.append(''.join((
                                '　', '　'*1, strelwithsp)))
                        if element1 not in writtenellist:
                            if rgx_datcl.search(element1):
                                strdesc = STR_DFLTDESC_D
                            elif cl_wdattrdic[element1][3]:
                                strdesc = STR_DFLTDESC_M
                            else:
                                strdesc = STR_DFLTDESC_S
                            strsel1 += [''.join((
                                    strel1, 'は、■{', strel1,
                                    'の説明', strdesc, '}。'))]
                            strdesc = ''
                            if element1 in cl_allstructdic.keys():
                                includetgt = _figstructel(
                                        2, element1, strel1, strsel1, ellist3,
                                        writtenellist, index, '')
                        strel1list.append(strel1)
                    if strel1list:
                        if 1 == len(strel1list):
                            strsel0 += [''.join((
                                    strel0, 'により、',
                                    strel1list[0], 'が実現される。'))]
                        else:
                            strsel0 += [''.join((
                                    strel0, 'により、',
                                    '、'.join(strel1list[:-1]), '及び',
                                    strel1list[-1], 'が実現される。'))]
                        strsel0 += strsel1
                    fig_streldic[index] = strsel0
                    numsbel = len(cl_allpgdic[element])
                    if 1 == numsbel:
                        sbel = cl_allpgdic[element][0]
                    else:
                        sbel = ''.join((
                                '、'.join(cl_allpgdic[element][:-1]),
                                '及び', cl_allpgdic[element][-1]))
                    if cl_wdattrdic[cl_allpgdic[element][0]][3]:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'により実現される', sbel,
                                'の一例を示すフローチャートである。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'により実現される', sbel,
                                'の一例を示すフローチャートである。'))
                    else:
                        strfig = ''.join((
                                '図', _zeno(index), 'は', element,
                                'により実現される', sbel,
                                'の一例を示す図である。'))
                        strfigref = ''.join((
                                '図', _zeno(index), 'は、',
                                strel0, 'により実現される', sbel,
                                'の一例を示す図である。'))
                    fig_dic[index] = [element, '', 3, strfig, strfigref]
                    index += 1
        for element in ellist3:
            if element not in writtenellist:
                writtenellist.append(element)
    p_fig_lines.append('★tTC')


def _figstructel(
        cnt, preel, prestrel, prestrsel, elupdatelist, writtenlist, index,
        cl1target):
    global p_fig_lines
    global cl_allstructdic
    global cl_wdattrdic
    includetgt = ''
    strel_nlist = []
    strsel_n = []
    for eln in natsorted(
            cl_allstructdic[preel], key=lambda x: (cl_wdattrdic[x][4], x)):
        if eln not in elupdatelist:
            elupdatelist.append(eln)
        strel_n, strelwithsp = _figelstr(index, eln)
        p_fig_lines.append(''.join(('　', '　'*cnt, strelwithsp)))
        if 10 > cnt:
            if eln not in writtenlist:
                strsel_n.append(''.join((
                        strel_n, 'は、■{', strel_n, 'の説明', '}。')))
                if eln in cl_allstructdic.keys():
                    includetgt = _figstructel(
                            cnt+1, eln, strel_n, strsel_n, elupdatelist,
                            writtenlist, index, cl1target)
        if 10 == cnt:
            strsel_n.append(''.join((
                    strel_n, 'は、■{', strel_n, 'の説明', '}。')))
        if eln == cl1target:
            includetgt = cl1target
        strel_nlist.append(strel_n)
    if strel_nlist:
        if 1 == len(strel_nlist):
            if prestrsel:
                prestrsel[-1] = ''.join((
                        prestrsel[-1], prestrel, 'は、例えば、',
                        strel_nlist[0], 'を含み得るが、例えば、',
                        strel_nlist[0], 'を含まなくてもよい',
                        '■{本実施の形態に記載すべき',
                        '要素か否かの判断等に基づき',
                        'この文/図面内容等を適宜修正下さい}。'))
            else:
                prestrsel.append(''.join((
                        prestrel, 'は、例えば、',
                        strel_nlist[0], 'を含み得るが、例えば、',
                        strel_nlist[0], 'を含まなくてもよい',
                        '■{本実施の形態に記載すべき',
                        '要素か否かの判断等に基づき',
                        'この文/図面内容等を適宜修正下さい}。')))
        else:
            if prestrsel:
                prestrsel[-1] = ''.join((
                        prestrsel[-1], prestrel, 'は、例えば、',
                        '、'.join(strel_nlist[:-1]), '及び',
                        strel_nlist[-1], 'を含み得るが、例えば、',
                        '、'.join(strel_nlist[:-1]), '及び',
                        strel_nlist[-1], 'のいずれかを含まなくても',
                        'よい■{本実施の形態に記載すべき',
                        '要素か否かの判断等に基づき',
                        'この文/図面内容等を適宜修正下さい}。'))
            else:
                prestrsel.append(''.join((
                        prestrel, 'は、例えば、',
                        '、'.join(strel_nlist[:-1]), '及び',
                        strel_nlist[-1], 'を含み得るが、例えば、',
                        '、'.join(strel_nlist[:-1]), '及び',
                        strel_nlist[-1], 'のいずれかを含まなくても',
                        'よい■{本実施の形態に記載すべき',
                        '要素か否かの判断等に基づき',
                        'この文/図面内容等を適宜修正下さい}。')))
        prestrsel += strsel_n
    return includetgt


def _figelstr(index, element):
    global cl_wdattrdic
    if 0 == cl_wdattrdic[element][7]:
        cl_wdattrdic[element][7] = index
    if 0 == cl_wdattrdic[element][5]:
        elstring = element
        elstringwithsp = element
    else:
        str_num = cl_wdattrdic[element][6]
        elstring = ''.join((element, str_num))
        elstringwithsp = ''.join((element, '　'*4, str_num))
    return elstring, elstringwithsp


def _abstgen():
    global p_abs_lines
    global cl_wdattrdic
    global cl_tgtdic
    global cl1_list
    global rgx_parentheses
    claimtgt = cl_tgtdic[1]
    if 0 < cl_wdattrdic[claimtgt][5]:
        strrefno = cl_wdattrdic[claimtgt][6]
        abstpct = ''.join((claimtgt, '（', strrefno, '）は、'))
    else:
        strrefno = ''
        abstpct = ''.join((claimtgt, 'は、'))
    abst = ''.join((claimtgt, strrefno, 'は、'))
    for strline in cl1_list:
        newline = rgx_parentheses.sub('', strline)
        resset = set()
        for wd in cl_wdattrdic.keys():
            if 1 == cl_wdattrdic[wd][7]:
                mres = regex.finditer(''.join((
                        ('(^|前記の|上記の|前記|上記|当該|該(?!当)|、|'
                         r'[^A-Za-zＡ-Ｚａ-ｚー・\p{Katakana}\p{Han}])'),
                        '{0}'.format(wd),
                        ('(?=(夫々|各々|又|若|及|並|或|上|内|中|＋'
                         r'★［[^＋]+］★＋|\p{Hiragana}|$))')
                        )), newline)
                for res in mres:
                    resset.add((wd, res.span()))
        deltgtmatchinfoset = {
                (word, span) for (word, span) in resset
                for (word2, span2) in resset if span != span2
                and span2[0] <= span[0] and span[1] <= span2[1]}
        resset = resset.difference(deltgtmatchinfoset)
        newlinepct = newline
        for (wd, span) in sorted(resset, key=lambda x: x[1][1], reverse=True):
            if 0 < cl_wdattrdic[wd][5]:
                strrefno = cl_wdattrdic[wd][6]
                strrefnopct = ''.join(('（', strrefno, '）'))
                newline = ''.join((
                        newline[:span[1]], strrefno, newline[span[1]:]))
                newlinepct = ''.join((
                        newlinepct[:span[1]], strrefnopct,
                        newlinepct[span[1]:]))
        abst = ''.join((abst, newline))
        abstpct = ''.join((abstpct, newlinepct))
    tmp_regex1 = regex.compile(''.join((
            '(コンピュータ(で|により)?(読み取り|読取り|読取)可能な)?',
            claimtgt, '(。|$)')))
    tmp_regex2 = regex.compile('(前記の|上記の|前記|上記|当該|該)')
    abst = tmp_regex1.sub('。', abst)
    abst = tmp_regex2.sub('', abst)
    abstpct = tmp_regex1.sub('。', abstpct)
    abstpct = tmp_regex2.sub('', abstpct)
    p_abs_lines.append(
            '★hTAabsJpList★hTB■JP要約情報(CLベース)★hTCabsJpList★hTD'
            '★tTSabsJpList★tTE')
    p_abs_lines.append('★sTS【書類名】★sTE要約書')
    p_abs_lines.append('★sTS【要約】★sTE')
    p_abs_lines.append(''.join((
            ('★sTS【課題】★sTE■{技術的課題/効果:～の低減/～の向上等}に'
             '有用な'),
            claimtgt, 'を提供する。')))
    p_abs_lines.append(''.join(('★sTS【解決手段】★sTE', abst)))
    p_abs_lines.append('★sTS【選択図】★sTE図１')
    p_abs_lines.append('★tTC')
    p_abs_lines.append(
        '★hTAabsPctList★hTB■PCT要約情報(CLベース)★hTCabsPctList★hTD'
        '★tTSabsPctList★tTE')
    p_abs_lines.append('★sTS【書類名】★sTE要約書')
    p_abs_lines.append(''.join(('　■{技術的課題}すべく、', abstpct)))
    p_abs_lines.append('★tTC')


def _spczinfogen():
    global SPC_NEWHEADSDIC
    global SPC_HEADSNODIC
    global SPC_HEADSBRNCHDIC
    global PTN_NONEEDWD
    global PTN_NONEEDEND
    global ZEN_NUM
    global HAN_NUM
    global ZEN
    global HAN
    global PTN_EBRFAFTEN
    global PTN_RF
    global PTN_EBGRPRF
    global PTN_LTDHD
    global p_spc_lines
    global p_spc_elines
    global noefspc_flg
    global p_spchd_lines
    global cl_wdnodic
    global cl_wdclassnodic
    global eb_dic
    global eb_wdinfodic
    global eb_wdnodic
    global spc_basedic
    global wdlines_dic
    global used_paranoset
    global je_wddic
    global rgx_englishend
    global rgx_hdbasic
    global rgx_para
    global rgx_spchdno
    global rgx_spchdnobr
    global rgx_del
    rgx_paratag = regex.compile('★pTX【(?P<para_no>[^】]+)】★pTY')
    rgx_stag = regex.compile('★sTS【(?P<heading>[^】]+)】★sTE')
    rgx_wdreftag = regex.compile(
            '★dTA(?P<wd_class>(k|w w))'
            '(?P<wd_no>[0-9]+) (?P<color>(b|y)) r★dTC'
            '(?P<c_d>[^★]+)★dTD(?P<jpword>[^★]+)★dTE(?P<jpref>'
            r'[^★\p{Han}\p{Hiragana}\p{Katakana}]*)')
    rgx_ltdhd = regex.compile(PTN_LTDHD)
    rgx_spcframe = regex.compile(
            r'^\s?(【.+】|[\[\(\<［（＜].+[\]\)\>］）＞]$)')
    rgx_allhd = regex.compile('【.+】')
    rgx_clinspc = regex.compile('■請求項(?P<clno>[1-9１-９][0-9０-９]*)')
    clwdinebparadic = {}
    enlistflg = False
    framepspclines = []
    paranum = 0
    linecnt = 0
    for key in sorted(spc_basedic.keys()):
        ealine = spc_basedic[key]
        linecnt += 1
        res = rgx_hdbasic.search(ealine)
        if res:
            heading = res.group('heading')
            respara = rgx_para.search(heading)
            spanhd = res.span()
            if respara:
                paranum = int(respara.group('paranum'))
                if paranum not in used_paranoset:
                    used_paranoset.add(paranum)
                    newline = ''.join((
                            ealine[:spanhd[0]], '★pTApa', str(paranum),
                            '★pTB【', heading, '】★pTC',
                            ealine[spanhd[1]:]))
                else:
                    newline = ''.join((
                            ealine[:spanhd[0]], '★pTX【', heading,
                            '】★pTY', ealine[spanhd[1]:]))
                    paranum = 0
            else:
                flg = True
                for spcheading in SPC_NEWHEADSDIC.keys():
                    if heading == spcheading:
                        newline = ''.join((
                                ealine[:spanhd[0]], '★sTS【',
                                heading, '】★sTE', ealine[spanhd[1]:]))
                        paranum = 0
                        flg = False
                        break
                if flg:
                    if rgx_spchdno.search(heading):
                        newline = ''.join((
                                ealine[:spanhd[0]], '★sTS【',
                                heading, '】★sTE', ealine[spanhd[1]:]))
                        paranum = 0
                        flg = False
                if flg:
                    if rgx_spchdnobr.search(heading):
                        newline = ''.join((
                                ealine[:spanhd[0]], '★sTS【',
                                heading, '】★sTE', ealine[spanhd[1]:]))
                        paranum = 0
                        flg = False
                if flg:
                    newline = ealine
        elif key in eb_dic.keys():
            resset = set()
            for word in [w for w in cl_wdnodic.keys() if w in ealine]:
                wdnum = cl_wdnodic[word]
                if rgx_englishend.search(word):
                    ptnkwd = ''.join((
                            '(', PTN_NONEEDWD,
                            ('|^|[^0-9０-９A-Za-zＡ-Ｚａ-ｚー・'
                             r'\p{Katakana}\p{Han}])'),
                            '(?P<wd>{0})'.format(word), '(',
                            PTN_NONEEDEND,
                            ('|$|[^A-Za-zＡ-Ｚａ-ｚー・'
                             r'\p{Katakana}\p{Han}])')))
                else:
                    ptnkwd = ''.join((
                            '(', PTN_NONEEDWD,
                            ('|^|[^0-9０-９A-Za-zＡ-Ｚａ-ｚー・'
                             r'\p{Katakana}\p{Han}])'),
                            '(?P<wd>{0})'.format(word), '(',
                            PTN_NONEEDEND,
                            r'|$|[^ー・\p{Katakana}\p{Han}])'))
                mres = regex.finditer(ptnkwd, ealine)
                for res in mres:
                    resset.add((True, wdnum, word, res.span('wd')))
            for word in [w for w in eb_wdnodic.keys() if w in ealine]:
                wdnum = eb_wdnodic[word]
                if rgx_englishend.search(word):
                    ptnkwd = ''.join((
                            '(', PTN_NONEEDWD,
                            ('|^|[^0-9０-９A-Za-zＡ-Ｚａ-ｚー・'
                             r'\p{Katakana}\p{Han}])'),
                            '(?P<wd>{0})'.format(word),
                            '(', PTN_NONEEDEND,
                            ('|$|[^A-Za-zＡ-Ｚａ-ｚー・'
                             r'\p{Katakana}\p{Han}])')))
                else:
                    ptnkwd = ''.join((
                            '(', PTN_NONEEDWD,
                            ('|^|[^0-9０-９A-Za-zＡ-Ｚａ-ｚー・'
                             r'\p{Katakana}\p{Han}])'),
                            '(?P<wd>{0})'.format(word),
                            '(', PTN_NONEEDEND,
                            r'|$|[^ー・\p{Katakana}\p{Han}])'))
                mres = regex.finditer(ptnkwd, ealine)
                for res in mres:
                    resset.add((False, wdnum, word, res.span('wd')))
            deltgtmatchinfoset = {
                    (cl_wd_flg, wdnum, word, span)
                    for (cl_wd_flg, wdnum, word, span) in resset
                    for (cl_wd_flg2, wdnum2, word2, span2) in resset
                    if span != span2
                    and span2[0] <= span[0] and span[1] <= span2[1]}
            resset = resset.difference(deltgtmatchinfoset)
            newline = ealine
            linewds = set()
            reswdset = set()
            for (cl_wd_flg, wdnum, word, span) in sorted(
                    resset, key=lambda x: x[3][0], reverse=True):
                if word in eb_wdinfodic.keys():
                    eb_wdinfodic[word][3] += 1
                linewds.add(word)
                if cl_wd_flg:
                    if word not in reswdset:
                        reswdset.add(word)
                        if paranum in clwdinebparadic.keys():
                            if (wdnum, word) not in clwdinebparadic[paranum]:
                                clwdinebparadic[paranum].append((wdnum, word))
                        else:
                            clwdinebparadic[paranum] = [(wdnum, word)]
                    if word in cl_wdclassnodic.keys():
                        strkwdclassno = str(cl_wdclassnodic[word])
                    else:
                        strkwdclassno = ''.join((' k', str(wdnum)))
                    newline = ''.join((
                            ealine[:span[1]], '★dTE', newline[span[1]:]))
                    newline = ''.join((
                            ealine[:span[0]], '★dTAk',
                            strkwdclassno, ' b r★dTCk', str(wdnum), '★dTD',
                            newline[span[0]:]))
                else:
                    newline = ''.join((
                            ealine[:span[1]], '★dTE', newline[span[1]:]))
                    newline = ''.join((
                            ealine[:span[0]], '★dTAw w',
                            str(wdnum), ' y r★dTCw', str(wdnum),
                            '★dTD', newline[span[0]:]))
            for linewd in linewds:
                strwdline = ''.join(('s', str(linecnt), '/0/', str(paranum)))
                if linewd not in wdlines_dic.keys():
                    wdlines_dic[linewd] = [strwdline]
                else:
                    wdlines_dic[linewd].append(strwdline)
        else:
            newline = ealine
        enline = newline
        frameline = newline
        mres = rgx_clinspc.finditer(newline)
        for res in sorted(mres, key=lambda x: x.span()[0], reverse=True):
            strclno = str(int(res.group('clno')))
            newline = ''.join((
                    newline[:res.span()[0]], '★qA', strclno,
                    '★qB', res.group(), '★qC', newline[res.span()[1]:]))
        newline = ''.join((
                '★lTAs', str(linecnt), '★lTB明細line', str(linecnt),
                '★lTC', newline, '★lTD'))
        p_spc_lines.append(newline)
        if je_wddic and noefspc_flg:
            enline = enline.replace(
                    '★pTA', '☆［').replace(
                    '★pTB', '］☆★pTX').replace('★pTC', '★pTY')
            enline = rgx_del.sub('', enline)
            respara = rgx_paratag.search(enline)
            res = rgx_stag.search(enline)
            if res:
                jp_heading = res.group('heading')
                if jp_heading in SPC_NEWHEADSDIC.keys():
                    enhd = SPC_NEWHEADSDIC[jp_heading]
                    enline = enline.replace(''.join((
                            '★sTS【', jp_heading, '】★sTE')),
                            ''.join(('★esTS[', enhd, ']★sTE')))
                else:
                    resp = rgx_spchdno.search(jp_heading)
                    if resp:
                        jpnum = resp.group('number')
                        ennum = str(int(jpnum))
                        for spcheadingno in SPC_HEADSNODIC.keys():
                            if jp_heading.startswith(spcheadingno):
                                enhd = ''.join((
                                        SPC_HEADSNODIC[spcheadingno], ennum))
                                enline = enline.replace(
                                        ''.join((
                                                '★sTS【', spcheadingno,
                                                jpnum, '】★sTE')),
                                        ''.join((
                                                '★esTS[', enhd, ']★sTE')))
                                break
                    else:
                        resp = rgx_spchdnobr.search(jp_heading)
                        if resp:
                            jpnum = resp.group('number_br')
                            ennum = jpnum.translate(jpnum.maketrans(ZEN, HAN))
                            ennum = ennum.upper()
                            if regex.search(r'\([A-Z]\)$', ennum):
                                ennum = ennum.replace(
                                        '(', '').replace(')', '')
                            for spcheadingbr in SPC_HEADSBRNCHDIC.keys():
                                if jp_heading.startswith(spcheadingbr):
                                    enhd = ''.join((
                                            SPC_HEADSBRNCHDIC[spcheadingbr],
                                            ennum))
                                    enline = enline.replace(
                                            ''.join((
                                                    '★sTS【', spcheadingbr,
                                                    jpnum, '】★sTE')),
                                            ''.join((
                                                    '★esTS[', enhd,
                                                    ']★sTE')))
                                    break
            elif respara:
                jpparano = respara.group('para_no')
                enparano = jpparano.translate(jpparano.maketrans(
                        ZEN_NUM, HAN_NUM))
                enline = enline.replace(''.join((
                        '★pTX【', jpparano, '】★pTY')),
                        ''.join(('★epTX[', enparano, ']★pTY')))
            elif key in eb_dic.keys():
                mres = rgx_wdreftag.finditer(enline)
                for res in mres:
                    noreplace = True
                    bgcolor = res.group('color')
                    strctod = res.group('c_d')
                    wd_class = res.group('wd_class')
                    wd_no = res.group('wd_no')
                    if 'w w' == wd_class:
                        newclass = ''.join(('w eww', wd_no))
                    else:
                        newclass = ''.join((wd_class, wd_no, ' ew', strctod))
                    jpwd = res.group('jpword')
                    tmpjpref = res.group('jpref')
                    jpref = ''
                    enref = ''
                    if rgx_englishend.search(jpwd):
                        ptnjpref = ''.join(('^', PTN_EBRFAFTEN, PTN_EBGRPRF))
                    else:
                        ptnjpref = ''.join(('^', PTN_RF, PTN_EBGRPRF))
                    resref = regex.search(ptnjpref, tmpjpref)
                    if resref:
                        jpref = ''.join((
                                resref.group('ref'), resref.group('rfgrp')))
                    if jpref:
                        enref = ''.join((' ', _hanref(jpref)))
                    if jpwd in je_wddic.keys():
                        enwd = je_wddic[jpwd]
                        if enwd:
                            enlistflg = True
                            enline = enline.replace(
                                    ''.join((
                                        '★dTA', wd_class, wd_no, ' ',
                                        bgcolor, ' r★dTC', strctod, '★dTD',
                                        jpwd, '★dTE', jpref)),
                                    ''.join((
                                        '★dTA', newclass, ' p f★dTY',
                                        enwd, '★dTE', enref)))
                            noreplace = False
                        else:
                            resltd = rgx_ltdhd.search(jpwd)
                            if resltd:
                                srchwd = jpwd[resltd.span()[1]:]
                                hdwd = jpwd[:resltd.span()[1]]
                                if srchwd in je_wddic.keys():
                                    if je_wddic[srchwd]:
                                        enlistflg = True
                                        enline = enline.replace(
                                                ''.join((
                                                    '★dTA', wd_class,
                                                    wd_no, ' ', bgcolor,
                                                    ' r★dTC', strctod,
                                                    '★dTD', jpwd, '★dTE',
                                                    jpref)),
                                                ''.join((
                                                    '★dTA', newclass,
                                                    ' p f★dTY', hdwd,
                                                    je_wddic[srchwd],
                                                    '★dTE', enref)))
                                        noreplace = False
                    else:
                        resltd = rgx_ltdhd.search(jpwd)
                        if resltd:
                            srchwd = jpwd[resltd.span()[1]:]
                            hdwd = jpwd[:resltd.span()[1]]
                            if srchwd in je_wddic.keys():
                                if je_wddic[srchwd]:
                                    enlistflg = True
                                    enline = enline.replace(
                                            ''.join((
                                                '★dTA', wd_class,
                                                wd_no, ' ', bgcolor,
                                                ' r★dTC', strctod, '★dTD',
                                                jpwd, '★dTE', jpref)),
                                            ''.join((
                                                '★dTA', newclass,
                                                ' p f★dTY', hdwd,
                                                je_wddic[srchwd],
                                                '★dTE', enref)))
                                    noreplace = False
                    if noreplace:
                        enline = enline.replace(
                                ''.join((
                                    '★dTA', wd_class, wd_no, ' ', bgcolor,
                                    ' r★dTC', strctod, '★dTD', jpwd,
                                    '★dTE', jpref)),
                                ''.join((
                                    '★dTA', newclass, ' ', bgcolor,
                                    ' f★dTY', jpwd, '★dTE', enref)))
            enline = ''.join(('★lTAC', enline, '★lTD'))
            p_spc_elines.append(enline)
        frameline = frameline.replace(
                '★pTA', '☆［').replace(
                '★pTB', '］☆★pTX').replace('★pTC', '★pTY')
        frameline = rgx_del.sub('', frameline)
        if key in eb_dic.keys():
            if rgx_spcframe.search(frameline):
                framepspclines.append(frameline)
        else:
            if rgx_allhd.search(frameline):
                framepspclines.append(frameline)
    if not enlistflg:
        p_spc_elines = []
    if 0 < len(framepspclines) < linecnt:
        clwdparalines = []
        p_spchd_lines.append(
                '★hTAspcHdList★hTB■明細俯瞰情報(原文明細書ベース)'
                '★hTCspcHdList★hTD★tTSspcHdList★tTE')
        for ealine in framepspclines:
            res = rgx_hdbasic.search(ealine)
            if res:
                heading = res.group('heading')
                res1 = rgx_para.search(heading)
                if res1:
                    parnum = int(res1.group('paranum'))
                    if parnum in clwdinebparadic.keys():
                        parline = ealine
                        if parnum:
                            parline = parline.replace('★pTX', ''.join((
                                    '★ptTApa', str(parnum),
                                    '★ptTB')))
                        for (wdnum, word) in sorted(
                                clwdinebparadic[parnum], key=lambda x: x[0]):
                            if word in cl_wdclassnodic.keys():
                                strkwdclassno = str(cl_wdclassnodic[word])
                            else:
                                strkwdclassno = ''.join((' k', str(wdnum)))
                            parline += ''.join((
                                    '　★dTAk', strkwdclassno, ' b r★dTCk',
                                    str(wdnum), '★dTD', word, '★dTE'))
                        clwdparalines.append(parline)
                else:
                    p_spchd_lines.append(ealine)
            else:
                p_spchd_lines.append(ealine)
        p_spchd_lines.append('★tTC')
        if clwdparalines:
            p_spchd_lines.append(
                '★hTAspcHdParaList★hTB'
                '■実施形態(EB)のCL重要語記載段落リスト'
                '★hTCspcHdParaList★hTD★tTSspcHdParaList★tTE')
            for ealine in clwdparalines:
                p_spchd_lines.append(ealine)
            p_spchd_lines.append('★tTC')


def _spcgen():
    global END_STRG
    global p_spccl_lines
    global cl_wdattrdic
    global cl_refdic
    global cl_tgtdic
    global cl_tgtgrpdic
    global cl_allpgdic
    global cl_strgdic
    global cl_pgdic
    global fig_dic
    global fig_streldic
    global rgx_pgcl
    p_spccl_lines.append(
            '★hTAspcClList★hTB■明細情報(CLベース)★hTCspcClList★hTD'
            '★tTSspcClList★tTE')
    cltgtlist = []
    for claimtgt in cl_tgtdic.values():
        if claimtgt not in cltgtlist:
            cltgtlist.append(claimtgt)
    target1 = cl_tgtdic[1]
    fulltgt1 = target1
    pg_name = ''
    if target1.endswith(END_STRG):
        if (1, target1) in cl_strgdic.keys():
            if 1 == len(cl_strgdic[(1, target1)]):
                strcontent = cl_strgdic[(1, target1)][0][1]
                if rgx_pgcl.search(strcontent):
                    if (1, strcontent) in cl_pgdic.keys():
                        pg_name = strcontent
            elif 2 == len(cl_strgdic[(1, target1)]):
                strcontent1 = cl_strgdic[(1, target1)][0][1]
                strcontent2 = cl_strgdic[(1, target1)][1][1]
                strcontent = ''.join((strcontent1, '及び', strcontent2))
                if rgx_pgcl.search(strcontent1):
                    if (1, strcontent1) in cl_pgdic.keys():
                        pg_name = strcontent1
                if rgx_pgcl.search(strcontent2):
                    if (1, strcontent2) in cl_pgdic.keys():
                        pg_name = strcontent2
            else:
                n_max = len(cl_strgdic[(1, target1)])
                strcontent = ''
                for n, (c, cont) in enumerate(cl_strgdic[(1, target1)]):
                    if rgx_pgcl.search(cont):
                        if (1, cont) in cl_pgdic.keys():
                            pg_name = cont
                    strcontent += cont
                    if (n_max-1) == n:
                        break
                    strcontent = ''.join((strcontent, '、'))
                strcontent1 = cl_strgdic[(1, target1)][-1][1]
                strcontent = ''.join((strcontent, '及び', strcontent1))
                if rgx_pgcl.search(strcontent1):
                    if (1, strcontent1) in cl_pgdic.keys():
                        pg_name = strcontent1
            if not pg_name:
                fulltgt1 = ''.join((strcontent, 'を記録した', target1))
            else:
                if 1 == len(cl_pgdic[(1, pg_name)]):
                    strcontent_p = cl_pgdic[(1, pg_name)][0][1]
                elif 2 == len(cl_pgdic[(1, pg_name)]):
                    strcontent_p = ''.join((
                            cl_pgdic[(1, pg_name)][0][1], '及び',
                            cl_pgdic[(1, pg_name)][1][1]))
                else:
                    n_max = len(cl_pgdic[(1, pg_name)])
                    strcontent_p = ''
                    for n, (c, cont) in enumerate(cl_pgdic[(1, pg_name)]):
                        strcontent_p = ''.join((strcontent_p, cont))
                        if (n_max-1) == n:
                            break
                        strcontent_p = ''.join((strcontent_p, '、'))
                    strcontent_p = ''.join((
                            strcontent_p, '及び',
                            cl_pgdic[(1, pg_name)][-1][1]))
                fulltgt1 = ''.join((
                        strcontent_p, 'のための', pg_name, 'を記録した',
                        target1))
    elif rgx_pgcl.search(target1):
        if (1, target1) in cl_pgdic.keys():
            if 1 == len(cl_pgdic[(1, target1)]):
                strcontent = cl_pgdic[(1, target1)][0][1]
            elif 2 == len(cl_pgdic[(1, target1)]):
                strcontent = ''.join((
                        cl_pgdic[(1, target1)][0][1], '及び',
                        cl_pgdic[(1, target1)][1][1]))
            else:
                n_max = len(cl_pgdic[(1, target1)])
                strcontent = ''
                for n, (c, cont) in enumerate(cl_pgdic[(1, target1)]):
                    strcontent = ''.join((strcontent, cont))
                    if (n_max-1) == n:
                        break
                    strcontent = ''.join((strcontent, '、'))
                strcontent = ''.join((
                        strcontent, '及び',
                        cl_pgdic[(1, target1)][-1][1]))
            fulltgt1 = ''.join((strcontent, 'のための', target1))
    numtgt = len(cltgtlist)
    if 1 == numtgt:
        title = target1
        strtechfield = ''.join(('　本開示は、', fulltgt1, 'に関する。'))
        strtgt = ''.join((
                '　本開示は、■{課題/効果:～の低減/～の向上等}に有用な',
                target1, 'を提供する。'))
    elif 2 == numtgt:
        title = ''.join((target1, '及び', cltgtlist[1]))
        strtechfield = ''.join((
                '　本開示は、', fulltgt1, '及び関連技術に関する。'))
        strtgt = ''.join((
                '　本開示は、■{課題/効果:～の低減/～の向上等}に有用な',
                target1, 'を提供する。また、本開示は、その', target1,
                'に関連する', cltgtlist[1], 'を提供する。'))
    elif 3 == numtgt:
        title = ''.join(('、'.join(cltgtlist[:-1]), '及び', cltgtlist[-1]))
        strtechfield = ''.join((
                '　本開示は、', fulltgt1, '及び関連技術に関する。'))
        strtgt = ''.join((
                '　本開示は、■{課題/効果:～の低減/～の向上等}に有用な',
                target1, 'を提供する。また、本開示は、その', target1,
                'に関連する', cltgtlist[1], '及び', cltgtlist[2],
                'を提供する。'))
    else:
        title = ''.join(('、'.join(cltgtlist[:-1]), '及び', cltgtlist[-1]))
        strtechfield = ''.join((
                '　本開示は、', fulltgt1, '及び関連技術に関する。'))
        strtgt = ''.join((
                '　本開示は、■{課題/効果:～の低減/～の向上等}に有用な',
                target1, 'を提供する。また、本開示は、その', target1,
                'に関連する', '、'.join(cltgtlist[1:-1]), '及び',
                cltgtlist[-1], 'を提供する。'))
    streffect = ''.join((
            '　本開示における', title,
            'は、■{課題/効果:～の低減/～の向上等}に有用である。'))
    cltgtdefdic = {}
    for cl in cl_tgtgrpdic.keys():
        cltgt = cl_tgtdic[cl]
        if cl_refdic[cl]:
            related_tgt = cl_tgtdic[cl_refdic[cl][0]]
        else:
            related_tgt = ''
        cltgtdefdic[cl] = (cltgt, related_tgt)
    p_spccl_lines.append('★sTS【書類名】★sTE明細書')
    p_spccl_lines.append(''.join(('★sTS【発明の名称】★sTE', title)))
    p_spccl_lines.append('★sTS【技術分野】★sTE')
    p_spccl_lines.append(strtechfield)
    p_spccl_lines.append('★sTS【背景技術】★sTE')
    p_spccl_lines.append(
            '　従来、■{従来技術:～の技術/～装置等}が知られている'
            '（例えば、特許文献■{１}参照）。')
    p_spccl_lines.append(
            '　また、■{従来技術}が知られている'
            '（例えば、非特許文献■{１～３}参照）。')
    p_spccl_lines.append('★sTS【先行技術文献】★sTE')
    p_spccl_lines.append('　★sTS【特許文献】★sTE')
    p_spccl_lines.append('　　★sTS【特許文献１】★sTE特開■{公開番号}号公報')
    p_spccl_lines.append('　★sTS【非特許文献】★sTE')
    p_spccl_lines.append(
            '　　★sTS【非特許文献１】★sTE■{著者名:～、外2名}、'
            '「■{論文名/刊行物名}」、■{発行国}、■{発行所}、'
            '■{発行年月日}、第■{}巻、第■{}号、p.■{}―■{}')
    p_spccl_lines.append(
            '　　★sTS【非特許文献２】★sTE■{著者名}著、「■{書名}」、'
            '第■{}版、第■{}巻、■{発行国}、■{発行所}、■{発行年月日}、'
            'p.■{}―■{}')
    p_spccl_lines.append(
            '　　★sTS【非特許文献３】★sTE■{著者名}、「■{表題}」、'
            '■{関連箇所:頁/欄/行/項番/図面番号/DB内index/最初&最後語句}、'
            '［online］、■{掲載年月日}、■{掲載者等}、'
            '［■{検索年月日}検索］、インターネット〈URL:http://'
            '■{WebページのURL}〉')
    p_spccl_lines.append('★sTS【発明の概要】★sTE')
    p_spccl_lines.append('★sTS【発明が解決しようとする課題】★sTE')
    p_spccl_lines.append(
            '　従来の技術は、■{理由等}、■{課題/効果:'
            '～の低減/～の向上等}に必ずしも有用とは限らない。')
    p_spccl_lines.append(strtgt)
    p_spccl_lines.append('★sTS【課題を解決するための手段】★sTE')
    strhd = '　'
    for cl in cltgtdefdic.keys():
        if not cltgtdefdic[cl][1]:
            strmeans4solving = ''.join((
                    strhd, '本開示における', cltgtdefdic[cl][0],
                    'は、■請求項', _zeno(cl), '。'))
        else:
            strmeans4solving = ''.join((
                    strhd, '本開示における', cltgtdefdic[cl][0],
                    'は、上述の', cltgtdefdic[cl][1], 'に関連し、■請求項',
                    _zeno(cl), '。'))
        p_spccl_lines.append(strmeans4solving)
        strhd = '　また、'
    p_spccl_lines.append('★sTS【発明の効果】★sTE')
    p_spccl_lines.append(streffect)
    p_spccl_lines.append('★sTS【図面の簡単な説明】★sTE')
    for index in sorted(fig_dic.keys()):
        figno = _zeno(index)
        strfig = fig_dic[index][3]
        p_spccl_lines.append(''.join((
                '　★sTS【図', figno, '】★sTE', strfig)))
    p_spccl_lines.append('★sTS【発明を実施するための形態】★sTE')
    printedflg = False
    strhd = '　'
    for cl in cl_tgtdic.keys():
        pgflg = False
        if cl in cltgtdefdic.keys():
            if not cltgtdefdic[cl][1]:
                strmeans4solving = ''.join((
                        strhd, '本開示における', cltgtdefdic[cl][0],
                        'は、■請求項', _zeno(cl), '。'))
            else:
                strmeans4solving = ''.join((
                        strhd, '本開示における', cltgtdefdic[cl][0],
                        'は、上述の', cltgtdefdic[cl][1],
                        'に関連し、■請求項', _zeno(cl), '。'))
            if rgx_pgcl.search(cltgtdefdic[cl][0]):
                pgel = cltgtdefdic[cl][0]
                pgflg = True
                sbel = '■{効果発揮処理内容等}'
                if pgel in cl_allpgdic.keys():
                    numsbel = len(cl_allpgdic[pgel])
                    if 1 == numsbel:
                        sbel = cl_allpgdic[pgel][0]
                    else:
                        sbel = ''.join((
                                '、'.join(cl_allpgdic[pgel][:-1]),
                                '及び', cl_allpgdic[pgel][-1]))
                str_ea_effect = ''.join((
                        '　この', pgel,
                        ('をプロセッサ（Microprocessor）を備える機器等に'
                         'インストールすることで、その機器等は、'),
                        sbel, 'を実現し得る。従って、この',
                        pgel, 'により、■{効果}が実現され得る。'))
            elif cltgtdefdic[cl][0].endswith(END_STRG):
                pgflg = True
                str_ea_effect = ''.join((
                        '　この', cltgtdefdic[cl][0],
                        ('の記録内容をプロセッサ（Microprocessor）を備える'
                         '機器等において活用することで、その機器等は、'
                         '■{効果発揮処理内容等}を実行し得る。従って、この'),
                        cltgtdefdic[cl][0],
                        'により、■{効果}が実現され得る。'))
                if (cl, cltgtdefdic[cl][0]) in cl_strgdic.keys():
                    for (c, cont) in cl_strgdic[(cl, cltgtdefdic[cl][0])]:
                        if rgx_pgcl.search(cont):
                            sbel = '■{効果発揮処理内容等}'
                            if cont in cl_allpgdic.keys():
                                numsbel = len(cl_allpgdic[cont])
                                if 1 == numsbel:
                                    sbel = cl_allpgdic[cont][0]
                                else:
                                    sbel = ''.join((
                                            '、'.join(cl_allpgdic[cont][:-1]),
                                            '及び', cl_allpgdic[cont][-1]))
                            str_ea_effect = ''.join((
                                    '　この', cltgtdefdic[cl][0],
                                    'に記録された', cont,
                                    ('をプロセッサ（Microprocessor）を備える'
                                     '機器等にインストールすることで、'
                                     'その機器等は、'),
                                    sbel, 'を実現し得る。従って、この',
                                    cltgtdefdic[cl][0],
                                    'により、■{効果}が実現され得る。'))
                            break
        else:
            if cl < 2:
                followerhd = '　'
            elif (cl-1) in cltgtdefdic.keys() and cl_tgtdic[
                    (cl-1)] == cl_tgtdic[cl]:
                followerhd = '　ここで、'
            else:
                followerhd = '　また、'
            strmeans4solving = ''.join((
                    followerhd, '例えば、■請求項', _zeno(cl),
                    'としてもよい。'))
        p_spccl_lines.append(strmeans4solving)
        if not pgflg:
            if not printedflg:
                str_ea_effect = (
                        '　これにより、■{理由等}、■{効果:～できる/～し得る/'
                        '～の可能性が高まる/～に有用である等}。')
                printedflg = True
            else:
                str_ea_effect = '　これにより、■{効果}。'
        p_spccl_lines.append(str_ea_effect)
        strhd = '　また、'
    p_spccl_lines.append(''.join((
            '　なお、上述した', cl_tgtdic[1],
            ('及びこれに関連する技術は、機器、装置、集積回路、システム、'
             '方法、コンピュータプログラム、コンピュータで読み取り可能な'
             '記録媒体等の全体又は一部としての各種態様で具現化され得る。'))))
    p_spccl_lines.append(
            '　以下、本開示における技術の理解を容易にすべく、'
            '実施の形態を例示し、適宜図面を参照して、詳細に説明する。'
            '但し、周知技術については適宜説明を省略する。なお、図面は、'
            '模式図であり、厳密に図示されたものではない。また、'
            'この実施の形態の説明及び図面における各種要素の数、配置、形状、'
            '属性、状態、数値、或いは、要素間の接続態様、実行順序、'
            '包含関係等は、一例に過ぎず、特許請求の範囲に記載した請求対象を'
            '限定するものではない。この実施の形態の説明及び図面における'
            '各種要素のうち、独立請求項に記載されていない要素は、'
            '任意に付加可能である。')
    chaptno = 1
    sectno = 1
    p_spccl_lines.append('　（実施の形態１）')
    tmpmainel1 = cl_tgtdic[1]
    if 1 in fig_dic.keys():
        fig1el = fig_dic[1][0]
        fig1type = fig_dic[1][2]
        if 3 == fig1type:
            numsbel = len(cl_allpgdic[fig1el])
            if 1 == numsbel:
                sbel = cl_allpgdic[fig1el][0]
                if 0 < cl_wdattrdic[sbel][5]:
                    strrefno = cl_wdattrdic[sbel][6]
                else:
                    strrefno = ''
                strrefsbel = ''.join((sbel, strrefno))
            else:
                sbel = ''.join((
                        '、'.join(cl_allpgdic[fig1el][:-1]),
                        '及び', cl_allpgdic[fig1el][-1]))
                strrefsbellist = []
                for sbe in cl_allpgdic[fig1el]:
                    if 0 < cl_wdattrdic[sbe][5]:
                        strrefno = cl_wdattrdic[sbe][6]
                    else:
                        strrefno = ''
                    strrefsbe = ''.join((sbe, strrefno))
                    strrefsbellist.append(strrefsbe)
                strrefsbel = ''.join((
                        '、'.join(strrefsbellist[:-1]), '及び',
                        strrefsbellist[-1]))
            mainel1 = ''.join((fig1el, 'により実現される', sbel))
            strrefmainel1 = ''.join((fig1el, 'により実現される', strrefsbel))
            strindapp = ''.join((sbel, 'に係るシステム等'))
        elif 4 == fig1type:
            mainel1 = ''.join((tmpmainel1, 'において記録される', fig1el))
            if 0 < cl_wdattrdic[fig1el][5]:
                strrefno = cl_wdattrdic[fig1el][6]
            else:
                strrefno = ''
            strrefmainel1 = ''.join((mainel1, strrefno))
            strindapp = ''.join((fig1el, 'を扱うシステム等'))
        else:
            mainel1 = tmpmainel1
            if 0 < cl_wdattrdic[mainel1][5]:
                strrefno = cl_wdattrdic[mainel1][6]
            else:
                strrefno = ''
            strrefmainel1 = ''.join((mainel1, strrefno))
            if cl_wdattrdic[mainel1][3]:
                strindapp = ''.join((mainel1, 'を用いるシステム等'))
            else:
                strindapp = ''.join((mainel1, '等'))
        p_spccl_lines.append(''.join((
                '　本実施の形態では、', mainel1,
                'の一例について、図面を用いて説明する。')))
        p_spccl_lines.append(''.join((
                '　［', _zeno(chaptno), '－', _zeno(sectno), '．', mainel1,
                'の構成］')))
        sectno += 1
        p_spccl_lines.append(''.join(('　', fig_dic[1][4])))
        for str_fig_element in fig_streldic[1]:
            p_spccl_lines.append(''.join(('　', str_fig_element)))
        for index in sorted(fig_dic.keys()):
            if 1 == index:
                continue
            tmpmainel = fig_dic[index][0]
            figtype = fig_dic[index][2]
            if 3 == figtype:
                numsbel = len(cl_allpgdic[tmpmainel])
                if 1 == numsbel:
                    sbel = cl_allpgdic[tmpmainel][0]
                else:
                    sbel = ''.join((
                            '、'.join(cl_allpgdic[tmpmainel][:-1]),
                            '及び', cl_allpgdic[tmpmainel][-1]))
                mainel = ''.join((tmpmainel, 'により実現される', sbel))
            elif 2 == figtype:
                mainel = ''.join((tmpmainel, 'における記録内容'))
            else:
                mainel = tmpmainel
            p_spccl_lines.append(''.join((
                    '　［', _zeno(chaptno), '－', _zeno(sectno), '．', mainel,
                    '］')))
            sectno += 1
            p_spccl_lines.append(''.join(('　', fig_dic[index][4])))
            for str_fig_element in fig_streldic[index]:
                p_spccl_lines.append(''.join(('　', str_fig_element)))
        p_spccl_lines.append(''.join((
                '　［', _zeno(chaptno), '－', _zeno(sectno), '．効果等］')))
        sectno += 1
        p_spccl_lines.append(''.join((
                '　上述した', strrefmainel1, 'によれば、'
                '■{効果発揮理由}ので、■{効果}できるようになる。')))
    else:
        mainel1 = tmpmainel1
        strindapp = ''.join((mainel1, '等'))
        p_spccl_lines.append(''.join((
                '　本実施の形態では、', mainel1,
                'の一例について、説明する。')))
        p_spccl_lines.append('　■{実施形態例の説明}。')
        p_spccl_lines.append(''.join((
                '　上述した', mainel1, 'の例によれば、'
                '■{効果発揮理由}ので、■{効果}できるようになる。')))
    p_spccl_lines.append('　（他の実施の形態等）')
    p_spccl_lines.append(
            '　以上のように、本出願において開示する技術の例示として、'
            '実施の形態１■{～ｎ}を説明した。しかしながら、'
            '本開示における技術は、これに限定されず、適宜、変更、置き換え、'
            '付加、省略等を行った実施の形態にも適用可能である。')
    p_spccl_lines.append(
            '　上述の実施の形態では、■{CL上位概念範囲確保すべく代替可能な'
            '実施の形態の一構成要素}が、■{上述例内容}する例を示したが、'
            '■{当該一構成要素}は、■{要件を明確にした代替構成/代替方式等}'
            'でもよい。')
    p_spccl_lines.append(
            '　上述の実施の形態では、■{必要に応じて上記同様の上位概念或いは'
            '中位概念の範囲確保のための記載}。')
    p_spccl_lines.append(
            '　また、上述の実施の形態では、■{CLで情報の取得を示す場合に'
            'おいて情報の取得に係る実施の形態の一構成要素}が、'
            '■{実施の形態で示した情報の取得に係る具体例内容}により情報を'
            '取得する例を示したが、この取得は、いかなる方式で実現してもよい。'
            'この情報の取得は、例えば、キーボード、マウス、音声入力装置'
            'その他の入力装置を介してユーザー（例えば人間、動物、ロボット等）'
            'から入力される情報を取得することであってもよく、イメージセンサ'
            'による撮像を含む各種センサによるセンシング結果の取得であっても'
            'よい。また、この情報の取得は、外部の通信装置からの情報信号の受信'
            'により実現されてもよいし、メモリカード等の着脱自在な記録媒体から'
            '情報を読み出すことで実現されてもよい。')
    p_spccl_lines.append(
            '　また、上述の実施の形態では、■{CLで情報の出力を示す場合'
            'において出力に係る実施の形態の一構成要素}が、■{実施の形態で'
            '示した出力に係る具体例内容}により情報を出力する例を示したが、'
            'この出力は、いかなる方式で実現してもよい。この出力は、例えば、'
            '情報を発光パターンで表した発光による出力であってもよく、'
            'ディスプレイ等へ情報を表す画像の表示であってもよい。また、'
            'この出力は、例えば、情報を表す音声の出力であってもよいし、'
            '外部の通信装置への情報信号の送信であってもよいし、'
            'メモリカード等の着脱自在な記録媒体に情報を記録すること'
            'であってもよい。')
    p_spccl_lines.append(
            '　また、上述した■{CLで各種機能実現に係る装置/システム等を'
            '示す場合においてその装置等}における上述した各部の機能分担は'
            '一例に過ぎず、任意に変更することができ、各部を統合してもよい。'
            'また、■{当該装置等}は、■{機能/処理名称等}を、■{当該装置等}と'
            '通信可能な外部の装置に分担させてもよい。また、■{当該装置等}'
            'における各機能構成要素としての機能ブロックの全部又は一部は、'
            'ＩＣ（Integrated Circuit）、ＬＳＩ（Large Scale Integration）等'
            'の半導体装置により実現されてもよく、その機能ブロックの全部又は'
            '一部を含むように１チップ化されてもよい。その１チップには'
            '各機能構成要素の機能を実現するためのプログラムを記録した'
            'メモリ及びマイクロプロセッサを含めてもよい。'
            'また、その半導体装置の全部又は一部には、ＦＰＧＡ'
            '（Field Programmable Gate Array）、或いは、ＬＳＩ内部の回路セル'
            'の接続や設定を再構成可能なリコンフィギュラブル・プロセッサを'
            '用いてもよい。なお、その機能ブロックは、半導体装置とは別の技術'
            '（例えばバイオ技術）で生成された構造物で実現されてもよい。')
    strmethodfigno = []
    for fignum in sorted(fig_dic.keys()):
        strfig = fig_dic[fignum][3]
        if regex.search('フローチャート', strfig):
            strmethodfigno.append(''.join(('図', _zeno(fignum))))
    nummthdflg = len(strmethodfigno)
    strmethodfigs = ''
    if 0 < nummthdflg:
        if 1 == nummthdflg:
            strmethodfigs = ''.join((
                    '（例えば', strmethodfigno[0], 'に示す手順等）'))
        else:
            strmethodfigs = ''.join((
                    '（例えば', '、'.join(strmethodfigno[:-1]), '及び',
                    strmethodfigno[-1], 'に示す手順等）'))
    strpglist = []
    for program in sorted(cl_allpgdic.keys()):
        strpglist.append(program)
    numpg = len(strpglist)
    strpgs = ''
    if 0 < numpg:
        if 1 == numpg:
            strpgs = ''.join(('（例えば', strpglist[0], '）'))
        else:
            strpgs = ''.join((
                    '（例えば', '、'.join(strpglist[:-1]), '及び',
                    strpglist[-1], '）'))
    p_spccl_lines.append(''.join((
            '　また、上述した■{CLで情報処理に係る装置/システム/方法等を'
            '示す場合においてその装置等}における各種処理の実行順序は、'
            '必ずしも、上述した通りの順序',
            strmethodfigs,
            'に制限されるものではなく、例えば、実行順序を入れ替えたり、'
            '複数の手順を並列に行ったり、その手順の一部を省略したりする'
            'ことができる。また、その各種処理の全部又は一部は、専用の'
            '電子回路等のハードウェアにより実現されても、プロセッサ及び'
            'ソフトウェアを用いて実現されてもよい。なお、ソフトウェアによる'
            '処理は、■{当該装置等}に含まれるマイクロプロセッサがメモリに'
            '記憶されたプログラム',
            strpgs,
            'を実行することにより実現されるものである。'
            'また、そのプログラムを、コンピュータが読み取り可能なＲＯＭ、'
            '光ディスク、ハードディスク等の非一時的な記録媒体に記録して'
            '頒布や流通させてもよい。例えば、頒布されたプログラムを、'
            'マイクロプロセッサを有する装置にインストールして、その'
            'インストール先の装置のマイクロプロセッサに実行させることで、'
            'その各種処理の全部又は一部を行わせることが可能となる。なお、'
            'そのプログラムは、■{当該装置等}が備える記録媒体に予め'
            '格納されていてもよいし、インターネット等を含む広域通信網を'
            '介してその記録媒体へ供給されてもよい。')))
    p_spccl_lines.append(
            '　また、上述した実施の形態で示した構成要素及び機能を任意に'
            '組み合わせることで実現される形態も本開示の範囲に含まれる。')
    p_spccl_lines.append('★sTS【産業上の利用可能性】★sTE')
    p_spccl_lines.append(''.join((
            '　本開示は、■{用途}のための', strindapp, 'に適用可能である。')))
    p_spccl_lines.append('★sTS【符号の説明】★sTE')
    for element, attrs in natsorted(
            cl_wdattrdic.items(), key=lambda x: x[1][6]):
        if 0 != attrs[5]:
            p_spccl_lines.append(''.join(('　', attrs[6], '　', element)))
    p_spccl_lines.append('★tTC')


def _tipdicgen():
    global p_array_tip
    global all_wdrefdic
    global cl_wdnodic
    global cl_allwddic
    global eb_wdnodic
    global eb_wdinfodic
    tmpwdset = set(cl_wdnodic.keys()) | set(eb_wdnodic.keys())
    for wd in tmpwdset:
        if wd in cl_wdnodic.keys():
            wdnum = cl_wdnodic[wd]
            tip = ''.join(('CL', ','.join(map(str, cl_allwddic[wdnum][1]))))
            if wd in eb_wdinfodic.keys():
                refnolist = eb_wdinfodic[wd][2]
                if refnolist:
                    tip = ''.join((
                            tip, ' EB-Ref',
                            _hanref(','.join(natsorted(refnolist))).replace(
                                    '"', '”')))
                    if 1 < eb_wdinfodic[wd][0]:
                        all_wdrefdic[wd] = {_hanref(x) for x in refnolist}
            wd_tip = ''.join(('k', str(wdnum), ':"', tip, '"'))
            p_array_tip.add(wd_tip)
        else:
            wdnum = eb_wdnodic[wd]
            if wd in eb_wdinfodic.keys():
                refnolist = eb_wdinfodic[wd][2]
                if refnolist:
                    tip = ''.join((
                            'EB-Ref',
                            _hanref(','.join(natsorted(refnolist))).replace(
                                    '"', '”')))
                    wd_tip = ''.join(('w', str(wdnum), ':"', tip, '"'))
                    p_array_tip.add(wd_tip)
                    if 1 < eb_wdinfodic[wd][0]:
                        all_wdrefdic[wd] = {_hanref(x) for x in refnolist}


def _efspcphrextr():
    global ef_spclines
    global all_wdrefdic
    global ephr_dic
    global p_array_ef
    eflinedic = {}
    efrefsdic = {}
    splitwds = [
            'a', 'about', 'above', 'across', 'after', 'against', 'along',
            'also', 'among', 'and', 'around', 'as', 'at', 'because', 'before',
            'behind', 'below', 'beneath', 'beside', 'besides', 'between',
            'beyond', 'but', 'by', 'despite', 'down', 'during', 'ether',
            'except', 'for', 'from', 'how', 'however', 'if', 'in', 'inside',
            'into', 'its', 'less', 'like', 'near', 'neither', 'nor', 'now',
            'of', 'off', 'on', 'once', 'only', 'onto', 'or', 'over', 'since',
            'so', 'than', 'that', 'this', 'the', 'these', 'those', 'though',
            'through', 'thus', 'till', 'to', 'toward', 'under', 'unless',
            'until', 'up', 'via', 'what', 'when', 'whenever', 'where',
            'whereas', 'wherever', 'whether', 'while', 'which', 'who', 'whom',
            'whose', 'why', 'with', 'within', 'without', 'yet']
    splitwds2 = [x.capitalize() for x in splitwds]
    splitwds.extend(splitwds2)
    rgx_splitwd = regex.compile(''.join((
            '(^| )(', '|'.join((splitwds)), ')(?= )')))
    for wd in all_wdrefdic.keys():
        ephrs = set()
        for e_ref in all_wdrefdic[wd]:
            rgx_eref = regex.compile(''.join((
                    r'(^|[\(\s])((?P<pre7>[a-zA-Z\-]*[a-zA-Z])\s)?'
                    r'((?P<pre6>[a-zA-Z\-]*[a-zA-Z])\s)?'
                    r'((?P<pre5>[a-zA-Z\-]*[a-zA-Z])\s)?'
                    r'((?P<pre4>[a-zA-Z\-]*[a-zA-Z])\s)?'
                    r'((?P<pre3>[a-zA-Z\-]*[a-zA-Z])\s)?'
                    r'((?P<pre2>[a-zA-Z\-]*[a-zA-Z])\s)?'
                    r'(?P<pre1>[a-zA-Z\-]*[a-zA-Z])\s',
                    e_ref, r'[.,:;? \t]')))
            for idx, eaefspcline in enumerate(ef_spclines):
                mres = rgx_eref.finditer(eaefspcline)
                for res in mres:
                    tmpewds = [
                            res.group('pre7'), res.group('pre6'),
                            res.group('pre5'), res.group('pre4'),
                            res.group('pre3'), res.group('pre2'),
                            res.group('pre1')]
                    ewds = [x for x in tmpewds if x]
                    if ewds:
                        if 1 == len(ewds) and (
                                'and' != ewds[0] or 'to' != ewds[0]
                                or 2 > len(ewds[0])):
                            continue
                        ephr = ' '.join((ewds))
                        ephrlist = rgx_splitwd.split(ephr)
                        ephr = ephrlist[-1]
                        if ephr.startswith(' '):
                            ephr = ephr[1:]
                        if 1 < len(ephr):
                            if ephr not in ephrs:
                                ephrs.add(ephr)
                            if wd in eflinedic.keys():
                                if str(idx) not in eflinedic[wd]:
                                    eflinedic[wd].append(str(idx))
                                if e_ref not in efrefsdic[wd]:
                                    efrefsdic[wd].append(e_ref)
                            else:
                                eflinedic[wd] = [str(idx)]
                                efrefsdic[wd] = [e_ref]
        if ephrs:
            delephrs = {
                    ephr1 for ephr1 in ephrs
                    for ephr2 in ephrs if (ephr2.lower() != ephr1.lower())
                    and ephr1.lower().endswith(ephr2.lower())}
            ephrs = ephrs.difference(delephrs)
            ephr_dic[wd] = ephrs
    for wd in eflinedic.keys():
        ef_line_info = ''.join((
                wd, ':"', '/'.join((eflinedic[wd])), '@@',
                '@'.join((efrefsdic[wd])), '"'))
        p_array_ef.add(ef_line_info)


def _impkwdjegen():
    global SP_WDS
    global PTN_LTDHD
    global JEDIC_FNAME
    global p_wdlist_lines
    global cl_wdnodic
    global cl_allwddic
    global cl_wdclassnodic
    global eb_wdinfodic
    global eb_wdnodic
    global je_wddic
    global ephr_dic
    try:
        with open(JEDIC_FNAME, mode='rb') as dict_file:
            je_dic = pickle.load(dict_file)
    except Exception:
        je_dic = {}
    if ephr_dic:
        for key in ephr_dic.keys():
            if key in je_dic.keys():
                for e_phr in ephr_dic[key]:
                    je_dic[key].add(e_phr)
            else:
                je_dic[key] = ephr_dic[key]
    if je_wddic or je_dic:
        rgx_ltdhd = regex.compile(PTN_LTDHD)
        if je_wddic:
            p_wdlist_lines.append(
                    '★hTAwdList★hTB■重要語リスト［keyword→英語表現'
                    '(▲:参考英語表現)］★hTCwdList★hTD★tTSwdList★tTE')
        else:
            p_wdlist_lines.append(
                    '★hTAwdList★hTB■重要語リスト［keyword→'
                    '▲参考英語表現］★hTCwdList★hTD★tTSwdList★tTE')
        p_wdlist_lines.append('★jTS【重要語リスト】★jTE')
        for wdnowdcl in natsorted(
                cl_allwddic.items(), key=lambda x: x[1][0]):
            wdnum = wdnowdcl[0]
            word = wdnowdcl[1][0]
            if word in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[word])
            else:
                strkwdclassno = ''.join((' k', str(wdnum)))
            strenwds = ''
            if je_wddic:
                if word in je_wddic.keys():
                    strenwds = je_wddic[word]
                    if not strenwds:
                        res = rgx_ltdhd.search(word)
                        if res:
                            srchwd = word[res.span()[1]:]
                            hdwd = word[:res.span()[1]]
                            if srchwd in je_wddic.keys():
                                if je_wddic[srchwd]:
                                    strenwds = ''.join((
                                            hdwd, je_wddic[srchwd]))
                else:
                    res = rgx_ltdhd.search(word)
                    if res:
                        srchwd = word[res.span()[1]:]
                        hdwd = word[:res.span()[1]]
                        if srchwd in je_wddic.keys():
                            if je_wddic[srchwd]:
                                strenwds = ''.join((hdwd, je_wddic[srchwd]))
            if strenwds:
                strenwdstag = '★zTZ'
            else:
                strenwdstag = '★zTF'
                if je_dic:
                    enwds = []
                    res = rgx_ltdhd.search(word)
                    if res:
                        srchwd = word[res.span()[1]:]
                        hdwd = word[:res.span()[1]]
                    else:
                        srchwd = word
                        hdwd = ''
                    if srchwd in je_dic.keys():
                        enwds = je_dic[srchwd]
                        strenwds = ''.join((
                                '▲', hdwd, '/'.join(natsorted(enwds))))
                    else:
                        tmp_word = ''
                        for sp_word in SP_WDS:
                            if srchwd.endswith(sp_word):
                                tmp_word = srchwd[:-len(sp_word)]
                                break
                        if tmp_word:
                            if tmp_word in je_dic.keys():
                                enwds = je_dic[tmp_word]
                                strenwds = ''.join((
                                        '▲', hdwd,
                                        '/'.join(natsorted(enwds)), sp_word))
            p_wdlist_lines.append(''.join((
                    '★zTAwk', str(wdnum), '★zTBk', strkwdclassno,
                    '★zTCwk', str(wdnum), '★zTD', word,
                    '★zTEwk', str(wdnum), strenwdstag, strenwds,
                    '★zTGwk', str(wdnum), '★zTH')))
        if eb_wdinfodic:
            for (word, val) in natsorted(
                    eb_wdinfodic.items(), key=lambda x: x[0]):
                if word not in cl_wdnodic.keys():
                    if 1 < val[0]:
                        ebwdnum = eb_wdnodic[word]
                        strenwds = ''
                        if je_wddic:
                            if word in je_wddic.keys():
                                strenwds = je_wddic[word]
                                if not strenwds:
                                    res = rgx_ltdhd.search(word)
                                    if res:
                                        srchwd = word[res.span()[1]:]
                                        hdwd = word[:res.span()[1]]
                                        if srchwd in je_wddic.keys():
                                            if je_wddic[srchwd]:
                                                strenwds = ''.join((
                                                        hdwd,
                                                        je_wddic[srchwd]))
                            else:
                                res = rgx_ltdhd.search(word)
                                if res:
                                    srchwd = word[res.span()[1]:]
                                    hdwd = word[:res.span()[1]]
                                    if srchwd in je_wddic.keys():
                                        if je_wddic[srchwd]:
                                            strenwds = ''.join((
                                                    hdwd, je_wddic[srchwd]))
                        if strenwds:
                            strenwdstag = '★zTZ'
                        else:
                            strenwdstag = '★zTF'
                            if je_dic:
                                enwds = []
                                res = rgx_ltdhd.search(word)
                                if res:
                                    srchwd = word[res.span()[1]:]
                                    hdwd = word[:res.span()[1]]
                                else:
                                    srchwd = word
                                    hdwd = ''
                                if srchwd in je_dic.keys():
                                    enwds = je_dic[srchwd]
                                    strenwds = ''.join((
                                            '▲', hdwd,
                                            '/'.join(natsorted(enwds))))
                                else:
                                    tmp_word = ''
                                    for sp_word in SP_WDS:
                                        if srchwd.endswith(sp_word):
                                            tmp_word = srchwd[:-len(sp_word)]
                                            break
                                    if tmp_word:
                                        if tmp_word in je_dic.keys():
                                            enwds = je_dic[tmp_word]
                                            strenwds = ''.join((
                                                    '▲', hdwd,
                                                    '/'.join(natsorted(
                                                            enwds)),
                                                    sp_word))
                        p_wdlist_lines.append(''.join((
                                '★zTAww', str(ebwdnum), '★zTXww',
                                str(ebwdnum), '★zTD', word, '★zTEww',
                                str(ebwdnum), strenwdstag, strenwds,
                                '★zTGww', str(ebwdnum), '★zTH')))
        p_wdlist_lines.append('★tTC')


def _clwdarraygen():
    global p_a_array
    global cl_wdnodic
    global wdlines_dic
    for wd in cl_wdnodic.keys():
        if wd in wdlines_dic.keys():
            wd_line = ','.join(wdlines_dic[wd])
            wdnum = cl_wdnodic[wd]
            wdnumline = "".join(("k", str(wdnum), ":'", wd_line, "'"))
            p_a_array.add(wdnumline)


def _clkwdsetgen():
    global p_wd_lines
    global cl_allwddic
    global cl_wdclassnodic
    global eb_wdinfodic
    if eb_wdinfodic:
        ebwdlist = list(eb_wdinfodic.keys())
        for eb_wd in eb_wdinfodic.keys():
            ebwdparts = regex.split('[:：]', eb_wd)
            if 1 < len(ebwdparts):
                for ebwdpart in ebwdparts:
                    if ebwdpart not in ebwdlist:
                        ebwdlist.append(ebwdpart)
        p_wd_lines.append(
                '★hTAwdClList1★hTB■CLのKeywordリスト(使用CL数順)'
                '［Keyword:使用CL番号 / －参照CL番号　▲:EBに同表現なし］'
                '★hTCwdClList1★hTD★tTSwdClList1★tTE')
        for wdnowdcl in natsorted(
                cl_allwddic.items(),
                key=lambda x: (len(x[1][1]), x[1][0]), reverse=True):
            strcl = ','.join(map(str, wdnowdcl[1][1]))
            wdnum = wdnowdcl[0]
            word = wdnowdcl[1][0]
            if word not in ebwdlist:
                strcl = ''.join((strcl, '　▲'))
            if word in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[word])
            else:
                strkwdclassno = ''.join((' k', str(wdnum)))
            p_wd_lines.append(''.join((
                    '■★kTXk', strkwdclassno, ' b★kTCbZk', str(wdnum),
                    '★kTD', word, '★kTE:', strcl,
                    '★stTSbZk', str(wdnum), '★stTE★stTC')))
        p_wd_lines.append('★tTC')
        p_wd_lines.append(
                '★hTAwdClList2★hTB■CLのKeywordリスト(語順)'
                '［Keyword:使用CL番号 / －参照CL番号　▲:EBに同表現なし］'
                '★hTCwdClList2★hTD★tTSwdClList2★tTE')
        for wdnowdcl in natsorted(cl_allwddic.items(), key=lambda x: x[1][0]):
            strcl = ','.join(map(str, wdnowdcl[1][1]))
            wdnum = wdnowdcl[0]
            word = wdnowdcl[1][0]
            if word not in ebwdlist:
                strcl = ''.join((strcl, '　▲'))
            if word in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[word])
            else:
                strkwdclassno = ''.join((' k', str(wdnum)))
            p_wd_lines.append(''.join((
                    '■★kTAk', str(wdnum), '★kTBk', strkwdclassno,
                    ' b★kTCaZk', str(wdnum), '★kTD', word, '★kTE:',
                    strcl, '★stTSaZk', str(wdnum), '★stTE★stTC')))
        p_wd_lines.append('★tTC')
    else:
        p_wd_lines.append(
                '★hTAwdClList1★hTB■CLのKeywordリスト(使用CL数順)'
                '［Keyword:使用CL番号 / －参照CL番号］'
                '★hTCwdClList1★hTD★tTSwdClList1★tTE')
        for wdnowdcl in natsorted(
                cl_allwddic.items(),
                key=lambda x: (len(x[1][1]), x[1][0]), reverse=True):
            strcl = ','.join(map(str, wdnowdcl[1][1]))
            wdnum = wdnowdcl[0]
            word = wdnowdcl[1][0]
            if word in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[word])
            else:
                strkwdclassno = ''.join((' k', str(wdnum)))
            p_wd_lines.append(''.join((
                    '■★kTXk', strkwdclassno, ' b★kTCbZk', str(wdnum),
                    '★kTD', word, '★kTE:', strcl,
                    '★stTSbZk', str(wdnum), '★stTE★stTC')))
        p_wd_lines.append('★tTC')
        p_wd_lines.append(
                '★hTAwdClList2★hTB■CLのKeywordリスト(語順)'
                '［Keyword:使用CL番号 / －参照CL番号］'
                '★hTCwdClList2★hTD★tTSwdClList2★tTE')
        for wdnowdcl in natsorted(cl_allwddic.items(), key=lambda x: x[1][0]):
            strcl = ','.join(map(str, wdnowdcl[1][1]))
            wdnum = wdnowdcl[0]
            word = wdnowdcl[1][0]
            if word in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[word])
            else:
                strkwdclassno = ''.join((' k', str(wdnum)))
            p_wd_lines.append(''.join((
                    '■★kTAk', str(wdnum), '★kTBk', strkwdclassno,
                    ' b★kTCaZk', str(wdnum), '★kTD', word, '★kTE:',
                    strcl, '★stTSaZk', str(wdnum), '★stTE★stTC')))
        p_wd_lines.append('★tTC')


def _ebwdarraygen():
    global p_a_array
    global eb_wdnodic
    global wdlines_dic
    for wd in eb_wdnodic.keys():
        if wd in wdlines_dic.keys():
            wd_line = ','.join(wdlines_dic[wd])
            wdnum = eb_wdnodic[wd]
            wdnumline = "".join(("w", str(wdnum), ":'", wd_line, "'"))
            p_a_array.add(wdnumline)


def _ebkwdsetgen():
    global p_wd_lines
    global cl_wdnodic
    global cl_wdclassnodic
    global eb_wdinfodic
    global eb_wdnodic
    p_wd_lines.append(
            '★hTAwdEbList1★hTB■原文実施形態(EB)のKeywordリスト(語順)'
            '［keyword:(重要Lv, EB記載数)　参照符号　▲:無符号表現混在］'
            '★hTCwdEbList1★hTD★tTSwdEbList1★tTE')
    for (word, val) in natsorted(eb_wdinfodic.items(), key=lambda x: x[0]):
        if 2 == val[1]:
            strmixref = '　▲'
        else:
            strmixref = ''
        if 1 < val[0]:
            strcnt = str(val[3])
        else:
            strcnt = '-'
        strval = ''.join((
                ' (Lv', str(val[0]), ', ', strcnt, ') ',
                ','.join(natsorted(val[2])), strmixref))
        if word in cl_wdnodic.keys():
            clwdnum = cl_wdnodic[word]
            if word in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[word])
            else:
                strkwdclassno = ''.join((' k', str(clwdnum)))
            p_wd_lines.append(''.join((
                    '■★kTOk', strkwdclassno, ' b★kTPcZk', str(clwdnum),
                    '★kTQ', word, '★kTR:', strval,
                    '★stTScZk', str(clwdnum), '★stTE★stTC')))
        else:
            if 1 < val[0]:
                ebwdnum = eb_wdnodic[word]
                p_wd_lines.append(''.join((
                        '■★kTAw', str(ebwdnum), '★kTBw w',
                        str(ebwdnum), ' y★kTCaZw', str(ebwdnum), '★kTD',
                        word, '★kTE:', strval, '★stTSaZw',
                        str(ebwdnum), '★stTE★stTC')))
            else:
                p_wd_lines.append(''.join(('・', word, ':', strval)))
    p_wd_lines.append('★tTC')
    p_wd_lines.append(
            '★hTAwdEbList2★hTB■原文実施形態(EB)のKeywordリスト(重要Lv順)'
            '［keyword:(重要Lv, EB記載数)　参照符号　▲:無符号表現混在］'
            '★hTCwdEbList2★hTD★tTSwdEbList2★tTE')
    for (word, val) in natsorted(
            eb_wdinfodic.items(),
            key=lambda x: (-x[1][0], -x[1][3], x[0]), reverse=False):
        if 2 == val[1]:
            strmixref = '　▲'
        else:
            strmixref = ''
        if 1 < val[0]:
            strcnt = str(val[3])
        else:
            strcnt = '-'
        strval = ''.join((
                ' (Lv', str(val[0]), ', ', strcnt, ') ',
                ','.join(natsorted(val[2])), strmixref))
        if word in cl_wdnodic.keys():
            clwdnum = cl_wdnodic[word]
            if word in cl_wdclassnodic.keys():
                strkwdclassno = str(cl_wdclassnodic[word])
            else:
                strkwdclassno = ''.join((' k', str(clwdnum)))
            p_wd_lines.append(''.join((
                    '■★kTOk', strkwdclassno, ' b★kTPdZk', str(clwdnum),
                    '★kTQ', word, '★kTR:', strval,
                    '★stTSdZk', str(clwdnum), '★stTE★stTC')))
        else:
            if 1 < val[0]:
                ebwdnum = eb_wdnodic[word]
                p_wd_lines.append(''.join((
                        '■★kTXw w', str(ebwdnum), ' y★kTCbZw',
                        str(ebwdnum), '★kTD', word, '★kTE:', strval,
                        '★stTSbZw', str(ebwdnum), '★stTE★stTC')))
            else:
                p_wd_lines.append(''.join(('・', word, ':', strval)))
    p_wd_lines.append('★tTC')


def patelier_installer():
    """patelier_installer for Command prompt (under development)

    This installs patelier App for Windows.
    The patelier App runs on Windows 10.
    The patelier App uses Chrome or Edge (web browser).
    So the patelier App needs Chrome or Edge installed.

    The patelier App reads text lines and gives them to Patisserie.
    The text lines need to include a claim written in Japanese,
        according to the Japanese patent application style.
    Patisserie is a class for analyzing the text lines.
    The patelier App shows the result of analysis by using browser.

    After patelier package is installed,
    command "install-patelier" is available to activate this installer.

    """
    rt = tkinter.Tk()
    rt.attributes('-topmost', True)
    rt.withdraw()
    initdir = '\\'
    crntdir = os.getcwd()
    if not _chk(crntdir):
        infomsg = '\n'.join((
                'Hello !', 'patelier is still under development.',
                datetime.datetime.now().strftime('%Y/%m/%d %H:%M')))
        tkinter.messagebox.showinfo(
                'patelier (under development)', infomsg, parent=rt)
        rt.destroy()
        return
    tkinter.messagebox.showinfo(
            'patelier App Installer',
            'patelier App インストール先フォルダーを選択してください。')
    installpath = tkinter.filedialog.askdirectory(initialdir=initdir)
    installpath = installpath.replace('/', os.sep)
    if os.path.isdir(installpath):
        patpath = os.path.join(installpath, 'patelier')
        patzpath = os.path.join(patpath, 'patelierzero.py')
        zpath = os.path.join(patpath, 'zero')
        hxpath = os.path.join(zpath, 'patelierzero.html')
        astspath = os.path.join(zpath, 'patelier-assets')
        csspath = os.path.join(astspath, 'patelier.css')
        jspath = os.path.join(astspath, 'patelier.js')
        icopath = os.path.join(astspath, 'patelier.ico')
        logopath = os.path.join(astspath, 'patelier.png')
        gifpath = os.path.join(astspath, 'patelier.gif')
        tcpath = os.path.join(astspath, 'pateliertc.png')
        zjpath = os.path.join(astspath, 'patelierzero.j')
        patflg = False
        patzflg = False
        zflg = False
        hxflg = False
        astsflg = False
        cssflg = False
        jsflg = False
        icoflg = False
        logoflg = False
        gifflg = False
        tcflg = False
        zjflg = False
        errflg = False
        if os.path.isdir(patpath):
            patflg = True
            if os.path.isfile(patzpath):
                patzflg = True
            if os.path.isdir(zpath):
                zflg = True
                if os.path.isfile(hxpath):
                    hxflg = True
                if os.path.isdir(astspath):
                    astsflg = True
                    if os.path.isfile(csspath):
                        cssflg = True
                    if os.path.isfile(jspath):
                        jsflg = True
                    if os.path.isfile(icopath):
                        icoflg = True
                    if os.path.isfile(logopath):
                        logoflg = True
                    if os.path.isfile(gifpath):
                        gifflg = True
                    if os.path.isfile(tcpath):
                        tcflg = True
                    if os.path.isfile(zjpath):
                        zjflg = True
        if (patzflg and hxflg and cssflg and jsflg and icoflg and logoflg
                and gifflg and tcflg and zjflg):
            errflg = True
            tkinter.messagebox.showerror(
                    'patelier App Installer Error',
                    ''.join((
                            'patelier Appが既にインストール(設定)'
                            'されています。\n再インストールする場合には'
                            '<patelier>フォルダー(',
                            patpath, ')を削除してください。')))
        if not errflg:
            path_dic = _pkg()
            if path_dic:
                if not patflg:
                    try:
                        os.mkdir(patpath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(<patelier>フォルダー生成)に失敗しました。')
                if (not patzflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['patzpath'], patpath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelierzero.py生成)に失敗しました。')
                if (not zflg) and (not errflg):
                    try:
                        os.mkdir(zpath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(<zero>フォルダー生成)に失敗しました。')
                if (not hxflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['hxpath'], hxpath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelierzero.html生成)に失敗しました。')
                if (not astsflg) and (not errflg):
                    try:
                        os.mkdir(astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(<patelier-assets>フォルダー生成)に'
                                '失敗しました。')
                if (not cssflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['csspath'], astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelier.css生成)に失敗しました。')
                if (not jsflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['jspath'], astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelier.js生成)に失敗しました。')
                if (not icoflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['icopath'], astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelier.ico生成)に失敗しました。')
                if (not logoflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['logopath'], astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelier.png生成)に失敗しました。')
                if (not gifflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['gifpath'], astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelier.gif生成)に失敗しました。')
                if (not tcflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['tcpath'], astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(pateliertc.png生成)に失敗しました。')
                if (not zjflg) and (not errflg):
                    try:
                        shutil.copy2(path_dic['zjpath'], astspath)
                    except OSError:
                        errflg = True
                        tkinter.messagebox.showerror(
                                'patelier App Installer Error',
                                'patelier設定'
                                '(patelierzero.j生成)に失敗しました。')
                if not errflg:
                    time.sleep(1)  # Timing Adjustment
                    try:
                        _pinst(patpath, icopath)
                        tkinter.messagebox.showinfo(
                                'patelier App Installer',
                                'patelier App インストールを完了しました。\n'
                                'インストール先フォルダー内の'
                                '<patelier>フォルダー配下にプログラム'
                                '(patelierzero.py)及び'
                                'リソースを生成しました。\n'
                                '不要になった場合は<patelier>フォルダー及び'
                                'デスクトップショートカットを'
                                '削除してください。')
                    except Exception:
                        tkinter.messagebox.showinfo(
                                'patelier App Installer',
                                'patelier App インストールを完了しました。\n'
                                'インストール先フォルダー内の'
                                '<patelier>フォルダー配下にプログラム'
                                '(patelierzero.py)及び'
                                'リソースを生成しました。\n'
                                '不要になった場合は<patelier>フォルダーを'
                                '削除してください。')
            else:
                tkinter.messagebox.showerror(
                        'patelier App Installer Error',
                        'patelierパッケージ実体が'
                        '正しくインストールされていません。')
    else:
        tkinter.messagebox.showerror(
                'patelier App Installer Error',
                ''.join((installpath, 'フォルダーが存在しません。')))


def _pinst(patrtpath, icopath):
    wshell = win32com.client.Dispatch('WScript.shell')
    deskpath = wshell.SpecialFolders('Desktop')
    shortpath = os.path.join(deskpath, 'patelier.lnk')
    shortcut = wshell.CreateShortcut(shortpath)
    shortcut.TargetPath = os.path.join(patrtpath, 'patelierzero.py')
    shortcut.WindowStyle = 1
    shortcut.IconLocation = icopath
    shortcut.WorkingDirectory = os.path.join(patrtpath)
    shortcut.Save()


def _chk(cdir):
    cpath = os.path.join(cdir, 'patelier.try')
    if os.path.exists(cpath):
        if os.path.isfile(cpath):
            return True
    return False

# This patelier package is still under development.
# If you'd like to experiment with more functions of patelier,
# just create a file "patelier.try" on the current directory.
# In the future,
# the above function "_chk" may check configuration file
#  for customizing functionality.
# Thank you for reading this far.
# I hope "patelier" helps you a little.
