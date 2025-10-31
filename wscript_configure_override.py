from waflib.Configure import conf

@conf
def find_msvc(self, *k, **kw):
    # Completely disable MSVC detection
    return False

