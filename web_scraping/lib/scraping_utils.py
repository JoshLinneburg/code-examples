import ast
import requests
import json
import sys


def show_obj_head(obj, n_chars=500, n_items=5):
    """
    Returns the "head" of the object passed in, if applicable.

    Parameters
    ----------
    obj : object
        Any Python object; has to be a str, list, dict or requests.model.Response to return a value

    n_chars : int (optional)
        Number of characters to return if the object is a str or requests.model.Response

    n_items : int (optional)
        Number of items to return if the object is a list

    Returns
    -------
    result : obj
        A str, list or dict containing the "head" of the data supplied to the function

    """
    try:

        if isinstance(obj, requests.models.Response):
            print(f'The text of the response object returns a str with {len(obj.text)} characters!')
            print('')
            result = obj.text[:n_chars]  # Only returns the first 500 char's

        elif isinstance(obj, str):
            print(f'The object passed in is a str with {len(obj)} characters!')
            print('')
            result = obj[:n_chars]  # Only returns the first 500 char's

        elif isinstance(obj, list):
            print(f'The object passed in is a list with {len(obj)} items!')
            print('')
            result = obj[:n_items]  # Only returns the first 5 items

        elif isinstance(obj, dict):
            print(f'The object passed in is a dict with {len(obj.keys())} items!')
            print('')
            result = obj

        return result

    except:
        print('Something went wrong... try another URL or try again.')


def equivalence_checker(obj_one, obj_two, expected_value):
    """
    Checks whether two objects are equivalent logically.
    Does not check whether two objects point to the same space in memory.

    Parameters
    ----------
    obj_one : object
        Any Python object

    obj_two : object
        Any Python object

    expected_value : bool
        TRUE or FALSE; the expected value when obj_one is compared to obj_two

    Returns
    -------
    None
    """
    actual_value = obj_one == obj_two

    if expected_value == actual_value:
        print('Josh knows a lot about Python - the actual matches expected!')
    else:
        print('Josh is wrong - the actual is different than the expected!')


def output_exception(exc):
    """
    Returns details about an exception: the name of the exception, the line number it occurred on and so forth.

    Parameters
    ----------
    exc : Python exception object.
        A captured Python exception: exc = sys.exc_info(); exc_str = au.output_exception(exc=exc)

    Returns
    -------
    exc_return : string
        Exception formatted as a string.
    """
    exc_type = exc[0]
    exc_msg = exc[1].__str__()
    exc_line = exc[2].tb_lineno
    exc_return = f'{exc_type} at line {exc_line}: {exc_msg}'

    return exc_return


def output_log(filename, text, append=True):
    """
    Writes out any text to a log file of your choice.

    Parameters
    ----------
    filename : str
        Path to the log file, including the filename and extension.

    text : str
        Text to output to the log file.

    append : bool (optional)
        Whether to append to an existing file or overwrite; default is True to append.

    Returns
    -------
    None
    """
    try:
        if type(append) != bool:
            raise ValueError

        if append:
            append_or_write = 'a+'
        else:
            append_or_write = 'w+'

        with open(filename, append_or_write, encoding='utf-8') as f:

            if not text.endswith('\n'):
                f.write('\n')

            f.write(text)

            print(text)

    except ValueError:
        text = f'append parameter must either be True or False (bool), it cannot be {type(append)}!'
        output_log(filename=filename,
                   text=text)
        print(text)


def read_json(path_to_file):
    """
    Reads in a .json file and returns the data as a dict or list

    Parameters
    ----------
    path_to_file : str
        The path to the .json file, including the file name and the extension

    Returns
    -------
    data : dict or list
        The data of the JSON file, decoded into a Python dict or list object
    """
    with open(path_to_file, 'r+', encoding='UTF-8') as f:
        data = json.load(f)

    return data


def clean_list_of_dicts(original_file_path, new_file_path=None, str_fields=None, int_fields=None, float_fields=None):
    """
    Reads in a .json file that contains a list of (flat) dictionaries. This function will
    clean each dictionary and convert any fields specified to strings, ints or floats.

    The function can optionally write out the cleaned data and will ultimately return the cleaned data
    in the same list of dictionary structure, but with cleaned data types.

    Parameters
    ----------
    original_file_path : str
        Path to the original file

    new_file_path : str
        Path to the new file to write, optional

    str_fields : list
        List of fields to convert to str, optional

    int_fields : list
        List of fields to convert to int, optional

    float_fields : list
        List of fields to convert to float, optional

    Returns
    -------
    data : list (of dicts)
        Cleaned list of dictionaries
    """
    if float_fields is None:
        float_fields = []
    if int_fields is None:
        int_fields = []
    if str_fields is None:
        str_fields = []

    try:
        with open(original_file_path, 'r+') as f:
            raw_data = f.read()
            f.close()
            data = ast.literal_eval(raw_data)

            for entry in data:
                for key, value in entry.items():
                    if key in str_fields:
                        entry[key] = str(value)
                    elif key in int_fields:
                        entry[key] = int(value)
                    elif key in float_fields:
                        entry[key] = float(value)

        if new_file_path:
            with open(new_file_path, 'w+', encoding='UTF-8') as writer:
                json.dump(obj=data, fp=writer, ensure_ascii=True, indent=4)

        return data

    except:
        exc = sys.exc_info()
        exc_str = output_exception(exc=exc)
        output_log(filename='../logs/clean_list_of_dicts.log',
                   text=exc_str,
                   append=True)
