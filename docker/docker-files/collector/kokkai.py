import argparse
import datetime
import json
import os
import time

import requests

# 日付形式
DATE_FORMAT = '%Y-%m-%d'

# デフォルト処理日付
DEFAULT_PROCESS_DATE = datetime.datetime.strptime(os.environ.get('DEFAULT_PROCESS_DATE', '2024-01-01'), DATE_FORMAT)

# このファイルのディレクトリパス
FILE_DIR = os.path.dirname(__file__)

# 処理日付保存ディレクトリ
PROCESS_DATE_SAVE_DIR = os.environ.get('PROCESS_DATE_SAVE_DIR', os.path.join(FILE_DIR, '.collector/config'))

# 処理日付保存ファイル名
PROCESS_DATE_FILE = 'process_date.txt'

# キャッシュ保存先ディレクトリ
CACHE_SAVE_DIR = os.environ.get('CACHE_SAVE_DIR', os.path.join(FILE_DIR, '.collector/cache'))

# 会議単位簡易出力 API URL
MEETING_LIST_API_URL = 'https://kokkai.ndl.go.jp/api/meeting_list'

# 会議単位出力 API URL
MEETING_API_URL = 'https://kokkai.ndl.go.jp/api/meeting'

# 通信間隔（秒）
REQUEST_INTERVAL_SECONDS = 5

# 会議単位データファイル出力ディレクトリ
MEETING_DATA_SAVE_DIR = os.environ.get('MEETING_DATA_SAVE_DIR', '/usr/share/logstash/ingest_data')


def load_process_date() -> datetime.datetime:
    """
    処理日付を取得する。
    :return: 日時
    """
    process_date_file_path = os.path.join(PROCESS_DATE_SAVE_DIR, PROCESS_DATE_FILE)
    # 処理対象日付格納ファイルパスの有無を判定する
    if os.path.exists(process_date_file_path):
        # ファイルから日付を取得する
        with open(process_date_file_path, 'r') as f:
            return datetime.datetime.strptime(f.readline(10), DATE_FORMAT)
    return DEFAULT_PROCESS_DATE


def save_process_date(process_date: datetime) -> None:
    """
    処理日付を保存する。
    :return:
    """
    # 処理日付格納ディレクトリが存在しない場合は作成する
    os.makedirs(PROCESS_DATE_SAVE_DIR, exist_ok=True)
    # 処理日付格納ファイルパス
    process_date_file_path = os.path.join(PROCESS_DATE_SAVE_DIR, PROCESS_DATE_FILE)
    # ファイルに次回の処理日付を保存する
    with open(process_date_file_path, 'w') as f:
        f.write(process_date.strftime(DATE_FORMAT))


def create_meeting_list_parameters(process_date: datetime.datetime) -> dict:
    """
    会議単位簡易出力 API パラメータを作成する。
    :param process_date: 日時
    :return: パラメータ
    """
    date_str = process_date.strftime(DATE_FORMAT)
    return {
        'maximumRecords': '100',
        'recordPacking': 'json',
        'from': date_str,
        'until': date_str,
    }


def create_cache_keys(url: str, params: dict) -> tuple[str, ...]:
    """
    キャッシュキーを作成する。
    :param url: URL
    :param params: パラメータ
    :return: キャッシュキー
    """
    url_key = url.replace("/", "_").replace(":", "_")
    param_keys = []
    if "from" in params:
        param_keys.append("from_" + params["from"])
    if "issueID" in params:
        param_keys.append("issueID_" + params["issueID"])
    return url_key, "_".join(param_keys)


def load_cached_data(*keys: str) -> dict | None:
    """
    キャッシュからデータをロードする。
    :param keys: キャッシュキー
    :return: キャッシュデータ
    """
    cache_file = os.path.join(CACHE_SAVE_DIR, *keys)
    if os.path.exists(cache_file):
        print(f"load_cached_data: {cache_file}")
        # ファイルからデータをロードする
        with open(cache_file, 'r') as f:
            return json.loads(f.read())
    return None


