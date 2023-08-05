
def next_token(function, *args, **kwargs):
    responses = []
    while True:
        response = function(*args, **kwargs)
        if 'NextToken' in response:
            kwargs['NextToken'] = response['NextToken']
        else:
            break
    return responses

