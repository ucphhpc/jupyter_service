import fs, os
from fs.sshfs import SSHFS


class DataStore:
    _client = None
    _target = ""

    def __init__(self, client):
        """
            :param client: This is the sshfs client instance that is used to access the datastore
        """
        self._client = client

    def list(self, path='.'):
        """
        :param path:
        file system path which items will be returned
        :return:
        A list of items in the path. There is no distinction between files and dirs
        """
        return self._client._sftp.listdir(path=path)

    def list_attr(self, path='.'):
        """
        :param path:
        directory path to be listed
        :return:
        A list of .SFTPAttributes objects
        """
        return self._client._sftp.listdir_attr(path=path)

    def read(self, filename):
        """
        :param file:
        File to be read
        :return:
        a string of the content within file
        """
        with self._client.open(filename) as open_file:
            return open_file.read()

    def read_binary(self, filename):
        """

        :param file:
        File to be read
        :return:
        a binary of the content within file
        """
        with self._client.openbin(filename) as open_file:
            return open_file.read()

    def open(self, filename, flag):
        """
        Used to get a python filehandler object
        :param filename:
        the name of the file to be opened
        :param flag:
        which mode should the file be opened in
        :return:
        a _io.TextIOWrapper object with utf-8 encoding
        """
        return self._client.open(filename, flag)

# TODO -> cleanup duplication
class ErdaShare(DataStore):
    _target = "@io.erda.dk/"

    def __init__(self, share_link):
        """
        :param share_link: This is the sharelink ID that is used to access the datastore,
            An overview over your sharelinks can be found at https://erda.dk/wsgi-bin/sharelink.py.
        """
        client = fs.open_fs("ssh://" + share_link + ":" + share_link + self._target)
        super().__init__(client=client)

# TODO -> cleanup duplication
class IDMCShare(DataStore):
    _target = "@io.idmc.dk/"

    def __init__(self, share_link):
        """
        :param share_link: This is the sharelink ID that is used to access the datastore,
            An overview over your sharelinks can be found at https://erda.dk/wsgi-bin/sharelink.py.
        """
        client = fs.open_fs("ssh://" + share_link + ":" + share_link + self._target)
        super().__init__(client=client)


class ErdaHome(DataStore):
    _target = "io.erda.dk"

    # TODO -> switch over to checking the OPENID session instead of username/password
    def __init__(self, username, password):
        """
        :param username:
        The username to the users ERDA home directory, as can be found at https://erda.dk/wsgi-bin/settings.py?topic=sftp
        :param password:
        Same as user but the speficied password instead
        """
        client = SSHFS(ErdaHome._target, user=username, passwd=password)
        super().__init__(client=client)

