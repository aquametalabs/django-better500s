
def exception_string():
    import traceback
    import sys
    return '\n'.join(traceback.format_exception(*sys.exc_info()))
    
def print_exception():
    print "######################## Exception #############################"
    print exception_string()
    print "################################################################"