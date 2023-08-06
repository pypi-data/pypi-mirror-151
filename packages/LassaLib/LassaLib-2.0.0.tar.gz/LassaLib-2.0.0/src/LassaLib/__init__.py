"""Convenient function set"""

try:
    import text_editing
    COLOR = True
except ModuleNotFoundError:
    COLOR = False

import typing


def enter(__prompt: str = '', __type: type = int) -> typing.Any:
    """
    This function allows to input any type
    :param __prompt: Text to print before recovery
    :param __type: The type to recover
    :return: The input in the requested type
    """
    if __type not in [
        bool, complex, float, int, list, set, slice, str,
        property, type
    ]:
        raise TypeError(f'{__type} is not a possible type.')
    var: str = input(__prompt)
    while True:
        try:
            '''  '''
            if __type == bool:
                if var.lower() in [
                    "yes", "是的", "हां", "sí", "si", "نعم", "হ্যাঁ", "oui", "да", "sim", "جی ہاں",
                    "y", "1", "true"
                ]:
                    return True
                elif var.lower() in [
                    "no", "不", "नहीं", "no", "لا", "না", "non", "нет", "não", "nao", "نہیں",
                    "n", "0", "false"
                ]:
                    return False
                else:
                    raise ValueError(f"could not convert string to bool: '{var}'")
            return __type(var)
        except ValueError:
            print(f"\"{var}\" is not the type {__type.__name__}")
            var: str = input(__prompt)


def str_object(obj: typing.Any, tab: int = 0, pass_: bool = False) -> str:
    """
    Create a string of all info about an object regardless of its class.
    :param obj: An object from Any type or class.
    :param tab:
    :param pass_: If pass the name of type
    :return: A string that summarizes the object in detail.
    """
    try:
        max_key_length = max([len(key) for key in obj.__dict__])
        txt = ('\t'*tab + f"{text_editing.color.COLOR_PURPLE if COLOR else ''}"
                          f"{obj.__class__.__name__} : \n") if not pass_ else '\n'

        for key in obj.__dict__:
            txt += '\t'*tab + f"\t - {key.center(max_key_length, ' ')} ({type(obj.__dict__[key]).__name__}) : " \
                              f"{str_object(obj.__dict__[key], tab + 1, True)}\n"

        return txt[:-1]
    except AttributeError:
        txt = ('\t'*tab + f"{text_editing.color.COLOR_YELLOW if COLOR else ''}"
                          f"{obj.__class__.__name__} : ") if not pass_ else ''
        txt += f"{text_editing.color.COLOR_GREEN if COLOR else ''}" \
               f"{str(obj)}"
        return txt


def show_value(value: typing.Any, tab_number: int = 0) -> None:
    """
    Prints in the terminal all the elements of a list, a dictionary or a tuple and its sub-elements.
    Prints in the terminal the other types and class.
    :param value: A value of any type or class.
    :param tab_number: The default number of tabs to put in front of the printout.
    :return: None
    """

    def sort_key(dico):
        if isinstance(dico, dict):
            liste_key = list(dico.keys())
            sorted_liste_key = []
            while len(liste_key) > 0:
                best = liste_key[0]
                for key_from_list in liste_key:
                    i = 0
                    stop = False
                    while i < min(len(str(best)), len(str(key_from_list))) and not stop:
                        if ord(str(best)[i]) > ord(str(key_from_list)[i]):
                            best = key_from_list
                            stop = True
                        elif ord(str(best)[i]) < ord(str(key_from_list)[i]):
                            stop = True
                        i += 1
                    if not stop:
                        if len(str(key_from_list)) < len(str(best)):
                            best = key_from_list
                liste_key.remove(best)
                sorted_liste_key.append(best)
            return sorted_liste_key
        else:
            return []

    if isinstance(value, typing.Union[list, dict, tuple]):
        print(f"{text_editing.color.COLOR_PURPLE if COLOR else ''}{type(value).__name__}", end="")
        print(f" ({len(value)} items):")
        for key in (sort_key(value) if isinstance(value, dict) else range(len(value))):
            print("\t" * tab_number + f"\t{text_editing.color.COLOR_GREEN if COLOR else ''}{key}: ", end='')
            show_value(value[key], tab_number + 1)
    else:
        print(str_object(value))


def space_number(number: typing.Union[int, float], spacing: str = ' ') -> str:
    """
    Separate with character defines the number entered every 3 digits.
    :param number: A value.
    :param spacing: A character.
    :return: A string of number separate.
    """
    if isinstance(number, int):
        number_list = list(str(number))
        txt = ""
        i = 0
        while len(number_list) != 0:
            if i == 3:
                i = 0
                txt = spacing + txt
            txt = number_list.pop() + txt
            i += 1
        return txt
    else:
        return space_number(int(number), spacing) + '.' + str(number).split('.')[1]


def last_iteration(iteration_text: str, txt: str | list) -> int | None:
    """
    Return the index of the last iteration on string.
    :param iteration_text: The searched iteration
    :param txt: The variable to search in.
    :return: The index of last iteration.
    """
    if isinstance(txt, str):
        liste = txt.split(iteration_text)
    else:
        liste = txt

    if len(liste) == 1:
        return None
    else:
        return len(txt) - (len(liste[-1]) + len(iteration_text))


def replace_last(sub_string: str, new_string: str, string: str) -> str:
    """
    Replaces the last iteration of the substring entered with the string chosen in the quoted string.
    :param sub_string: The substring entered.
    :param new_string: The string chosen.
    :param string: The quoted string.
    :return: The quoted string with the last iteration of the substring replaced by the chosen string.
    """
    li = last_iteration(sub_string, string)
    if li is None:
        return string
    return string[0:li] + new_string + string[li + len(sub_string):]
