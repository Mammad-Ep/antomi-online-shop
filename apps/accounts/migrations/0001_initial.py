# Generated by Django 3.2.11 on 2024-04-13 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('mobile_number', models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')),
                ('name', models.CharField(max_length=30, null=True, verbose_name='نام')),
                ('family', models.CharField(max_length=50, null=True, verbose_name='نام خانوادگی')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='ایمیل')),
                ('gender', models.CharField(blank=True, choices=[('man', 'مرد'), ('female', 'زن')], default='man', max_length=50, null=True, verbose_name='جنسیت')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
                ('is_admin', models.BooleanField(default=False, verbose_name='کاربر ادمین/معمولی')),
                ('active_code', models.CharField(blank=True, max_length=7, null=True, verbose_name='کد تایید')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, null=True, verbose_name='تلفن ثابت')),
                ('postal_code', models.CharField(max_length=10, null=True, verbose_name='کدپستی')),
                ('address', models.CharField(max_length=500, null=True, verbose_name='آدرس')),
                ('image_name', models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='عکس پروفایل')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر/مشتری')),
            ],
            options={
                'verbose_name': 'مشتری',
                'verbose_name_plural': 'مشتری ها',
            },
        ),
    ]
