# @author       Siegfried Hadatsch
# @created      2023-09-27
# @lastmodified 2023-10-18 
# @version      2.2.4.2

from Definitions import Parser, LadeConfig, VerarbeiteZeile, Bearbeitungszeit

if __name__ == "__main__":
    
    args = Parser()
    Feldnamen = LadeConfig(args)
    start_time = Bearbeitungszeit()
    VerarbeiteZeile(args, Feldnamen,start_time)
