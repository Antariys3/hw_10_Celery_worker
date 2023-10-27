import phonenumbers
from django import forms

from sms.models import PhoneNumberVerification


class SMSSendForm(forms.Form):
    sender_number = forms.CharField(label='Номер отправителя', widget=forms.TextInput(attrs={'required': True}))
    receiver_number = forms.CharField(label='Номер получателя', widget=forms.TextInput(attrs={'required': True}))
    message_text = forms.CharField(label='Текст сообщения', widget=forms.Textarea(attrs={'required': True}))

    def clean_sender_number(self):
        sender_number = self.cleaned_data['sender_number']
        if not sender_number:
            raise forms.ValidationError("Поле не может быть пустым")
        try:
            parsed = phonenumbers.parse(sender_number, None)
        except phonenumbers.NumberParseException as e:
            raise forms.ValidationError(e.args[0])
        return phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

    def clean_receiver_number(self):
        receiver_number = self.cleaned_data["receiver_number"]
        if not receiver_number:
            raise forms.ValidationError("Поле не может быть пустым")
        try:
            parsed = phonenumbers.parse(receiver_number, None)
        except phonenumbers.NumberParseException as e:
            raise forms.ValidationError(e.args[0])
        return phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

    def clean_message_text(self):
        message_text = self.cleaned_data['message_text']
        if len(message_text) > 50:
            raise forms.ValidationError("Слишком длинное сообщение")
        return message_text


class AuthenticationForm(forms.Form):
    class Meta:
        model = PhoneNumberVerification
        fields = ["authentication"]
        label = {"authentication": 'Введите номер телефона'}
        widgets = {"authentication": forms.TextInput(attrs={'required': True})}

    authentication = forms.CharField(label='Введите номер телефона', widget=forms.TextInput(attrs={'required': True}))

    def clean_authentication(self):
        authentication = self.cleaned_data.get("authentication")
        if not authentication:
            raise forms.ValidationError("Поле не может быть пустым")
        try:
            parsed = phonenumbers.parse(authentication, None)
        except phonenumbers.NumberParseException as e:
            raise forms.ValidationError(e.args[0])
        return phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )


class VerificationForm(forms.Form):
    verification_code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
