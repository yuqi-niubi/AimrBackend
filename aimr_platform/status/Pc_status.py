# encoding: utf-8
"""
@author: chenxd
@software: PyCharm
@file: Pc_status.py
@time: 2020/9/25 11:00
"""
from aimr_platform.status.Status import status_join

MODULE = "100"

# 员工登录
login_success = status_join(MODULE, 100, "登録しました")
login_fail = status_join(MODULE, 101, "登録失敗、ユーザーまたはパスワード不正です")


# 「ポータル」页面初期化
get_portal_data_success = status_join(MODULE, 102, "データを取得完了しました")
get_portal_data_fail = status_join(MODULE, 103, "データがない")


# 获取検針データ
get_meter_reading_data_success = status_join(MODULE, 104, "データを取得完了しました")
get_meter_reading_data_fail = status_join(MODULE, 105, "データを取得失敗しました")


# 获取タスク更新確認状态
get_task_success = status_join(MODULE, 106, "データを取得完了しました")
get_task_fail = status_join(MODULE, 107, "データを取得失敗しました")


# 获取水道料金設定
get_price_success = status_join(MODULE, 108, "データを取得完了しました")
get_price_fail = status_join(MODULE, 109, "データを取得失敗しました")


# 設定水道料金更新
set_price_success = status_join(MODULE, 110, "データを更新完了しました")
set_price_fail = status_join(MODULE, 111, "データを更新失敗しました")

# 获取エリア
set_area_uccess = status_join(MODULE, 113, "データを取得完了しました")
set_area_fail = status_join(MODULE, 114, "データを取得失敗しました")

# token失效
emp_expired_status = status_join(MODULE, 112, "タイムアウトですので、再登録してください")

# 创建路线
create_route_success = status_join(MODULE, 201, "ルートの新規登録が完了しました")
create_route_fail = status_join(MODULE, 202, "ルートの新規登録に失敗しました")

# 更新路线
update_route_success = status_join(MODULE, 203, "ルートの更新が完了しました")
update_route_fail = status_join(MODULE, 204, "ルートの更新に失敗しました")

# 删除路线
delete_route_success = status_join(MODULE, 205, "ルートの削除が完了しました")
delete_route_fail = status_join(MODULE, 206, "ルートの削除に失敗しました")

# 创建物件
create_routelist_success = status_join(MODULE, 207, "物件の新規登録が完了しました")
create_routelist_fail = status_join(MODULE, 208, "物件の新規登録に失敗しました")

# 更新物件
update_routelist_success = status_join(MODULE, 209, "物件の更新が完了しました")
update_routelist_fail = status_join(MODULE, 210, "物件の更新に失敗しました")

# 删除物件
delete_routelist_success = status_join(MODULE, 211, "物件の削除が完了しました")
delete_routelist_fail = status_join(MODULE, 212, "物件の削除に失敗しました")

# 创建客户
create_meter_success = status_join(MODULE, 213, "お客様の新規登録が完了しました")
create_meter_fail_customer = status_join(MODULE, 214, "お客様の新規登録に失敗しました、該当お客様を存在します")
create_meter_fail_meter = status_join(MODULE, 221, "お客様の新規登録に失敗しました、該当メーター番号を存在します")
create_meter_fail = status_join(MODULE, 222, "お客様の新規登録に失敗しました、該当メーター番号とお客様を存在します")

# 更新客户
update_meter_success = status_join(MODULE, 215, "お客様の更新が完了しました")
update_meter_fail = status_join(MODULE, 216, "お客様の更新に失敗しました、該当お客様を存在します")

# 删除客户
delete_meter_success = status_join(MODULE, 217, "お客様の削除が完了しました")
delete_meter_fail = status_join(MODULE, 218, "お客様の削除に失敗しました")

# 送信
send_message_success = status_join(MODULE, 219, "タスクを送信完しました")
send_message_fail = status_join(MODULE, 220, "今月のタスクは送信完了ですので、重複送信できません。")
