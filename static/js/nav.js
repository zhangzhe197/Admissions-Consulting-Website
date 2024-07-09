$(document).ready(function() {
    $(".menu-icon").on("click", function() {
          $("nav ul").toggleClass("showing");
    });
});

// Scrolling Effect

$(window).on("scroll", function() {
    if($(window).scrollTop()) {
          $('nav').addClass('black');
    }

    else {
          $('nav').removeClass('black');
    }
})

// 将 openPopup 函数移到全局作用域中
function openPopup() {
      const popupContainer = document.getElementById('popup-container');
      popupContainer.style.display = 'block';
    }
    
    // 关闭弹窗
    function closePopup() {
      const popupContainer = document.getElementById('popup-container');
      popupContainer.style.display = 'none';
    }
    
    document.addEventListener('DOMContentLoaded', function() {
      const popupContainer = document.getElementById('popup-container');
      const popupClose = document.getElementById('popup-close');
    
      // 点击关闭按钮或弹窗外部区域时关闭弹窗
      popupClose.addEventListener('click', closePopup);
      popupContainer.addEventListener('click', function(e) {
        if (e.target === popupContainer) {
          closePopup();
        }
      });
    });
    