# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from alyun.Sqlhelper.hepler import DBHelper


class AlyunPipeline:
    def process_item(self, item, spider):
        _mysql = DBHelper()
        _exit_sql = 'SELECT del_url FROM `post` WHERE del_url = %s'
        _exit_arg = (str(item['del_url']))
        exit_id = _mysql.exit_id(_exit_sql, _exit_arg)
        print(f"exit_id", exit_id)
        _exit_insert_logs = 'INSERT INTO ddd.Logs(request_id, request_http, request_url)VALUES(%s, %s, %s)'
        _exit_insert_logs_arg = (str(item['Id']), str(item['response_url']), str(item['del_url']))
        _log_request_id = _mysql.insert(_exit_insert_logs, _exit_insert_logs_arg)
        print(f"logs", _log_request_id)
        # 判断条数如果大于40条 则结束脚本
        # _select_log_sql = 'select'

        if exit_id is None:
            _text = "".join(item['context'])
            _yun_href = ",".join(item['yun_href'])
            _insert_sql = 'INSERT INTO `post`(Title,htmlContext,Tags,request_id,aliyun_url,del_url,next_url,createTime)' \
                          ' VALUES (%s, %s, %s, %s, %s, %s,%s,%s)'
            _insert_age = (str(item['title']), _text, int(item['tag']),
                           str(item['Id']), _yun_href, str(item['del_url']), item['link_next'], item['create_time'])
            result_id = _mysql.insert(_insert_sql, _insert_age)
            print(f"插入的id", result_id)
        else:
            print(f"存在当前数据正在结束", item["Id"])
        return item
