import argparse
import json
from collections import defaultdict
from tabulate import tabulate


def parse_args():
    parser = argparse.ArgumentParser(description='Обработчик логов')
    parser.add_argument(
        '--file',
        nargs='+',
        required=True,
        help='Путь к фаилу/фаилам'
    )
    parser.add_argument(
        '--report',
        choices=['average'],
        required=True,
        help='Тип получения отчета'
    )
    return parser.parse_args()


def read_logs(file_paths):
    logs = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return logs


def generate_average_report(logs):
    endpoint_stats = defaultdict(lambda: {'count': 0, 'total_time': 0})

    for log in logs:
        endpoint = log.get('path')
        time = log.get('time')
        if endpoint and time is not None:
            endpoint_stats[endpoint]['count'] += 1
            endpoint_stats[endpoint]['total_time'] += time

    report = []
    for endpoint, stats in endpoint_stats.items():
        avg_time = stats['total_time'] / stats['count']
        report.append([endpoint, stats['count'], f'{avg_time:.3f}'])

    return report


def main():
    args = parse_args()
    logs = read_logs(args.file)

    if args.report == 'average':
        report_data = generate_average_report(logs)
        headers = ['hendlers', 'total', 'average_rsponse_time']
        print(tabulate(report_data, headers=headers, tablefmt='grid'))


if __name__ == "__main__":
    main()
