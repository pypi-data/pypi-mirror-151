/*
Copyright (c) 2022-2027 Starfive

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include "Python.h"
#include "c_gpio.h"
#include "py_constants.h"
#include "py_sense.h"


// python function cleanup(gpioport=None)
static PyObject *py_cleanup(PyObject *self, PyObject *args, PyObject *kwargs)
{
   int i;
   int gpiocount = -666;
   int found = 0;
   int gpioport = -666;
   unsigned int gpiooffset;
   PyObject *gpiolist = NULL;
   PyObject *gpiotuple = NULL;
   PyObject *tempobj;
   static char *kwlist[] = {"gpioport", NULL};

   if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|O", kwlist, &gpiolist))
      return NULL;

   if (gpiolist == NULL) {  // gpioport kwarg not set
      // do nothing
#if PY_MAJOR_VERSION > 2
   } else if (PyLong_Check(gpiolist)) {
      gpioport = (int)PyLong_AsLong(gpiolist);
//#else
//   } else if (PyInt_Check(gpiolist)) {
//      gpioport = (int)PyInt_AsLong(gpiolist);
#endif
      if (PyErr_Occurred())
         return NULL;
      gpiolist = NULL;
   } else if (PyList_Check(gpiolist)) {
      gpiocount = PyList_Size(gpiolist);
   } else if (PyTuple_Check(gpiolist)) {
      gpiotuple = gpiolist;
      gpiolist = NULL;
      gpiocount = PyTuple_Size(gpiotuple);
   } else {
      // raise exception
      PyErr_SetString(PyExc_ValueError, "Channel must be an integer or list/tuple of integers");
      return NULL;
   }

  if (gpioport == -666 && gpiocount == -666) {   // gpioport not set - cleanup everything

     // set everything back to input
     for (i=0; i<54; i++) {
        if (gpio_direction[i] != -1) {
           setup_gpio(i, INPUT, PUD_OFF);
           gpio_direction[i] = -1;
           found = 1;
        }
     }
  } else if (gpioport != -666) {    // gpioport was an int indicating single gpioport
     if (get_gpio_offset(gpioport, &gpiooffset))
        return NULL;
     cleanup_one(gpioport, &found);
  } else {  // gpioport was a list/tuple
     for (i=0; i<gpiocount; i++) {
        if (gpiolist) {
           if ((tempobj = PyList_GetItem(gpiolist, i)) == NULL) {
              return NULL;
           }
        } else { // assume gpiotuple
           if ((tempobj = PyTuple_GetItem(gpiotuple, i)) == NULL) {
              return NULL;
           }
        }

#if PY_MAJOR_VERSION > 2
        if (PyLong_Check(tempobj)) {
           gpioport = (int)PyLong_AsLong(tempobj);
//#else
//            if (PyInt_Check(tempobj)) {
//               gpioport = (int)PyInt_AsLong(tempobj);
#endif
           if (PyErr_Occurred())
              return NULL;
        } else {
           PyErr_SetString(PyExc_ValueError, "Channel must be an integer");
           return NULL;
        }

        if (get_gpio_offset(gpioport, &gpiooffset))
           return NULL;
        cleanup_one(gpioport, &found);
     }
  }


   // check if any gpioports set up - if not warn about misuse of GPIO.cleanup()
   if (!found ) {
      PyErr_WarnEx(NULL, "No gpioports have been set up yet - nothing to clean up!  Try cleaning up at the end of your program instead!", 1);
   }

   Py_RETURN_NONE;
}

// python function setup(GPIO port(s), direction, pull_up_down=PUD_OFF, initial=None)
static PyObject *py_setup_gpioport(PyObject *self, PyObject *args, PyObject *kwargs)
{
   int gpioport = -1;
   int direction;
   int i, gpiocount;
   PyObject *gpiolist = NULL;
   PyObject *gpiotuple = NULL;
   PyObject *tempobj;
   int pud = PUD_OFF;
   int initial = -1;
   static char *kwlist[] = {"gpioport", "direction", "pull_up_down", "initial", NULL};

   if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Oi|ii", kwlist, &gpiolist, &direction, &pud, &initial))
      return NULL;

#if PY_MAJOR_VERSION > 2
   if (PyLong_Check(gpiolist)) {
      gpioport = (int)PyLong_AsLong(gpiolist);
//#else
//   if (PyInt_Check(gpiolist)) {
//      gpioport = (int)PyInt_AsLong(gpiolist);
#endif
      if (PyErr_Occurred())
         return NULL;
      gpiolist = NULL;
   } else if (PyList_Check(gpiolist)) {
      // do nothing
   } else if (PyTuple_Check(gpiolist)) {
      gpiotuple = gpiolist;
      gpiolist = NULL;
   } else {
      // raise exception
      PyErr_SetString(PyExc_ValueError, "Channel must be an integer or list/tuple of integers");
      return NULL;
   }

   if (direction != INPUT && direction != OUTPUT) {
      PyErr_SetString(PyExc_ValueError, "An invalid direction was passed to setup()");
      return 0;
   }

   if (direction == OUTPUT && pud != PUD_OFF) {
      PyErr_SetString(PyExc_ValueError, "pull_up_down parameter is not valid for outputs");
      return 0;
   }

   if (direction == INPUT && initial != -1) {
      PyErr_SetString(PyExc_ValueError, "initial parameter is not valid for inputs");
      return 0;
   }

   if (pud != PUD_OFF && pud != PUD_DOWN && pud != PUD_UP) {
      PyErr_SetString(PyExc_ValueError, "Invalid value for pull_up_down - should be either PUD_OFF, PUD_UP or PUD_DOWN");
      return NULL;
   }

   if (gpiolist) {
       gpiocount = PyList_Size(gpiolist);
   } else if (gpiotuple) {
       gpiocount = PyTuple_Size(gpiotuple);
   } else {
       if (!setup_one(gpioport, direction, initial))
          return NULL;
       Py_RETURN_NONE;
   }

   for (i=0; i<gpiocount; i++) {
      if (gpiolist) {
         if ((tempobj = PyList_GetItem(gpiolist, i)) == NULL) {
            return NULL;
         }
      } else { // assume gpiotuple
         if ((tempobj = PyTuple_GetItem(gpiotuple, i)) == NULL) {
            return NULL;
         }
      }

#if PY_MAJOR_VERSION > 2
      if (PyLong_Check(tempobj)) {
         gpioport = (int)PyLong_AsLong(tempobj);
//#else
//      if (PyInt_Check(tempobj)) {
//         gpioport = (int)PyInt_AsLong(tempobj);
#endif
         if (PyErr_Occurred())
             return NULL;
      } else {
          PyErr_SetString(PyExc_ValueError, "Channel must be an integer");
          return NULL;
      }

      if (!setup_one(gpioport, direction, initial))
         return NULL;
   }

   Py_RETURN_NONE;
}

// python function output_py(gpioport(s), value(s))
static PyObject *py_output_gpio(PyObject *self, PyObject *args)
{
   int gpioport = -1;
   int value = -1;
   int i;
   int gpiocount = -1;
   int valuecount = -1;   
   PyObject *gpiolist = NULL;
   PyObject *valuelist = NULL;
   PyObject *gpiotuple = NULL;
   PyObject *valuetuple = NULL;
   PyObject *tempobj = NULL;


   if (!PyArg_ParseTuple(args, "OO", &gpiolist, &valuelist))
       return NULL;

#if PY_MAJOR_VERSION >= 3
   if (PyLong_Check(gpiolist)) {
      gpioport = (int)PyLong_AsLong(gpiolist);
//#else
//   if (PyInt_Check(gpiolist)) {
//      gpioport = (int)PyInt_AsLong(gpiolist);
#endif
      if (PyErr_Occurred())
         return NULL;
      gpiolist = NULL;
   } else if (PyList_Check(gpiolist)) {
      // do nothing
   } else if (PyTuple_Check(gpiolist)) {
      gpiotuple = gpiolist;
      gpiolist = NULL;
   } else {
       PyErr_SetString(PyExc_ValueError, "Channel must be an integer or list/tuple of integers");
       return NULL;
   }

#if PY_MAJOR_VERSION >= 3
   if (PyLong_Check(valuelist)) {
       value = (int)PyLong_AsLong(valuelist);
//#else
//   if (PyInt_Check(valuelist)) {
//       value = (int)PyInt_AsLong(valuelist);
#endif
      if (PyErr_Occurred())
         return NULL;
       valuelist = NULL;
   } else if (PyList_Check(valuelist)) {
      // do nothing
   } else if (PyTuple_Check(valuelist)) {
      valuetuple = valuelist;
      valuelist = NULL;
   } else {
       PyErr_SetString(PyExc_ValueError, "Value must be an integer/boolean or a list/tuple of integers/booleans");
       return NULL;
   }

   if (gpiolist)
       gpiocount = PyList_Size(gpiolist);
   if (gpiotuple)
       gpiocount = PyTuple_Size(gpiotuple);
   if (valuelist)
       valuecount = PyList_Size(valuelist);
   if (valuetuple)
       valuecount = PyTuple_Size(valuetuple);
   if ((gpiocount != -1 && gpiocount != valuecount && valuecount != -1) || (gpiocount == -1 && valuecount != -1)) {
       PyErr_SetString(PyExc_RuntimeError, "Number of gpioports != number of values");
       return NULL;
   }

   if (gpiocount == -1) {
      if (!output_py(gpioport, value))
         return NULL;
      Py_RETURN_NONE;
   }

   for (i=0; i<gpiocount; i++) {
      // get gpioport number
      if (gpiolist) {
         if ((tempobj = PyList_GetItem(gpiolist, i)) == NULL) {
            return NULL;
         }
      } else { // assume gpiotuple
         if ((tempobj = PyTuple_GetItem(gpiotuple, i)) == NULL) {
            return NULL;
         }
      }

#if PY_MAJOR_VERSION >= 3
      if (PyLong_Check(tempobj)) {
         gpioport = (int)PyLong_AsLong(tempobj);
//#else
//      if (PyInt_Check(tempobj)) {
//         gpioport = (int)PyInt_AsLong(tempobj);
#endif
         if (PyErr_Occurred())
             return NULL;
      } else {
          PyErr_SetString(PyExc_ValueError, "Channel must be an integer");
          return NULL;
      }

      // get value
      if (valuecount > 0) {
          if (valuelist) {
             if ((tempobj = PyList_GetItem(valuelist, i)) == NULL) {
                return NULL;
             }
          } else { // assume valuetuple
             if ((tempobj = PyTuple_GetItem(valuetuple, i)) == NULL) {
                return NULL;
             }
          }
#if PY_MAJOR_VERSION >= 3
          if (PyLong_Check(tempobj)) {
             value = (int)PyLong_AsLong(tempobj);
//#else
//          if (PyInt_Check(tempobj)) {
//             value = (int)PyInt_AsLong(tempobj);
#endif
             if (PyErr_Occurred())
                 return NULL;
          } else {
              PyErr_SetString(PyExc_ValueError, "Value must be an integer or boolean");
              return NULL;
          }
      }
      if (!output_py(gpioport, value))
         return NULL;
   }

   Py_RETURN_NONE;
}

// python function value = input_py(gpioport)
static PyObject *py_input_gpio(PyObject *self, PyObject *args)
{
   int gpioport;
   unsigned int gpiooffset;
   PyObject *value;

   if (!PyArg_ParseTuple(args, "i", &gpioport))
      return NULL;

   if (get_gpio_offset(gpioport, &gpiooffset))
       return NULL;

   // check gpioport is set up as an input or output
   if (gpio_direction[gpioport] != INPUT && gpio_direction[gpioport] != OUTPUT)
   {
      PyErr_SetString(PyExc_RuntimeError, "You must setup() the GPIO gpioport first");
      return NULL;
   }

   if (input_py(gpioport)) {
      value = Py_BuildValue("i", HIGH);
   } else {
      value = Py_BuildValue("i", LOW);
   }
   return value;
}


static const char moduledocstring[] = "Python GPIO module for starfive";

PyMethodDef sfv_gpio_methods[] = {
	{"setup", (PyCFunction)py_setup_gpioport, METH_VARARGS | METH_KEYWORDS, "Set up a GPIO gpioport or list of gpioports with a direction and (optional) pull/up down control\ngpioport        - either board pin number or BCM number depending on which mode is set.\ndirection      - IN or OUT\n[pull_up_down] - PUD_OFF (default), PUD_UP or PUD_DOWN\n[initial]      - Initial value for an output gpioport"},
	{"cleanup", (PyCFunction)py_cleanup, METH_VARARGS | METH_KEYWORDS, "Clean up by resetting all GPIO gpioports that have been used by this program to INPUT with no pullup/pulldown and no event detection\n[gpioport] - individual gpioport or list/tuple of gpioports to clean up.  Default - clean every gpioport that has been used."},
	{"output", py_output_gpio, METH_VARARGS, "Output to a GPIO gpioport or list of gpioports\ngpioport - either board pin number or BCM number depending on which mode is set.\nvalue   - 0/1 or False/True or LOW/HIGH"},
	{"input", py_input_gpio, METH_VARARGS, "Input from a GPIO gpioport.	Returns HIGH=1=True or LOW=0=False\ngpioport - either board pin number or BCM number depending on which mode is set."},
	{NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef sfvgpiomodule = {
   PyModuleDef_HEAD_INIT,
   "Starfive._GPIO",      // name of module
   moduledocstring,
   -1,
   sfv_gpio_methods
};
#endif

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit__GPIO(void)
#else
PyMODINIT_FUNC init_GPIO(void)
#endif
{
   int i;
   PyObject *module = NULL;

#if PY_MAJOR_VERSION > 2
   if ((module = PyModule_Create(&sfvgpiomodule)) == NULL)
      return NULL;
#else
   if ((module = Py_InitModule3("Starfive._GPIO", sfv_gpio_methods, moduledocstring)) == NULL)
      return;
#endif

   define_py_constants(module);

   for (i=0; i<54; i++)
      gpio_direction[i] = -1;

   // Add TH class
   if (TH_init_THType() == NULL)
#if PY_MAJOR_VERSION > 2
      return NULL;
#else
      return;
#endif
   Py_INCREF(&THType);
   PyModule_AddObject(module, "TH", (PyObject*)&THType);

#if PY_MAJOR_VERSION > 2
   return module;
#else
   return;
#endif
}
