/* Общее для всех страниц: формы заявок.
   Галочка согласия включает кнопку; после отправки показываем состояние «Заявка принята».
   Куда уходят заявки – не настроено (см. README): подключить обработчик в send(). */
(function () {
  function send(form) {
    // TODO: отправка заявки (CRM, Telegram-бот, почта). Сейчас данные никуда не уходят.
    return Promise.resolve(new FormData(form));
  }
  document.addEventListener('change', function (e) {
    if (!e.target.matches('[data-agree]')) return;
    var btn = e.target.closest('form').querySelector('button[type="submit"]');
    if (btn) btn.disabled = !e.target.checked;
  });
  document.addEventListener('submit', function (e) {
    var form = e.target.closest('.js-form');
    if (!form) return;
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    send(form).then(function () {
      form.classList.add('sent');
      var ok = form.querySelector('.form__ok');
      if (ok && ok.getBoundingClientRect().top < 0) ok.scrollIntoView({ block: 'center', behavior: 'smooth' });
    });
  });
})();
