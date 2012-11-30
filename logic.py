#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    Author:cleverdeng
    E-mail:clverdeng@gmail.com
"""

import cjson
import os, time
import settings

encode_json = cjson.encode
try:
    from PIL import Image
except:
    raise EnvironmentError('Must have the PIL (Python Imaging Library).')

path_exists = os.path.exists
normalize_path = os.path.normpath
absolute_path = os.path.abspath
split_path = os.path.split
split_ext = os.path.splitext

root = settings.BASE_PATH
file_manager_path = settings.FILE_MANAGER_PATH

class CkFinder(object):
    def __init__(self):
        pass


    def dirlist(self, request):
        result =['<ul class="jqueryFileTree" style="display: none;">']
        dir = request.arguments.get('dir', file_manager_path)[0]
        
        try:
            for f_item in os.listdir(root+dir):
                f_sub = os.path.join((root+dir), f_item)
                
                if os.path.isdir(f_sub):
                    result.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (dir + f_item, f_item))
                else:
                    ext = os.path.splitext(f_item)[1][1:]
                    result.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (ext, (dir + f_item), f_item))

            result.append('</ul>')
        except:
            pass

        return ''.join(result)


    def rename(self, old, new):
        result = {}
        try:
            old_full_name = root + old
            old_path, old_name = split_path(old_full_name)
            if os.path.isdir(old_path + "/"):
                old_path += '/'

            newpath = old_path + '/' + new
            os.rename(old_full_name, newpath)
            error_message = new
            success_code = "0"
            if os.path.isdir(newpath+"/"):
                newpath += '/'
        except:
            success_code = "500"
            error_message = "There was an error renaming the file."
        finally:
            result = {
                        "Old Path" : old_path.replace(root, "") + "/",
                        "Old Name" : old_name,
                        "New Path" : split_path(newpath)[0].replace(root, "") + "/",
                        "New Name" : new,
                        "Error" : error_message,
                        "Code" : success_code
                    }

        return encode_json(result)


    def delete(self, path):
        result = {}
        try:
            full_path = root + path
            if os.path.isdir(full_path+"/"):
                if not full_path[-1] == '/':
                    full_path += '/'

            dir_path, name = split_path(full_path)
            os.remove(full_path)
            error_message = name + ' was deleted successfully.'
            success_code = "0"
        except:
            success_code = "500"
            error_message = "There was an error deleting the file. <br/> The operation was either not permitted or it may hav    e already been deleted."
        finally:
            result = {
                        "Path" : full_path.replace(root, ""),
                        "Name" : name,
                        "Error" : error_message,
                        "Code" : success_code
                    }

        return encode_json(result)
        

    def addfolder(self, path, name):
        try:
            full_path = root + path
            name = name.replace(" ", "_")
            new_path = full_path + name + "/"
            if path_exists(full_path):
                os.mkdir(new_path)
                success_code = "0"
                error_message = 'Successfully created folder.'
            else:
                success_code = "500"
                error_message = 'There is no Root Directory.'
        except:
            error_message = 'There was an error creating the directory.'
            success_code = "500"
        finally:
            result = {
                        "Path" : full_path,
                        "Parent" : path,
                        "Name" : name,
                        "New Path" : new_path,
                        "Error" : error_message,
                        "Code" : success_code
                    }

        return encode_json(result)


    def upload(self, path, files):
        file_path = root + path + files[0]["filename"]
        
        with file(file_path, 'wb+') as fd:
            fd.write(files[0]["body"])

        result = {
                    "Name" : files[0]["filename"],
                    "Path" : path,
                    "Code" : "0",
                    "Error" : ""
                }
        return '<textarea>' + encode_json(result) + '</textarea>'


    def get_dir_file(self, path):
        result = {}
        dir_list = os.listdir(root+path)
        for filename in dir_list:
            file_path = path + filename
            info = self.get_info(file_path)
            result[file_path] = info

        return result

    def get_info(self, request_path):
        path = root + request_path
        preview = request_path
        imagetypes = ['.gif','.jpg','.jpeg','.png']
        if os.path.isdir(path):
            thefile = {
                            "Path" : request_path + "/",
                            "Filename" : split_path(path)[-1],
                            "File Type" : split_path(path)[1],
                            "Preview" : 'images/fileicons/_Open.png',
                            "Properties" : {
                                                "Date Created" : '',
                                                "Date Modified" : '',
                                                "Width" : '',
                                                "Height" : '',
                                                "Size" : ''
                                            },
                            "Return" : request_path,
                            "Error" : '',
                            "Code" : 0,
                        }
            thefile["File Type"] = 'Directory'
        else:
            ext = split_ext(path)
            preview = 'images/fileicons/'+ ext[1][1:] + '.png'
            thefile = {
                            "Path" : request_path,
                            "Filename" : split_path(path)[-1],
                            "File Type" : split_path(path)[1][1:],
                            "Preview" : preview,
                            "Properties" : {
                                                "Date Created" : '',
                                                "Date Modified" : '',
                                                "Width" : '',
                                                "Height" : '',
                                                "Size" : ''
                                            },
                            "Return" : request_path,
                            "Error" : '',
                            "Code" : 0
                        }
            if ext[1] in imagetypes:
                try:
                    img = Image.open(open(path,"r"))
                    xsize, ysize = img.size
                    thefile["Properties"]["Width"] = xsize
                    thefile["Properties"]["Height"] = ysize
                    thefile["Preview"] = request_path
                except:
                    preview = 'images/fileicons/'+ ext[1][1:] + '.png'
                    thefile["Preview"] = preview

            thefile["File Type"] = os.path.splitext(path)[1][1:]
            thefile["Properties"]["Date Created"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(path))) 
            thefile["Properties"]["Date Modified"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path)))
            thefile["Properties"]["Size"] = os.path.getsize(path)
        
        return thefile
