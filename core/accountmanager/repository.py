

""" get object """
def get_object(modelName, key):
    return modelName.objects.get(**key)

"""Filter queryset"""
def filter_attribute(modelName, filterKeys):
    return modelName.objects.filter(**filterKeys)
    
"""Authenticate access token"""
def authenticate_token(modelName, access_token):
    return modelName.objects.filter(access_token=access_token)

"""Authenticate admin"""
def authenticate_admin(modelName, user_id):
    return modelName.objects.filter(id=user_id)



"""Update"""
def update(modelName, filterKeys, updateWithData):
    # updateWith.update({'updated_at':datetime.datetime.now()})
    return modelName.objects.filter(**filterKeys).update(**updateWithData) 

"""Fetch all"""
def fetch_all(modelName):
    return modelName.objects.all()

""" Create"""
def store(modelName, data):
    return modelName.objects.create(**data)

""" Delete"""
def delete(modelName, filterKeys):
    return modelName.objects.filter(**filterKeys).delete()

def filter_with_values(modelName, filterKeys):
    return modelName.objects.filter(**filterKeys).values()

""" check is exists """
def is_exists(modelName, filterKeys):
    return modelName.objects.filter(**filterKeys).exists()

""" check object count """
def obj_count(modelName, filterKeys):
    return modelName.objects.filter(**filterKeys).count()

