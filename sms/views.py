import random

from django.shortcuts import render, redirect

from .forms import SMSSendForm, AuthenticationForm, VerificationForm
from .models import PhoneNumberVerification
from .tasks import send_sms


def index(request):
    return render(request, "index.html")


def authentication(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(request, "authentication.html", {"form": form})

    form = AuthenticationForm(request.POST)
    if form.is_valid():
        phone_number = form.cleaned_data["authentication"]
        request.session['phone_number'] = phone_number
        verification_code = random.randint(1000, 9999)
        try:
            # Checks if the user with the given phone number already exists in the database
            user_verification = PhoneNumberVerification.objects.get(phone_number=phone_number)
            user_verification.verification_code = verification_code
            user_verification.attempts_counter = 0
            user_verification.save()
        except PhoneNumberVerification.DoesNotExist:
            # If user doesn't exist, creates a new entry in the database
            PhoneNumberVerification.objects.create(phone_number=phone_number, verification_code=verification_code)
        finally:
            # Sends an SMS with the verification code asynchronously
            send_sms.delay(phone_number, f"Код для верификации {verification_code}")
            return redirect("verification")
    return render(request, "authentication.html", {"form": form})


def verification(request):
    if request.method == "GET":
        form = VerificationForm()
        return render(request, "verification.html", {"form": form})

    form = VerificationForm(request.POST)

    if form.is_valid():
        phone_number = request.session.get('phone_number', None)
        sms_code = form.cleaned_data["verification_code"]

        try:
            verification_object = PhoneNumberVerification.objects.get(phone_number=phone_number)

            if sms_code == verification_object.verification_code:
                # If the code is correct, increments the attempts counter and redirects to success page
                verification_object.attempts_counter += 1
                verification_object.save()

                return redirect("verification_success")
            elif verification_object.attempts_counter >= 3:
                # If attempts exceed 3, clears the session and redirects to error page
                del request.session['phone_number']
                return redirect("authentication_error")
            else:
                # If code is incorrect, adds error to the form and increments attempts counter
                form.add_error('verification_code', 'Неверный код верификации')
                verification_object.attempts_counter += 1
                verification_object.save()
        except PhoneNumberVerification.DoesNotExist:
            form.add_error('verification_code', 'Ошибка: Номер телефона не найден в базе данных')

    return render(request, "verification.html", {"form": form})


def verification_success(request):
    return render(request, "verification_success.html")


def authentication_error(request):
    return render(request, "authentication_error.html")


def send_an_sms(request):
    if request.method == "GET":
        form = SMSSendForm()
        return render(request, "send_an_sms.html", {"form": form})
    form = SMSSendForm(request.POST)
    if form.is_valid():
        send_sms.delay(form.cleaned_data['receiver_number'], form.cleaned_data['message_text'])
        return render(request, 'success_page.html')
    return render(request, "send_an_sms.html")
