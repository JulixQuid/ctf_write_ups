import re

def deobfuscate_powershell(payload):
    # Reverse the payload string (critical first step)
    decoded = payload[::-1]

    # Clean up concatenation artifacts
    decoded = decoded.replace("ukz+ukz", "").replace("ukz", "")

    # Decode [char]XX values
    decoded = re.sub(
        r'\[char\](\d+)',
        lambda m: chr(int(m.group(1))),
        decoded,
        flags=re.IGNORECASE
    )

    # Apply string replacements from original script
    replacements = {
        r'IiD': "'",        # Single quote
        r'yzp': "'",        # Single quote
        r'aro': '$',       # Dollar sign (case-sensitive)
        r'lbH': '"',        # Double quote
        r'ask': '"',        # Double quote
        r'olt': '|',       # Pipe character
        r'ra9shellid': '$shellId',  # Variable name
        r'jqzakf': 'fkazqj',  # Reversed temporary value
        r'P81': 'FLE',      # Part of URL decoding
        r'QMR': 'rm',       # Invoke-Expression (IEX) alias
        r'\]rAhc\[': ']RAhC[',  # Fix char array casing
    }

    for pattern, replacement in replacements.items():
        decoded = re.sub(pattern, replacement, decoded, flags=re.IGNORECASE)

    # Clean up PowerShell syntax artifacts
    decoded = (
        decoded.replace(" . ", ".")
                .replace(" )", ")")
                .replace("}yrt{", "{try}")
                .replace("}hctac{", "{catch}")
    )

    return decoded

# Your provided payload
payload = """))]rahC[,)18]rahC[+77]rahC[+28]rahC[(ecalperc-93]rahC[,'ukz'ecalperc-63]rahC[,'akF'ecalperc-)') uk'+'zukz'+'nioj-]) htgnel.jqzakf ( -.. 1 -'+'[jqzakf ()ukzxukz+'+']03[emohspakf+]4[emohspakf (. ; )  qmr iex( (ukz & ( ra9shellid'+'[1]+ra9shellid[13]+iidxiiD)( (u'+'kz+ukz((lbh{15}{11}{10}{1}ukz+ukz{22}{35}{24}{21ukz+'+'ukz}{4}{34}{8}{9}{16}{27}{5}{38}{33}{23}{14}{20}{6}{26}{13}{17}{7}{28}{ukz+ukz37}{31}{29}{2}{32}{ukz+ukz1'+'2ukz+ukz}{36}{0}ukz+ukz{19}{3}{18}{25}{30}lbh-fiiDriDmoiiD,iiD3]rahC[,yzpc1hyzpecalpeukz+ukzr-93]rah'+'C[,iiD,iiD]diug[(yziiD,iiD((( )yzpxyzp+]43[emohspariiD,iiDhc[iiD,iiDzpos si gayzp+yziiD,iiDukz+ukzyzpnlqsnyzp+yz'+'plyzp+yzpqukz+ukzsyzp+yzppyzp+yzp81 tsoh-eukz+ukztiyzp+yzprw ;pyzp+yzp81yzp+yukz+ukzzp}yryzp+yzpr0wukz+ukz_tn'+'0d_3r4yzp+'+'yzpwl4m_tn1yzp+yzpa_s1htiiD,iiDyyzukz+ukzp+yzpr'+'otceriD'+' eyzp+yzppy'+'tmyzukz+u'+'kzp+yzpetyzp'+'+'+'yzpi- riDyzp+yzpiiD,iiD[(ecalper-)yzpukz+ukzp81!ti ukz+ukzd'+'iiD,iiDyzp+yzpnifyzp+yzukz+ukzp ogyziiD,iiD )6i'+'D,iiukz+ukz'+'diable '+'n7a1u (ask )iiD,iiDzp+yzpaPdlihc- yzp+ukz+ukzyzppmet:vneiiDukz+ukz,iiDp81ukz+ukztyzp+yzpxt.galfp8yzp+yzp1 yzp+yzphtyzp+yzpaPdlihukz+ukzc- r'+'i'+'Dmodnay'+'zp+yzprc1h htap- yzp+yzp'+'hukz+ukztayzp+ukz+ukzyzpp-nioj( h'+'tap- tnyzp+yzpetnoc-tyzp+yzukz+ukzpes yzp+yzp;'+'lyzp+yzpluyzp+yzpniiD,i'+'D llehSrewoiiD,iiDset-variiD,iiDp+yzp os metsys ruo'+'y no eryzp+iiD,ii'+'D-tuo vyzp+yzpvq yzp+uk'+'z+ukzyzpiiD,iiD+]4[emohspu'+'kz+uk'+'zaro ( . ask ) ; -join ( variaBleI'+'iD,iiDyzp+yzpdnarc1'+'yzp+yzphyukz+ukzzpiiD,iiDyzp+yzpp moyukz+ukzzp+yzpdnar nyzp+yzpur yzp+yzpttyzp+yz'+'pnhNnodukz+ukz yzp+'+'yzpyletinifeDyzp+iiD,iiD]rahC[,)811]u'+'kz+ukzrahC[+68]rahC[+18'+']rahC['+'( ecalper-43]rahC[,'+'yzpp81yzp  ecalpeR'+'ukz+ukzc-69]'+'r'+'aiiD,iiD)611]raukz+ukzhc[+87]iiD,iiDzp+yzp uoyiiD,iiDhc['+'+27]'+'rahC[(ecalperc- ukz+ukz ukz+ukz421iiD,ukz+ukzii'+'D  n'+'7a1u -valueo  )[ -1.ukz+ukz. -( ( var'+'iable  n7a1u iiD,iiD{tic'+'p8yzp+yukz+u'+'kzzp1'+' eulaV-yzukz+ukzp+yzp )iiD,iiDyzpehweukz+ukzmyzp'+'+yiiD,iiDmodnayzp+yzp'+'ryzp+yzpcyzp+yzp1h hyzp+yzptap-yzp+yzp myzukz+ukzp+yzpe'+'ti-yzp+'+'yzpwen ;))(gnyzp+yukz+ukzzpirtsoT.)('+'diuukz+ukzgwyzp+yziiD,iiD:ukz+ukzyzp+yzukz+ukzpiiD,iiD-valueo  ).lengtH )]oltiexiiD,iiDn:iiD,iiukz+ukzDp'+'+yzp htYIuk'+'z+ukziD,ukz+ukziiDno dnifyukz+ukziiD,iiD,)801]rahC[+18]rahC[+511]rahCiiD,iukz+u'+'kziDraiD,iiDc1h htap- htap-nioyzp+yzpj = iukz+ukziD,iiDpeukz+ukziiD,iiDpukz+ukzlf eht ,syawyyzp+yzpnukz+ukza tu'+'b yzp+yzp.yzp+yzp.tenretni eht iiD)) -replaceiiDoltiiD,['+'char]124  -replaceiiDyzpiiD,[char]39  -creplace iiDaroii'+'D,[ukz+ukzchar]36-creplace ([char]97+[char]115+[char]107),[char]34) '+')ukz).replace(([char]73+[char]105+[char]68),[string][char]39).replace(([char]114+[char]65+[char]57),[string][char]36).replace(([char]108+[char]98+[char]72),[string][char]34)"""
result = deobfuscate_powershell(payload)
print("Deobfuscated payload:")
print(result)