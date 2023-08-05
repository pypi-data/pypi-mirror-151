import copy
from decimal import Decimal

from django.db.models import ManyToManyField, DateField, TimeField, ForeignKey, DateTimeField
from django_filters.rest_framework import FilterSet
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, \
    CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .response import APIResponse
from .log import create_addition_log, create_change_log, create_delete_log


class AiitFilter(FilterSet):

    @classmethod
    def filter_for_field(cls, field, field_name, lookup_expr='exact'):
        filter_class = super().filter_for_field(field, field_name, lookup_expr)
        if lookup_expr == 'exact':
            filter_class.extra['help_text'] = '{0}等于'.format(field.verbose_name)
        elif lookup_expr == 'contains':
            filter_class.extra['help_text'] = '{0}包含'.format(field.verbose_name)
        elif lookup_expr == 'gte':
            filter_class.extra['help_text'] = '{0}大于等于'.format(field.verbose_name)
        elif lookup_expr == 'gt':
            filter_class.extra['help_text'] = '{0}大于'.format(field.verbose_name)
        elif lookup_expr == 'lt':
            filter_class.extra['help_text'] = '{0}小于'.format(field.verbose_name)
        elif lookup_expr == 'lte':
            filter_class.extra['help_text'] = '{0}小于等于'.format(field.verbose_name)
        return filter_class


def convert_obj_to_dict(obj, fields=None, exclude=None):
    """
    将 Model 对象 obj 转化为字典格式返回
    :param obj: 通过 model.objects.filter().first() 、model.objects.get() 或者 for i in QuerySet 获取的对象
    :param fields: 要选择性呈现的字段
    :param exclude: 排除呈现的字段
    :return: 返回字典 {'id': 1, 'field1': 'field1_data'}
    """
    data = {}
    for f in getattr(obj, '_meta').concrete_fields + getattr(obj, '_meta').many_to_many:
        value = f.value_from_object(obj)

        if fields and f.name not in fields:
            continue

        if exclude and f.name in exclude:
            continue

        if isinstance(f, ManyToManyField):
            value = [i.id for i in value] if obj.pk else None

        elif isinstance(f, DateTimeField):
            value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

        elif isinstance(f, DateField):
            value = value.strftime('%Y-%m-%d') if value else None

        elif isinstance(f, TimeField):
            value = value.strftime('%H:%M:%S') if value else None

        elif isinstance(f, Decimal):
            value = float(f)

        # ForeignKey 特殊处理
        if isinstance(f, ForeignKey):
            data[f.column] = value
            data[f.name] = value
        else:
            data[f.name] = value

    # 获取 property 里面的数据
    for p in getattr(getattr(obj, '_meta'), '_property_names'):
        value = getattr(obj, p)
        if isinstance(value, (str, int, Decimal)):
            data[p] = value
    return data


def obj_list(self):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return APIResponse(serializer.data)


def obj_create(self, request):
    new_data = copy.deepcopy(request.data)
    request_user = request.user
    user_id = None
    if request_user:
        user_id = request_user.id
        if user_id:
            new_data['created_by'] = user_id
            new_data['updated_by'] = user_id
    serializer = self.get_serializer(data=new_data)
    serializer.is_valid(raise_exception=True)
    oj = serializer.save()
    create_addition_log(user_id=user_id, oj=oj)
    headers = self.get_success_headers(serializer.data)
    return APIResponse(serializer.data, headers=headers)


def obj_retrieve(self):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return APIResponse(data=serializer.data)


def obj_update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    origin_data = convert_obj_to_dict(instance)
    new_data = copy.deepcopy(request.data)
    request_user = request.user
    user_id = None
    if request_user:
        user_id = request_user.id
        if user_id:
            user_id = user_id
            new_data['updated_by'] = request_user.id
    serializer = self.get_serializer(instance, data=new_data, partial=partial)
    serializer.is_valid(raise_exception=True)
    oj = serializer.save()
    create_change_log(user_id, oj, origin_data, new_data)

    if getattr(instance, '_prefetched_objects_cache', None):
        instance._prefetched_objects_cache = {}

    return APIResponse(data=serializer.data)


def obj_delete(self, request):
    instance = self.get_object()
    request_user = request.user
    user_id = None
    if request_user:
        user_id = request_user.id
    create_delete_log(user_id, oj=instance)
    self.perform_destroy(instance)
    return APIResponse(status=204)


class AiitListAPIView(ListAPIView):

    def list(self, request, *args, **kwargs):
        return obj_list(self)


class AiitCreateAPIView(CreateAPIView):

    def create(self, request, *args, **kwargs):
        return obj_create(self, request)


class AiitListCreateAPIView(ListCreateAPIView):

    def list(self, request, *args, **kwargs):
        return obj_list(self)

    def create(self, request, *args, **kwargs):
        return obj_create(self, request)


class AiitRetrieveAPIView(RetrieveAPIView):
    filter_backends = []

    def retrieve(self, request, *args, **kwargs):
        return obj_retrieve(self)


class AiitRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    filter_backends = []

    def retrieve(self, request, *args, **kwargs):
        return obj_retrieve(self)

    def update(self, request, *args, **kwargs):
        return obj_update(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class AiitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    filter_backends = []

    def retrieve(self, request, *args, **kwargs):
        return obj_retrieve(self)

    def update(self, request, *args, **kwargs):
        return obj_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return obj_delete(self, request)

    def post(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
