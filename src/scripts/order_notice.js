function togglePaymentNotice1() {
  let paymentNotice = document.getElementById('payment-notice');
  if (paymentNotice.style.display === 'none') {
    paymentNotice.style.display = 'block';
  } else {
    paymentNotice.style.display = 'none';
  }
}

function togglePaymentNotice2() {
  let noticeElement = document.getElementById('recipient-information');
  if (noticeElement.style.display === 'none') {
    noticeElement.style.display = 'block';
  } else {
    noticeElement.style.display = 'none';
  }
}

export { togglePaymentNotice1, togglePaymentNotice2 } 