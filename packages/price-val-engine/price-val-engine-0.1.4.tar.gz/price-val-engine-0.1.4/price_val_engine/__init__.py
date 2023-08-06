import price_val_engine

def get_version():
   try:
      return price_val_engine.__version__
   except:
      pass