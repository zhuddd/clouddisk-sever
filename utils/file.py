import os

from pay.models import UserOrders
from sever import settings


def set_file_user(user_id, p, tree: dict):
    """
    设置文件树
    :param user_id:  用户id
    :param p:  父文件夹id
    :param tree:  文件树
    :return:    包含文件id的文件树
    """
    from file.models import FileUser
    r = {}
    name = tree.get("name", None)
    type = tree.get("type", None)
    children = tree.get("children", [])
    if name is None or type is None or children is None:
        return r
    is_folder = True if type == "folder" else False
    try:
        f = FileUser.objects.create(user_id=user_id, file_name=name, file_type=type, parent_folder=p,
                                    is_folder=is_folder, is_uploaded=is_folder)
        r[tree.get("uid")] = f.id
        for i in range(len(children)):
            new_list = set_file_user(user_id, f.id, tree["children"][i])
            r.update(new_list)
        return r
    except:
        return r


def get_file_from_model(file_hash, check_hash, size):
    """
    通过文件的md5值获取文件
    :param file_hash: 文件的md5值
    :param check_hash: 校验值
    :param size: 文件的大小
    :return: 文件
    """
    from file.models import Files
    try:
        return Files.objects.filter(hash=file_hash, check_hash=check_hash, size=size)[0]
    except:
        return Files.objects.create(hash=file_hash, check_hash=check_hash, size=size, broken=True)


def check_file(file_hash):
    """
    检查文件是否存在和完整
    :param file_hash:
    :return:
    """
    path = settings.STATIC_FILES_DIR_FILE / file_hash
    if os.path.exists(path):
        with open(path, 'rb') as f:
            import hashlib
            m = hashlib.sha256()
            m.update(f.read())
            return m.hexdigest() == file_hash
    return False


def get_file_hash_file(file, key=""):
    """
    获取文件的md5值
    :param file: 文件
    :param key: md5值的key
    :return: md5值
    """
    import hashlib
    m = hashlib.sha256(key.encode())
    m.update(file)
    return m.hexdigest()


def get_user_file_by_id(user_id, file_id):
    from file.models import FileUser
    try:
        return FileUser.objects.get(user_id=user_id, id=file_id, is_delete=False, is_uploaded=True)
    except Exception as e:
        print(e)
        return None


def get_user_tree_by_id(user_id, file_id):
    from file.models import FileUser
    try:
        file = FileUser.objects.get(user_id=user_id, id=file_id, is_delete=False, is_uploaded=True).tree_dict()
        if file["is_folder"]:
            file["children"] = []
            for i in FileUser.objects.filter(user_id=user_id, parent_folder=file_id, is_delete=False, is_uploaded=True):
                file["children"].append(get_user_tree_by_id(user_id, i.id))
        return file
    except Exception as e:
        print(e)
        return None


def get_file_user_list(user_id,find_type, msg ):
    from file.models import FileUser
    try:
        if find_type == 0:
            data = FileUser.objects.filter(user_id=user_id, parent_folder=int(msg), is_delete=False,
                                           is_uploaded=True)
            return [i.dict() for i in data]
        elif find_type == 1:
            data = FileUser.objects.filter(user_id=user_id, file_name__icontains=msg, is_delete=False, is_uploaded=True)
            return [i.dict() for i in data]
    except Exception as e:
        print(e)
        return []


def file_copy(user_id, file_id, parent_folder):
    from file.models import FileUser
    try:
        file = FileUser.objects.get(id=file_id, is_delete=False, is_uploaded=True)
        usedSize = getUsedStorage(user_id)
        totalSize = gettotalSize(user_id)
        size = file.file.size if file.file else 0
        if usedSize + size > totalSize:
            return 0
        new_file = FileUser.objects.create(file_face=file.file_face, file_name=file.file_name, file_type=file.file_type,
                                           parent_folder=parent_folder, is_folder=file.is_folder, file_id=file.file_id,
                                           user_id=user_id,
                                           is_uploaded=True)
        if file.is_folder:
            for i in FileUser.objects.filter(parent_folder=file_id, is_delete=False,
                                             is_uploaded=True):
                code = file_copy(user_id, i.id, new_file.id)
                if code in [0, -1]:
                    return code
        return 1
    except Exception as e:
        print(e)
        return -1


def file_delete(user_id, file_id):
    from file.models import FileUser
    try:
        file = FileUser.objects.get(user_id=user_id, id=file_id, is_delete=False, is_uploaded=True)
        file.is_delete = True
        file.save()
        if file.is_folder:
            for i in FileUser.objects.filter(user_id=user_id, parent_folder=file_id, is_delete=False,
                                             is_uploaded=True):
                file_delete(user_id, i.id)
        return True
    except Exception as e:
        print(e)
        return False


def getUsedStorage(user_id):
    from file.models import FileUser
    from django.db.models import Sum
    try:
        used = FileUser.objects.filter(user_id=user_id, is_delete=False, is_uploaded=True).aggregate(
            size=Sum('file__size'))["size"]
        return used if used else 0
    except Exception as e:
        print(e)
        return 0


def gettotalSize(user_id):
    from account.models import User
    from datetime import datetime
    try:
        now = datetime.now()
        default = User.objects.get(id=user_id).total_size
        orders = UserOrders.objects.filter(user_id=user_id, is_pay=True, valid_time__gte=now, is_valid=True)
        for i in orders:
            default += i.menu.storage_size * i.menu.storage_unit
        return default
    except Exception as e:
        print(e)
        return 0
