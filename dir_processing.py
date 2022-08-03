from pathlib import Path
from typing import List, Iterable
import requests
from bs4 import BeautifulSoup

BASE = 'https://github.com/'
# __all__ = ["BASE", "save_repo"]


def _get_files(url):
    """Obtains a list of all files and directories in a GitHub repo
    Parameters
    ----------
    url: str
        A url to a github repo
    """
    # url = 'https://github.com/realpython/materials'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    content = []
    final = []
    el = soup.find('div', role='grid')
    if el is not None:
        for i in el.find_all('div', role='row')[1:]:
            # print(i.find('a')['href'])
            if i.find('a').get('rel') is None:
                content.append(BASE + i.find('a')['href'])
    for i in content:
        final.append(_get_files(i))
    if not content:
        return url
    return _flatten(final)


def _flatten(lst: List):
    """Transforms a nested list into a plain one
    Parameters
    ----------
    lst: List
        List to be transformed
    """
    gather = []
    for item in lst:
        if isinstance(item, (list, tuple, set)):
            gather.extend(_flatten(item))
        else:
            gather.append(item)
    return gather


def save_repo(url: str, base_dir: str, excluded: Iterable = ()):
    """
    Parameters
    ----------
    url : str
        Url to a repo's main directory
    base_dir : str
        Base directory of the repo
    excluded : Iterable
        An Iterable of excluded file extensions
    """
    start_dir = Path('.') / base_dir
    # if not start_dir.exists():
    start_dir.mkdir(exist_ok=True)
    for i in _get_files(url):
        # cur = i[i.rfind(base_dir):]
        file_name = i[i.rfind('/') + 1:]
        cur_path = i[i.rfind(base_dir):i.rfind('/') + 1].replace('/', '\\')
        cur_path = Path(cur_path)
        if not cur_path == start_dir:
            cur_path.mkdir(parents=True, exist_ok=True)
        if cur_path.suffix != '\n':
            # (cur_path / file_name).touch(exist_ok=True)
            _check_extension(i, (cur_path / file_name), (cur_path / file_name).suffix, excluded)
            # get content dziala
            # get_content(i, (cur_path / file_name))
    # print(placeholder[0][placeholder[0].rfind(base_dir)+1:])


def _get_content(url: str, file_path: Path):
    """Obtains and reads text content into a file
    Parameters
    ----------
    url : str
        Url of a file
    file_path : Path
        Path of a file
    Raises
    ------
        AttributeError
            Raised if a wrong extension is provided
    """
    if not 'https://github.com' in url:
        raise ValueError('Wrong Path') from None

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        code = ''
        for i in soup.find('table').find_all('tr'):
            code += f"{i.find_all('td')[1].text}\n"
        file_path.write_text(code, encoding='utf-8')
    except AttributeError:
        print(f'Wrong Extension in: {file_path}')


def _check_extension(url: str, path: Path, file_ext: str, excluded: Iterable):
    """Checks an extension of a given file
    Parameters
    ----------
    url : str
        Url of a file
    file_path : Path
        Path of a file
    file_ext: str
        Extension of a file
    excluded : Iterable
        An Iterable of excluded file extensions
    """
    if file_ext in excluded:
        return
    path.touch(exist_ok=True)
    if file_ext in ['.jpg', '.png', '.wav', '.mp3', '.mp4', '.ogg']:  # and so on...
        _get_content_bytes(url, path)
    elif file_ext == '.md':
        _get_markdown(url, path)
    else:
        _get_content(url, path)


def _get_content_bytes(url: str, file_path: Path):
    """Obtains and reads bytes content into a file
    Parameters
    ----------
    url : str
        Url of a file
    file_path : Path
        Path of a file
    Raises
    ------
        AttributeError
            Raised if a wrong extension is provided
    """
    try:
        r = requests.get(url + '?raw=true')
        file_path.write_bytes(r.content)
    except AttributeError:
        print(f'Wrong Extension in: {file_path}')


def _get_markdown(url: str, file_path: Path):
    """Obtains and reads markdown content into a file
    Parameters
    ----------
    url : str
        Url of a file
    file_path : Path
        Path of a file
    Raises
    ------
        AttributeError
            Raised if a wrong extension is provided
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        file_path.write_text(soup.find('div', id='readme').find('article').text)
    except AttributeError:
        print(f'Wrong Extension in: {file_path}')


if __name__ == '__main__':
    # print(get_files('https://github.com/realpython/materials/tree/master/flask-connexion-rest-part-3'))
    save_repo('https://github.com/realpython/materials/tree/master/serverless-sms-service',
              'serverless-sms-service', ['.md', '.txt', '.json'])
