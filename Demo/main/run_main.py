#coding:utf-8

from base.run_method import RunMethod
from data.get_data import GetData
from util.common_util import CommonUtil
from data.dependent_data import DependentData
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RunTest:
    def __init__(self):
        self.run_method = RunMethod()
        self.data = GetData()
        self.common_util = CommonUtil()

    def go_on_run(self):
        """获取用例行数"""
        row_count = self.data.get_case_line()
        print("用例行数:",row_count)
        pass_count = []
        fail_count = []

        #循环执行用例
        for i in range(1,row_count):
            is_run = self.data.get_is_run(i)
            print("is_run:", is_run)
            if is_run:
                url = self.data.get_url(i)
                print("url:", url)
                request_type = self.data.get_request_type(i)
                print("request_type:", request_type)
                data = self.data.get_data_for_json(i)
                print("data:", data)
                dependent_case = self.data.is_depend(i)
                #dependent_more_case = self.data.is_more_depend(i, 1, 1)
                print("dependent_case:", dependent_case)
                #print("dependent_more_case:", dependent_more_case)
                if dependent_case != None:
                    self.dependent_data = DependentData(dependent_case)
                    #获取依赖的响应数据
                    dependent_response_data = self.dependent_data.get_data_for_key(i, 0)
                    print("dependent_response_data", dependent_response_data)
                    #token_header = self.data.get_token_header(i, dependent_response_data)
                    token_value = self.common_util.getToken()
                    token_header = self.data.get_token_header(i, token_value)
                    print("token_header:", token_header)
                    if url == "http://182.61.33.241:8089/app/api/private/1.0/client/":
                        new_url = url+self.dependent_data.get_data_for_key(i, 1)
                        print("------------------------------------")
                        print("new_url:", new_url)
                        #new_header = self.data.get_token_header(i, self.dependent_data.get_data_for_key(i, 0))
                        result = self.run_method.run_main(request_type, new_url, data, token_header)
                    else:
                        # result = self.run_method.run_main(request_type, url, data, token_header)
                        result = self.run_method.get_main(url, data, token_header)
                else:
                    header = self.data.get_header(i)
                    print("header:", header)
                    result = self.run_method.post_main(url, data, header)
                    #result = self.run_method.run_main(request_type, url, data, header)
                    print("返回结果：", result)

                    #获取token值
                    with open(self.common_util.base_dir(), 'w') as f:
                        f.write(result["data"]["token"])

                except_res = self.data.get_except(i)
                print("except_res:", except_res)
                if self.common_util.is_contain(except_res, result):
                    self.data.write_result(i,"测试通过")
                    print("测试通过")
                    pass_count.append(i)
                else:
                    self.data.write_result(i, result)
                    print("测试失败")
                    fail_count.append(i)
            print("打印结果：", result)
        print("通过数：", len(pass_count))
        print("失败数：", len(fail_count))
        return result

if __name__ == '__main__':
    run_test = RunTest()
    run_test.go_on_run()