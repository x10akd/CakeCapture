// 建立評論
$("#commentForm").submit(function (e) {
    e.preventDefault();

    // 建立要顯示的日期格式
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    let date = new Date();
    let formatDate = date.getDate() + " " + monthNames[date.getUTCMonth()] + ", " + date.getFullYear();


    $.ajax({
        // 傳遞序列化表單數據(serialize():將表單的數據序列化為 URL 編碼的字符串)
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",

        success: function (response) {

            if (response.bool == true) {
                // 隱藏評論輸入框
                $("#addReview").hide()
                // 更新評論數及平均分數
                $(".reviewsCount").text(response.context.reviews_count);
                $(".averageRating").text(response.context.average_rating.toFixed(1));

                // 動態渲染評論html
                let _html = '<div class="rounded-xl bg-blue-100 p-5 shadow-lg shadow-blue-gray-500/40">';
                _html += '<div class="flex justify-between">';
                _html += '<div class="flex gap-4">';
                _html += '<p class="text-blue-500">' + response.context.user + '</p>';
                _html += '<p class="text-sm text-gray-600">' + formatDate + '</p>';
                _html += '</div>';
                _html += '<div class="flex items-center">';

                for (let i = 1; i <= 5; i++) {
                    if (i <= response.context.rating) {
                        _html += '<svg class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">';
                        _html += '<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>';
                        _html += '</svg>';
                    } else {
                        _html += '<svg class="w-5 h-5 text-gray-300 dark:text-gray-300" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">';
                        _html += '<path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>';
                        _html += '</svg>';
                    }
                }

                _html += '</div>';
                _html += '</div>';
                _html += '<p class="my-5">' + response.context.review + '</p></div>';

                $(".comment-list").prepend(_html);
            }
        }
    });
});



// 編輯評論 
// 點擊編輯按鈕展開編輯表單
$(document).on('click', '#edit-review', function () {
    let reviewId = $(this).data('review-id');
    $('#edit-review-form-' + reviewId).toggle();
});

// 處理表單資料
$(document).on('submit', '.editCommentForm', function (e) {
    e.preventDefault();
    let reviewId = $(this).data('review-id');

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",

        success: function (response) {

            if (response.bool == true) {
                const reviewElement = $('#review-' + reviewId)
                // 隱藏編輯表單
                $('#edit-review-form-' + reviewId).hide();
                // 更新評論內容及星星
                reviewElement.find('p.review-text').text(response.context.review);
                reviewElement.find('svg').each(function (index) {
                    $(this).toggleClass('text-yellow-400', index < response.context.rating);
                    $(this).toggleClass('text-gray-300', index >= response.context.rating);
                });
                // 更新評論數及平均分數
                $(".reviewsCount").text(response.context.reviews_count);
                $(".averageRating").text(response.context.average_rating.toFixed(1));
            }
        }
    })
})


