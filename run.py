import pytest
from action.send_email import SendEmail as se

if __name__ == '__main__':
    res_path = 'report/allure-results'
    pytest.main(['-s', '--alluredir', res_path, 'testcase', '--html=report/html/report.html',
                 '--self-contained-html'])  # allure报告 & html测试报告

    se().send_email('report/html/report.html')

    # os.system('allure generate' + res_path + '-o' + 'report/allure-static')  # allure静态报告
