import typer
from typer import Option

from common import run_command


def reproject(src_filename: str = Option(...),
              dst_filename: str = Option(...),
              src_proj_sys: str = Option('EPSG:2434'),
              dst_proj_sys: str = Option('EPSG:3857')):
    cmd_str = f'gdalwarp -s_srs {src_proj_sys} -t_srs {dst_proj_sys} -r near -of GTiff -overwrite {src_filename} {dst_filename}'
    run_command(cmd_str.split(' '))


if __name__ == '__main__':
    typer.run(reproject)
