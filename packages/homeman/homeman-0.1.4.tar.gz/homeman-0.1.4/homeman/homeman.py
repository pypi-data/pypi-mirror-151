from typing import Dict, Union, List
import os
import colorama
import logging
import tempfile
import json
import shutil
import subprocess
from urllib import request
import zipfile
import tarfile
import argparse
import filecmp
import difflib


# logger
colorama.init()
class CustomFormatter(logging.Formatter):

    log_colors = {
        'DEBUG'  : colorama.Fore.BLUE,
        'INFO'   : colorama.Fore.GREEN,
        'WARNING': colorama.Fore.YELLOW,
        'ERROR'  : colorama.Fore.RED
    }

    log_levels = {
        'DEBUG': 'DEBUG',
        'INFO': 'INFO',
        'WARNING': 'WARN',
        'ERROR': 'ERROR'
    }

    def __init__(self, color: bool = False):
        self.color = color
        if color:
            fmt = '%(log_color)s[%(log_level)5s]' + colorama.Style.RESET_ALL + ' %(message)s'
        else:
            fmt = '[%(log_level)5s] %(message)s'
        super().__init__(fmt=fmt)

    def format(self, record: logging.LogRecord) -> str:
        if self.color:
            record.__dict__['log_color'] = self.log_colors[record.levelname]
        record.__dict__['log_level'] = self.log_levels[record.levelname]
        return super().format(record)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(CustomFormatter(True))

