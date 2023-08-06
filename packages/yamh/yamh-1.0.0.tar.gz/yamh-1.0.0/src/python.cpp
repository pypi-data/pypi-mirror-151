#include <pybind11/pybind11.h>
#include <iostream>
#include "murmur3.h"

namespace py = pybind11;

namespace pybind11
{

namespace detail
{

template <>
struct type_caster<std::string_view> : public string_caster<std::string_view, true>
{
public:
    /// Custom string view loader from memory handle
    bool load(handle src, bool x)
    {
        if (PyMemoryView_Check(src.ptr()))
        {
            auto buffer = PyMemoryView_GET_BUFFER(src.ptr());
            value = std::string_view(reinterpret_cast<const char *>(buffer->buf),
                buffer->len);
        }
        else if (PyByteArray_Check(src.ptr()))
        {
            value = std::string_view(
                PyByteArray_AsString(src.ptr()),
                PyByteArray_Size(src.ptr()));
        }
        else
            return string_caster<std::string_view, true>::load(src, x);

        return !PyErr_Occurred();
    }
};

} // detail namespace

} // pybind11 namespace

PYBIND11_MODULE(yamh, m)
{
    m.doc() = "A hashing library for murmur v3 with "
        "a similar interface to hashlib";

    py::class_<yamh::murmur3_32>(m, "murmur3_32")
            .def(py::init<std::uint32_t>(), py::arg("seed") = 0)
            .def("update", &yamh::murmur3_32::update)
            .def("digest", &yamh::murmur3_32::digest);
}
