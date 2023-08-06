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
#include "SHTC3_dev.h"

typedef struct
{
    PyObject_HEAD
} THObject;

// python method TH.__init__(self)
static int TH_init(THObject *self, PyObject *args, PyObject *kwds) {
	return 0;
}

// python method TH.start(self)
static PyObject *TH_start(THObject *self, PyObject *args)
{
	int ret = 0;
	PyObject *Opy;

	ret = SHTC3_Open();
	Opy = Py_BuildValue("i", ret);

	return Opy;
}

// python method TH.stop(self)
static PyObject *TH_stop(THObject *self, PyObject *args)
{
	SHTC3_Close();
	Py_RETURN_NONE;
}

// deallocation method
static void TH_dealloc(THObject *self)
{
    Py_TYPE(self)->tp_free((PyObject*)self);
}

// python function TH.reset()
static PyObject *TH_reset(THObject *self, PyObject *args)
{
   SHTC_SOFT_RESET();
   Py_RETURN_NONE;
}

// python function TH.getTem()
static PyObject *TH_getTem(THObject *self, PyObject *args)
{
	float Dtemp = 0.0;
	PyObject *Opy;

	Dtemp = SHTC3_GetTemp();
	Opy = Py_BuildValue("f", Dtemp);

	return Opy;
}

// python function TH.getHum()
static PyObject *TH_getHum(THObject *self, PyObject *args)
{
	float Dhum = 0.0;
	PyObject *Opy;

	Dhum = SHTC3_GetHum();
	Opy = Py_BuildValue("f", Dhum);

	return Opy;
}

static PyMethodDef
TH_methods[] = {
	{"start", (PyCFunction)TH_start, METH_VARARGS, "open sensor dev file"},
	{"stop", (PyCFunction)TH_stop, METH_VARARGS, "close sensor dev file"},	
	{"reset", (PyCFunction)TH_reset, METH_VARARGS, "reset sensor"},	
	{"getTem", (PyCFunction)TH_getTem, METH_VARARGS, "Get temperature"},
	{"getHum", (PyCFunction)TH_getHum, METH_VARARGS, "Get humidity"},
	{NULL, NULL, 0, NULL}
};

PyTypeObject THType = {
   PyVarObject_HEAD_INIT(NULL,0)
   "Starfive.GPIO.TH",        // tp_name
   sizeof(THObject),          // tp_basicsize
   0,                         // tp_itemsize
   (destructor)TH_dealloc,    // tp_dealloc
   0,                         // tp_print
   0,                         // tp_getattr
   0,                         // tp_setattr
   0,                         // tp_compare
   0,                         // tp_repr
   0,                         // tp_as_number
   0,                         // tp_as_sequence
   0,                         // tp_as_mapping
   0,                         // tp_hash
   0,                         // tp_call
   0,                         // tp_str
   0,                         // tp_getattro
   0,                         // tp_setattro
   0,                         // tp_as_buffer
   Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, // tp_flag
   "Class for sense hat",    // tp_doc
   0,                         // tp_traverse
   0,                         // tp_clear
   0,                         // tp_richcompare
   0,                         // tp_weaklistoffset
   0,                         // tp_iter
   0,                         // tp_iternext
   TH_methods,                // tp_methods
   0,                         // tp_members
   0,                         // tp_getset
   0,                         // tp_base
   0,                         // tp_dict
   0,                         // tp_descr_get
   0,                         // tp_descr_set
   0,                         // tp_dictoffset
   (initproc)TH_init,         // tp_init
   0,                         // tp_alloc
   0,                         // tp_new
};

PyTypeObject *TH_init_THType(void)
{
   THType.tp_new = PyType_GenericNew;
   if (PyType_Ready(&THType) < 0)
      return NULL;

   return &THType;
}

