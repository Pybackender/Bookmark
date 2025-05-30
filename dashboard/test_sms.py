from django.test import TestCase
from .utils import send_otp_code

class SmsTestCase(TestCase):
    def test_send_otp_code(self):
        phone = '09012994672'  # شماره تست
        otp = '123456'         # کد OTP تست

        # فراخوانی تابع ارسال OTP
        send_otp_code(phone, otp)

        # در اینجا می‌توانید بررسی کنید که آیا پیامک ارسال شده است یا خیر.
        # این بررسی ممکن است شامل چک کردن یک پایگاه داده یا استفاده از یک API برای تأیید ارسال باشد.


#####################3
# otp-form 
# <!DOCTYPE html>
# <html lang="fa">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>تأیید کد OTP</title>
#     <style>
#         .hidden {
#             display: none;
#         }
#     </style>
# </head>
# <body>
#     <h1>تأیید کد OTP</h1>
    
#     <!-- فرم شماره تلفن -->
#     <div id="phoneForm">
#         <label for="phone">شماره تلفن:</label>
#         <input type="text" id="phone" name="phone" required>
#         <button id="sendOtpButton">ارسال کد OTP</button>
#     </div>

#     <!-- فرم تأیید کد OTP -->
#     <div id="otpVerification">
#         <label for="code">کد تأیید:</label>
#         <input type="text" id="code" name="code" required>
#         <button id="verifyCodeButton">تأیید کد</button>
#     </div>

#     <script>
#         document.getElementById('sendOtpButton').onclick = async function(event) {
#             event.preventDefault(); // جلوگیری از ارسال پیش‌فرض فرم

#             const phone = document.getElementById('phone').value;

#             // ارسال شماره تلفن برای دریافت کد OTP
#             const response = await fetch('api/send-otp/', {
#                 method: 'POST',
#                 headers: {
#                     'Content-Type': 'application/json',
#                 },
#                 body: JSON.stringify({ phone: phone }),
#             });

#             if (response.ok) {
#                 // نمایش فرم تأیید کد پس از ارسال موفقیت‌آمیز شماره تلفن
#                 document.getElementById('phoneForm').classList.add('hidden');
#                 document.getElementById('otpVerification').classList.remove('hidden');
#             } else {
#                 const error = await response.json();
#                 alert(error.detail);
#             }
#         };

#         document.getElementById('sendOtpButton').onclick = async function(event) {
#     event.preventDefault(); // جلوگیری از ارسال پیش‌فرض فرم

#     const phone = document.getElementById('phone').value;

#     // بررسی اینکه شماره تلفن وارد شده است
#     if (!phone) {
#         alert('لطفاً شماره تلفن را وارد کنید.');
#         return;
#     }

#     // ارسال شماره تلفن برای دریافت کد OTP
#     const response = await fetch('api/send-otp/', {
#         method: 'POST',
#         headers: {
#             'Content-Type': 'application/json',
#         },
#         body: JSON.stringify({ phone: phone }),
#     });

#     if (response.ok) {
#         // نمایش فرم تأیید کد پس از ارسال موفقیت‌آمیز شماره تلفن
#         document.getElementById('phoneForm').classList.add('hidden');
#         document.getElementById('otpVerification').classList.remove('hidden');
#     } else {
#         const error = await response.json();
#         alert(error.detail || 'خطا در ارسال کد OTP. لطفاً دوباره تلاش کنید.');
#     }
# };

#     </script>
# </body>
# </html>
