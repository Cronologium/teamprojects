import re
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader

import random
import math
import sys


plaintext_regex = r'^[a-z ]*$'
ciphertext_regex = r'^[A-Z ]*$'

def rabinMiller(n):
    s = n - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1
    k = 0
    while k < 128:
        a = random.randrange(2, n - 1)
        # a^s is computationally infeasible.  we need a more intelligent approach
        # v = (a**s)%n
        # python's core math module can do modular exponentiation
        v = pow(a, s, n)  # where values are (num,exp,mod)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % n
        k += 2
    return True


def isPrime(n):
    # lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
    # under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
    # of composite numbers from our potential pool without resorting to Rabin-Miller
    lowPrimes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
        , 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179
        , 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269
        , 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367
        , 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461
        , 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571
        , 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661
        , 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773
        , 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883
        , 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if (n >= 3):
        if (n % 2 != 0):
            for p in lowPrimes:
                if (n == p):
                    return True
                if (n % p == 0):
                    return False
            return rabinMiller(n)
    return False


def generateLargePrime(k):
    # k is the desired bit length
    r = 100 * (math.log(k, 2) + 1)  # number of attempts max
    r_ = r
    while r > 0:
        # randrange is mersenne twister and is completely deterministic
        # unusable for serious crypto purposes
        n = random.randrange(2 ** (k - 1), 2 ** k)
        r -= 1
        if isPrime(n) == True:
            return n
    return 0


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def encrypt(request):
    text = request.POST['text']

    if re.search(plaintext_regex, text) is None:
        return JsonResponse({'msg': 'Plaintext is invalid!'})
    n = int(request.POST['n'])
    e = int(request.POST['e'])

    m = 0
    for ch in text:
        if ch == ' ':
            m = m * 27 % n
        else:
            m = (m * 27 + ord(ch) - ord('a') + 1) % n

    enc = pow(m, e, n)
    text = ''
    while enc:
        mod = enc % 27
        if mod == 0:
            text = ' ' + text
        else:
            text = chr(ord('a') - 1 + mod) + text
        enc = enc // 27
    return JsonResponse({'msg': text.upper()})


def decrypt(request):
    text = request.POST['text']

    if re.search(ciphertext_regex, text) is None:
        return JsonResponse({'msg': 'Invalid cipher text!'})

    text = text.lower()
    d = int(request.POST['d'])
    n = int(request.POST['n'])

    m = 0
    for ch in text:
        if ch == ' ':
            m = (m * 27) % n
        else:
            m = (m * 27 + ord(ch) - ord('a') + 1) % n

    dec = pow(m, d, n)
    text = ''
    while dec:
        mod = dec % 27
        if mod == 0:
            text = ' ' + text
        else:
            text = chr(ord('a') - 1 + mod) + text
        dec = dec // 27
    return JsonResponse({'msg': text})


def xgcd(a, b):
    prevx, x, prevy, y = 1, 0, 0, 1
    while b:
        q = a//b
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, a % b
    return a, prevx, prevy


def generate_keys():
    p = generateLargePrime(128)
    q = generateLargePrime(128)
    n = p * q
    theta_n = (p - 1) * (q - 1)

    e = random.randrange(2, theta_n - 1)
    g, x, y = xgcd(e, theta_n)
    while g != 1:
        e = random.randrange(2, theta_n - 1)
        g, x, y = xgcd(e, theta_n)

    # aka d = modular inverse of e modulo theta_n (d * e = 1 % theta_n)
    d = x % theta_n

    return {
        'private': d,
        'public_n': n,
        'public_e': e
    }


def home(request):
    homepage = loader.get_template('home.html')
    keys = generate_keys()
    return HttpResponse(homepage.render(keys, request))
