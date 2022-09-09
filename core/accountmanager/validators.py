from accountmanager.models import User


def validate_user_role(mobile):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        user=User.objects.get(mobile=mobile)
        if user.is_user:
            return False
        return True
    except ObjectDoesNotExist:
        return True
    
        
def validate_mobile(mobile):
    if len(mobile) != 10:
        return False
    return True


def validate_user_otp(data):
    if len(data['mobile'])==12 and len(data['otp'])==6:
        return True
    else:
        return False


# def uploadto_AWS(path, uploaded_by, category=None):
#     s3 = boto3.client('s3', aws_access_key_id = 'AKIAJWSTVWT7F67VCMGQ',  aws_secret_access_key = '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',config=Config(signature_version='s3v4'))
#     s3.upload_file(path, AWS_STORAGE_BUCKET_NAME, 'media/documents/'+name,ExtraArgs = {
#                 'ACL': 'public-read', 
#                 'ContentType': 'image/png', 
#                 'ContentDisposition': 'inline'
#             })
#     upload = Uploads.objects.create(id=uuid.uuid4(),name=name,
# 								self_link=generate_self_link(AWS_STORAGE_BUCKET_NAME, name),
# 								category=category, uploaded_by=uploaded_by, group=None)
#     print("uploaded to aws")
#     return {
# 		'self_link': upload.self_link
# 	}