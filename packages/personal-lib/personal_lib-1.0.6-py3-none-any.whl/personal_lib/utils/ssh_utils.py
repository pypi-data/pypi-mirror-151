import paramiko
import socket
import logging
import time
import os
import warnings


class SSH():
    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.transport = None
        self.chan = None

    def status(self):
        if self.transport is None:
            return False
        return self.transport.is_active()

    def connect(self, times=0):
        times += 1
        try:
            logging.info('%s:start connect server...' % time.strftime('%H:%M:%S'))
            socket_ = socket.socket()
            socket_.connect((self.host, self.port))
            transport = paramiko.Transport(socket_)
            transport.connect(username=self.username, password=self.pwd)
            chan = transport.open_session()
            chan.get_pty()
            chan.invoke_shell()
            self.transport = transport
            self.chan = chan
            time.sleep(1)
            logging.info('%s:connect success!' % time.strftime('%H:%M:%S'))
            rec = self.chan.recv(-1)
            content = str(rec, encoding='utf-8')
            # logging.info(content)
            return True
        except Exception as e:
            logging.error('%s' % e)
            if times >= 3:
                logging.error('失败次数已超过3次，不再尝试连接')
                return False
            else:
                logging.error('%s:连接失败，重新连接……' % time.strftime('%H:%M:%S'))
                self.connect(times)

    def close(self):
        if self.chan is not None:
            self.chan.close()
        if self.transport is not None:
            self.transport.close()

    def exec_command(self, cmd, callback=None):
        '''
        执行命令
        :param cmd:
        :param callback:
        :return:
        '''
        ssh_client = paramiko.SSHClient()
        ssh_client._transport = self.transport
        stdin, stdout, stderr = ssh_client.exec_command(cmd + '\n')
        while not stdout.channel.exit_status_ready():
            line = stdout.readline()
            if len(line) != 0:
                print(line, end='')
                logging.info(line[0:-1])
                if callback is not None:
                    callback(line[0:-1])

            # 由于在退出时，stdout还是会有一次输出，因此需要单独处理，处理完之后，就可以跳出了
            if stdout.channel.exit_status_ready():
                lines = stdout.readlines()
                for line in lines:
                    print(line, end='')
                    logging.info(line[0:-1])
                    if callback is not None:
                        callback(line[0:-1])
                break

    def exec_cmd(self, cmd):
        '''
        执行命令，已废弃
        :param cmd:
        :return:
        '''
        warnings.warn("this function is deprecated", DeprecationWarning)
        self.chan.send(cmd + '\n')
        content = ''
        tmp = None
        rec_info = ''
        while True:
            rec = None
            b = self.chan.recv(-1)
            try:
                if tmp is None:
                    rec = str(b, encoding='utf-8')
                else:
                    rec = str(tmp + b, encoding='utf-8')
            except:
                if tmp is None:
                    tmp = b
                else:
                    tmp = tmp + b
                continue
            tmp = None
            print(len(rec), '====================')
            if len(rec) > 0:
                for r in rec:
                    rec_info = '%s%s' % (rec_info, r)
                    if r == '\r':
                        print(rec_info, end='')
                        rec_info = ''
                content = '%s%s' % (content, rec)
            if rec[len(rec) - 1:len(rec)] == '$':
                break
        print(content, end='')
        logging.info(content, False)
        return content

    def download(self, src_files, dst_dir, file_rename=None):
        '''
        下载src_files列表到本地dst_dir目录，可根据需要重命名file_rename
        :param src_files:
        :param dst_dir:
        :param file_rename:
        :return:
        '''
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        result = 0
        if file_rename is not None and len(file_rename) != len(src_files):
            return -1
        file_names = []
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        for i in range(len(src_files)):
            src_file = src_files[i]
            try:
                sftp.stat(src_file)
            except Exception as e:
                logging.error('%s:下载文件%s不存在！' % (time.strftime('%H:%M:%S'), src_file))
                result = -1
                continue
            index = src_file.rfind('/')
            file_name = src_file[index + 1:len(src_file)]
            if file_rename is not None:
                file_name = file_rename[i]
            dst_path = os.path.join(dst_dir, file_name)
            sftp.get(src_file, dst_path)
            file_names.append(file_name)
            logging.info('下载文件成功,保存路径：【%s】' % dst_path)
        sftp.close()
        return result

    def download_all(self, src_dir, dst_dir, filter_func=None, callback=None):
        '''
        下载远程目录src_dir中所有文件到本地dst_dir目录，可用filter_func对文件进行过滤
        :param src_dir:
        :param dst_dir:
        :param filter_func:
        :param callback:
        :return:
        '''
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        files = sftp.listdir(src_dir)
        if filter_func is not None:
            files = filter_func(files)
        for file in files:
            src_file = src_dir + '/' + file
            local_file = dst_dir + '/' + file
            sftp.get(src_file, local_file)
            logging.info(f'download file from 【{src_file}】 to 【{local_file}】')
            if callback is not None:
                callback(f'download file from 【{src_file}】 to 【{local_file}】')
        sftp.close()

    def upload(self, src_files, dst_dir, file_rename=None, callback=None):
        '''
        上传本地文件src_files到远程目录dst_dir
        :param src_files:
        :param dst_dir:
        :param file_rename:
        :param callback:
        :return:
        '''
        try:
            result = 0
            if file_rename is not None and len(file_rename) != len(src_files):
                return -1
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            for i in range(len(src_files)):
                src_file = src_files[i]
                if not os.path.exists(src_file):
                    logging.error('未找到要上传的文件【%s】' % src_file)
                    if callback is not None:
                        callback('未找到要上传的文件【%s】' % src_file)
                    continue

                index = src_file.rfind('/')
                file_name = src_file[index + 1:len(src_file)]
                if file_rename is not None:
                    file_name = file_rename[i]
                dst_path = dst_dir + '/' + file_name
                # dst_path = os.path.join(dst_dir, file_name)
                print(src_file, dst_path)
                sftp.put(src_file, dst_path)
                logging.info('上传文件成功,保存路径：【%s】' % dst_path)
                if callback is not None:
                    callback('上传文件成功,保存路径：【%s】' % dst_path)
            sftp.close()
            return result
        except Exception as e:
            print(e)
            exit()

    def upload_dir(self, local_dir, remote_dir, callback=None):
        '''
        上传本地文件夹到远程目录
        :param local_dir:
        :param remote_dir:
        :param callback:
        :return:
        '''
        local_dir = local_dir.replace('\\', '/').strip()
        if local_dir[-1] == '/':
            local_dir = local_dir[0:-1]
        dir_name = local_dir[local_dir.rindex('/') + 1:].replace('/', '')
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        for parent, dirnames, filenames in os.walk(local_dir):
            parent = parent.replace('\\', '/')
            absolute_dir = remote_dir + '/' + parent[parent.rindex(dir_name):]
            try:
                sftp.stat(absolute_dir)
            except Exception as e:
                cmd = 'mkdir -p %s' % absolute_dir
                print(cmd)
                if callback is not None:
                    callback(cmd)
                self.exec_command(cmd)
            for filename in filenames:
                parent = parent.replace('\\', '/')
                local_file = os.path.join(parent, filename).replace('\\', '/')
                remote_file = remote_dir + '/' + local_file[local_file.rindex(dir_name):]
                sftp.put(local_file, remote_file)
                print(f'upload file from {local_file} to {remote_file}')
                if callback is not None:
                    callback(f'upload file from {local_file} to {remote_file}')

    def check_file(self, src_file, stop_time=None, cur_date=None):
        '''
        个性化需求（校验文件是否在9:25之后更新）
        :param src_file:
        :param stop_time:
        :param cur_date:
        :return:
        '''
        check = False
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        while 1:
            try:
                if stop_time is not None:
                    current_time = int(time.strftime('%H%M%S'))
                    if current_time >= int(stop_time.replace(':', '')):
                        break
                attr = sftp.stat(src_file)
                if cur_date is not None:
                    mdate_time = int(TimeStampToTime(attr.st_mtime).replace('-', '').replace(':', '').replace(' ', ''))
                    if mdate_time >= int(cur_date) * 1000000 + 92500:
                        check = True
                        break
                else:
                    check = True
                    break
                time.sleep(1)
            except:
                time.sleep(1)
        sftp.close()
        return check

    def is_file_update(self, files, check_time):
        '''
        个性化需求（校验文件是否在check_time之后更新）
        :param files:
        :param check_time:
        :return:
        '''
        check = False
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        update_info_dict = {}
        for file in files:
            update_info_dict[file] = [0, int(check_time), 0]  # 文件大小、时间、是否更新完成
        update_count = 0
        while 1:
            print(time.strftime('%H:%M:%S'), 'checking update')
            try:
                for file in files:
                    attr = sftp.stat(file)
                    mdate_time = int(TimeStampToTime(attr.st_mtime).replace('-', '').replace(':', '').replace(' ', ''))
                    file_size = attr.st_size
                    if mdate_time < int(check_time):
                        continue
                    else:
                        last_file_size = update_info_dict[file][0]
                        last_update_time = update_info_dict[file][1]
                        if file_size != last_file_size or mdate_time != last_update_time:
                            update_info_dict[file][0] = file_size
                            update_info_dict[file][1] = mdate_time
                            continue
                        else:
                            update_info_dict[file][2] = 1
                print(update_info_dict)
                for file in files:
                    update_count += update_info_dict[file][2]
                if update_count == len(files):
                    break
                time.sleep(1)
            except:
                time.sleep(1)
        sftp.close()
        return check


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)
