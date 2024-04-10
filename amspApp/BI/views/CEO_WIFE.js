var allowPaste = function (e) {
    e.stopImmediatePropagation();
    return true;
};
document.addEventListener('paste', allowPaste, true);

function querySelectorIncludesText(selector, text) {
    return Array.from(document.querySelectorAll(selector))
        .find(el => el.textContent.includes(text));
}


function setValueInput(label, value) {
    querySelectorIncludesText('label', label).parentNode.querySelector('input').value = value;
    querySelectorIncludesText('label', label).parentNode.querySelector('input').dispatchEvent(new Event('click'));
    querySelectorIncludesText('label', label).parentNode.querySelector('input').dispatchEvent(new Event('input'));
    querySelectorIncludesText('label', label).parentNode.querySelector('input').dispatchEvent(new Event('change'));
}

function setValueInputForSelect(label, value) {
    querySelectorIncludesText('label', label).parentNode.querySelector('select').value = value;
    querySelectorIncludesText('label', label).parentNode.querySelector('select').dispatchEvent(new Event('click'));
    querySelectorIncludesText('label', label).parentNode.querySelector('select').dispatchEvent(new Event('input'));
    querySelectorIncludesText('label', label).parentNode.querySelector('select').dispatchEvent(new Event('change'));
}

function birthdateClick() {
    querySelectorIncludesText('label', '*تاریخ تولد:').parentNode.querySelector('input').dispatchEvent(new Event('click'));
    querySelectorIncludesText('label', '*تاریخ تولد:').parentNode.querySelector('input').dispatchEvent(new Event('input'));
    querySelectorIncludesText('label', '*تاریخ تولد:').parentNode.querySelector('input').dispatchEvent(new Event('blur'));

    querySelectorIncludesText('label', '*تاریخ صدور شناسنامه:').parentNode.querySelector('input').dispatchEvent(new Event('click'));
    querySelectorIncludesText('label', '*تاریخ صدور شناسنامه:').parentNode.querySelector('input').dispatchEvent(new Event('input'));
    querySelectorIncludesText('label', '*تاریخ صدور شناسنامه:').parentNode.querySelector('input').dispatchEvent(new Event('blur'));
}


querySelectorIncludesText('label', '*استان تولد:').parentNode.querySelector('select').value = '12';
querySelectorIncludesText('label', '*استان تولد:').parentNode.querySelector('select').dispatchEvent(new Event('change'));
querySelectorIncludesText('label', '* استان صدور شناسنامه:').parentNode.querySelector('select').value = '12';
querySelectorIncludesText('label', '* استان صدور شناسنامه:').parentNode.querySelector('select').dispatchEvent(new Event('change'));
querySelectorIncludesText('label', '*استان:').parentNode.querySelector('select').value = '7';
querySelectorIncludesText('label', '*استان:').parentNode.querySelector('select').dispatchEvent(new Event('change'));

var scrollingElement = (document.scrollingElement || document.body);
scrollingElement.scrollTop = scrollingElement.scrollHeight-1000;



setTimeout(function () {


    setValueInputForSelect('*شهر صدور شناسنامه:', '1304');
    setValueInputForSelect('*شهر محل تولد:', '1291');
    setValueInputForSelect('*شهر:', '819');

    setTimeout(function () {
        setValueInput('نام:', 'فاطمه');
        setValueInput('نام خانوادگی:', 'کریمیان');
        setValueInput('*نام پدر:', 'قهرمان');
        setValueInput('*کدملی:', '4819698788');
        setValueInput('*شماره شناسنامه:', '71');
        setValueInputForSelect('*جنسیت:', 'false');
        setValueInput('*سریال شناسنامه:', '730204');
        setValueInput('*تاریخ تولد:', '1362/03/04');
        setValueInput('*تاریخ صدور شناسنامه:', '1362/04/01');
        console.log('step 1 done');
        setValueInputForSelect('* استان صدور شناسنامه:', '12');
        setValueInputForSelect('*استان تولد:', '12');
        setValueInputForSelect('شغل:', '2');
        setValueInputForSelect('نحوه آشنایی با شرایط فروش:', '1');
        setValueInputForSelect('*نوع پلاک درخواستی:', '2');
        console.log('step 2 done');
        setValueInput('*خیابان اصلی:', 'پاسداران');
        setValueInput('*خیابان فرعی:', 'ساقدوش');
        setValueInput('*کوچه:', 'پیری شرقی');
        setValueInput('*پلاک:', '1');
        console.log('step 3 done');
        setValueInput('*منطقه شهرداری:', '4');
        setValueInput('*کدپستی:', '1665649605');
        setValueInput('*نام بانک:', 'ملی');
        setValueInput('*شماره شبا:', '850170000000225598362006');
        setValueInput('شماره گواهینامه:', '9407286972');
        setValueInput('*تلفن همراه:', '09123243115');
        setValueInput('تلفن ثابت:', '02122310037');
        setValueInput('ایمیل:', 'ftm.karimian@yahoo.com');

        setTimeout(function () {
            birthdateClick();
        }, 300)

    }, 500)


    document.querySelectorAll("#has_certficate_number")[0].checked = true;

}, 1000)
