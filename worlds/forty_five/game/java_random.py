"""
Replicates java.util.Random (LCG) exactly, since Kotlin's Random(seed) wraps it.
Also provides PermaSaveState.runRandom() and Kotlin range-extension equivalents.
"""

_MULTIPLIER = 0x5DEECE66D
_ADDEND = 0xB
_MASK = (1 << 48) - 1


class JavaRandom:
    def __init__(self, seed: int) -> None:
        self._seed = (seed ^ _MULTIPLIER) & _MASK

    def _next(self, bits: int) -> int:
        self._seed = (self._seed * _MULTIPLIER + _ADDEND) & _MASK
        return self._seed >> (48 - bits)

    def next_int(self, n: int | None = None) -> int:
        if n is None:
            return self._next(32)
        if n <= 0:
            raise ValueError("n must be positive")
        if n & (n - 1) == 0:
            return (n * self._next(31)) >> 31
        while True:
            bits = self._next(31)
            val = bits % n
            if bits - val + (n - 1) >= 0:
                return val

    def next_long(self) -> int:
        hi = self._next(32)
        lo = self._next(32)
        # Java: ((long)(int)hi << 32) + (int)lo — both halves are sign-extended as 32-bit ints
        if hi >= (1 << 31):
            hi -= (1 << 32)
        if lo >= (1 << 31):
            lo -= (1 << 32)
        return (hi << 32) + lo

    def next_float(self) -> float:
        return self._next(24) / (1 << 24)

    def next_double(self) -> float:
        return ((self._next(26) << 27) + self._next(27)) / float(1 << 53)

    def next_boolean(self) -> bool:
        return self._next(1) != 0


def int_range_random(lo: int, hi: int, rnd: JavaRandom) -> int:
    """Kotlin: rnd.nextInt(lo..hi)  →  lo + nextInt(hi - lo + 1)"""
    return lo + rnd.next_int(hi - lo + 1)


def float_range_random(lo: float, hi: float, rnd: JavaRandom) -> float:
    """Kotlin: rnd.nextDouble() * (hi - lo) + lo"""
    return rnd.next_double() * (hi - lo) + lo


def run_random(current_random: int, i: int) -> int:
    """
    Replicates PermaSaveState.runRandom(i):
        val random = Random(currentRandom)
        repeat(i) { random.nextLong() }
        return random.nextLong()
    Road seeds: road1 = run_random(seed, 1), road2 = run_random(seed, 2), road3 = run_random(seed, 3)
    """
    rnd = JavaRandom(current_random)
    for _ in range(i):
        rnd.next_long()
    return rnd.next_long()