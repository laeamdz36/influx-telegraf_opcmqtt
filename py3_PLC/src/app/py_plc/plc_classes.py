"""Module to definition of PLC models for ethenret IP"""
from pycomm3 import LogixDriver, StructTag


class PLCcmplx():
    """Class to handle PLC connection"""

    def __init__(self, ip):
        self.ip = ip
        self.plc = self.create_conn()
        try:
            self.plc.open()
            tags = self.plc.tags
            if tags:
                print("Tags Loaded")
        except Exception as e:
            print(f"ERROR {e}")
            raise e

    def create_conn(self):
        """Create connection to the PLC"""
        return LogixDriver(self.ip)

    def __enter__(self):
        """Execute at starts of with block, try to open connection"""
        try:
            if self.plc.open():
                print(f"Connection success {self.ip}")
                print(f"PLC time: {self.plc.get_plc_time()}")
                return self.plc
            else:
                raise Exception("Could not possibel to connect")
        except Exception as e:
            print("No se pudo abrir la conexion")
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """Esto se ejecuta siempre al salir del bloque with"""

        if self.plc.connected:
            self.plc.close()
        return False

    def read_tag(self, tag: str):
        """Read a simple tag from the current PLC"""

        # check is PLC is connected
        # thus read tag
        if self.plc.connected:
            r = self.plc.read(tag)
        else:
            if self.plc.open():
                r = self.plc.read(tag)
                self.plc.close()
        return r

    def read_tags(self):
        """Read all PLC Tags"""
        if self.plc.connected:
            tags = self.plc.get_tag_list()
            for i, tag in enumerate(tags):
                print(f"{i}\t{tag}")
        else:
            if self.plc.open():
                tags = self.plc.get_tag_list()
                for i, tag in enumerate(tags):
                    print(f"{i}\t{tag}")
