import typer
from typer import Option

from common import run_command


def get_resolution(src_filename: str):
    cmd_str_list = ['gdalinfo', src_filename]
    line_list = run_command(cmd_str_list)
    meter_per_pixel = None
    for line in line_list:
        if line.startswith(b'Pixel Size'):
            print(line)
            meter_per_pixel = float(line.split(b'(')[1].split(b',')[0])
    if meter_per_pixel is None:
        raise ValueError('Wrong gdalinfo output')
    return meter_per_pixel


def change_resolution(src_filename: str = Option(...),
                      dst_filename: str = Option(...),
                      ratio: float = Option(default=1, min=0.01, max=1)):
    org_meter_per_pixel = get_resolution(src_filename)
    meter_per_pixel = org_meter_per_pixel / ratio
    print(org_meter_per_pixel, meter_per_pixel)
    cmd_str = f"gdalwarp -tr {meter_per_pixel} {meter_per_pixel} -overwrite {src_filename} {dst_filename}"
    run_command(cmd_str.split(' '))


if __name__ == '__main__':
    typer.run(change_resolution)
