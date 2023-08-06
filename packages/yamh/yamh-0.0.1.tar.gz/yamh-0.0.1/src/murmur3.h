#ifndef YAMH_MURMUR3_H_
#define YAMH_MURMUR3_H_

#include <cstdint>
#include <string_view>

namespace yamh
{

class murmur3_32
{
public:
    murmur3_32(std::uint32_t seed = 0);

    void update(std::string_view bytes);

    std::uint32_t digest();

private:
    std::size_t processed_;
    std::uint32_t h1_;
    char temp_[4];
    unsigned temp_size_;
};

} // yamh namespace

#endif // YAMH_MURMUR3_H_
