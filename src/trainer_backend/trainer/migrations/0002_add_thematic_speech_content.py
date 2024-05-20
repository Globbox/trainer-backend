# Generated by Django 5.0.2 on 2024-09-04 16:58

from django.db import migrations


def add_thematic_speech_content(apps, _):
    """Добавить данные по тематическому контенту."""
    ThematicSpeechContent = apps.get_model(
        'trainer', 'ThematicSpeechContent'
    )

    contents = [
        ('А',
         'Повседневная жизнь семьи. Межличностные отношения в семье, с друзьями и знакомыми. Конфликтные ситуации, их предупреждение и разрешение'),
        ('Б', 'Внешность и характеристика человека, литературного персонажа'),
        ('В',
         'Здоровый образ жизни и забота о здоровье: режим труда и отдыха, спорт, сбалансированное питание, посещение врача. Отказ от вредных привычек'),
        ('Г',
         'Школьное образование, школьная жизнь, школьные праздники. Школьные социальные сети. Переписка с зарубежными сверстниками. Взаимоотношения в школе. Проблемы и решения. Подготовка к выпускным экзаменам'),
        ('Д',
         'Современный мир профессий. Проблема выбора профессии. Альтернативы в продолжении образования'),
        ('Е',
         'Место иностранного языка в повседневной жизни и профессиональной деятельности в современном мире. Роль иностранного языка в планах на будущее'),
        ('Ж',
         'Молодёжь в современном обществе. Ценностные ориентиры. Участие молодёжи в жизни общества. Досуг молодёжи: увлечения и интересы. Любовь и дружба'),
        ('З',
         'Покупки: одежда, обувь и продукты питания. Карманные деньги. Молодёжная мода'),
        ('И',
         'Роль спорта в современной жизни: виды спорта, экстремальный спорт, спортивные соревнования, Олимпийские игры'),
        ('К',
         'Деловое общение: особенности делового общения, деловая этика, деловая переписка, публичное выступление'),
        ('Л',
         'Туризм. Виды отдыха. Экотуризм. Путешествия по России и зарубежным странам. Виртуальные путешествия'),
        ('М',
         'Вселенная и человек. Природа. Проблемы экологии. Защита окружающей среды. Стихийные бедствия. Проживание в городской/сельской местности'),
        ('Н',
         'Средства массовой информации: пресса, телевидение, радио, Интернет, социальные сети'),
        ('О',
         'Технический прогресс: перспективы и последствия. Современные средства коммуникации (пресса, телевидение, Интернет, социальные сети и другие). Интернет-безопасность'),
        ('П', 'Проблемы современной цивилизации'),
        ('Р',
         'Родная страна и страна/страны изучаемого языка: географическое положение, столица, крупные города, регионы; система образования; достопримечательности, культурные особенности (национальные и популярные праздники, знаменательные даты, традиции, обычаи); страницы истории. Россия и мир: вклад России в мировую культуру, науку, технику'),
        ('С',
         'Выдающиеся люди родной страны и страны/стран изучаемого языка: государственные деятели, учёные, писатели, поэты, художники, композиторы, путешественники, спортсмены, актёры и т.д.'),
    ]

    ThematicSpeechContent.objects.all().delete()
    for short_designation, description in contents:
        ThematicSpeechContent.objects.create(
            short_designation=short_designation,
            description=description
        )


class Migration(migrations.Migration):
    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_thematic_speech_content)
    ]
