import base64
from os import listdir
from os.path import isfile, dirname, realpath, join
import subprocess
from flask import url_for
import collections

epub_directory_path = "/home/hzengin-dev/KindleGate/epubs/"  # path that stores our archive
static_path = dirname(realpath(__file__))+"/static/"  # finding where is our "static" folder


def convert_ebook(input_name):
    output_name = input_name.replace('.epub', '.mobi')  # ebook-convert uses the file extension to determine conversion
    if isfile(static_path + output_name):  # if requested and converted before return the existing one
        return url_for('static', filename=output_name)
    process = subprocess.Popen(['ebook-convert', epub_directory_path + input_name, static_path + output_name], stdout=subprocess.PIPE)  # call ebook-convert as a subprocess
    process.wait()  # wait until it finishes it work
    # TODO: Add control to result for success or error
    return url_for('static', filename=output_name)


def create_link(ebook_name):
    encoded = str_to_base64(ebook_name)  # E-Book file names can contain invalid characters to use in url, encode with base64
    return "ebook/" + encoded


def get_epubs(path, keyword):
    return [f for f in listdir(path) if isfile(join(path, f)) and f[-4:] == "epub" and keyword in f]  # list directory & exclude directories & filter with keyword


def str_to_base64(s):
    return base64.b64encode(s.encode('utf-8')).decode("utf-8")


def base64_to_str(b):
    return base64.b64decode(b.encode('utf-8')).decode('utf-8')


def group_results(results):
    groups = collections.defaultdict(list)
    for result in results:
        groups[result["name"][0]].append(result)
    return collections.OrderedDict(sorted(groups.items())).items()
