import Swal from "sweetalert2";
import Alpine from "alpinejs";

import { togglePaymentNotice1, togglePaymentNotice2 } from "./order_notice.js";



window.Alpine = Alpine;
window.Swal = Swal;
window.togglePaymentNotice1 = togglePaymentNotice1
window.togglePaymentNotice2 = togglePaymentNotice2

Alpine.start();
