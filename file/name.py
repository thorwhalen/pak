__author__ = 'thorwhalen'

def fileparts(file):
    """

    :param file: a filepath
    :return: the root, name, and extension of the file
    """
    import os.path
    (root, ext) = os.path.splitext(file)
    (x, name) = os.path.split(root)
    if root==name:
        return ('', name, ext)
    else:
        return (root, name, ext)

def fullfile(root,name,ext):
    """

    :param root:
    :param name:
    :param ext:
    :return: the root, name, and extension of the file
    """
    import os.path
    return os.path.join(root,name+ext)

# input: filename
# output: True if the extension (.csv, .tab, or .txt) looks like it might be a delim file
def is_delim_file(dataname):
    from util.coll import ismember
    root,name,ext = fileparts(dataname)
    if ext and ismember(ext,['.csv','.tab','.txt']):
        return True
    else:
        return False

# input: dataname
# output: csv file path for this dataname, if such a file exists, looking for files that have the template
#   data_folder + dataname + csvExtensions
# given the list of csvExtensions (default ['.csv', '.tab', '.txt']) and list of data_folders
# where the list of csvExtensions is traversed in priority, and only if dataname has no extension already
# and the list of data_folders is traversed in second priority, and only if dataname is a simple filename (i.e. has no head path)
#
# Note: If no existing file is found, the function returns an empty string
#
#   if dataname includes an extension which is in csvExtensions
#     dataname
#       and if dataname has no heading path...
#         'csv/' + dataname
#         data_folder + dataname
#         data_folder + '/csv/' + dataname
#   if dataname has no extension
#     dataname + csvExtensions
#       and if dataname has no heading path...
#         'csv/' + dataname + csvExtensions
#         data_folder + dataname + csvExtensions
#         data_folder + '/csv/' + dataname + csvExtensions
def delim_file(dataname,data_folder=['','csv'],csvExtensions=['.csv', '.tab', '.txt']):
    import os.path
    from util.coll import ismember
    # set up lists of folders and extensions we'll be looking through
    root,name,ext = fileparts(dataname)
    if ext and ismember(ext,csvExtensions): # if dataname had a permissable extension
        csvExtensions = [ext]
    if root: # if dataname has a path header (i.e. is specified by a full path)
        data_folder = [root]
    else:
        if isinstance(data_folder,list):
            tail_options = data_folder
            data_folder = ['']
        else:
            tail_options = ['','data','daf']
            data_folder = [data_folder]
        data_folder = [os.path.join(f,t) for f in data_folder for t in tail_options]
        # look through possibilities until a file is found (or not)
    for folder in data_folder:
        for ext in csvExtensions:
            try_filename = fullfile(folder,name,ext)
            if os.path.exists(try_filename):
                return try_filename
    return '' # if no file was found

# input: dataname
# output: file path for this dataname, if such a file exists, looking for files that have the template
#   data_folder + dataname + fileExtensions
# NOTE: Same as delim_file (see this function for more details), but with different fileExtensions defaults
def data_file(dataname,data_folder=['','data','daf'],fileExtensions=['']):
    import os.path
    from util.coll import ismember
    # set up lists of folders and extensions we'll be looking through
    root,name,ext = fileparts(dataname)
    if ext and ismember(ext,fileExtensions): # if dataname had a permissable extension
        fileExtensions = [ext]
    if root: # if dataname has a path header (i.e. is specified by a full path)
        data_folder = [root]
    else:
        if isinstance(data_folder,list):
            tail_options = data_folder
            data_folder = ['']
        else:
            tail_options = ['','data','daf']
            data_folder = [data_folder]
        data_folder = [os.path.join(f,t) for f in data_folder for t in tail_options]
        # look through possibilities until a file is found (or not)
    for folder in data_folder:
        for ext in fileExtensions:
            try_filename = fullfile(folder,name,ext)
            if os.path.exists(try_filename):
                return try_filename
    return '' # if no file was found