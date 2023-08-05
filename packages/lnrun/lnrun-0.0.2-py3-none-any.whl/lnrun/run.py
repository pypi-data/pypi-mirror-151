import subprocess
import sys

from lnrun.send_message import send_message


def main(_: bool = False):
    cmds = sys.argv[1:]
    if cmds[0] == 'run':
        cmds = cmds[1:]

    process_res = subprocess.run(cmds, capture_output=True)
    message = 'nrun done running : {}'.format(' '.join(cmds))
    print(process_res.stdout.decode())
    if len(process_res.stderr) > 0:
        message += f'\nwith error:\n{process_res.stderr.decode()}'
        print(process_res.stderr.decode())
    else:
        message += ' without errors'
        print('cmd run without errors')

    send_message(message)


if __name__ == '__main__':
    main()
