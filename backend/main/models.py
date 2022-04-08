from django.db import models


class Category(models.Model):
    CATS = [
        ('comp', 'Kompyuter'),
        ('lang', 'Ingliz tili')
    ]
    name = models.CharField(max_length=255, verbose_name="Yo'nalish nomi")
    slug = models.SlugField(max_length=255, unique=True)
    type = models.CharField(max_length=10, choices=CATS, default="comp", verbose_name="Kurs turi")

    class Meta:
        verbose_name = "Yo'nalish "
        verbose_name_plural = "Yo'nalishlar"

    def __str__(self):
        return f"{self.name} | {self.type}"


class Subject(models.Model):
    title = models.CharField(max_length=255, verbose_name="Oylik reja")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="Mavzular", related_name="mavzular", null=True)
    content = models.TextField(verbose_name="Mavzular ro'yhati", max_length=4090)

    class Meta:
        verbose_name = "Mavzu "
        verbose_name_plural = "Mavzular"

    def __str__(self) -> str:
        return f"{self.title} - {self.course.name}"


class FAQ(models.Model):
    question = models.CharField(max_length=200, verbose_name="Savol")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name="Mavzular", related_name="savollar", null=True)
    answer = models.CharField(max_length=200, verbose_name="Javob")

    class Meta:
        verbose_name = "Savol - javob "
        verbose_name_plural = "Savollar"

    def __str__(self) -> str:
        return f"{self.question} - {self.course.name}"


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kurs nomi")
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="courses", verbose_name="Kurs yo'nalishi")
    image_url = models.URLField(max_length=200, verbose_name="Kurs rasmi (online)")
    price = models.PositiveIntegerField(verbose_name="Kurs narxi (so'm)", default=0)
    content = models.TextField(verbose_name="Kurs haqida ma'lumot", max_length=1020, null=True)
    
    class Meta:
        verbose_name = "Kurs "
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return f"{self.name}"

    
class Teacher(models.Model):
    name = models.CharField(max_length=255, verbose_name="O'qituvchi")
    slug = models.SlugField(max_length=255, unique=True, null=True)
    image_url = models.URLField(max_length=200, verbose_name="O'qituchi rasmi (online)")
    content = models.TextField(verbose_name="O'qituchi haqida ma'lumot", max_length=1020)
    course = models.ForeignKey(Course, on_delete=models.PROTECT,related_name="teachers", verbose_name="Kurs nomi", null=True)

    class Meta:
        verbose_name = "O'qituvchi "
        verbose_name_plural = "O'qituvchilar"

    def __str__(self):
        return f"{self.name} | {self.course}"

    
class User(models.Model):
    full_name = models.CharField(verbose_name="Foydalanuvchi", max_length=100)
    username = models.CharField(verbose_name="Telegram username", max_length=100, null=True)
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', unique=True)
    phone = models.CharField(verbose_name='Telefon', max_length=50, null=True)
    # create = models.DateTimeField(verbose_name="Qo'shilgan vaqt", null=True)

    class Meta:
        verbose_name = "Foydalanuvchi "
        verbose_name_plural = "Foydalanivchilar"

    def __str__(self):
        return f"{self.telegram_id} - {self.full_name}"