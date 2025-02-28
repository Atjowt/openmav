def prompt(msg: str, default='') -> str:
    try:
        if default:
            answer = input(f'{msg} (default={default}): ')
        else:
            answer = input(f'{msg}: ')
    except EOFError:
        print('Exiting...')
        exit()
    if not answer:
        answer = default
    return answer
