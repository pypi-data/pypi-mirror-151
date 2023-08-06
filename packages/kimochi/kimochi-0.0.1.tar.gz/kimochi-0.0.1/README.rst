Kimochi
==================

Easy to use python library for showing your emotions.

Key Features
------------
- Modern Pythonic Interface
- Easy to use


Installing
----------

**Python 3.8 or higher**

To install the library, run the following command

.. code:: sh

  #Linux/macOS
  python3 -m pip install -U git+https://github.com/VarMonke/kimochi
  #Windows
  py -m pip install -U git+https://github.com/VarMonke/kimochi


Quick Example
-------------
  
.. code:: py
  
  import asyncio
  import kimochi
  
  client = kimochi.Client()
  async def kiss():
      return await client.kiss

 print(asyncio.run(kiss()))
.. code:: sh
  <Kiss url: https://cdn.otakugifs.xyz/gifs/kiss/a07b3bcb00751dae.gif>

 
