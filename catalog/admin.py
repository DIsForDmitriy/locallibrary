from django.contrib import admin

from catalog.models import Author, Book, BookInstanse, Genre, Lang

admin.site.register(Genre)
admin.site.register(Lang)

class BooksInline(admin.TabularInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [
        BooksInline,
        ]
admin.site.register(Author, AuthorAdmin)


class BookInstanseAdmin(admin.ModelAdmin):
    list_display = ('book', 'due_back', 'status', 'id', 'borrower')
    list_filter = ('due_back', 'status')
    fieldsets = (
        ('Info', {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(BookInstanse, BookInstanseAdmin)

class BooksInstanseInline(admin.TabularInline):
    model = BookInstanse
    extra = 0


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [
        BooksInstanseInline,
        ]

admin.site.register(Book, BookAdmin)





