# -*- coding: utf-8 -*-
import subprocess


def run_command(cmd_str_list):
    print(cmd_str_list)
    print(' '.join(cmd_str_list))
    p = subprocess.Popen(cmd_str_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output_list = []
    for o in p.stdout:
        print(o)
        output_list.append(o)
        p.stdout.flush()
    return output_list
