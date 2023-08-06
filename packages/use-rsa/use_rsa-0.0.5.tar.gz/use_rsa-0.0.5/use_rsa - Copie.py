import random as rd
import re
class Encryptor_stable:
    def __init__(self, keys_1, keys_2):
        self.p = keys_1
        self.q = keys_2
    def eucalg(self, a, b):
        swapped = False
        if a < b:
            a, b = b, a
            swapped = True
        ca = (1, 0)
        cb = (0, 1)
        while b != 0:k = a // b;a, b, ca, cb = b, a-b*k, cb, (ca[0]-k*cb[0], ca[1]-k*cb[1])
        if swapped:return (ca[1], ca[0])
        else:return ca
    def modpow(self, b, e, n):
        tst = 1
        siz = 0
        while e >= tst:
            tst <<= 1
            siz += 1
        siz -= 1
        r = 1
        for i in range(siz, -1, -1):
            r = (r * r) % n
            if (e >> i) & 1: r = (r * b) % n
        return r
    def keysgen(self, p, q):
        p , q = self.p , self.q
        n = self.p * self.q
        lambda_n = (p - 1) * (q - 1)
        e = 35537
        d = self.eucalg(e, lambda_n)[0]
        if d < 0: d += lambda_n
        return {'priv': (d, n), 'pub': (e, n)}
    #Encrypt number
    def numencrypt(self, m, pub):return self.modpow(m, pub[0], pub[1])
    def numdecrypt(self, m, priv):return self.modpow(m, priv[0], priv[1])
    def second_cryptor(self, m, pub):
        xxx = m
        m = int(''.join([i for i in m if i in  '0123456789']))
        i = self.numencrypt( m, pub)
        s = str(i)
        m = ''
        for x in s:m += str(rd.choice([chr(k) for k in range(256) if chr(k) not in '0123456789'])) + x
        return m
    def second_decryptor(self, m, priv):
        m = int(''.join([i for i in m if i in '0123456789']))
        return self.numdecrypt(m, priv)
    def is_prime(self, n):
        if n == 2 or n == 3: return True
        if n < 2 or n%2 == 0: return False
        if n < 9: return True
        if n%3 == 0: return False
        r = int(n**0.5)
        f = 5
        while f <= r:
            if n % f == 0: return False
            if n % (f+2) == 0: return False
            f += 6
        return True 
    #=====================================
    def get_list_prime(self):
        l = []
        for i in range(35537, 2000000):
            if self.is_prime(i):
                l += [i]
        return l
    def g(self, l):
        a = rd.choice(l)
        b = rd.choice(l)
        while (a == b) or (l.index(b) == l.index(b) + 1) or (b < a):
            b = rd.choice(l)
        return a, b
    #Encrypte string
    def ___(self, str_, pub, bb = 35):
        x = [45, bb, 78]
        return ''.join([rd.choice(['a','b','B','b',"Z","@",'z','Y','$','£'])+i for i in chr(x[1]).join([str(self.numencrypt(ord(i),pub))for i in str_])])
    def __(self, s, priv, bb = 35):
        x = [45, bb, 78]
        return ''.join([chr(self.numdecrypt(int(''.join(re.findall(r'\d+',i))), priv))for i in s.split(chr(x[1]))])