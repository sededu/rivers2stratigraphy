import sys

def get_response():

    posInput = ['y', 'yes']
    negInput = ['n', 'no']
    allInput = posInput + negInput

    badInput = True
    while badInput:
        resp = input('\nWould you like to launch the module now? [y/n] \n').lower()
        check = resp in allInput
        badInput = not check
        if badInput:
            print('invalid input: select [y/n]')

    return resp


def check_response(resp):
    if resp in ['y', 'yes']:
        print('okay, launching module . . . . .\n')
        return True
    elif resp in ['n', 'no']:
        print('okay, not launching module . . . . .\n')
        return False
    else:
        raise ValueError('invalid input: select [y/n]')


def run_import():
    from . import main


def import_runner():
    '''
    a super simple method to run the gui from a Python shell
    '''

    print('\n    SedEdu -- rivers2stratigraphy module')

    resp = get_response()
    launch = check_response(resp)
    if launch:
        run_import()
    else:
        print('you will need to unload and reload module\n',
              'to run again, or relaunch python')
