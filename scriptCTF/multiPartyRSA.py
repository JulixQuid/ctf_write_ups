from math import gcd
from functools import reduce

def chinese_remainder(n, a):
    """Chinese Remainder Theorem solver"""
    sum = 0
    prod = reduce(lambda x, y: x*y, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * inverse_mod(p, n_i) * p
    return sum % prod

def inverse_mod(a, m):
    """Modular inverse using extended Euclidean algorithm"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def nth_root(x, n):
    """Find integer nth root"""
    high = 1
    while high ** n < x:
        high *= 2
    low = high // 2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

def decrypt_multi_rsa(encrypted_messages, moduli, e):
    """
    Decrypt a message encrypted with multiple RSA keys with small exponent
    
    Args:
        encrypted_messages: list of ciphertexts (c₁, c₂, ..., cₖ)
        moduli: list of RSA moduli (N₁, N₂, ..., Nₖ)
        e: the public exponent (must be small, e.g., 3 or 5)
        
    Returns:
        The decrypted message as bytes
    """
    # Verify we have enough ciphertexts
    if len(encrypted_messages) < e:
        raise ValueError(f"Need at least {e} ciphertexts for exponent {e}")
    
    # Solve using CRT
    result = chinese_remainder(moduli, encrypted_messages)
    
    # Take the e-th root to recover the message
    m = nth_root(result, e)
    
    # Convert to bytes
    return int_to_bytes(m)

def int_to_bytes(x):
    """Convert integer to bytes"""
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def bytes_to_int(b):
    """Convert bytes to integer"""
    return int.from_bytes(b, 'big')

# Example usage
if __name__ == "__main__":
    # Example with e=3 and 3 different RSA keys
    e = 3
    
    # Moduli (N values) for 3 different RSA public keys
    moduli = [
        156503881374173899106040027210320626006530930815116631795516553916547375688556673985142242828597628615920973708595994675661662789752600109906259326160805121029243681236938272723595463141696217880136400102526509149966767717309801293569923237158596968679754520209177602882862180528522927242280121868961697240587,
        81176790394812943895417667822424503891538103661290067749746811244149927293880771403600643202454602366489650358459283710738177024118857784526124643798095463427793912529729517724613501628957072457149015941596656959113353794192041220905793823162933257702459236541137457227898063370534472564804125139395000655909,
        140612513823906625290578950857303904693579488575072876654320011261621692347864140784716666929156719735696270348892475443744858844360080415632704363751274666498790051438616664967359811895773995052063222050631573888071188619609300034534118393135291537302821893141204544943440866238800133993600817014789308510399
    ]
    
    # Encrypt with each key (in real attack, we only have ciphertexts)
    ciphertexts = [
        77845730447898247683281609913423107803974192483879771538601656664815266655476695261695401337124553851404038028413156487834500306455909128563474382527072827288203275942719998719612346322196694263967769165807133288612193509523277795556658877046100866328789163922952483990512216199556692553605487824176112568965,
        40787486105407063933087059717827107329565540104154871338902977389136976706405321232356479461501507502072366720712449240185342528262578445532244098369654742284814175079411915848114327880144883620517336793165329893295685773515696260299308407612535992098605156822281687718904414533480149775329948085800726089284,
        100744134973371882529524399965586539315832009564780881084353677824875367744381226140488591354751113977457961062275480984708865578896869353244823264759044617432862876208706282555040444253921290103354489356742706959370396360754029015494871561563778937571686573716714202098622688982817598258563381656498389039630

    ]
    
    # Attack: Recover message from ciphertexts without private keys
    try:
        recovered_msg = decrypt_multi_rsa(ciphertexts, moduli, e)
        print("Recovered message:", recovered_msg)
        print("Success:",  recovered_msg)
    except ValueError as e:
        print("Error:", e)