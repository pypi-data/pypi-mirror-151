import json

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


def get_content_type_for_model(obj):
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)


def field_value_to_json(f_value):
    if str(type(f_value)) in [
        "<class 'django.db.models.fields.files.FieldFile'>",
        "<class 'django.db.models.fields.files.ImageFile'>",
        "<class 'django.db.models.fields.files.ImageFieldFile'>",
        "<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>"
    ]:
        value = f_value.name
    elif str(type(f_value)) in [
        "<class 'uuid.UUID'>",
        "<class 'datetime.datetime'>",
        "<class 'datetime.date'>",
        "<class 'bool'>"
    ]:
        value = str(f_value)
    elif 'models' in str(type(f_value)):
        value = f_value.pk
    elif str(type(f_value)) in [
        "<class 'decimal.Decimal'>"
    ]:
        value = str(float(f_value))
    else:
        value = str(f_value)
    return value


def create_addition_log(user_id, oj):
    if not user_id:
        return False
    lg = LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=get_content_type_for_model(oj).pk,
        object_id=oj.pk,
        object_repr=str(oj),
        action_flag=ADDITION,
    )
    # 因为 LogEntry 不会保存具体数据，需要另外将操作涉及的数据存入该条记录中
    addition_message_dict = {
        'addition': {
            'fields': list(),
            'values': list()
        }
    }
    for i in oj._meta.fields:
        fields = i.attname
        value = getattr(oj, fields)
        addition_message_dict['addition']['fields'].append(fields)
        addition_message_dict['addition']['values'].append(field_value_to_json(value))
    addition_message = json.dumps(addition_message_dict, ensure_ascii=False)
    lg.change_message = addition_message
    lg.save()
    return True


def create_change_log(user_id, oj, origin_data, new_data):
    if not user_id:
        return False
    lg = LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=get_content_type_for_model(oj).pk,
        object_id=oj.pk,
        object_repr=str(oj),
        action_flag=CHANGE,
    )
    change_message_dict = {
        'changed': {
            'fields': list(),
            'origin_values': list(),
            'new_values': list(),
        }
    }
    for fields, value in new_data.items():
        origin_value = origin_data.get(fields)
        if value != origin_value and fields in origin_data:
            change_message_dict['changed']['fields'].append(fields)
            change_message_dict['changed']['origin_values'].append(field_value_to_json(origin_value))
            change_message_dict['changed']['new_values'].append(field_value_to_json(value))
    change_message = json.dumps(change_message_dict, ensure_ascii=False)
    lg.change_message = change_message
    lg.save()
    return True


def create_delete_log(user_id, oj):
    if not user_id:
        return False
    lg = LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=get_content_type_for_model(oj).pk,
        object_id=oj.pk,
        object_repr=str(oj),
        action_flag=DELETION,
    )
    # 因为 LogEntry 不会保存具体数据，需要另外将操作涉及的数据存入该条记录中
    delete_message_dict = {
        'delete': {
            'fields': list(),
            'values': list()
        }
    }
    for i in oj._meta.fields:
        fields = i.attname
        value = getattr(oj, fields)
        delete_message_dict['delete']['fields'].append(fields)
        delete_message_dict['delete']['values'].append(field_value_to_json(value))
    delete_message = json.dumps(delete_message_dict, ensure_ascii=False)
    lg.change_message = delete_message
    lg.save()
    return True
