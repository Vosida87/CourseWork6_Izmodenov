from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from blog.models import Blog
from django.utils.text import slugify


class BlogCreateView(CreateView):
    """
    Создание блога
    """
    model = Blog
    fields = ('title', 'content')
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.owner = self.request.user
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """
    Редактирование блога
    """
    model = Blog
    fields = ('title', 'content')
    # success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog_view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    """
    Отображение блогов
    """
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    """
    Информация о блоге
    """
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    """
    Удаление блога
    """
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
