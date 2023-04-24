from .models import UserFollows, Ticket, Review
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur',
                               widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'}),
                               min_length=4,
                               max_length=150
                               )
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(label='Confirmer mot de passe',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer Mot de passe'})
                                )

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

    def clean_followname(self):
        followname = self.cleaned_data['followname'].lower()
        r = User.objects.filter(username=followname)
        if not r.count():
            raise ValidationError("Nom d\'utilisateur n'existe pas")
        return followname

    def exist_already(self, user):
        followname = self.cleaned_data.get('followname')
        to_follow = User.objects.get(username=followname)
        exist = UserFollows.objects.get(user=user, followed_user=to_follow)
        if exist:
            self.add_error("followname", f"Vous suivez déjà {followname}")
            return True
        return False

    def save(self, user):
        followname = self.cleaned_data.get('followname')
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
        user = User.objects.get(username=username)
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


class ReviewForm(forms.Form):
    ticket = None
    # Review Fields
    headline = forms.CharField(label='En-Tête', min_length=1, max_length=128)
    CHOICES = [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    rating = forms.ChoiceField(label="Note",
                               required=True,
                               widget=forms.RadioSelect,
                               choices=CHOICES
                               )
    body = forms.CharField(label='Commentaire', max_length=8192, widget=forms.Textarea, required=False)

    def clean_headline(self):
        headline = self.cleaned_data['headline']
        return headline

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        return rating

    def clean_body(self):
        body = self.cleaned_data['body']
        return body

    def set_ticket(self, ticket):
        self.ticket = ticket

    def save(self, username, commit=True):
        user = User.objects.get(username=username)
        # Make a review
        review = Review(ticket=self.ticket,
                        rating=self.cleaned_data['rating'],
                        user=user,
                        headline=self.cleaned_data['headline'],
                        body=self.cleaned_data['body']
                        )
        review.save(commit)
        return review

    def edit(self, review):
        review = Review(id=review.id,
                        ticket=review.ticket,
                        rating=self.cleaned_data['rating'],
                        user=review.user,
                        headline=self.cleaned_data['headline'],
                        body=self.cleaned_data['body'],
                        time_created=review.time_created
                        )
        review.save()
        return review


class ReviewTicketForm(ReviewForm):
    # Ticket Fields
    ticket_title = forms.CharField(label='Titre', min_length=1, max_length=128)
    ticket_description = forms.CharField(label='Description', widget=forms.Textarea, required=False)
    ticket_image = forms.ImageField(label='Image', required=False)
    # Review Fields
    '''
        headline = forms.CharField(label='En-Tête', min_length=1, max_length=128)
        CHOICES = [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
        rating = forms.ChoiceField(label="Note",
                                   required=True,
                                   widget=forms.RadioSelect,
                                   choices=CHOICES
                                   )
        body = forms.CharField(label='Commentaire', max_length=8192, widget=forms.Textarea, required=False)
    '''

    def clean_ticket_title(self):
        ticket_title = self.cleaned_data['ticket_title']
        return ticket_title

    def clean_ticket_description(self):
        ticket_description = self.cleaned_data['ticket_description']
        return ticket_description

    def clean_ticket_image(self):
        ticket_image = self.cleaned_data['ticket_image']
        return ticket_image

    def save(self, username, commit=True):
        user = User.objects.get(username=username)
        # Make a Ticket
        ticket = Ticket(title=self.cleaned_data['ticket_title'],
                        description=self.cleaned_data['ticket_description'],
                        user=user,
                        image=self.cleaned_data['ticket_image']
                        )
        ticket.save(commit)
        # Make a review
        review = Review(ticket=ticket,
                        rating=self.cleaned_data['rating'],
                        user=user,
                        headline=self.cleaned_data['headline'],
                        body=self.cleaned_data['body']
                        )
        review.save(commit)
        return review
