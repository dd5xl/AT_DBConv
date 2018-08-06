'''
Created on 26.07.2018

@author: bert
'''


import argparse

#INFILE = 'user.bin'
#OUTFILE = 'import.csv'

# predefined fields
STATEDICTGER = {0:'SA/MVP', 1:"BE", 2:"HH/SH", 3:"NS", 4:"NRW", 5:"RP/SR", 6:"HE", 7:"BW", 8:"BY", 9:"SN/TH"}
COUNTRY = 'DMR'
CALLTYPE = 'Private Call'
CALLALERT = 'None'
OUTFORMAT = '{0},{1},{2},{3},{4},{5},{6},{7},{8}\n'

'''
Format user.bin:
ID, Callsign, Name, City, State, Remark(1st name)

German entries have street address & city instead of city & state :-(
For privacy reasons outfile city will be city, state will be set by STATEDICTGER according to 4th digit of ID,
street address will be dropped.

Format OUTFILE:
ID, Callsign, Name, City, State, Country, Remarks, CallType, CallAlert
'''


parser = argparse.ArgumentParser(description = 'Convert MD380 user.bin into AT-D868 Digital Contacts import file')
parser.add_argument('infile', metavar='Infile', type=str, help='Input file (user.bin)')
parser.add_argument('outfile', metavar='Outfile', type=str, help='Output file (*.csv)')
args=parser.parse_args()

with open (args.infile, 'r', encoding='iso8859-15') as filein, open (args.outfile, 'w', encoding='iso8859-15') as fileout:
    cnt = 0
    print ('\nConverting line:')
    for line in filein:
        print (cnt+1, end='\r')
        line = line.strip() # discard leading spaces and trailing NLs
        if len(line) == 7 or ',Time,' in line: # erste und letzte Zeile in user.bin verwerfen
            continue
        (dmrid, call, pname, city, state, remark, dummy) = line.split(',', 6)
        if dmrid == call or len(dmrid) == 6: # drop reflector entries as well as any repeater IDs
            if dmrid == '262997': # keep BM parrot entry
                pass
            else:
                continue
        cnt += 1
        mcc = dmrid[0:3]
        if mcc == '262' or mcc == '263': # different formatting for german calls
            gst = int(dmrid[3]) # extract german state id
            lineout = OUTFORMAT.format(dmrid, call, pname, state, STATEDICTGER[gst], COUNTRY, remark, CALLTYPE, CALLALERT)
        else:
            lineout = OUTFORMAT.format(dmrid, call, pname, city, state, COUNTRY, remark, CALLTYPE, CALLALERT) 
        fileout.write(lineout)

print ("\nAll done!\n")
