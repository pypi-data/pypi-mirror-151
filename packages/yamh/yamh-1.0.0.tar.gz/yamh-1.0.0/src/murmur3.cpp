#include "murmur3.h"
#include <cassert>
#include "intmem.h"

#ifdef _MSC_VER

#include <stdlib.h>

#endif // _MSC_VER

namespace
{

const std::uint32_t c1 = 0xcc9e2d51;
const std::uint32_t c2 = 0x1b873593;

inline std::uint32_t rotl32(std::uint32_t x, std::int8_t r)
{
#ifdef _MSC_VER

    return _rotl(x, y)

#else // _MSC_VER

    return (x << r) | (x >> (32 - r));

#endif // ! _MSC_VER
}

inline std::uint32_t fmix32(std::uint32_t h)
{
    h ^= h >> 16;
    h *= 0x85ebca6b;
    h ^= h >> 13;
    h *= 0xc2b2ae35;
    h ^= h >> 16;

    return h;
}

inline std::uint32_t process_block(const std::string_view &view, std::uint32_t h1)
{
    assert(view.size() >= 4);

    auto k1 = intmem::loadu_le<std::uint32_t>(view.data());

    k1 *= c1;
    k1 = rotl32(k1, 15);
    k1 *= c2;

    h1 ^= k1;
    h1 = rotl32(h1, 13);
    return h1 * 5 + 0xe6546b64;
}

} // Private namespace

namespace yamh
{

murmur3_32::murmur3_32(std::uint32_t seed)
: processed_(0),
  h1_(seed),
  temp_size_(0)
{
}

void murmur3_32::update(std::string_view bytes)
{
    if (bytes.size() + temp_size_ < sizeof(std::uint32_t))
    {
        std::copy(bytes.begin(), bytes.end(), temp_ + temp_size_);
        temp_size_ += bytes.size();
        return;
    }

    if (temp_size_)
    {
        auto remaining = sizeof(temp_) - temp_size_;
        std::copy(bytes.begin(), bytes.begin() + remaining, temp_ + temp_size_);
        bytes.remove_prefix(remaining);

        h1_ = process_block(std::string_view(temp_, temp_size_), h1_);
        processed_ += 4;
    }

    while (bytes.size() >= sizeof(std::uint32_t))
    {
        h1_ = process_block(bytes, h1_);
        bytes.remove_prefix(sizeof(std::uint32_t));
        processed_ += 4;
    }

    if (bytes.size())
    {
        std::copy(bytes.begin(), bytes.end(), temp_);
        temp_size_ = bytes.size();
    }
}

std::uint32_t murmur3_32::digest()
{
    const uint8_t *tail = reinterpret_cast<const std::uint8_t *>(temp_);

    uint32_t retval = h1_;
    if (temp_size_)
    {
        processed_ += temp_size_;
        for (unsigned n = temp_size_; n < sizeof(std::uint32_t); ++n)
            temp_[n] = 0;

        auto k1 = intmem::loadu_le<std::uint32_t>(temp_);
        k1 *= c1;
        k1 = rotl32(k1, 15);
        k1 *= c2;
        retval ^= k1;
    }

    retval ^= processed_;
    return fmix32(retval);
}

} // yamh namespace
