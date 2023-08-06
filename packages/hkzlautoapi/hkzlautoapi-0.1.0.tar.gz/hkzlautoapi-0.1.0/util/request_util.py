import json
from conftest import *
import requests
import re
from util.json_util import JsonHandler
from util.keyword_function import *
from urllib.parse import urlencode


# 请求数据预处理
def api_preprocess(request_data):
    logging.info("请求原始数据：%s" % request_data)
    try:
        # 匹配需要调用唯一数函数的参数
        if re.search(r"\$\{get_unique_num\w*\}", request_data):
            unique_num = get_unique_num()
            # 从用例中获取唯一数的变量名，供后续接口关联使用
            global_num_name = re.search(r"\$\{get_(unique_\w*)\}", request_data).group(1)
            # 将调用获取的唯一数的变量名和值存入全局变量中，供后续接口关联使用
            PARAM_GLOBAL_DICT[global_num_name] = unique_num
            request_data = re.sub(r"\$\{get_unique_num\w*\}", unique_num, request_data)
        # 匹配需要进行关联的参数
        if re.search(r"\$\{\w+\}", request_data):
            for var_data in re.findall(r"\$\{\w+\}", request_data):
                var = re.search(r"\$\{(\w+)\}", var_data).group(1)
                if isinstance(PARAM_GLOBAL_DICT[var], str):
                    request_data = re.sub(r"\$\{%s\}" % var, PARAM_GLOBAL_DICT[var], request_data)
                else:
                    request_data = re.sub(r'(\$\{%s\})' % var, str(PARAM_GLOBAL_DICT[var]), request_data)
        # 匹配需要进行函数化的参数
        if re.search(r"\$\{\w+?\(.+?\)\}", request_data):
            for var_data in re.findall(r"\$\{\w+?\(.+?\)\}", request_data):
                func_var = re.search(r"\$\{(\w+?\(.+?\))\}", var_data).group(1)
                func_result = eval(func_var)
                request_data = re.sub(r"\$\{(\w+?\(.+?\))\}", func_result, request_data)
        logging.info("请求数据预处理结果：%s" % request_data)
        return request_data
    except:
        print("请求数据预处理异常：【%s】" % request_data)
        print(traceback.format_exc())
        raise


# 响应数据关联参数提取
def api_postprocess(response_data, extract_var):
    try:
        if extract_var.strip() == "" or extract_var.lower() == "无":
            logging.info("无关联参数提取..")
            return
        extract_var_list = re.split(r",|\|", extract_var)  # 以“|”或“,”分隔
        if not isinstance(extract_var_list, list):
            print("关联参数格式有误！【%s】" % extract_var_list)
            print(traceback.format_exc())
            raise
        # 各关联参数以逗号分割
        for key in extract_var_list:
            key_result = JsonHandler.find_value(response_data, key)
            PARAM_GLOBAL_DICT[key] = key_result
            logging.info("关联参数提取成功：【%s】" % (key+": "+str(key_result)))
    except:
        print("响应数据关联参数提取异常：【关联参数：%s】【响应数据：%s】" % (extract_var, response_data))
        print(traceback.format_exc())
        raise
# def get_token():
#     url = "http://" + HOSTNAME + ":" + "8890" + "/yk/base/logining"
#     print(url)
#     # 请求参数
#     payload = {
#         "password": "a0a127ff7ce6b968e7145b4d17249578",
#         "username": USERNAME
#     }
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
#     res = requests.post(url, headers=headers, data=payload)
#     Mytoken = res.text.split("data")[1][2:-1]
#     print(Mytoken)
#     return Mytoken

# 接口调用函数
def api_request( uri, method, data, response_var, headers=None, cookies=None):
    url = Test_ip
    # headers = headers
    # a = get_token()
    # print('a',a)
    # headers['token'] = a
    try:
        if method.lower() == "post":
            # post 对请求体数据进行预处理
            request_data = api_preprocess(data)
            # request_data = json.dumps(request_data)
            # request_data = eval(data)
            mydata = request_data.encode('utf-8')
            # data_gb2312 = urlencode(mydata,encoding='gb2312')
            response = requests.post((url+uri), data=request_data, headers=headers, cookies=cookies)
            print('response', response.json())
        elif method.lower() == "get":
            # get 对请求URL数据进行预处理
            # uri = api_preprocess(uri)
            response = requests.get((url+uri),params=data, headers=headers)
            print('response',response.json())
        elif method.lower() == "put":
            request_data = api_preprocess(data)
            response = requests.put((url + uri), data=request_data, headers=headers, cookies=cookies)
        else:
            print("接口【%s】请求方法【%s】有误！" % ((url+uri), method))
            raise
        logging.info("接口调用成功！")
        api_postprocess(response.text, response_var)
        return response
    except:
        print("接口请求失败：【%s】【%s】\n" % ((url+uri), method))
        print(traceback.format_exc())
        raise


# 调用注册和登录接口，获取userid和token并放入全局变量中
# def get_token():
#     register_request_data = '{"username":"juno${get_unique_num100}","password":"juno999999","email":"juno123@qq.com"}'
#     api_request("http://39.100.104.214:8080", "/register/", "post", register_request_data, "userid")
#     login_request_data = '{"username":"juno${unique_num100}", "password": "${md5('+"'"+'juno999999'+"'"+')}"}'
#     api_request("http://39.100.104.214:8080", "/login/", "post", login_request_data, "token")


if __name__ == "__main__":
    pass