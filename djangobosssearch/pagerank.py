
'''
Google PageRank Checksum Algorithm (Internet Explorer Toolbar)
	Downloaded from http://pagerank.phurix.net/
'''

import urllib
import httplib

class GoogleRank():
    
    # Definitions
    def  int_str(self, String, Integer, Factor):
        for i in range(len(String)) :
            Integer *= Factor
            Integer &= 0xFFFFFFFF
            Integer += ord(String[i])
        return Integer


    def hash_url(self, Str):
        C1 = self.int_str(Str, 0x1505, 0x21)
        C2 = self.int_str(Str, 0, 0x1003F)

        C1 >>= 2
        C1 = ((C1 >> 4) & 0x3FFFFC0) | (C1 & 0x3F)
        C1 = ((C1 >> 4) & 0x3FFC00) | (C1 & 0x3FF)
        C1 = ((C1 >> 4) & 0x3C000) | (C1 & 0x3FFF)

        T1 = (C1 & 0x3C0) << 4
        T1 |= C1 & 0x3C
        T1 = (T1 << 2) | (C2 & 0xF0F)

        T2 = (C1 & 0xFFFFC000) << 4
        T2 |= C1 & 0x3C00
        T2 = (T2 << 0xA) | (C2 & 0xF0F0000)

        return (T1 | T2)


    def check_hash(self, HashInt):
        HashStr = "%u" % (HashInt)
        Flag = 0
        CheckByte = 0

        i = len(HashStr) - 1
        while i >= 0:
            Byte = int(HashStr[i])
            if 1 == (Flag % 2):
                Byte *= 2;
                Byte = Byte / 10 + Byte % 10
            CheckByte += Byte
            Flag += 1
            i -= 1

        CheckByte %= 10
        if 0 != CheckByte:
            CheckByte = 10 - CheckByte
            if 1 == Flag % 2:
                if 1 == CheckByte % 2:
                    CheckByte += 9
                CheckByte >>= 1

        return '7' + str(CheckByte) + HashStr


    def get_rank(self, query):
        prhost='toolbarqueries.google.com'
        url = self.get_url(query)
        conn = httplib.HTTPConnection(prhost)
        conn.request("GET", url)
        response = conn.getresponse()
        data = response.read()
        status = response.status
        conn.close()
        pr = data.split(":")[-1].strip('\n')
        if len(pr) == 0 or status != 200:
            pr = '-1'
            f = open('/tmp/pr', 'w')
            f.write("Data: \n")
            f.write(str(data))
            f.write("URL\n")
            f.write(url)
            f.write("\n")
            f.close()
        return pr
        
    def get_url(self, query):
        prurl='/tbr?client=navclient-auto&ch=%s&features=Rank&q=info:%s'
    	hash = self.check_hash(self.hash_url(query))
    	url = prurl % (hash, query)
    	return url



