import sys
log_performance = len(sys.argv) == 2 and sys.argv[1] == '--perf'
def log(x):
    if log_performance:
        sys.stdout.write(x)

def fib0(n):
    result = _fib0(n)
    log('0\n')
    return result
def _fib0(n):
    log('.')
    if n <= 1:
        return n
    return _fib0(n - 1) + _fib0(n - 2)
assert fib0(6) == 8
log('\n')

def fib1(n):
    result = _fib1(n, 0, 1)
    log('1\n')
    return result
def _fib1(n, a, b):
    log('.')
    if n == 0:
        return a
    return _fib1(n - 1, b, a + b)
assert fib0(10) == fib1(10)
log('\n')

def fib2(n):
    a, b = 0, 1
    for _ in xrange(n):
        log('.')
        a, b = b, a + b
    log('2\n')
    return a
assert fib1(100) == fib2(100)
log('\n')

def fib3(n):
    fib_n = transform_power(fib_transform, n)
    log('3\n')
    result = apply_transform(fib_n, (0, 1))
    return result[0]
fib_transform = ((0, 1), (1, 1))
def apply_transform(((a, b), (c, d)), (x, y)):
    return (x * a + y * b, x * c + y * d)
def compose_transforms(t, ((a, b), (c, d))):
    aa, cc = apply_transform(t, (a, c))
    bb, dd = apply_transform(t, (b, d))
    return ((aa, bb), (cc, dd))
def transform_power(a, n):
    log('.')
    if n == 0:
        return identity
    if n % 2 == 1:
        return compose_transforms(transform_power(a, n - 1), a)
    return transform_power(compose_transforms(a, a), n / 2)
identity = ((1, 0), (0, 1))
assert fib2(1000) == fib3(1000)
log('\n')
print fib3(10000)
fib3(100000)
#fib2(1000000) # haha nope

def fib4(n):
    result = phi_ring_power(phi_val, n)
    log('4\n')
    return result[1]
# Our representation is (a, b) -> (a + sqrt(5)*b) / 2
phi_val = (1, 1)
def phi_ring_mul((a, b), (c, d)):
    return ((a * c + 5 * b * d) / 2, (a * d + b * c) / 2)
def phi_ring_power(a, n):
    log('.')
    if n == 0:
        return ring_identity
    if n % 2 == 1:
        return phi_ring_mul(phi_ring_power(a, n - 1), a)
    return phi_ring_power(phi_ring_mul(a, a), n / 2)
ring_identity = (2, 0)

for i in xrange(10):
    print phi_ring_power(phi_val, i)
import time
t = time.time(); fib4(1000000); t1 = time.time(); log("%f\n" % (t1 - t))
t = time.time(); fib3(1000000); t1 = time.time(); log("%f\n" % (t1 - t))
