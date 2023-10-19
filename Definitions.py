import sys
import json
import argparse
import time


#Parser fuer cmd-zeile

def Parser():

    parser = argparse.ArgumentParser(description='Einfaches Tool zur Analyse von LDT-Dateien. Die Standardausgabe der analysierten Datei(en) erfolgt als:  FELDKENNUNG - FELDINHALT ')


    parser.add_argument('-b', '--bitcount', action='store_true', help='Ausgabe des Bitcounts je Zeile')
    parser.add_argument('-e', '--erweitert', action='store_true', help='Erweiterte Ausgabe der LDT-Datei mit Bedeutung des Feldinhaltes')
    parser.add_argument('-k', '--komplett', action='store_true', help= 'Ausgabe der Zeilen mit saemtlichen vefuegbaren Informationen')
    parser.add_argument('-o', '--objectident', action='store_true', help='Ausgabe der Zeilen die Objekt-Ident enthalten')
    parser.add_argument('-t', '--time', action='store_true', help='Ausgabe der Bearbeitungsdauer')
    parser.add_argument('--find', nargs='?', const=2, help='Suche nach angegebenem Begriff mit Ausgabe der Zeile (falls vorhanden)')
    parser.add_argument('--version', nargs='?', const=2, type=int, help='Auswahl der LDT-Version, in der Datei ausgelesen werden soll (Standard: LDT 2).')

    parser.add_argument('datei', type=str, help='Zu verarbeitende LDT-Datei')
    
    args = parser.parse_args()
    parser.add_argument("other_args", nargs=argparse.REMAINDER) #Gemischte Argumente
    return args



#Lade Config-Datei basierend auf Eingabeparameter

def LadeConfig(args):
    config_LDT ="config/config_Feldnamen_LDT2.json"

    if args.version == 3:
       config_LDT = "config/config_Feldnamen_LDT3.json" 
    elif args.version == 2 or args.version == None:
       config_LDT

    else:
        input(f"LDT-Version {args.version} ist nicht hinterlegt. Wechsle zu Version LDT-2. (ENTER zum Fortfahren)")
        config_LDT

    with open(f"{config_LDT}", "r",encoding='utf-8') as config_Feldnamen:
        Feldnamen = json.load(config_Feldnamen)
        return Feldnamen

def FindeStringinLDT(args):
    suchstring = args.find
    print(suchstring)



#Funktion fuer Messung der Bearbeitungsdauer

def Bearbeitungszeit():
    start_time = time.time()
    return start_time


#Funktion für Verarbeitung der LDT-Datei zeilenweise

def VerarbeiteZeile(args,Feldnamen,start_time):

    try:
        with open(args.datei, 'r') as datei:
                zeilen = datei.readlines()
        
        modifizierte_zeilen = []
        ldt_trennstellen = [0,3,7]
        obj_idents = ["6329","8000","8001","8002","8003",]

        for zeile in zeilen:
            
            ldt_teil0 = zeile[ldt_trennstellen[0]:ldt_trennstellen[1]]  # Bitlaenge der Zeile
            ldt_teil1 = zeile[ldt_trennstellen[1]:ldt_trennstellen[2]]  # Wert Feldname (zB: 8000)
            ldt_teil2 = zeile[ldt_trennstellen[2]:]                     # Inhalt Feldname (zB. Krankenhaus XY) 

            ersetztes_kuerzel = ""
            bitcount = ""

            if args.bitcount:
                bitcount = ldt_teil0+'\t'

            if args.objectident:

                 if ldt_teil1 in obj_idents:
                    ldt_teil1 =""
                    continue

            if args.erweitert:
                ersetztes_kuerzel = Feldnamen.get(ldt_teil1, 'Bedeutung in aktueller LDT-Version nicht hinterlegt')
                ersetztes_kuerzel = ersetztes_kuerzel.ljust(60)
            
            if args.komplett:
                bitcount = ldt_teil0+'\t'
                ersetztes_kuerzel = Feldnamen.get(ldt_teil1, 'Bedeutung in aktueller LDT-Version nicht hinterlegt')
                ersetztes_kuerzel = ersetztes_kuerzel.ljust(60)

            
            modifizierte_zeile = f"{bitcount}{ldt_teil1}\t{ersetztes_kuerzel}\t{ldt_teil2}"
            modifizierte_zeilen.append(modifizierte_zeile)

        sys.stdout.writelines(modifizierte_zeilen)

        if args.time:
            print("\n"*2,">>> Bearbeitungszeit: %s seconds" % (time.time() - start_time))
        
    except FileNotFoundError:
        print(f"Die Datei {args.datei} wurde nicht gefunden!")
        sys.exit(1)
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {str(e)}")
        sys.exit(1)


