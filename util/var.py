__author__ = 'thorwhalen'


def my_to_list(x):
    """
    to_list(x) blah blah returns [x] if x is not already a list, and x itself if it's already a list
    Use: This is useful when a function expects a list, but you want to also input a single element without putting this
    this element in a list
    """
    print isinstance(x,list)
    if not isinstance(x,list): x = [x]
    return x

if __name__=="__main__":
    print to_list('asdf')

