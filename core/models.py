from django.db import models


# Обычная модель с полями
class Customer(models.Model):
    first_name = models.CharField('имя', max_length=255)
    last_name = models.CharField('фамилия', max_length=255)
    email = models.EmailField('почта', blank=True, null=True)
    year_of_birth = models.IntegerField('год рождения')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# -----------------------Примеры по связям--------------------------------

# ForeignKey

class Category(models.Model):
    name = models.CharField('название', max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=200)
    category = models.ForeignKey(
        Category,
        verbose_name='категории',
        related_name='products',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# рекурсивные отношения ForeignKey

class Tree(models.Model):
    name = models.CharField('название узла', max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return self.name


# Many-to-many (обычный пример)

class Tag(models.Model):
    name = models.CharField('название тега', max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('название статьи', max_length=200)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


'''
    Пример:
    Создаем корневой узел
    root = Tree.objects.create(name="Корень")
    
    Создаем дочерний узел
    child = Tree.objects.create(name="Дочерний узел", parent=root)
    
    Создаем потомок
    grandchild = Tree.objects.create(name="Потомственный узел", parent=child)
'''


# рекурсивные отношения Many-to-many

class CategoryProd(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ManyToManyField('self', blank=True, null=True, related_name='children')

    def __str__(self):
        return self.name

'''
    Создание категорий
    electronics = Category.objects.create(name="Электроника")
    books = Category.objects.create(name="Книги")
    home_goods = Category.objects.create(name="Товары для дома")
    
    Установление отношений родительства
    electronics.children.add(books, home_goods)
    
    Получение всех дочерних категорий для Electronics
    print(electronics.children.all())
    
    Получение всех родительских категорий для Books
    print(books.parent.filter(children__id=books.id).first())
'''


# пример где используется промежуточная модель для связи многие ко многим

class Book(models.Model):
    title = models.CharField('', max_length=200)
    authors = models.CharField('', max_length=500)

    def __str__(self):
        return self.title


class Reader(models.Model):
    name = models.CharField('', max_length=100)

    def __str__(self):
        return self.name


class Loan(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE)
    reader = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE)
    loan_date = models.DateField('дата взятия', auto_now_add=True)
    due_date = models.DateField('дата возврата')
    purpose_of_taking = models.CharField('цель взятия книги', max_length=255)

    def __str__(self):
        return f"{self.book.title} ({self.reader.name})"


'''
    Пример создание связи:
    Создаем книгу
    book = Book.objects.create(title="Война и мир", authors="Лев Толстой")
    
    Создаем читателя
    reader = Reader.objects.create(name="Иван Иванов")
    
    Создаем заимствование
    loan = Loan.objects.create(book=book, reader=reader, due_date="2024-12-12")
'''


# One-to-one

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField('информация', blank=True)
    birth_date = models.DateField('дата рождения', null=True, blank=True)

    def __str__(self):
        return self.user.username


'''
    Пример:
    Создаем пользователя
    user = User.objects.create_user(username='admin', email='admin@gmail.com', password='root')
    
    Создаем профиль пользователя
    profile = UserProfile(user=user, bio="Информация о себе", birth_date="2000-01-01")
    profile.save()
'''


# рекурсивные отношения One-to-one
# пример демонстрирует иерархую отделов

class Department(models.Model):
    name = models.CharField('название', max_length=255)
    parent_department = models.OneToOneField('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


''' 
    Пример:
    Создаем корневой отдел
    root_department = Department.objects.create(name="HR")
    
    Создаем дочерний отдел
    child_department = Department.objects.create(name="Рекрутеры", parent_department=root_department)
'''


# --------------------------Наследование моделей--------------------------------

# Абстрактные базовые классы

# Meta наследование

# Определяем абстрактный базовый класс предметов библеотеки с базовыми атрибутами


class LibraryItem(models.Model):
    title = models.CharField('название', max_length=200)
    author = models.CharField('автор', max_length=200)
    status = models.CharField('статус', max_length=20, choices=[('available', 'Доступно'), ('borrowed', 'Занято')],
                              default='available')

    class Meta:
        abstract = True
        ordering = ['title']


class Booknew(LibraryItem):
    publication_year = models.IntegerField('год публикации')

    class Meta(LibraryItem.Meta):
        verbose_name_plural = "книги"


class Magazine(LibraryItem):
    issue_date = models.DateField('дата выпуска')

    class Meta(LibraryItem.Meta):
        verbose_name_plural = "журналы"


class Dvd(LibraryItem):
    director = models.CharField('режисер', max_length=100)

    class Meta(LibraryItem.Meta):
        verbose_name_plural = "DVD"


# Multi-table наследование

class Vehicle(models.Model):
    model = models.CharField('модель', max_length=50)
    year = models.IntegerField()


class Car(Vehicle):
    doors = models.IntegerField('кол-во дверей')
    has_trunk = models.BooleanField('есть ли богажник', default=True)


# Прокси-модели

class OrderItem(models.Model):
    product_or_service = models.CharField('продукт или услуга', max_length=50)
    description = models.TextField('описание')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('количество')

    def __str__(self):
        return f"{self.product_or_service} - {self.description}"


class DetailedOrderItem(OrderItem):
    class Meta:
        proxy = True

    def calculate_total_with_tax(self):
        tax_rate = 0.20  # налог
        total_before_tax = self.price * self.quantity
        total_with_tax = total_before_tax + (total_before_tax * tax_rate)
        return total_with_tax


'''
    Пример:
    detailed_order_item = DetailedOrderItem.objects.create(
    product_or_service="Коробка",
    description="Стеклянная коробка",
    price=100,
    quantity=2
    )

    print(detailed_order_item.calculate_total_with_tax()) 
'''


# множественное наследование

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Custom(models.Model):
    custom_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)


class UserProfiles(User, Custom):
    pass
