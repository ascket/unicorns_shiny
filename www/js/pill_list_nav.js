"use strict";


// let row_element = document.getElementsByClassName("row");
// row_element[0].classList["value"] = "noclass";

const colSm = document.querySelector("ul.nav.nav-pills.nav-stacked")
colSm.insertAdjacentHTML('beforebegin', '<div class="d-flex">\n' +
    '                    <i class="lni lni-python"></i>\n' +
    '                <div class="sidebar-logo">\n' +
    '                    <a href="#">Shiny Dashboard</a>\n' +
    '                </div>\n' +
    '            </div>')


/* Иконка схлопывания панели слева находится в этой же панели. Закрой эти стили .col-sm-2 .d-flex i */
/*const colSm = document.querySelector("ul.nav.nav-pills.nav-stacked")
colSm.insertAdjacentHTML('beforebegin', '<div class="d-flex"><button class="toggle-btn" type="button"><i class="lni lni-menu"></i></button> </div>')*/

const hamBurger = document.querySelector(".toggle-btn");


/* Чтобы левая панель была схлопнута при первом открытии страницы. Чтобы была открыта, просто закоментируй две строки снизу*/
document.querySelector(".col-sm-2.well").classList.toggle("expand");
document.querySelector(".col-sm-10").classList.toggle("expand");

hamBurger.addEventListener("click", function () {
    document.querySelector(".col-sm-2.well").classList.toggle("expand");
    document.querySelector(".col-sm-10").classList.toggle("expand");
});


//document.querySelector(".col-sm-2").prepend(<p>This is my tag</p>)


//let well_element = document.querySelector(".well");
// well_element.setAttribute("id", "sidebar");
//well_element.classList["value"] = "expand";

// let nav_pills_ul = document.querySelector(".nav.nav-pills.nav-stacked");
// nav_pills_ul.classList["value"] = "sidebar-nav";

// let nav_pills_li = document.querySelector(".nav-item");
// nav_pills_ul.classList["value"] = "sidebar-item";

/*const tooltipElement = document.getElementById('nav_panel_table-table_tooltip');
//tooltipElement.dataset.bsTrigger = 'hover focus';
tooltipElement.dataset.bsCustomClass = "custom-tooltip";
tooltipElement.dataset.bsPlacement = "top";*/
