import logging
import pathlib
import shutil
from xml.etree import ElementTree
import zipfile


class Dat:
    def __init__(self, system: str):
        self.system = system
        self.games = []
        self.roms_by_sha1hex = {}


class Game:
    def __init__(self, name: str, dat: Dat):
        self.name = name
        self.roms = []
        self.dat = dat


class ROM:
    def __init__(self, name: str, size: int, sha1hex: str, game: Game):
        self.name = name
        self.size = size
        self.sha1hex = sha1hex
        self.game = game


class DatParsingException(Exception):
    pass


class DatParser:
    def __init__(self):
        self.tag_path = []
        self.dat = None
        self.game = None

    def start(self, tag, attribs):
        self.tag_path.append(tag)

        if self.tag_path == ["datafile", "game"]:
            if self.game:
                raise DatParsingException("Found a <game> within another <game>")
            if not self.dat:
                raise DatParsingException("Found a <game> before the <header> was parsed")

            self.game = Game(name=self._get_required_attrib(attribs, "name"), dat=self.dat)

        elif self.tag_path == ["datafile", "game", "rom"]:
            if not self.game:
                raise DatParsingException("Found a <rom> that was not within a <game>")

            try:
                size_attrib = self._get_required_attrib(attribs, "size")
                size = int(size_attrib)
            except ValueError:
                raise DatParsingException(f"<rom> has size attribute that is not an integer: {size_attrib}")

            rom = ROM(
                name=self._get_required_attrib(attribs, "name"),
                size=size,
                sha1hex=self._get_required_attrib(attribs, "sha1"),
                game=self.game,
            )

            self.game.roms.append(rom)
            roms_with_sha1 = self.dat.roms_by_sha1hex.setdefault(rom.sha1hex, [])
            roms_with_sha1.append(rom)

    def _get_required_attrib(self, attribs, name) -> str:
        value = attribs.get(name)
        if not value:
            raise DatParsingException(f"Found a <{self.tag_path[-1]}> without a {name} attribute")
        return value

    def end(self, tag):
        if self.tag_path == ["datafile", "game"]:
            self.dat.games.append(self.game)
            self.game = None

        self.tag_path.pop()

    def data(self, data):
        if self.tag_path == ["datafile", "header", "name"]:
            self.dat = Dat(system=data)

    def close(self) -> Dat:
        return self.dat


class FileLikeParserFeeder:
    def __init__(self, parser):
        self.parser = parser

    def write(self, b):
        self.parser.feed(b)


def load_dat(dat_path: pathlib.Path) -> Dat:
    def parse_dat_file(dat_file) -> Dat:
        xml_parser = ElementTree.XMLParser(target=DatParser())
        shutil.copyfileobj(dat_file, FileLikeParserFeeder(xml_parser))
        dat = xml_parser.close()
        logging.info(f"Datfile loaded successfully with {len(dat.games)} games")
        return dat

    if dat_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(dat_path) as zip:
            for zip_member_info in zip.infolist():
                if not zip_member_info.filename.lower().endswith(".dat"):
                    continue
                logging.debug(f'Loading Datfile "{zip_member_info.filename}" from "{dat_path}"')
                with zip.open(zip_member_info) as dat_file:
                    return parse_dat_file(dat_file)
        raise DatParsingException("No .dat file found within provided .zip")
    else:
        logging.debug(f'Loading Datfile "{dat_path}"')
        with open(dat_path, "rb") as dat_file:
            return parse_dat_file(dat_file)
