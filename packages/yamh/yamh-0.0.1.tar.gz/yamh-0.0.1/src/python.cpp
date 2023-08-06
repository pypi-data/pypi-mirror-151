#include <pybind11/pybind11.h>
#include "murmur3.h"

namespace py = pybind11;

PYBIND11_MODULE(yamh, m)
{
    m.doc() = "A hashing library for murmur v3 with "
        "a similar interface to hashlib";

    py::class_<yamh::murmur3_32>(m, "murmur3_32")
            .def(py::init<std::uint32_t>(), py::arg("seed") = 0)
            .def("update", &yamh::murmur3_32::update)
            .def("digest", &yamh::murmur3_32::digest);
}
