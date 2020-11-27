# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: App_status.py
@time: 2020/9/25 11:45
"""
from aimr_platform.status.Status import status_join

MODULE = "200"

# 员工登录
login_success = status_join(MODULE, 100, "登録しました")
login_fail = status_join(MODULE, 101, "登録失敗、ユーザーまたはパスワード不正です")

# 异常报告界面，送信状态
report_error_success = status_join(MODULE, 102, "異常の報告を送信しました")
report_error_fail = status_join(MODULE, 103, "異常の報告を送信失敗しました")

# 一括送信状态
report_all_success = status_join(MODULE, 104, "一括送信を完了しました")
report_all_fail = status_join(MODULE, 105, "一括送信を失敗しました")

# 任务状态
have_task = status_join(MODULE, 106, "新しいタスクがあります")
have_no_task = status_join(MODULE, 107, "新しいタスクがない")

# 获取任务状态
have_task_success = status_join(MODULE, 108, "新しいタスクを取得完了しました")
have_task_fail = status_join(MODULE, 109, "新しいタスクがありません")

# 确认任务接收完成
accept_task_over = status_join(MODULE, 110, "該当タスクを取得完了、確認しました")
accept_task_pause = status_join(MODULE, 111, "該当タスクを取得失敗、確認しました")

# 任务下载状态
download_task_success = status_join(MODULE, 112, "一つタスクをダウンロード完了しました")
download_task_fail = status_join(MODULE, 113, "一ついタスクをダウンロード失敗しました")

# 抄表任务更新状态
read_meter_success = status_join(MODULE, 114, "検針データが更新完了しました")
read_meter_fail = status_join(MODULE, 115, "検針データが更新失敗しました")

# 员工信息更新状态
user_info_success = status_join(MODULE, 116, "ユーザー情報が更新完了しました")
user_info_fail = status_join(MODULE, 117, "ユーザー情報が更新失敗しました")



