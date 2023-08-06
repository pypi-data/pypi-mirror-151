import os

 # 工程根目录
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 维护唯一数参数的文件路径
UNIQUE_NUM_FILE_PATH = os.path.join(PROJECT_ROOT_DIR, "conf", "unique_num.txt")

# 维护一个参数化全局变量：供接口关联使用
PARAM_GLOBAL_DICT = {}

# 日志配置文件路径
LOG_CONF_FILE_PATH = os.path.join(PROJECT_ROOT_DIR, "conf", "logger.conf")

# 测试用例数据列号
TEST_NO = 0
TEST_DESC = 1
API_URI = 2
REQUEST_METHOD = 3
API_REQUEST_DATA = 4
RESPONSE_ASSERT_KEYWORD = 5
RESPONSE_EXTRACT_VAR = 6
BEFORETESTSQL = 7
AFTERTESTSQL = 8
SQL_EXTRACT_VAR = 9
ASSERTSQL = 10




#测试环境
Test_ip = 'http://10.0.40.62:8890'

# 主机接口地址/服务端账号密码
HOSTNAME = "10.0.40.62"
SERVICEPORT = "8890"
USERNAME = "hkzl123456"
PASSWORD = "zdhk123456"


#mongo DB 数据库配置信息
MONGOIP="10.0.40.62"
MONGOPORT= 20000
MONGOUSER="Hik706706"
MONGOPWD="Alibaba&Cetiti"
MONOGOBASE = "yk_base"

#MQTT服务信息
MQTTIP = "10.0.40.24"
MQTTPORT = 1883


cookies = None


# 测试用例文件存放目录
Company_Controller_Data_Dir = os.path.join(PROJECT_ROOT_DIR, "test_data","Company_Controller","test_base_companyPage.xlsx")
Company_Controller_Data_Dir1 = os.path.join(PROJECT_ROOT_DIR, "test_data","Company_Controller", "test_base_insertCompany.xlsx")
Company_Controller_Data_Dir3 = os.path.join(PROJECT_ROOT_DIR, "test_data","Company_Controller", "test_base_deleteCompany.xlsx")
Company_Controller_Data_Dir4 = os.path.join(PROJECT_ROOT_DIR, "test_data","Company_Controller", "test_base_editCompany.xlsx")
Company_Controller_Data_Dir5 = os.path.join(PROJECT_ROOT_DIR, "test_data","Company_Controller", "test_base_findCompany.xlsx")
Department_Controller_Data_Dir = os.path.join(PROJECT_ROOT_DIR, "test_data","Department_Controller","test_base_topDepartmentList.xlsx")
Department_Controller_Data_Dir1 = os.path.join(PROJECT_ROOT_DIR, "test_data","Department_Controller","test_base_insertDepartment.xlsx")
Department_Controller_Data_Dir2 = os.path.join(PROJECT_ROOT_DIR, "test_data","Department_Controller","test_base_findDepartment.xlsx")
Department_Controller_Data_Dir3 = os.path.join(PROJECT_ROOT_DIR, "test_data","Department_Controller","test_base_editDepartment.xlsx")
Department_Controller_Data_Dir4 = os.path.join(PROJECT_ROOT_DIR, "test_data","Department_Controller","test_base_departmentPage.xlsx")
Department_Controller_Data_Dir5 = os.path.join(PROJECT_ROOT_DIR, "test_data","Department_Controller","test_base_deleteDepartment.xlsx")
UserRole_Controller_Data_Dir = os.path.join(PROJECT_ROOT_DIR, "test_data","User_Role_Controller","test_base_userRolePage.xlsx")
UserRole_Controller_Data_Dir1 = os.path.join(PROJECT_ROOT_DIR, "test_data","User_Role_Controller","test_base_insertUserRole.xlsx")

# if __name__ == "__main__":
#     # print(PROJECT_ROOT_DIR)
#     # print(LOG_CONF_FILE_PATH)
