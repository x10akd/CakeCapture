import Swal from "sweetalert2";
import Alpine from "alpinejs";

import { togglePaymentNotice1, togglePaymentNotice2 } from "./order_notice.js";
import { Toast } from "./alert.js"
import { carousel } from "./carousel.js";

window.Toast = Toast;
window.Alpine = Alpine;
window.Swal = Swal;
window.togglePaymentNotice1 = togglePaymentNotice1
window.togglePaymentNotice2 = togglePaymentNotice2
window.carousel = carousel

Alpine.start();
