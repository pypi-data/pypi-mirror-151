#ifndef __SCIHOOK_H_
#define __SCIHOOK_H_

#include <fstream>
#include <iomanip>
#include <type_traits>
#include <limits>
#include <utility>
#include <cmath>
#include <stdexcept>
#include <Python.h>
#include <pybind11/embed.h>
#include <pybind11/stl.h>

namespace py = pybind11;

namespace SciHook
{
    struct SciHookExecutionContext
    {
        std::string name = "SciHookExecutionContext";
        const pybind11::object get_name() const { return pybind11::cast(name); }

        SciHookExecutionContext() {}
        SciHookExecutionContext(std::string name) : name(name) {}
        virtual ~SciHookExecutionContext() = default;
    };

    SciHookExecutionContext create_context(std::string name);

    /**
     * @brief Registers the event as a complex event triggered by the provided list of events.
     * @throws std::invalid_argument If the event to register already exists, or if any of the
     * listed triggering events does not exist.
     * 
     * @param event_name name of the complex event to register.
     * @param triggering_events events (base or complex) triggering the complex event to register.
     */
    void register_complex_event(std::string event_name, std::list<std::string> triggering_events);

    void register_complex_events(std::map<std::string, std::list<std::string>> complex_events);

    /**
     * @brief Registers the event as a base event.
     * @throws std::invalid_argument If the event to register already exists.
     * 
     * @param event_name name of the base event to register.
     */
    size_t register_base_event(std::string event_name);

    std::list<std::string> get_base_events();

    __attribute__((visibility("default")))
    void register_scihook(std::string event_name, py::function scihook);

    __attribute__((visibility("default")))
    void unregister_scihook(std::string event_name, py::function scihook);

    bool has_registered_scihooks(size_t event);

    std::list<py::function> get_registered_scihooks(size_t event);

    void trigger(std::string event_name, std::shared_ptr<SciHookExecutionContext> scope);

    void trigger(size_t event_id, std::shared_ptr<SciHookExecutionContext> scope);

    __attribute__((visibility("default")))
    void initialize_scihook(std::vector<std::string> python_path,
        std::vector<std::string> python_scripts,
        std::string interface_module,
        std::function<void (py::module_)> interface_module_initializer=[](py::module_ m) { });
}
#endif