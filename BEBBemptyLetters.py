import os
import requests
import alephmarcreader


class BEBBemptyLetters:

    def generate_empty_letters(self):
        """
        Method that organizes all tasks to generate the empty letter XML files.
        """
        print('Starting...')
        numbers = self.__get_numbers
        print('Got Numbers: {}'.format(len(numbers)))
        alephx_dict = self.__load_metadata(numbers)
        print('Downloaded AlephX files: {}'.format(self._loaded))
        print('Cached AlephX files: {}'.format(self._cached))
        print('Total AlephX files: {}'.format(len(alephx_dict)))
        res = self.__generate_XMLs(alephx_dict)
        print('Created XML files: {}'.format(res))
        print('Finished.')

    @property
    def __get_numbers(self):
        """
        Get all system numbers to work with.

        This requires a file `input/all_numbers.txt`.
        A file `input/exclude.txt` is optional.

        :return: [str]: A list of system numbers.
        """

        with open("input/all_numbers.txt") as f:
            all_numbers = f.readlines()
        all_numbers = list(map(lambda l: l.strip(), all_numbers))
        print('    All system numbers: {}'.format(len(all_numbers)))

        ignore = []
        with open("input/exclude.txt") as f:
            ignore = f.readlines()
        ignore = list(map(lambda l: l.strip(), ignore))
        print('    System numbers to ignore: {}'.format(len(ignore)))

        res = list(filter(lambda n: n not in ignore, all_numbers))

        return res

    def __load_metadata(self, numbers, overwrite=False):
        """
        Load and cache a number of AlephX files.

        The files will be stored to `cache/`.
        The flag `overwrite` decides, if pre-existing files should be re-loaded and overwritten, or loaded from cache.
        Re-loading ensures that the meta data is up to date; reading from cache is a lot faster.

        Note: This method uses the AlephX interface of the University Library of Basel.
        AlephX can only be accessed from within the Uni network or the VPN.

        :param [str] numbers: A list of system numbers.
        :param bool overwrite: True, to force reload already cached meta data; false by default.

        :return: dict: A dict, pairing system numbers and strings of loaded AlephX files
                (both from AlephX and from cache).
        """

        res = dict()

        self._cached = 0
        self._loaded = 0

        for nb in numbers:
            alephx = self.__get_alephx(nb, overwrite)
            res[nb] = alephx

        return res

    def __generate_XMLs(self, alephX_dict):
        """
        Generate empty XML letters from alephX meta data.

        :param dict alephX_dict: A dictionary with system numbers as keys and alephX strings as values.

        :return: int: number of files created.
        """
        res = 0
        # TODO: implement
        return res

    def __get_alephx(self, system_number, overwrite):
        path = "cache/" + system_number + ".xml"

        if os.path.isfile(path):
            if overwrite:
                os.remove(path)
            else:
                return self.__load_cached(path)

        alephx = self.__load_from_alephx(system_number)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(alephx)

        return alephx

    def __load_cached(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
        self._cached = self._cached + 1
        return data

    def __load_from_alephx(self, system_number):
        url = 'https://www.ub.unibas.ch/cgi-bin/ibb/alephx?op=find-doc&doc-num=' + system_number + '&base=dsv05'
        request = requests.get(url)
        if request.status_code != 200:
            raise Exception('Error when requesting {}: Could not connect to AlephX. Status code: {}. '
                            '(NB: Are you in VPN?)'.format(system_number, request.status_code))
        if request.text.startswith('<?xml version = \"1.0\" encoding = \"UTF-8\"?>\n<find-doc>\n'
                                   '<error>Error reading document</error>'):
            raise Exception('Error when requesting {}: No such file found.'.format(system_number))

        self._loaded = self._loaded + 1
        print('    loaded: {}'.format(system_number))
        return request.text


if __name__ == "__main__":
    letter_maker = BEBBemptyLetters()
    letter_maker.generate_empty_letters()
