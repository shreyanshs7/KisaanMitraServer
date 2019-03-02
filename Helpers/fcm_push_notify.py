from pyfcm import FCMNotification
from django.conf import settings

def fcm_push_notify(token, full_name, blood_type):
    push_service = FCMNotification(api_key=FCM_API_KEY)
    registration_id = token
    message_title = "Blood Donation Required"
    message_body = ("%s is requesting blood donation of blood type %s")%(full_name, blood_type)
    push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return True