def save_cached_data(data: dict, *keys) -> None:
    """
    キャッシュからデータをロードする。
    :param data: キャッシュデータ
    :param keys: キャッシュキー
    :return: キャッシュデータ
    """
    cache_file = os.path.join(CACHE_SAVE_DIR, *keys)
    print(f"save_cached_data: {cache_file}")
    # ディレクトリが存在しない場合は作成する
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    # ファイルにデータを保存する
    with open(cache_file, 'w') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def get_request(url: str, params: dict | None = None) -> dict | None:
    """
    HTTP GETリクエストを送信し、レスポンスを取得する関数
    :param url: リクエストURL
    :param params: リクエストパラメータ
    :return:
    """
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError("データを取得できませんでした")
    # データ数を検証
    if data["nextRecordPosition"]:
        # 100 件以上のデータが存在する場合はエラーとする
        raise ValueError("100 件以上のデータが存在します")
    return data


def get_meeting_list(process_date: datetime.datetime) -> dict:
    """
    会議単位簡易データを取得する。
    :param process_date: 日時
    :return: 会議単位簡易データ
    """
    # パラメータを作成する
    params = create_meeting_list_parameters(process_date)
    # キャッシュキーを作成する
    cache_keys = create_cache_keys(MEETING_LIST_API_URL, params)
    # キャッシュからデータをロードする
    data = load_cached_data(*cache_keys)
    if not data:
        # API 呼び出しを待つ
        print(f'wait {REQUEST_INTERVAL_SECONDS} seconds')
        time.sleep(REQUEST_INTERVAL_SECONDS)
        # キャッシュからデータが取得できなかった場合は API からデータを取得する
        data = get_request(MEETING_LIST_API_URL, params)
        # キャッシュにデータを保存する
        save_cached_data(data, *cache_keys)
    return data


def create_meeting_parameter(issue_id: str) -> dict:
    """
    会議単位出力 API パラメータを作成する。
    :param issue_id: 会議ID
    :return: パラメータ
    """
    return {
        'recordPacking': 'json',
        'issueID': issue_id,
    }


def get_meeting(issue_id: str) -> dict:
    """
    会議単位データを取得する。
    :param issue_id: 会議ID
    :return: 会議単位データ
    """
    # パラメータを作成する
    params = create_meeting_parameter(issue_id)
    # キャッシュキーを作成する
    cache_keys = create_cache_keys(MEETING_API_URL, params)
    # キャッシュからデータをロードする
    data = load_cached_data(*cache_keys)
    if not data:
        # API 呼び出しを待つ
        print(f'wait {REQUEST_INTERVAL_SECONDS} seconds')
        time.sleep(REQUEST_INTERVAL_SECONDS)
        # キャッシュからデータが取得できなかった場合は API からデータを取得する
        data = get_request(MEETING_API_URL, params)
        # キャッシュにデータを保存する
        save_cached_data(data, *cache_keys)
    return data


def main():
    """
    メイン関数
    :return:
    """
    # コマンドライン引数を解析する
    parser = argparse.ArgumentParser(description="国会会議データ収集")
    parser.add_argument("-s", "--start-date", help=f"開始日付(${DATE_FORMAT.replace("%", "%%")})")
    parser.add_argument("-e", "--end-date", help=f"終了日付(${DATE_FORMAT.replace("%", "%%")})")
    args = parser.parse_args()

    # 処理対象日付を取得する
    if args.start_date:
        process_date = datetime.datetime.strptime(args.start_date, DATE_FORMAT)
    else:
        process_date = load_process_date()

    # 処理終了日を取得する
    if args.end_date:
        end_date = datetime.datetime.strptime(args.end_date, DATE_FORMAT)
    else:
        end_date = None

    while True:
        print(f'process_date: {process_date}')
        # 会議単位簡易データを取得する
        meeting_lists = get_meeting_list(process_date)

        if meeting_lists["numberOfReturn"] >= 1:
            for meeting_list in meeting_lists["meetingRecord"]:
                # 会議単位データを取得する
                meeting = get_meeting(meeting_list["issueID"])
                # print(f'meeting: {meeting}')
                # 会議単位データを出力する
                with open(os.path.join(MEETING_DATA_SAVE_DIR, f'meeting_{meeting_list["issueID"]}.json'), 'w') as f:
                    f.write(json.dumps(meeting["meetingRecord"][0], ensure_ascii=False))

        # 終了日なら終了する
        if end_date and process_date >= end_date:
            break

        # 処理対象日付に一日加算する
        process_date += datetime.timedelta(days=1)
        # 処理対象日付を保存する
        save_process_date(process_date)


if __name__ == '__main__':
    main()
