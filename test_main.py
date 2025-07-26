import pytest
import json
from main import read_logs, generate_average_report
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def sample_logs():
    return [
        {'path': '/api/users', 'time': 0.1},
        {'path': '/api/users', 'time': 0.2},
        {'path': '/api/products', 'time': 0.3},
        {"path": '/api/products', 'time': 0.5},
        {"path": '/api/products', 'time': 0.7},
    ]


@pytest.fixture
def log_files(sample_logs):
    with open(
        'd:/Dev/logs_analyse_script/test1.json', 'w'
        ) as f1, open(
            'd:/Dev/logs_analyse_script/test2.json', 'w'
    ) as f2:

        json.dump(sample_logs[0], f1)
        f1.write('\n')
        json.dump(sample_logs[1], f1)
        f1.write('\n')
        f1.flush()

        json.dump(sample_logs[2], f2)
        f2.write('\n')
        json.dump(sample_logs[3], f2)
        f2.write('\n')
        json.dump(sample_logs[4], f2)
        f2.write('\n')
        f2.flush()

        yield [f1.name, f2.name]


def test_read_logs(log_files, sample_logs):
    logs = read_logs(log_files)
    assert len(logs) == 5
    assert all(log in sample_logs for log in logs)


def test_generate_average_report(sample_logs):
    report = generate_average_report(sample_logs)
    assert len(report) == 2

    endpoint_map = {row[0]: row for row in report}
    assert endpoint_map['/api/users'][1] == 2
    assert endpoint_map['/api/users'][2] == '0.150'
    assert endpoint_map['/api/products'][1] == 3
    assert endpoint_map['/api/products'][2] == '0.500'
