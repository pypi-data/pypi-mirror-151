import traceback
import logging


# 封装断言功能
# def assert_keyword(response, keyword):
#     keyword_list = keyword.split("|")
#     for keyword in keyword_list:
#         try:
#             print('keyword',type(keyword))
#             assert keyword.strip() in response
#             logging.info("【%s】关键字断言成功【%s】" % (keyword, response))
#             logging.info("\n")
#         except:
#             logging.error("【%s】关键字断言失败【%s】" % (keyword, response))
#             logging.info("\n")
#             logging.error(traceback.format_exc())
#             raise

def assert_keyword(response, keyword):
    keyword_list = keyword.split("|")
    for keyword in keyword_list:
        try:
            # print('keyword',keyword_list,type(keyword_list))
            keyword1 = (str(keyword).split("{"))[1].split("}")[0]
            print('keyword1',keyword1)
            # print('response',response)
            assert keyword1 in str(response)
            logging.info("【%s】关键字断言成功【%s】" % (keyword1, response))
            logging.info("\n")
        except:
            logging.error("【%s】关键字断言失败【%s】" % (keyword, response))
            logging.info("\n")
            logging.error(traceback.format_exc())
            raise

def assert_SQL(SQLVAR, assertSQL):
    keyword_list = SQLVAR.split("|")
    for keyword in keyword_list:
        try:
            keyword1 = (str(keyword).split("{"))[1].split("}")[0]
            print('keyword1',keyword1)
            assert keyword1 in str(assertSQL)
            logging.info("【%s】数据库断言成功【%s】" % (keyword1, assertSQL))
            logging.info("\n")
        except:
            logging.error("【%s】数据库断言失败【%s】" % (keyword1, assertSQL))
            logging.info("\n")
            logging.error(traceback.format_exc())
            raise
