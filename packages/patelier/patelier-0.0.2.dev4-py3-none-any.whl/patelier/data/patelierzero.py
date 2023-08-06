#!/usr/bin/env python3
"""patelier App main module 'patelierzero' (under development)

This patelierzero module is still under development.

This is a module for analyzing a Japanese file.
This module is also able to analyze clipboard text.
The file (or clipboard text) needs a claim written in Japanese,
    according to the Japanese patent application style.
The file is a text file or a document file,
    so its filename extention needs to be txt or docx.
This patelierzero module runs on Windows 10.
This patelierzero module runs
    only when a patelier package, and,
    Chrome or Edge are installed.
    (Chrome is a web browser developed by Google.)
    (Edge is a web browser developed by Microsoft.)

This patelierzero module has a patelierzero function
    and imports the pateliercore module from the patelier package.
The patelierzero function launches the patelier App
    using patelierzero.html.
The patelierzero function reads text lines
    from the file or clipboard.

If a Japanese-English dictionary file in <patelier> folder,
    the patelierzero may convert the dictionary file to patelier.dic
    and the patelier may use it.
The dictionary file's name is 'edict2'.
The file 'edict2' uses EUC-JP encoding.
You may be able to get the dictionary file from the internet.
The 'edict2' is a useful dictionary created by a project established
    by an Australian former professor James William Breen.
Using the same format of 'edict2',
    you may create a new dictionary of the same filename.

The patelierzero function uses the pateliercore's Patisserie.
Patisserie employs patissier for analyzing the text lines.
Patisserie outputs result files.
The result files show the result of the patissier's analysis.
The result files include res-utf8.txt, patelier.html and patelierjs.js.
The res-utf8.txt is a plain text version of the patelier.html.
The patelier.html uses patelierjs.js.
The result files use Japanese language of UTF-8 encoding.

I hope "patelier" helps you a little.

Copyright 2019-2022 K2UNIT

"""

# patelier-package-library
from patelier import __version__
from patelier import pateliercore

# I would like to thank the developers of each of the libraries below.

# standard-library
import datetime
import os
import pickle
import shutil
import time

# 3rd-party-library
import eel
import pyperclip
import regex


def patelierzero():
    """patelierzero function for patelier App

    This launches the patelier App.
    The patelier reads text lines from a file or clipboard.
    The patelier shows results of analyzing input text lines.
    The patelier uses patelierzero.html in <zero> folder.

    The patelier generates patelier.html.
    The patelier displays the results by using the patelier.html.
    The patelier.html uses patelierjs.js and some resouces.

    The patelier also generates res-utf8.txt.
    The res-utf8.txt is a plain text version of the patelier.html.
    The res-utf8.txt uses Japanese language of UTF-8 encoding.

    The input text lines must contain a Japanese patent claim
        written in Japanese.

    """
    print("patelier is preparing to run.")
    _edict2conv()
    eel.init("zero", allowed_extensions=['.j'])
    try:
        eel.start(
                'patelierzero.html',
                mode='chrome',
                cmdline_args=['--start-maximized'],
                block=False)
    except Exception:
        try:
            eel.start(
                    'patelierzero.html',
                    mode='edge',
                    block=False)
        except Exception as e:
            print(''.join((
                    '■Error:アプリ起動に失敗しました。: ',
                    str(e.args[0]))))
        else:
            while True:
                print("patelier is running.")
                eel.sleep(3.0)
    else:
        while True:
            print("patelier is running.")
            eel.sleep(3.0)


@eel.expose
def py_showver():
    """py_showver function

    This function sends version.

    """
    eel.jsDispVer(__version__)


@eel.expose
def py_srclist():
    """py_srclist function for displaying list

    This displays the list of generated folders.
    Each of the folders is in <zero> folder.
    Each folder contains HTML file which shows the analysis result.

    """
    dirs = []
    files = os.listdir('./zero')
    for eachfile in files:
        if 'patelier-assets' != eachfile:
            if os.path.isdir(os.path.join('./zero', eachfile)):
                dirs.append(eachfile)
    eel.jsDispSrcList(sorted(dirs, reverse=True))


@eel.expose
def py_rmdir(dirname):
    """py_rmdir function for removing folder

    This removes the folder of the designated name.
    This removes the folder in <zero> folder.

    Args:
        dirname(string): a folder name.

    """
    current_dir = os.getcwd()
    zero_path = os.path.join(current_dir, 'zero')
    dirpath = os.path.join(zero_path, dirname)
    print(''.join(('Start removing the folder:', dirpath)))
    status = '■原文({0})を原文Listから削除します。'.format(dirname)
    eel.jsDispStat(status)
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
        print('The folder has been removed.')
    else:
        print('No folder.')
    status = '■原文({0})を原文Listから削除しました。'.format(dirname)
    eel.jsDispStat(status)
    py_srclist()


