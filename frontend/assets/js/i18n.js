(function () {
  var LANGS = {
    bg: {
      // Nav
      'nav.menu': 'Меню',
      'nav.home': 'Начало',
      'nav.experts': 'Контакти',
      'nav.credit_info': 'Информация за кредити',
      'nav.calculator': 'Кредитен калкулатор',
      'nav.book': 'Запис на час',
      'nav.profile': 'Моят профил',
      'nav.appointments': 'Моите срещи',
      'nav.login': 'Вход',
      'nav.signup': 'Регистрация',
      'nav.blog': 'Блог',
      // Homepage
      'home.hero.title': 'Вашият доверен партньор в кредитирането!',
      'home.hero.sub': 'Професионални кредитни консултации за вашия финансов успех и спокойствие.',
      'home.hero.cta1': 'Безплатна консултация',
      'home.hero.cta2': 'Научете повече',
      'home.services.eyebrow': 'Експертиза',
      'home.services.title': 'Нашите услуги',
      'home.s1.title': 'Жилищни кредити',
      'home.s1.desc': 'Намираме най-добрите условия и лихвени проценти за закупуване на вашия нов дом или рефинансиране.',
      'home.s2.title': 'Потребителски кредити',
      'home.s2.desc': 'Бързо одобрение и гъвкави погасителни планове за вашите лични проекти, пътувания или ремонт.',
      'home.s3.title': 'Бизнес финансиране',
      'home.s3.desc': 'Експертни решения за растеж на вашия бизнес, инвестиционни кредити и оборотен капитал.',
      'home.why.title': 'Защо да изберете Gfinance?',
      'home.why1.title': 'Без такси за клиента',
      'home.why1.desc': 'Нашите услуги се заплащат от банковите институции, не от вас.',
      'home.why2.title': 'Пълно съдействие',
      'home.why2.desc': 'Подготвяме всички необходими документи и преговаряме вместо вас.',
      'home.why3.title': 'Най-добри пазарни оферти',
      'home.why3.desc': 'Работим с всички водещи банки, за да осигурим най-добрите условия.',
      'home.why4.title': 'Експертен анализ',
      'home.why4.desc': 'Детайлно сравнение на условията.',
      'home.cta.title': 'Готови ли сте за следващата стъпка?',
      'home.cta.desc': 'Свържете се с нас днес за безплатна и необвързваща консултация относно вашия кредит.',
      'home.cta.btn': 'Свържете се с нас',
      // Footer
      'footer.experts': 'Контакти',
      'footer.credits': 'Кредити',
      'footer.book': 'Запис на час',
      'footer.profile': 'Моят профил',
      'footer.appointments': 'Моите срещи',
      'footer.login': 'Вход',
      'footer.terms': 'Общи условия',
      'footer.privacy': 'Поверителност',
      // Credit Calculator
      'calc.title': 'Изчислете вашия кредит',
      'calc.sub': 'Направете предварително изчисление на вашите месечни вноски с Gfinance.',
      'calc.sum.label': 'Сума на кредита (eur.)',
      'calc.months.label': 'Срок на кредита',
      'calc.rate.label': 'Лихвен процент (%)',
      'calc.monthly.label': 'Месечна вноска',
      'calc.total.label': 'Обща сума',
      'calc.interest.label': 'Общо лихва',
      'calc.promo.title': 'Индивидуални условия',
      'calc.promo.desc': 'Gfinance договаря най-добрите условия за вас спрямо вашия профил.',
      'calc.cta': 'Заяви консултация',
      'calc.disclaimer': '* Изчисленията са ориентировъчни и не представляват официална оферта. Gfinance е регистриран кредитен посредник.',
      // Booking
      'book.title': 'Кредитна консултация',
      'book.sub': 'Изберете удобен за вас ден и час за среща с наш експерт.',
      'book.slots.title': 'Свободни часове',
      'book.name.label': 'Име и фамилия',
      'book.name.placeholder': 'Вашето име',
      'book.email.label': 'Имейл',
      'book.phone.label': 'Телефон',
      'book.notes.label': 'Бележки',
      'book.notes.placeholder': 'За какво се отнася консултацията?',
      'book.service.label': 'Вид консултация',
      'book.consultant.label': 'Изберете консултант',
      'book.submit': 'Потвърди часа',
      // Booking Confirmed
      'confirmed.title': 'Вашата заявка е изпратена за потвърждение!',
      'confirmed.sub': 'Вашата резервация е изпратена на консултанта. Ще получите потвърждение по имейл, когато бъде одобрена.',
      'confirmed.card.title': 'Детайли за срещата',
      'confirmed.consultant.label': 'Консултант',
      'confirmed.date.label': 'Дата',
      'confirmed.time.label': 'Час',
      'confirmed.home.btn': 'Към началната страница',
      // My Appointments
      'appt.tab.upcoming': 'Предстоящи',
      'appt.tab.past': 'Минали',
      'appt.section.title': 'Моите срещи',
      'appt.next.title': 'Следващи консултации',
      'appt.past.title': 'Минали консултации',
      'appt.login.prompt': 'Влезте в профила си за да видите вашите срещи',
      'appt.login.link': 'Вход',
      'appt.login.sub': 'Управлявайте вашите запазени часове с финансови експерти',
      'appt.cta.title': 'Нуждаете се от още помощ?',
      'appt.cta.sub': 'Нашите експерти са на разположение за нова консултация.',
      'appt.cta.btn': 'Запази нов час',
      // My Profile
      'profile.personal': 'Лична информация',
      'profile.name.label': 'Име',
      'profile.email.label': 'Имейл',
      'profile.phone.label': 'Телефон',
      'profile.edit.btn': 'Редактирай',
      'profile.security': 'Сигурност',
      'profile.password.title': 'Промяна на паролата',
      'profile.consultations': 'Моите консултации',
      'profile.planned.title': 'Планирани срещи',
      'profile.planned.sub': 'Вижте графика си',
      'profile.preferences': 'Предпочитания',
      'profile.notif.title': 'Известия',
      'profile.notif.sub': 'Push и имейл известия',
      'profile.logout': 'Изход',
      'profile.edit.cancel': 'Отказ',
      'profile.edit.save': 'Запази',
      // Login
      'login.title': 'Вход в профила',
      'login.sub': 'Добре дошли в портала на Gfinance',
      'login.email.label': 'Имейл',
      'login.email.placeholder': 'Въведете вашия имейл',
      'login.pw.label': 'Парола',
      'login.pw.placeholder': 'Въведете вашата парола',
      'login.forgot': 'Забравена парола?',
      'login.remember': 'Запомни ме на това устройство',
      'login.btn': 'Вход',
      'login.no_account': 'Нямате профил?',
      'login.register': 'Регистрирайте се',
      'login.back': '← Назад',
      'login.terms': 'Условия за ползване',
      'login.privacy': 'Политика за поверителност',
      'login.contact': 'Контакти',
      'login.forgot.title': 'Забравена парола',
      'login.forgot.desc': 'Въведете имейла си и ще ви изпратим линк за възстановяване.',
      'login.forgot.cancel': 'Отказ',
      'login.forgot.send': 'Изпрати линк',
      // Signup
      'signup.title': 'Регистрация',
      'signup.sub': 'Станете част от Gfinance и управлявайте вашите кредити професионално.',
      'signup.name.label': 'Име и фамилия',
      'signup.name.placeholder': 'Вашите две имена',
      'signup.email.label': 'Имейл',
      'signup.phone.label': 'Телефон',
      'signup.pw.label': 'Парола',
      'signup.pw.placeholder': 'Минимум 8 знака',
      'signup.confirm.label': 'Потвърди парола',
      'signup.confirm.placeholder': 'Повторете паролата',
      'signup.btn': 'Създай профил',
      'signup.has_account': 'Вече имате профил?',
      'signup.login_link': 'Влезте тук',
      // Consultants
      'consultants.h1': 'Нашите Консултанти',
      'consultants.sub': 'Запознайте се с нашия екип от опитни финансови специалисти.',
      'consultants.book.btn': 'Запиши час',
      'consultants.hero.title': 'Кредитни консултанти в Бургас',
      'consultants.hero.sub': 'Безплатна консултация за жилищен кредит, ипотека и рефинансиране — без ангажимент.',
      'consultants.g1.role': 'Специалист в банкирането',
      'consultants.g1.bio': 'Кредитен консултант с над 25 години опит в банковия сектор. Специализиран в жилищно кредитиране и ипотеки в Бургас.',
      'consultants.g2.role': 'Специалист',
      'consultants.g2.bio': 'Специалист потребителско кредитиране с 15 години стаж. Помага на клиенти в Бургас да намерят най-изгодния кредит.',
      'consultants.g3.role': 'Експерт жилищно кредитиране',
      'consultants.g3.bio': 'Експерт ипотечен кредит Бургас с над 20 години опит в най-големите банки в България. Консултира за рефинансиране и жилищно кредитиране.',
      'consultants.footer': '© 2026 Gfinance. Всички права запазени.',
      // Contact section (shared between homepage and consultants_info)
      'contact.title': 'Информация за контакт',
      'contact.address.label': 'Адрес',
      'contact.phone.label': 'Телефон',
      'contact.email.label': 'Имейл',
      'contact.map.btn': 'Намерете ни в Бургас – отвори в Google Maps',
      // Trust bar (homepage mobile)
      'home.trust.banks': 'банки сравнени',
      'home.trust.free': 'безплатно за вас',
      'home.trust.loc': 'и онлайн',
      // Credit Info
      'credit.h1': 'Видове кредити',
      'credit.sub': 'Всичко, което трябва да знаете за жилищни, потребителски и бизнес кредити.',
    },
    en: {
      // Nav
      'nav.menu': 'Menu',
      'nav.home': 'Home',
      'nav.experts': 'Contacts',
      'nav.credit_info': 'Credit Information',
      'nav.calculator': 'Credit Calculator',
      'nav.book': 'Book Appointment',
      'nav.profile': 'My Profile',
      'nav.appointments': 'My Appointments',
      'nav.login': 'Login',
      'nav.signup': 'Register',
      'nav.blog': 'Blog',
      // Homepage
      'home.hero.title': 'Your Trusted Partner in Credit!',
      'home.hero.sub': 'Professional credit consultations for your financial success and peace of mind.',
      'home.hero.cta1': 'Free Consultation',
      'home.hero.cta2': 'Learn More',
      'home.services.eyebrow': 'Expertise',
      'home.services.title': 'Our Services',
      'home.s1.title': 'Home Loans',
      'home.s1.desc': 'We find the best terms and interest rates for purchasing your new home or refinancing.',
      'home.s2.title': 'Consumer Loans',
      'home.s2.desc': 'Fast approval and flexible repayment plans for your personal projects, travel, or home improvements.',
      'home.s3.title': 'Business Financing',
      'home.s3.desc': 'Expert solutions for business growth, investment loans, and working capital.',
      'home.why.title': 'Why Choose Gfinance?',
      'home.why1.title': 'No Client Fees',
      'home.why1.desc': 'Our services are paid by banking institutions, not by you.',
      'home.why2.title': 'Full Support',
      'home.why2.desc': 'We prepare all necessary documents and negotiate on your behalf.',
      'home.why3.title': 'Best Market Offers',
      'home.why3.desc': 'We work with all leading banks to ensure the best terms.',
      'home.why4.title': 'Expert Analysis',
      'home.why4.desc': 'Detailed comparison of terms.',
      'home.cta.title': 'Ready for the Next Step?',
      'home.cta.desc': 'Contact us today for a free, no-obligation consultation about your loan.',
      'home.cta.btn': 'Contact Us',
      // Footer
      'footer.experts': 'Experts',
      'footer.credits': 'Credits',
      'footer.book': 'Book Appointment',
      'footer.profile': 'My Profile',
      'footer.appointments': 'My Appointments',
      'footer.login': 'Login',
      'footer.terms': 'Terms of Service',
      'footer.privacy': 'Privacy Policy',
      // Credit Calculator
      'calc.title': 'Calculate Your Loan',
      'calc.sub': 'Calculate your monthly payments in advance with Gfinance.',
      'calc.sum.label': 'Loan Amount (EUR)',
      'calc.months.label': 'Loan Term',
      'calc.rate.label': 'Interest Rate (%)',
      'calc.monthly.label': 'Monthly Payment',
      'calc.total.label': 'Total Amount',
      'calc.interest.label': 'Total Interest',
      'calc.promo.title': 'Individual Terms',
      'calc.promo.desc': 'Gfinance negotiates the best terms for you based on your profile.',
      'calc.cta': 'Request Consultation',
      'calc.disclaimer': '* Calculations are indicative and do not constitute an official offer. Gfinance is a registered credit intermediary.',
      // Booking
      'book.title': 'Credit Consultation',
      'book.sub': 'Choose a convenient day and time to meet with our expert.',
      'book.slots.title': 'Available Slots',
      'book.name.label': 'Full Name',
      'book.name.placeholder': 'Your name',
      'book.email.label': 'Email',
      'book.phone.label': 'Phone',
      'book.notes.label': 'Notes',
      'book.notes.placeholder': 'What is the consultation about?',
      'book.service.label': 'Consultation Type',
      'book.consultant.label': 'Choose a Consultant',
      'book.submit': 'Confirm Appointment',
      // Booking Confirmed
      'confirmed.title': 'Your Request Has Been Submitted!',
      'confirmed.sub': 'Your reservation has been sent to the consultant. You will receive an email confirmation once it is approved.',
      'confirmed.card.title': 'Meeting Details',
      'confirmed.consultant.label': 'Consultant',
      'confirmed.date.label': 'Date',
      'confirmed.time.label': 'Time',
      'confirmed.home.btn': 'Back to Homepage',
      // My Appointments
      'appt.tab.upcoming': 'Upcoming',
      'appt.tab.past': 'Past',
      'appt.section.title': 'My Appointments',
      'appt.next.title': 'Upcoming Consultations',
      'appt.past.title': 'Past Consultations',
      'appt.login.prompt': 'Sign in to view your appointments',
      'appt.login.link': 'Sign In',
      'appt.login.sub': 'Manage your scheduled appointments with financial experts',
      'appt.cta.title': 'Need more help?',
      'appt.cta.sub': 'Our experts are available for a new consultation.',
      'appt.cta.btn': 'Book New Appointment',
      // My Profile
      'profile.personal': 'Personal Information',
      'profile.name.label': 'Name',
      'profile.email.label': 'Email',
      'profile.phone.label': 'Phone',
      'profile.edit.btn': 'Edit',
      'profile.security': 'Security',
      'profile.password.title': 'Change Password',
      'profile.consultations': 'My Consultations',
      'profile.planned.title': 'Scheduled Appointments',
      'profile.planned.sub': 'View your schedule',
      'profile.preferences': 'Preferences',
      'profile.notif.title': 'Notifications',
      'profile.notif.sub': 'Push and email notifications',
      'profile.logout': 'Sign Out',
      'profile.edit.cancel': 'Cancel',
      'profile.edit.save': 'Save',
      // Login
      'login.title': 'Sign In',
      'login.sub': 'Welcome to the Gfinance portal',
      'login.email.label': 'Email',
      'login.email.placeholder': 'Enter your email',
      'login.pw.label': 'Password',
      'login.pw.placeholder': 'Enter your password',
      'login.forgot': 'Forgot password?',
      'login.remember': 'Remember me on this device',
      'login.btn': 'Sign In',
      'login.no_account': "Don't have an account?",
      'login.register': 'Register',
      'login.back': '← Back',
      'login.terms': 'Terms of Service',
      'login.privacy': 'Privacy Policy',
      'login.contact': 'Contact',
      'login.forgot.title': 'Forgot Password',
      'login.forgot.desc': 'Enter your email and we will send you a recovery link.',
      'login.forgot.cancel': 'Cancel',
      'login.forgot.send': 'Send Link',
      // Signup
      'signup.title': 'Register',
      'signup.sub': 'Join Gfinance and manage your loans professionally.',
      'signup.name.label': 'Full Name',
      'signup.name.placeholder': 'Your full name',
      'signup.email.label': 'Email',
      'signup.phone.label': 'Phone',
      'signup.pw.label': 'Password',
      'signup.pw.placeholder': 'Minimum 8 characters',
      'signup.confirm.label': 'Confirm Password',
      'signup.confirm.placeholder': 'Repeat password',
      'signup.btn': 'Create Account',
      'signup.has_account': 'Already have an account?',
      'signup.login_link': 'Sign in here',
      // Consultants
      'consultants.h1': 'Our Consultants',
      'consultants.sub': 'Meet our team of experienced financial specialists.',
      'consultants.book.btn': 'Book Appointment',
      'consultants.hero.title': 'Credit Consultants in Burgas',
      'consultants.hero.sub': 'Free consultation for home loans, mortgages and refinancing — no obligation.',
      'consultants.g1.role': 'Banking Specialist',
      'consultants.g1.bio': 'Credit consultant with over 25 years of experience in the banking sector. Specialised in home loans and mortgages in Burgas.',
      'consultants.g2.role': 'Consumer Credit Specialist',
      'consultants.g2.bio': 'Consumer lending specialist with 15 years of experience. Helps clients in Burgas find the most favourable loan.',
      'consultants.g3.role': 'Mortgage Expert',
      'consultants.g3.bio': 'Mortgage expert in Burgas with over 20 years of experience at leading Bulgarian banks. Advises on refinancing and home loans.',
      'consultants.footer': '© 2026 Gfinance. All rights reserved.',
      // Contact section (shared between homepage and consultants_info)
      'contact.title': 'Contact Information',
      'contact.address.label': 'Address',
      'contact.phone.label': 'Phone',
      'contact.email.label': 'Email',
      'contact.map.btn': 'Find us in Burgas – open in Google Maps',
      // Trust bar (homepage mobile)
      'home.trust.banks': 'banks compared',
      'home.trust.free': 'free for you',
      'home.trust.loc': 'and online',
      // Credit Info
      'credit.h1': 'Types of Credit',
      'credit.sub': 'Everything you need to know about home, consumer, and business loans.',
    }
  };

  var _lang = localStorage.getItem('gf-lang') || 'bg';

  function t(key) {
    return (LANGS[_lang] && LANGS[_lang][key]) || (LANGS.bg[key]) || key;
  }

  function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      el.textContent = t(el.getAttribute('data-i18n'));
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
      el.placeholder = t(el.getAttribute('data-i18n-placeholder'));
    });
    document.documentElement.lang = _lang;
    var label = document.getElementById('lang-label');
    if (label) label.textContent = _lang === 'bg' ? 'EN' : 'БГ';
  }

  function toggle() {
    _lang = _lang === 'bg' ? 'en' : 'bg';
    localStorage.setItem('gf-lang', _lang);
    applyTranslations();
  }

  // Expose months/days arrays for JS that builds dynamic content
  function getMonths() {
    return _lang === 'en'
      ? ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      : ['Януари', 'Февруари', 'Март', 'Април', 'Май', 'Юни', 'Юли', 'Август', 'Септември', 'Октомври', 'Ноември', 'Декември'];
  }

  function getDays() {
    return _lang === 'en'
      ? ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
      : ['Нд', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
  }

  window.i18n = { toggle: toggle, t: t, apply: applyTranslations, getMonths: getMonths, getDays: getDays, getLang: function () { return _lang; } };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', applyTranslations);
  } else {
    applyTranslations();
  }
})();
