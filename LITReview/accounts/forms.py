from .models import UserFollows, Ticket
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', min_length=4, max_length=150)
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer mot de passe', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Nom d\'utilisateur existe déjà")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Mots de passe ne corresponde pas")
        return password2

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            None,
            self.cleaned_data['password1']
        )
        return user


class FollowForm(forms.Form):
    followname = forms.CharField(label='Nom d\'utilisateur', min_length=4, max_length=150)
    errors_message = None

    def clean_followname(self):
        followname = self.cleaned_data['followname'].lower()
        r = User.objects.filter(username=followname)
        if not r.count():
            raise ValidationError("Nom d\'utilisateur n'existe pas")
        return followname

    def save(self, username):
        user = User.objects.filter(username=username)[0]
        followname = self.cleaned_data['followname']
        followed_user = User.objects.filter(username=followname)
        if followed_user:
            if UserFollows.objects.filter(user=user, followed_user=followed_user[0]):
                return None
            user_follow = UserFollows(user=user, followed_user=followed_user[0])
            user_follow.save()
            return user_follow


class TicketForm(forms.Form):
    title = forms.CharField(label='Titre', min_length=1, max_length=128)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False)
    image = forms.ImageField(label='Image', required=False)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

    def save(self, username, commit=True):
        user = User.objects.filter(username=username)[0]
        ticket = Ticket(title=self.cleaned_data['title'],
                        description=self.cleaned_data['description'],
                        user=user,
                        image=self.cleaned_data['image']
                        )
        ticket.save(commit)
        return ticket

    def edit(self, ticket):
        image = self.cleaned_data['image']
        if image is None:
            image = ticket.image
        elif image is False:
            Ticket.objects.filter(image=ticket.image)[0].image.delete()
            image = None
        else:
            Ticket.objects.filter(image=ticket.image)[0].image.delete()

        ticket = Ticket(id=ticket.id,
                        title=self.cleaned_data['title'],
                        description=self.cleaned_data['description'],
                        user=ticket.user,
                        image=image,
                        time_created=ticket.time_created
                        )
        ticket.save()
        return ticket