@eel.expose
def py_fileanalyze():
    """py_fileanalyze function

    This gets a file data and analyzing it.

    """
    patisserie = pateliercore.Patisserie()
    patisserie.readf_setting_z()
    if patisserie.ret():
        fname = patisserie.get_infilename()
        if fname:
            eel.jsFReadComp()
            start_time = datetime.datetime.now()
            outdir = ''.join((
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S'), '_',
                    fname))
            patisserie.set_outdir(outdir)
            print('Start analyzing the file.')
            status = '■新規原文分析開始'
            eel.jsDispStat(status)
            patisserie.start()
            prgrss_cnt = 0
            tmp_prgrss = 0
            prev_p_prgrss = 0
            # prgrss:0,3,7,14,28,45,60,90,100
            range_max_set = {6, 13, 27, 44, 59, 89, 99}
            while True:
                time.sleep(2)
                p_prgrss = patisserie.get_prgrss()
                if 100 == p_prgrss:
                    break
                if 0 < p_prgrss < 100:
                    if prev_p_prgrss != p_prgrss:
                        prgrss_cnt = 0
                    tmp_prgrss = p_prgrss + prgrss_cnt
                    status = ''.join((
                            '■新規原文分析中(', str(tmp_prgrss),
                            '%):しばらくお待ちください。'))
                    eel.jsDispStat(status)
                    if tmp_prgrss not in range_max_set:
                        prgrss_cnt += 1
                prev_p_prgrss = p_prgrss
            patisserie.join()
            if patisserie.ret():
                now_time = datetime.datetime.now()
                delta_time = now_time - start_time
                status = ''.join((
                        '■分析終了(処理時間{0}sec):新規原文({1})'.format(
                            delta_time.seconds, outdir),
                        'を原文listに追加しました。'))
                eel.jsDispStat(status)
            else:
                status = '■異常発生のため分析を中止しました。'
                eel.jsDispStat(status)
    else:
        eel.jsFReadErr()
    del patisserie
    py_srclist()


@eel.expose
def py_clip():
    """py_clip function for getting data

    This reads text lines from the clipboard.

    """
    print('Start analyzing the clipboad text.')
    textlines = pyperclip.paste().splitlines()
    _analyze('clipboard', textlines)
    py_srclist()


def _analyze(dir_name, textlines):
    start_time = datetime.datetime.now()
    status = '■新規原文分析開始'
    eel.jsDispStat(status)
    outdir = ''.join((
            datetime.datetime.now().strftime('%Y%m%d%H%M%S'), '_',
            dir_name))
    patisserie = pateliercore.Patisserie()
    patisserie.setting(textlines, True, outdir, '')
    patisserie.start()
    prgrss_cnt = 0
    tmp_prgrss = 0
    prev_p_prgrss = 0
    # prgrss:0,3,7,14,28,45,60,90,100
    range_max_set = {6, 13, 27, 44, 59, 89, 99}
    while True:
        time.sleep(2)
        p_prgrss = patisserie.get_prgrss()
        if 100 == p_prgrss:
            break
        if 0 < p_prgrss < 100:
            if prev_p_prgrss != p_prgrss:
                prgrss_cnt = 0
            tmp_prgrss = p_prgrss + prgrss_cnt
            status = ''.join((
                    '■新規原文分析中(', str(tmp_prgrss),
                    '%):しばらくお待ちください。'))
            eel.jsDispStat(status)
            if tmp_prgrss not in range_max_set:
                prgrss_cnt += 1
        prev_p_prgrss = p_prgrss
    patisserie.join()
    if patisserie.ret():
        now_time = datetime.datetime.now()
        delta_time = now_time - start_time
        status = ''.join((
                '■分析終了(処理時間{0}sec):新規原文({1})'.format(
                    delta_time.seconds, outdir),
                'を原文listに追加しました。'))
        eel.jsDispStat(status)
    else:
        status = '■異常発生のため分析を中止しました。'
        eel.jsDispStat(status)
    del patisserie


def _edict2conv():
    je_dict = {}
    src_dict_filename = 'edict2'
    je_dict_filename = 'patelier.dic'
    current_dir = os.getcwd()
    src_dict_filepath = os.path.join(current_dir, src_dict_filename)
    je_dict_filepath = os.path.join(current_dir, je_dict_filename)
    if not os.path.isfile(je_dict_filepath):
        if os.path.isfile(src_dict_filepath):
            print('Start converting edict2 to patelier.dic.')
            dictlines = _readfeucjp(src_dict_filepath)
            if dictlines:
                ptn_sub_a = regex.compile(
                        r'( ?\[[^\]]+\] ?| ?\([^\)]+\) ?| ?\{[^\}]+\} ?|'
                        r'/EntL.+/|\n)')
                ptn_sub_b = regex.compile(' /')
                ptn_sub_c = regex.compile('/$')
                for dictline in dictlines:
                    newline = dictline.rstrip()
                    newline = ptn_sub_a.sub('', dictline)
                    newline = ptn_sub_b.sub('/', newline)
                    newline = ptn_sub_c.sub('', newline)
                    words = newline.split('/')
                    ewords = set(words[1:])
                    jwords = words[0].split(';')
                    if ewords:
                        for jword in jwords:
                            if jword not in je_dict.keys():
                                je_dict[jword] = ewords
                            else:
                                for eword in ewords:
                                    je_dict[jword].add(eword)
                try:
                    # binary open
                    with open(je_dict_filepath, mode='wb') as out_file:
                        pickle.dump(je_dict, out_file)  # dictionary object
                    print('The patelier.dic has been generated.')
                except OSError:
                    print(''.join((
                            '■Error:edict2変換先ファイルのOpenに失敗しました:',
                            je_dict_filepath)))
                except Exception as e:
                    print(''.join((
                            '■Error:edict2変換先ファイルのOpenに失敗しました:',
                            je_dict_filepath, ' ', str(e.args[0]))))


def _readfeucjp(filepath):
    try:
        with open(filepath, mode='rt', encoding='euc-jp') as f:
            return f.readlines()
    except OSError:
        print(''.join((
                '■Error:edict2ファイルのOpen(EUC-JP指定)に失敗しました:',
                filepath)))
        return []
    except Exception as e:
        print(''.join((
                '■Error:edict2ファイルのOpen(EUC-JP指定)に失敗しました:',
                filepath, ' ', str(e.args[0]))))
        return []


patelierzero()