log_file = os.path.join(tempfile.gettempdir(), 'homeman.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(CustomFormatter())

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# homeman
class HomeManException(Exception):
    pass


class HomeMan:
    def __init__(self):
        self.lock_file = os.path.join(tempfile.gettempdir(), 'homeman.lock')
        self.usr_home = os.path.expanduser('~')
        self.man_home = os.getenv('MAN_HOME', os.path.join(self.usr_home, '.manhome'))
        if not os.path.isdir(self.man_home):
            os.makedirs(self.man_home)
        self.man_json = os.path.join(self.man_home, 'homeman.json')

    def __enter__(self):
        try:
            with open(self.lock_file, 'x'):
                pass
        except:
            raise HomeManException('acquire lock failed, another script is running')
        else:
            logger.debug('acquire lock')
        
        if not os.path.isfile(self.man_json):
            with open(self.man_json, 'w') as f:
                f.write('{}')
        with open(self.man_json, 'r') as f:
            self.data: Dict = json.load(f)
            logger.debug('load data')
        return self
    
    def __mark_changed(self):
        self.data['homeman_changed'] = True
    
    def __exit__(self, t, e, tb):
        if e is None:
            if 'homeman_changed' in self.data.keys():
                del self.data['homeman_changed']
                self.__tidy_data()
                with open(self.man_json, 'w') as f:
                    json.dump(self.data, f, indent=2)
                    logger.debug('save data')
        os.remove(self.lock_file)
        logger.debug('release lock')

    def get_route(self, path: str) -> str:
        path = os.path.abspath(path)
        if path == self.man_home or path == self.usr_home:
            route = ''
        elif path.startswith(self.man_home + os.path.sep):
            route = path[len(self.man_home):]
        elif path.startswith(self.usr_home + os.path.sep):
            route = path[len(self.usr_home):]
        else:
            raise HomeManException(f'path illegal: {path}')
        if 'homeman' in route:
            raise HomeManException(f'route illegal: {route}')
        logger.debug('route: %s', route)
        return route

    def get_data(self, route: str, force: bool = False) -> Union[Dict, None]:
        cur_data: Dict = self.data
        for name in route.split(os.path.sep)[1:]:
            if 'homeman' in cur_data.keys():
                return
            if name not in cur_data.keys():
                if force:
                    cur_data[name] = {}
                else:
                    return
            cur_data: Dict = cur_data[name]
        logger.debug('data: %s', cur_data)
        return cur_data

    def __scan_data(self, d: Dict) -> List[Dict[str, str]]:
        if 'homeman' in d.keys():
            logger.debug('scan: %s', d)
            return [d]
        else:
            d_list = []
            for key in d.keys():
                d_list += self.__scan_data(d[key])
            return d_list

    def __tidy_data(self):
        self.__do_tidy_data(self.data)
        logger.debug('tidy data')

    def __do_tidy_data(self, d: Dict[str, Dict]) -> bool:
        flag = True
        empty_keys = []
        for key in d.keys():
            dd = d[key]
            if len(dd.keys()) != 0:
                if 'homeman' in dd.keys():
                    flag = False
                else:
                    if self.__do_tidy_data(dd):
                        empty_keys.append(key)
                    else:
                        flag = False
            else:
                empty_keys.append(key)
        for key in empty_keys:
            del d[key]
        return flag
    
    def add(self, route: str, meta: Dict[str, str]):
        logger.debug('========< add >========')
        if route == '':
            raise HomeManException('cannot add home itself')
        data = self.get_data(route, force=True)
        if data is None or len(data.keys()) != 0:
            raise HomeManException(f'conflict occur: {route}')
        data['homeman'] = route
        for key in meta.keys():
            data[key] = meta[key]
        logger.info('add: %s', route)
        self.__mark_changed()
        try:
            if 'url' in meta.keys():
                self.__pull(data, True)
            else:
                self.__sync(data, True)
        except HomeManException as e:
            logger.warning(e)

    def remove(self, route: str):
        logger.debug('========< remove >========')
        data = self.get_data(route)
        if data is None:
            logger.debug('route not exists: %s', route)
            return
        for homeman_data in self.__scan_data(data):
            try:
                self.__remove(homeman_data)
            except HomeManException as e:
                logger.warning(e)
    
    def __remove(self, data: Dict[str, str]):
        self.__restore(data)
        self.__mark_changed()
        route = data['homeman']
        man_path = self.man_home + route
        if os.path.isfile(man_path):
            os.remove(man_path)
        elif os.path.isdir(man_path):
            shutil.rmtree(man_path)
        elif os.path.exists(man_path):
            raise HomeManException(f'cannot remove: {man_path}')
        os.makedirs(man_path)
        os.removedirs(man_path)
        data.clear()
        self.__mark_changed()
        logger.info('remove: %s', route)

    def pull(self, route: str, force: bool):
        logger.debug('========< pull >========')
        data = self.get_data(route)
        if data is None:
            logger.debug('route not exists: %s', route)
            return
        for homeman_data in self.__scan_data(data):
            try:
                self.__pull(homeman_data, force)
            except HomeManException as e:
                logger.warning(e)
    
    def __pull(self, data: Dict[str, str], force: bool):
        if 'url' not in data.keys():
            return
        route = data['homeman']
        man_path = self.man_home + route
        if not force and os.path.exists(man_path):
            return
        url = data['url']
        with tempfile.TemporaryDirectory() as tempdir:
            temp_node = os.path.join(tempdir, 'node')
            if url.endswith('.git'):
                cmd = ['git', 'clone', '--depth', '1']
                if 'branch' in data.keys():
                    cmd.append('--branch')
                    cmd.append(data['branch'])
                cmd.append(url)
                cmd.append(temp_node)
                returncode = subprocess.call(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                if returncode != 0:
                    raise HomeManException(f'cannot clone git repo: {url}')
                else:
                    shutil.rmtree(os.path.join(temp_node, '.git'))
            else:
                try:
                    request.urlretrieve(url, filename=temp_node)
                except:
                    raise HomeManException(f'cannot download url: {url}')
                if url.endswith('.zip'):
                    shutil.move(temp_node, temp_node + '.zip')
                    try:
                        with zipfile.ZipFile(temp_node + '.zip') as z:
                            z.extractall(temp_node)
                    except:
                        raise HomeManException(f'cannot extract zip from url: {url}')
                elif url.endswith('.tar') or \
                        url.endswith('.tar.gz') or url.endswith('.tgz') or \
                        url.endswith('.tar.bz2') or url.endswith('.tbz2') or \
                        url.endswith('.tar.xz') or url.endswith('.txz'):
                    shutil.move(temp_node, temp_node + '.tarfile')
                    try:
                        with tarfile.open(temp_node + '.tarfile') as t:
                            t.extractall(temp_node)
                    except:
                        raise HomeManException(f'cannot extract tar from url: {url}')
            if os.path.isfile(man_path):
                os.remove(man_path)
            elif os.path.isdir(man_path):
                shutil.rmtree(man_path)
            elif os.path.exists(man_path):
                raise HomeManException(f'cannot remove: {man_path}')
            os.makedirs(man_path)
            os.rmdir(man_path)
            shutil.move(temp_node, man_path)
            data['mode'] = bin(os.stat(man_path).st_mode)
            self.__mark_changed()
            logger.info('pull: %s', route)
            self.__sync(data, False)

    def sync(self, route: str, reverse: bool):
        logger.debug('========< sync >========')
        data = self.get_data(route)
        if data is None:
            logger.debug('route not exists: %s', route)
            return
        for homeman_data in self.__scan_data(data):
            try:
                self.__sync(homeman_data, reverse)
            except HomeManException as e:
                logger.warning(e)
    
    def __sync(self, data: Dict[str, str], reverse: bool):
        usr_path = self.usr_home + data['homeman']
        man_path = self.man_home + data['homeman']
        if reverse:
            if not os.path.exists(usr_path):
                raise HomeManException(f'not exists: {usr_path}')
            self.__backup(data, False)
            if os.path.isfile(man_path):
                os.remove(man_path)
            elif os.path.isdir(man_path):
                shutil.rmtree(man_path)
            elif os.path.exists(man_path):
                raise HomeManException(f'cannot remove: {man_path}')
            os.makedirs(man_path)
            os.rmdir(man_path)
            if os.path.isfile(usr_path):
                shutil.copy(usr_path, man_path)
            elif os.path.isdir(usr_path):
                shutil.copytree(usr_path, man_path)
            else:
                raise HomeManException(f'cannot copy: {usr_path}')
            data['mode'] = bin(os.stat(man_path).st_mode)
            self.__mark_changed()
            logger.info('sync reversely: %s', data['homeman'])
        else:
            if not os.path.exists(man_path):
                raise HomeManException(f'not exists: {man_path}')
            self.__backup(data, False)
            if os.path.isfile(usr_path):
                os.remove(usr_path)
            elif os.path.isdir(usr_path):
                shutil.rmtree(usr_path)
            elif os.path.exists(usr_path):
                raise HomeManException(f'cannot remove: {usr_path}')
            os.makedirs(usr_path)
            os.rmdir(usr_path)
            if os.path.isfile(man_path):
                shutil.copy(man_path, usr_path)
            elif os.path.isdir(man_path):
                shutil.copytree(man_path, usr_path)
            else:
                raise HomeManException(f'cannot copy: {man_path}')
            os.chmod(usr_path, int(data['mode'], 2))
            logger.info('sync: %s', data['homeman'])

    def backup(self, route: str, force: bool):
        logger.debug('========< backup >========')
        data = self.get_data(route)
        if data is None:
            logger.debug('route not exists: %s', route)
            return
        for homeman_data in self.__scan_data(data):
            try:
                self.__backup(homeman_data, force)
            except HomeManException as e:
                logger.warning(e)
    
    def __backup(self, data: Dict[str, str], force: bool):
        route = data['homeman']
        usr_path = self.usr_home + route
        usr_path_bak = usr_path + '.homeman.bak'
        usr_path_bak2 = usr_path_bak + '.empty'
        if not force and (os.path.exists(usr_path_bak) or os.path.exists(usr_path_bak2)):
            return
        if os.path.isfile(usr_path_bak):
            os.remove(usr_path_bak)
        elif os.path.isdir(usr_path_bak):
            shutil.rmtree(usr_path_bak)
        elif os.path.isfile(usr_path_bak2):
            os.remove(usr_path_bak2)
        if os.path.isfile(usr_path):
            shutil.copy(usr_path, usr_path_bak)
        elif os.path.isdir(usr_path):
            shutil.copytree(usr_path, usr_path_bak)
        else:
            os.makedirs(usr_path)
            os.rmdir(usr_path)
            with open(usr_path_bak2, 'w'):
                pass
        logger.info('backup: %s', route)

    def restore(self, route: str):
        logger.debug('========< restore >========')
        data = self.get_data(route)
        if data is None:
            logger.debug('route not exists: %s', route)
            return
        for homeman_data in self.__scan_data(data):
            try:
                self.__restore(homeman_data)
            except HomeManException as e:
                logger.warning(e)
    
    def __restore(self, data: Dict[str, str]):
        route = data['homeman']
        usr_path = self.usr_home + route
        usr_path_bak = usr_path + '.homeman.bak'
        usr_path_bak2 = usr_path_bak + '.empty'
        if not os.path.exists(usr_path_bak) and not os.path.exists(usr_path_bak2):
            return
        if os.path.isfile(usr_path):
            os.remove(usr_path)
        elif os.path.isdir(usr_path):
            shutil.rmtree(usr_path)
        if os.path.exists(usr_path_bak):
            shutil.move(usr_path_bak, usr_path)
        else:
            os.remove(usr_path_bak2)
            os.mkdir(usr_path)
            os.removedirs(usr_path)
        logger.info('restore: %s', route)

    def check(self, route: str, show_diff: bool, formatter: str = 'none'):
        logger.debug('========< check >========')
        data = self.get_data(route)
        if data is None:
            logger.debug('route not exists: %s', route)
            return
        for homeman_data in self.__scan_data(data):
            try:
                self.__check(homeman_data, show_diff, formatter)
            except HomeManException as e:
                logger.warning(e)
    
    def __check(self, data: Dict[str, str], show_diff: bool, formatter: str = 'none'):
        route = data['homeman']
        usr_path = self.usr_home + route
        usr_path_bak = usr_path + '.homeman.bak'
        usr_path_bak2 = usr_path_bak + '.empty'
        if not os.path.exists(usr_path_bak) and not os.path.exists(usr_path_bak2):
            logger.warning('not backup: %s', route)
        else:
            man_path = self.man_home + route
            if not os.path.exists(man_path):
                logger.warning('not exists inside: %s', route)
            elif not os.path.exists(usr_path):
                logger.warning('not exists outside: %s', route)
            else:
                diff_files = []
                if os.path.isfile(usr_path) and os.path.isfile(man_path):
                    if not filecmp.cmp(usr_path, man_path):
                        diff_files.append(route)
                elif os.path.isdir(usr_path) and os.path.isdir(man_path):
                    def collect_diff_files(dcmp, dfs: List[str]):
                        for name in dcmp.diff_files:
                            dfs.append(dcmp.left[len(self.usr_home):] + os.path.sep + name)
                        for sub_dcmp in dcmp.subdirs.values():
                            collect_diff_files(sub_dcmp, dfs)
                    collect_diff_files(filecmp.dircmp(usr_path, man_path), diff_files)
                if len(diff_files) == 0:
                    logger.info('sync: %s', route)
                else:
                    logger.warning('no sync: %s', route)
                    if show_diff:
                        differ = difflib.Differ()
                        for f in diff_files:
                            print(f'[{f}]')
                            usr_f = self.usr_home + f
                            man_f = self.man_home + f
                            if not os.path.exists(usr_f):
                                print('not exists outside')
                            elif not os.path.exists(man_f):
                                print('not exists inside')
                            elif os.path.isdir(usr_f):
                                print('is dir outside')
                            elif os.path.isdir(man_f):
                                print('is dir inside')
                            else:
                                with open(usr_f, 'r') as uf, open(man_f, 'r') as mf:
                                    if formatter == 'json':
                                        ulines = json.dumps(
                                            json.load(uf), indent=2
                                        ).splitlines(keepends=True)
                                        mlines = json.dumps(
                                            json.load(mf), indent=2
                                        ).splitlines(keepends=True)
                                    else:
                                        ulines = uf.readlines()
                                        mlines = mf.readlines()
                                    res = ['------ start ------\n']
                                    res.extend(list(differ.compare(ulines, mlines)))
                                    res.append('------ end ------\n')
                                    common_counter = 0
                                    last_line = '\n'
                                    for line in res:
                                        if line.startswith('  '):
                                            common_counter += 1
                                            last_line = line
                                        else:
                                            if common_counter != 0:
                                                if common_counter == 1:
                                                    print(last_line, end='')
                                                else:
                                                    print(f'------ {common_counter} common lines ------')
                                            print(line, end='')
                                            common_counter = 0


def main():
    homeman_parse = argparse.ArgumentParser(
        prog='homeman',
        description='this is a tool to manage your files or directories in user home, base on symbol links.'
    )

    homeman_parse.add_argument(
        '-d', '--debug', action='store_true',
        help='set the console log level to DEBUG'
    )
    homeman_parse.add_argument(
        '-i', '--info', action='store_true',
        help='set the console log level to INFO'
    )
    homeman_parse.add_argument(
        '-w', '--warn', action='store_true',
        help='set the console log level to WARNING'
    )
    homeman_parse.add_argument(
        '-e', '--error', action='store_true',
        help='set the console log level to ERROR'
    )
    homeman_parse.add_argument(
        '-q', '--quit', action='store_true',
        help='DO NOT print console log'
    )

    homeman_commands = homeman_parse.add_subparsers(dest='command')

    # add
    command_add = homeman_commands.add_parser(
        'add', help='add a resource to homeman'
    )
    command_add.add_argument(
        'path', type=str,
        help='the location of resource'
    )
    command_add.add_argument(
        '-u', '--url', type=str,
        help='special a remote resource'
    )
    command_add.add_argument(
        '-b', '--branch', type=str,
        help='special the branch name when resource type is git'
    )

    # pull
    command_pull = homeman_commands.add_parser(
        'pull', help='load a resource'
    )
    command_pull.add_argument(
        'path', type=str,
        help='the location of resource'
    )
    command_pull.add_argument(
        '-f', '--force', action='store_true',
        help='set the console log level to DEBUG'
    )

    # remove
    command_remove = homeman_commands.add_parser(
        'remove', help='remove a resource'
    )
    command_remove.add_argument(
        'path', type=str,
        help='the location of resource'
    )

    # sync
    command_sync = homeman_commands.add_parser(
        'sync', help='list a resource'
    )
    command_sync.add_argument(
        'path', type=str,
        help='the location of resource'
    )
    command_sync.add_argument(
        '-v', '--reverse', action='store_true',
        help='set the console log level to DEBUG'
    )

    # backup
    command_backup = homeman_commands.add_parser(
        'backup', help='list a resource'
    )
    command_backup.add_argument(
        'path', type=str,
        help='the location of resource'
    )
    command_backup.add_argument(
        '-f', '--force', action='store_true',
        help='set the console log level to DEBUG'
    )

    # restore
    command_restore = homeman_commands.add_parser(
        'restore', help='list a resource'
    )
    command_restore.add_argument(
        'path', type=str,
        help='the location of resource'
    )

    # check
    command_check = homeman_commands.add_parser(
        'check', help='list a resource'
    )
    command_check.add_argument(
        'path', type=str,
        help='the location of resource'
    )
    command_check.add_argument(
        '-v', '--show', action='store_true',
        help='show diff'
    )
    command_check.add_argument(
        '-f', '--formatter', type=str, choices=['none', 'json'], default='none',
        help='show diff'
    )

    args = homeman_parse.parse_args()

    if args.quit:
        console_handler.setLevel(logging.CRITICAL)
    elif args.error:
        console_handler.setLevel(logging.ERROR)
    elif args.warn:
        console_handler.setLevel(logging.WARNING)
    elif args.info:
        console_handler.setLevel(logging.INFO)
    elif args.debug:
        console_handler.setLevel(logging.DEBUG)

    try:
        with HomeMan() as hm:
            route = hm.get_route(args.path)
            if args.command == 'add':
                meta = {}
                if args.url:
                    meta['url'] = args.url
                    if args.branch:
                        meta['branch'] = args.branch
                hm.add(route, meta)
            elif args.command == 'remove':
                hm.remove(route)
            elif args.command == 'pull':
                hm.pull(route, args.force)
            elif args.command == 'sync':
                hm.sync(route, args.reverse)
            elif args.command == 'backup':
                hm.backup(route, args.force)
            elif args.command == 'restore':
                hm.restore(route)
            elif args.command == 'check':
                hm.check(route, args.show, args.formatter)
    except HomeManException as e:
        logger.error(e)
        return 1
    except Exception as e:
        logger.exception(e)
        return 2
    else:
        return 0
