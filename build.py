import argparse
import subprocess
import sys

MODES = ['base', 'local', 'dev', 'prod']


def get_mode():
    """
    Get the mode in which you want to build docker images
    :return:
    """
    # build.py --mode <mode>
    # build.py -m <mode>

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--mode',
        help=f"Docker build mode({','.join(MODES)})"
    )
    args = parser.parse_args()

    # 모듈 호출 시 옵션으로 mode를 전달한 경우
    if args.mode:
        mode = args.mode.strip().lower()

    # 사용자 입력으로 mode를 선택한 경우
    else:
        while True:
            print('Select the mode you want to build')
            for index, mode_name in enumerate(MODES, start=1):
                print(f'{index}. {mode_name}')

            selected_mode = input('Choice mode: ')
            try:
                mode_index = int(selected_mode) - 1
                mode = MODES[mode_index]
                break
            except IndexError:
                print('Please input correct index number')

    return mode


def mode_function(mode):
    """
    build docker image when the user choose the mode
    :param mode:
    :return:
    """
    if mode in MODES:
        cur_module = sys.modules[__name__]
        getattr(cur_module, f'build_{mode}')()
    else:
        raise ValueError(f"The mode should be one of {MODES}")


def build_base():
    """
    build 'base' tagged docker images and push that images to Docker Hub
    :return:
    """
    try:
        subprocess.call('docker build -t subway:base -f Dockerfile.base .', shell=True)
    finally:
        print("Built 'base' tagged docker image successfully")
        subprocess.call('docker tag subway:base smallbee3/subway:base', shell=True)
        subprocess.call('docker push smallbee3/subway:base', shell=True)
        print("Pushed 'base' tagged docker image to Docker Hub successfully")


def build_local():
    """
    build 'local' tagged docker images and push that images to Docker Hub
    :return:
    """
    try:
        subprocess.call('docker build -t subway:local -f Dockerfile.local .', shell=True)
    finally:
        print("Built 'local' tagged docker image successfully")


def build_dev():
    """
    build 'dev' tagged docker images and push that images to Docker Hub
    :return:
    """
    try:
        subprocess.call('docker build -t subway:dev -f Dockerfile.dev .', shell=True)
    finally:
        print("Built 'dev' tagged docker image successfully")


def build_prod():
    """
    build 'prod' tagged docker images and push that images to Docker Hub
    :return:
    """
    try:
        subprocess.call('docker build -t subway:prod -f Dockerfile.prod .', shell=True)
    finally:
        print("Built 'prod' tagged docker image successfully")


if __name__ == '__main__':
    mode = get_mode()
    mode_function(mode)
