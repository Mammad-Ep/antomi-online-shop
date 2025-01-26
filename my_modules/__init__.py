from pathlib import Path
import os
from django.conf import settings
from django.contrib import admin
from django.urls import path,include,re_path,reverse
from urllib.parse import urlencode
from django.conf.urls.static import static
from django.shortcuts import render,redirect,get_object_or_404
from django.template import loader
from django.template.loader import render_to_string

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,EmailMultiAlternatives
from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,PermissionsMixin,BaseUserManager,UserManager
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory,formset_factory
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.apps import AppConfig
from django.contrib.auth.admin import UserAdmin
from django.test import TestCase
from django.db.models import Q,Count,Min,Max,Avg,Sum
from django.http import (Http404,HttpRequest,HttpResponse,HttpResponseBadRequest,JsonResponse,
                         HttpResponseForbidden,HttpResponseNotFound,HttpResponseRedirect,HttpResponsePermanentRedirect,
                         HttpResponseServerError)
from django.core.paginator import Paginator
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from datetime import datetime
import django_filters

from django.views import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.utils.html import html_safe,mark_safe

from django.core import serializers
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description,order_field
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core import validators

import uuid
import requests
import json
import random



