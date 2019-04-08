import subprocess
import pydocstyle


def flake8_checker(config_dict):
    config = []
    if config_dict['line_length'] and config_dict['ignore_errors']:
        config.append('--max-line-length')
        config.append(config_dict['line_length'])
        config.append('--ignore='+config_dict['ignore_errors'])

        print(config)
        commands = ['flake8', config[2], config[0], config[1], 'code.txt']
        p = subprocess.Popen(commands, stdout=subprocess.PIPE)
    elif config_dict['line_length']:
        config.append('--max-line-length')
        config.append(config_dict['line_length'])
        commands = ['flake8', config[0], config[1], 'code.txt']
        p = subprocess.Popen(commands, stdout=subprocess.PIPE)
    elif config_dict['ignore_errors']:
        print('error')
        config.append('--ignore=' + config_dict['ignore_errors'])
        print(config[0])
        commands = ['flake8', config[0], 'code.txt']
        p = subprocess.Popen(commands, stdout=subprocess.PIPE)
    else:
        commands = ['flake8', 'code.txt']
        p = subprocess.Popen(commands, stdout=subprocess.PIPE)
    result = str(p.communicate())
    arr = result.split('code.txt:')
    arr.pop(0)
    results = []
    n = 1
    for res in arr:
        row, col, msg = res.split(":", 2)
        msg = msg.replace("\\n", '')
        dict_result = {'n': n, 'row': row, 'col': col, 'msg': msg}
        n += 1
        results.append(dict_result)
    return results


def mypy_checker(args):
    args.insert(0, "mypy")
    args.insert(len(args), "code.txt")
    p = subprocess.Popen(["mypy", "code.txt"], stdout=subprocess.PIPE)
    result = str(p.communicate())
    arr = result.split('code.txt:')
    arr.pop(0)
    results = []
    n = 1
    for res in arr:
        row, col, msg = res.split(":", 2)
        msg = msg.replace("\\n", '')
        dict_result = {'n': n, 'row': row, 'col': col, 'msg': msg}
        n += 1
        results.append(dict_result)
    return results


def pydocstyle_checker(errors_to_ignore):
    errors = str(errors_to_ignore)
    ignored = set(errors.split(','))
    result = list(pydocstyle.checker.check(["code.txt"], ignore=ignored))
    results = []
    n = 1
    for res in result:
        unneeded2, row, type_of_error, msg = str(res).split(":", 3)
        dict_result = {'n': n, 'row': row, 'type_of_error': type_of_error, 'msg': msg}
        n += 1
        results.append(dict_result)
    return results


def coverage_checker():
    ps = subprocess.Popen(('coverage', 'run', 'code.txt'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('coverage', 'report'), stdin=ps.stdout)
    ps.wait()
    result = []
    result.append(str(output))
    return result