// 加載更多評論
$('#loadMoreReviewsBtn').on('click', function () {
    // 定義模板上要用的資料
    let page = $(this).data('page');
    let loadMoreReviewsUrl = $(this).data('url');
    let csrfToken = $(this).data('csrf-token');
    let ajaxEditReviewUrl = "{% url 'products:edit_review' 0 %}".slice(0, -2); // ajax_edit_review/0/ 切掉後面的 0/


    $.ajax({
        url: loadMoreReviewsUrl,
        method: 'GET',
        data: { page: page },
        dataType: 'json',

        success: function (response) {
            response.reviews.forEach(function (review) {
                let reviewHtml = `
                <div class="rounded-xl bg-gray-100 p-5 shadow-lg shadow-blue-gray-500/40" id="review-${review.id}">
                    <div class="flex justify-between">
                        <div class="flex gap-4">
                            <p class="text-blue-500">${review.user}</p>
                            <p class="text-sm text-gray-600">${review.date}</p>
                        </div>
                        <div class="flex items-center">
                            ${[...Array(5).keys()].map(i => `
                                <svg class="w-5 h-5 ${i < review.rating ? 'text-yellow-400' : 'text-gray-300'}" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364 1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"></path>
                                </svg>
                            `).join('')}
                        </div>
                    </div>
                    <p class="my-5 review-text">${review.review}</p>
                    ${review.is_user_review ? `
                    <div>
                        <button class="text-blue-500 hover:text-red-400 edit-button" data-review-id="${review.id}" id="edit-review">編輯</button>
                    </div>
                    ` : ''}
                </div>
                <div class="my-4" style="display:none" id="edit-review-form-${review.id}">
                    <h4 class="mb-5 font-bold text-xl border-b-2 border-red-400">編輯評論</h4>
                    <form action="${ajaxEditReviewUrl}${review.id}/" method="POST" class="flex gap-6 editCommentForm" data-review-id="${review.id}">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <div>
                            <textarea name="review" id="editReviewText" rows="5" cols="80" class="focus:outline-none border-2 border-gray-300 rounded-xl p-5">${review.review}</textarea>
                        </div>
                        <div class="flex flex-col justify-between">
                            <select name="rating" id="editReviewRating" class="border-2 border-gray-300 rounded-xl p-2 focus:outline-none">
                                <option value="1" ${review.rating == 1 ? 'selected' : ''}>★☆☆☆☆</option>
                                <option value="2" ${review.rating == 2 ? 'selected' : ''}>★★☆☆☆</option>
                                <option value="3" ${review.rating == 3 ? 'selected' : ''}>★★★☆☆</option>
                                <option value="4" ${review.rating == 4 ? 'selected' : ''}>★★★★☆</option>
                                <option value="5" ${review.rating == 5 ? 'selected' : ''}>★★★★★</option>
                            </select>
                            <input type="hidden" name="review_id" id="editReviewId" value="${review.id}">
                            <div>
                                <button type="submit" class="text-xl text-white font-bold p-3 rounded-xl bg-red-400 hover:scale-105">更新留言</button>
                            </div>
                        </div>
                    </form>
                </div>
                `;
                $('.comment-list').append(reviewHtml);
            });

            if (response.has_next) {
                $('#loadMoreReviewsBtn').data('page', page + 1);
            } else {
                $('#loadMoreReviewsBtn').remove();
            }
        }
    });
});



// 購物車
// $(document).ready(function () {
//     var isProductInCart = false; // 旗標變量，用於追蹤商品是否已加入購物車

//     $(document).on('click', '#add_cart', function (e) {
//         e.preventDefault();
//         console.log('123')
//         if (isProductInCart) {
//             // 商品已在購物車中，顯示提示訊息
//             Swal.fire({
//                 icon: 'warning',
//                 title: '購物車裡已有商品',
//                 showConfirmButton: false,
//                 timer: 1500 // 提示框顯示時間
//             });
//         } else {
//             // 商品未在購物車中，發送Ajax請求
//             $.ajax({
//                 type: 'POST',
//                 url: "{% url 'carts:add' %}",
//                 data: {
//                     product_id: $('#add_cart').val(),
//                     product_qty: $('#quantity-input').val(),
//                     csrfmiddlewaretoken: '{{ csrf_token }}',
//                     action: 'post'
//                 },
//                 success: function (json) {
//                     document.getElementById('cart_quantity').textContent = json.qty;
//                     // 使用SweetAlert2顯示成功提示框
//                     Swal.fire({
//                         icon: 'success',
//                         title: '商品已被加入購物車',
//                         showConfirmButton: false,
//                         timer: 1500 // 提示框顯示時間
//                     });
//                     // 設置旗標為true，表示商品已在購物車中
//                     isProductInCart = true;
//                 },
//                 error: function (xhr, errmsg, err) {
//                     // 錯誤處理，可以根據需要進行擴展
//                 }
//             });
//         }
//     });
// });