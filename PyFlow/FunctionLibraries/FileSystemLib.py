# -*- coding: utf-8 -*-
from ..Core.FunctionLibrary import *
from ..Core.AGraphCommon import *
import os
from Qt.QtWidgets import QFileDialog


class FileSystemLib(FunctionLibraryBase):
    '''
    Default library builting stuff, variable types and conversions
    '''
    def __init__(self):
        super(FileSystemLib, self).__init__()


    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0),nodeType=NodeTypes.Callable, meta={'Category': 'FileSystem', 'Keywords': ["get","pick","folder"]})
    ## Pick a folder from Dialog
    def pickFolder():
        '''Pick a folder from Dialog'''    
        return str(QFileDialog.getExistingDirectory(None, "Select Directory"))
      

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## Return a normalized absolutized version of the pathname path.
    def abspath(path=(DataTypes.String, "")):
        '''Return a normalized absolutized version of the pathname path. On most platforms, this is equivalent to calling the function normpath()'''      
        return os.path.abspath(path)      

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system).
    def realpath(path=(DataTypes.String, "")):
        '''Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system).'''      
        return os.path.realpath(path) 

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## Return the base name of pathname path. This is the second element of the pair returned by passing path to the function split(). Note that the result of this function is different from the Unix basename program; where basename for '/foo/bar/' returns 'bar', the basename() function returns an empty string ('')
    def basename(path=(DataTypes.String, "")):
        '''Return the base name of pathname path. This is the second element of the pair returned by passing path to the function split(). Note that the result of this function is different from the Unix basename program; where basename for '/foo/bar/' returns 'bar', the basename() function returns an empty string ('')'''      
        return os.path.basename(path)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## Normalize the case of a pathname. On Unix and Mac OS X, this returns the path unchanged; on case-insensitive filesystems, it converts the path to lowercase. On Windows, it also converts forward slashes to backward slashes.
    def normcase(path=(DataTypes.String, "")):
        '''Normalize the case of a pathname. On Unix and Mac OS X, this returns the path unchanged; on case-insensitive filesystems, it converts the path to lowercase. On Windows, it also converts forward slashes to backward slashes.'''      
        return os.path.normcase(path)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B. This string manipulation may change the meaning of a path that contains symbolic links. On Windows, it converts forward slashes to backward slashes. To normalize case, use normcase().
    def normpath(path=(DataTypes.String, "")):
        '''Normalize a pathname by collapsing redundant separators and up-level references so that A//B, A/B/, A/./B and A/foo/../B all become A/B. This string manipulation may change the meaning of a path that contains symbolic links. On Windows, it converts forward slashes to backward slashes. To normalize case, use normcase().'''      
        return os.path.normpath(path)   

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## Return the directory name of pathname path.
    def dirname(path=(DataTypes.String, "")):
        '''Return the directory name of pathname path.'''      
        return os.path.dirname(path)        
        
    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user’s home directory.
    def expanduser(path=(DataTypes.String, "")):
        '''On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user’s home directory.

On Unix, an initial ~ is replaced by the environment variable HOME if it is set; otherwise the current user’s home directory is looked up in the password directory through the built-in module pwd. An initial ~user is looked up directly in the password directory.

On Windows, HOME and USERPROFILE will be used if set, otherwise a combination of HOMEPATH and HOMEDRIVE will be used. An initial ~user is handled by stripping the last directory component from the created user path derived above.

If the expansion fails or if the path does not begin with a tilde, the path is returned unchanged.'''      
        return os.path.expanduser(path)       

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.String, 0), meta={'Category': 'FileSystem', 'Keywords': ["file","folder"]})
    ## Return the argument with environment variables expanded.
    def expandvars(path=(DataTypes.String, "")):
        '''Return the argument with environment variables expanded. Substrings of the form $name or ${name} are replaced by the value of environment variable name. Malformed variable names and references to non-existing variables are left unchanged.

On Windows, %name% expansions are supported in addition to $name and ${name}.'''      
        return os.path.expandvars(path)         

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, 0), meta={'Category': 'FileSystem', 'Keywords': ["test","file","folder"]})
    ## Return True if path refers to an existing path. Returns False for broken symbolic links. On some platforms, this function may return False if permission is not granted to execute os.stat() on the requested file, even if the path physically exists.
    def exists(path=(DataTypes.String, "")):
        '''Return True if path refers to an existing path. Returns False for broken symbolic links. On some platforms, this function may return False if permission is not granted to execute os.stat() on the requested file, even if the path physically exists.'''      
        return os.path.exists(path)  

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, 0), meta={'Category': 'FileSystem', 'Keywords': ["test","folder","Directory","dir"]})
    ## Return True if path is an existing directory. This follows symbolic links, so both islink() and isdir() can be true for the same path.
    def isDir(path=(DataTypes.String, "")):
        '''Return True if path is an existing directory. This follows symbolic links, so both islink() and isdir() can be true for the same path.'''      
        return os.path.isdir(path)

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, 0), meta={'Category': 'FileSystem', 'Keywords': ["test","file"]})
    ## Return True if path is an existing regular file. This follows symbolic links, so both islink() and isfile() can be true for the same path.
    def isFile(path=(DataTypes.String, "")):
        '''Return True if path is an existing regular file. This follows symbolic links, so both islink() and isfile() can be true for the same path.'''      
        return os.path.isFile(path) 

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, 0), meta={'Category': 'FileSystem', 'Keywords': ["test","file"]})
    ## Return True if path refers to a directory entry that is a symbolic link. Always False if symbolic links are not supported by the Python runtime.
    def islink(path=(DataTypes.String, "")):
        '''Return True if path refers to a directory entry that is a symbolic link. Always False if symbolic links are not supported by the Python runtime.'''      
        return os.path.islink(path) 

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, 0), meta={'Category': 'FileSystem', 'Keywords': ["test","file"]})
    ## Return True if path is an absolute pathname. On Unix, that means it begins with a slash, on Windows that it begins with a (back)slash after chopping off a potential drive letter.
    def isabs(path=(DataTypes.String, "")):
        '''Return True if path is an absolute pathname. On Unix, that means it begins with a slash, on Windows that it begins with a (back)slash after chopping off a potential drive letter.'''      
        return os.path.isabs(path)       

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, 0), meta={'Category': 'FileSystem', 'Keywords': ["test","file"]})
    ## Return True if pathname path is a mount point: a point in a file system where a different file system has been mounted. The function checks whether path’s parent, path/.., is on a different device than path, or whether path/.. and path point to the same i-node on the same device — this should detect mount points for all Unix and POSIX variants.
    def ismount(path=(DataTypes.String, "")):
        '''Return True if pathname path is a mount point: a point in a file system where a different file system has been mounted. The function checks whether path’s parent, path/.., is on a different device than path, or whether path/.. and path point to the same i-node on the same device — this should detect mount points for all Unix and POSIX variants.'''      
        return os.path.ismount(path)            

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Bool, 0), meta={'Category': 'FileSystem', 'Keywords': ["test","file"]})
    ## Return True if both pathname arguments refer to the same file or directory (as indicated by device number and i-node number).
    def samefile(path=(DataTypes.String, ""),path2=(DataTypes.String, "")):
        '''Return True if both pathname arguments refer to the same file or directory (as indicated by device number and i-node number).'''      
        return os.path.samefile(path,path2) 

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0), meta={'Category': 'FileSystem', 'Keywords': ["time","file"]})
    ## Return the time of last access of path.
    def getatime(path=(DataTypes.String, "")):
        '''Return the time of last access of path.'''      
        return os.path.getatime(path)     

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0), meta={'Category': 'FileSystem', 'Keywords': ["time","file"]})
    ## Return the time of last access of path.
    def getmtime(path=(DataTypes.String, "")):
        '''Return the time of last access of path.'''      
        return os.path.getmtime(path,path2)     

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Float, 0), meta={'Category': 'FileSystem', 'Keywords': ["time","file"]})
    ## Return the system’s ctime which, on some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time for path.
    def getctime(path=(DataTypes.String, "")):
        '''Return the system’s ctime which, on some systems (like Unix) is the time of the last metadata change, and, on others (like Windows), is the creation time for path.'''      
        return os.path.getctime(path,path2)       

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Int, 0), meta={'Category': 'FileSystem', 'Keywords': ["size","file"]})
    ## Return the size, in bytes, of path.
    def getsize(path=(DataTypes.String, "")):
        '''Return the size, in bytes, of path.'''      
        return os.path.getctime(path,path2)                

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["get","folder","dir","Directory"]})
    ## Lists directories on Path
    def getFolders(path=(DataTypes.String, "")):
        '''Lists directories on Path'''      
        return [os.path.join(path,x) for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))]

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["get","File","dir","Directory"]})
    ## Lists files  on Path
    def getFiles(path=(DataTypes.String, "")):
        '''Lists files on Path'''      
        return [os.path.join(path,x) for x in os.listdir(path) if os.path.isfile(os.path.join(path,x))]

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["get","folder","file","Directory","dir"]})
    ## Lists files and directories on Path
    def listDir(path=(DataTypes.String, "")):
        '''Lists files and directories on Path'''      
        return [os.path.join(path,x) for x in os.listdir(path)]

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["get","folder","file","Directory","dir"]})
    ## Lists files and directories on Path recursive
    def walk(path=(DataTypes.String, ""),topdown=(DataTypes.Bool, False)):
        '''Lists files and directories on Path recursive'''  
        paths = []
        for root, dirs, files in os.walk(path, topdown=topdown):
           for name in files:
              paths.append(os.path.join(root, name))
           for name in dirs:
              paths.append(os.path.join(root, name))
        return paths

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["file"]})
    ## Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that. The tail part will never contain a slash; if path ends in a slash, tail will be empty. If there is no slash in path, head will be empty. If path is empty, both head and tail are empty. Trailing slashes are stripped from head unless it is the root (one or more slashes only). In all cases, join(head, tail) returns a path to the same location as path (but the strings may differ). Also see the functions dirname() and basename().
    def split(path=(DataTypes.String, "")):
        '''Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that. The tail part will never contain a slash; if path ends in a slash, tail will be empty. If there is no slash in path, head will be empty. If path is empty, both head and tail are empty. Trailing slashes are stripped from head unless it is the root (one or more slashes only). In all cases, join(head, tail) returns a path to the same location as path (but the strings may differ). Also see the functions dirname() and basename().'''      
        return list(os.path.split(path))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["file"]})
    ## Split the pathname path into a pair (drive, tail) where drive is either a drive specification or the empty string. On systems which do not use drive specifications, drive will always be the empty string. In all cases, drive + tail will be the same as path.
    def splitdrive(path=(DataTypes.String, "")):
        '''Split the pathname path into a pair (drive, tail) where drive is either a drive specification or the empty string. On systems which do not use drive specifications, drive will always be the empty string. In all cases, drive + tail will be the same as path.'''      
        return list(os.path.splitdrive(path)   )

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["file"]})
    ## Split the pathname path into a pair (root, ext) such that root + ext == path, and ext is empty or begins with a period and contains at most one period. Leading periods on the basename are ignored; splitext('.cshrc') returns ('.cshrc', '').
    def splitext(path=(DataTypes.String, "")):
        '''Split the pathname path into a pair (root, ext) such that root + ext == path, and ext is empty or begins with a period and contains at most one period. Leading periods on the basename are ignored; splitext('.cshrc') returns ('.cshrc', '').'''
        return list(os.path.splitext(path)   )

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["file"]})
    ## Split the pathname path into a pair (unc, rest) so that unc is the UNC mount point (such as r'\\host\mount'), if present, and rest the rest of the path (such as r'\path\file.ext'). For paths containing drive letters, unc will always be the empty string.
    def splitunc(path=(DataTypes.String, "")):
        '''Split the pathname path into a pair (unc, rest) so that unc is the UNC mount point (such as r'\\host\mount'), if present, and rest the rest of the path (such as r'\path\file.ext'). For paths containing drive letters, unc will always be the empty string.'''
        return list(os.path.splitunc(path))

    @staticmethod
    @IMPLEMENT_NODE(returns=(DataTypes.Array, []), meta={'Category': 'FileSystem', 'Keywords': ["file"]})
    ## Split the pathname path into a pair (unc, rest) so that unc is the UNC mount point (such as r'\\host\mount'), if present, and rest the rest of the path (such as r'\path\file.ext'). For paths containing drive letters, unc will always be the empty string.
    def splitunc(path=(DataTypes.String, "")):
        '''Split the pathname path into a pair (unc, rest) so that unc is the UNC mount point (such as r'\\host\mount'), if present, and rest the rest of the path (such as r'\path\file.ext'). For paths containing drive letters, unc will always be the empty string.'''
        return list(os.path.splitunc(path))