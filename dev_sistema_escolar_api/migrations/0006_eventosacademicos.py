from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dev_sistema_escolar_api', '0005_alter_administradores_update_alter_alumnos_update_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventosAcademicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_evento', models.CharField(max_length=255)),
                ('tipo_evento', models.CharField(choices=[('Conferencia', 'Conferencia'), ('Taller', 'Taller'), ('Seminario', 'Seminario'), ('Concurso', 'Concurso')], max_length=20)),
                ('fecha_realizacion', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('lugar', models.CharField(max_length=255)),
                ('publico_objetivo', models.JSONField(default=list)),
                ('programa_educativo', models.CharField(blank=True, max_length=80, null=True)),
                ('descripcion_breve', models.TextField(max_length=300)),
                ('cupo_maximo', models.PositiveSmallIntegerField()),
                ('creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('update', models.DateTimeField(auto_now=True, null=True)),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='eventos_responsable', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

