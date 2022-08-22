import subprocess

import typer
from typer import Option


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


def get_ullr(src_filename: str):
    cmd_str_list = ['gdalinfo', src_filename]
    line_list = run_command(cmd_str_list)
    upper_left_x, upper_left_y, lower_right_x, lower_right_y = None, None, None, None
    for line in line_list:
        if line.startswith(b'Upper Left'):
            print(line.split(b' '))
            upper_left_x_str, upper_left_y_str = line.replace(b'Upper Left', b'').strip().split(b' ')[0:2]
            upper_left_x = float(upper_left_x_str[1:-1])
            upper_left_y = float(upper_left_y_str[:-1])
        elif line.startswith(b'Lower Right'):
            lower_right_x_str, lower_right_y_str = line.replace(b'Lower Right', b'').strip().split(b' ')[0:2]
            lower_right_x = float(lower_right_x_str[1:-1])
            lower_right_y = float(lower_right_y_str[:-1])
    print([upper_left_x, upper_left_y, lower_right_x, lower_right_y])
    if not all([upper_left_x, upper_left_y, lower_right_x, lower_right_y]):
        raise ValueError('Wrong gdalinfo output')
    return upper_left_x, upper_left_y, lower_right_x, lower_right_y


def correct_and_compress(src_filename: str = Option(...),
                         dst_filename: str = Option(...),
                         dx_in_meters: float = Option(...),
                         dy_in_meters: float = Option(...)):
    upper_left_x, upper_left_y, lower_right_x, lower_right_y = get_ullr(src_filename)
    ul_x, ul_y, lr_x, lr_y = (upper_left_x + dx_in_meters,
                              upper_left_y + dy_in_meters,
                              lower_right_x + dx_in_meters,
                              lower_right_y + dy_in_meters)
    cmd_str = f'gdal_translate -a_ullr {ul_x} {ul_y} {lr_x} {lr_y} -co COMPRESS=LZW -co PREDICTOR=2 -co ZLEVEL=9 {src_filename} {dst_filename}'
    run_command(cmd_str.split(' '))


if __name__ == '__main__':
    typer.run(correct_and_compress)
