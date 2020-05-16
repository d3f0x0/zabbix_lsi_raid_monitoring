import subprocess
import re
import json


def run_command(index=None):
    try:
        if index == None:
            return subprocess.run(['/opt/sas3ircu', 'list'], stdout=subprocess.PIPE, encoding='utf-8')
        else:
            return subprocess.run(['/opt/sas3ircu', '{}'.format(index), 'display'],
                                  stdout=subprocess.PIPE, encoding='utf-8')
    except FileNotFoundError as e:
        print('Отсутствует файл: ', e)


def parse_result_command(result_command, pattern):
    pattern = re.compile(pattern)
    result_parse = re.findall(pattern, result_command.stdout)
    return result_parse


def discover_controller():
    """Скрипт для обнаружения индексов контроллеров"""
    result_command = run_command()
    index_controller = parse_result_command(result_command, '\s+(\d)\s+\w')
    data = {}
    for i in index_controller:
        key = '"{#INDEX}"'
        data.setdefault("data", []).append({key: i})
    return json.dumps(data, indent=2)


def discover_physical_disk(index):
    """Скрипт для обнаружения распололжения дисков корсзина:слот"""
    result_command = run_command(index)
    # Parse: enclosure, slot, status disk
    discover_disk = parse_result_command(result_command, 'Enclosure\s#\s+:\s(\d)\s*Slot.*:\s(\d)')
    output = []
    for enc, slot in discover_disk:
        output.append({'"{#ENC}"': enc, '"{#SLOT}"': slot})
    output = {"data": output}
    return json.dumps(output, indent=2)


def info_physical_disk(index, encd, slotd):
    """Скрипт для получения статуса о диске"""
    result_command = run_command(index)
    info_disk = parse_result_command(result_command,
                                     'Enclosure\s#\s+:\s(\d)\s*Slot.*:\s(\d)\s*.*\s*State\s+:\s\w+\s\((\w+)')
    data = {}
    for enc, slot, status in info_disk:
        if encd == enc and slotd == slot:
            data.setdefault("data", []).append({'"{#STATUS}"': status})
    return json.dumps(data, indent=2)


def status_raid(index):
    """Скрипт для получения статуса raid"""
    result_command = run_command(index)
    status = parse_result_command(result_command, 'Status of volume\s+:\s\w+\s\((\w+)')
    data = {}
    for i in status:
        data.setdefault("data", []).append({'"{#RAID}"': i})
    return json.dumps(data, indent=2)


if __name__ == '__main__':
    print('This is lib')
