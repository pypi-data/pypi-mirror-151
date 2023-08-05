// License:MIT
/*
 * SPI testing utility (using spidev driver)
 *
 * Copyright (c) 2025  Starfive, Inc.
 * Author: lousl
 *
 */

#include "Python.h"
#include "spi_dev.h"

static const char moduledocstring[] = "SPI functionality of a VisionFive1 using Python";



static PyObject *py_spi_transfer(PyObject *self, PyObject *args)
{

	   int			 i      = 0;
	   int			 retval = 0;
	   char           *data  = NULL;
	   unsigned char  datalen = 0;
	   PyObject      *p     = NULL;


	   //get Item count
	   datalen = PyTuple_Size(args);
	   if(datalen <= 0 || datalen > 255){
		   PyErr_SetString(PyExc_RuntimeError, "SPI Transfer input error");
		   return 0;
	   }
	   printf("data len is:%d\n",datalen);
	   data = malloc(sizeof(int) * datalen);
	   if(data == NULL){
		   PyErr_SetString(PyExc_RuntimeError, "SPI Transfer data malloc failed");
		   return 0;
	   }

	   memset(data, 0, datalen);



	   //Parse every data
	   for(i=0; i<datalen; i++){
		   p = PyTuple_GetItem(args, i);
		   if(p == NULL){
			   PyErr_SetString(PyExc_RuntimeError, "get input data  failed");
			   return 0;
		   }
		   if(!PyArg_Parse(p, "i", &data[i])){
		   		PyErr_SetString(PyExc_RuntimeError, "args Parse failed");
		   		return 0;
		   	}
	   }
	   retval = spi_transfer(data, datalen);
	   if(retval < 0){
		   PyErr_SetString(PyExc_RuntimeError, "SPI Transfer failed");
		   return 0;
	   }
	   return Py_BuildValue("i", retval);

}

static PyObject *py_spi_setmode(PyObject *self, PyObject *args)
{
	int mode   = 0;
	int speed  = 0;
	int bits   = 0;
	int retval = 0;

	if(!PyArg_ParseTuple(args, "iii", &speed, &mode, &bits)){
		PyErr_SetString(PyExc_RuntimeError, "args Parse failed");
		return 0;
	}
    retval = spi_setmode(speed, mode, bits);
    if(retval < 0){
    	PyErr_SetString(PyExc_RuntimeError, "args Parse failed");
		return 0;
    }
    return Py_BuildValue("i", retval);
}


PyMethodDef vfpi_spi_methods[] = {
   {"setmode",  py_spi_setmode,  METH_VARARGS, "set spi every mode, including work mode, BITS_PER_WORD, MAX_SPEED."},
   {"transfer", (PyCFunction)py_spi_transfer, METH_VARARGS, "write data to spi device, or read data from spi device"},
   {NULL, NULL, METH_NOARGS, NULL}
};

#if PY_MAJOR_VERSION > 2
static struct PyModuleDef vfispimodule = {
   PyModuleDef_HEAD_INIT,
   "vfPi",      // name of module
   moduledocstring,  // module documentation, may be NULL
   -1,               // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
   vfpi_spi_methods
};
#endif

#if PY_MAJOR_VERSION > 2
PyMODINIT_FUNC PyInit_vfPi(void)
#else
PyMODINIT_FUNC init_vfPi(void)
#endif
{
	PyObject *module;

#if PY_MAJOR_VERSION > 2
   module = PyModule_Create(&vfispimodule);
   if(module == NULL){
	   return NULL;
   }
#else
   module = Py_InitModule3("vfpi", vfpi_spi_methods, moduledocstring);
   if (module == NULL){
	   return NULL;
  }
#endif


#if PY_MAJOR_VERSION > 2
   return module;
#else
  return;
#endif
}
