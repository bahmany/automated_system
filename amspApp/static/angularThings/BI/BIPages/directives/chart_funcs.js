function convert_month_number_to_month_name(month_num) {
    return ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'][month_num - 1]
}

function convert_number_to_word(number) {
    return Num2persian(number)
}

function convert_number_to_word_with_m(number) {
    return Num2persian(number) + "م"
}

String.prototype.toFaDigit = function () {
    var find = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    var replace = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    var replaceString = this;
    var regex;
    for (var i = 0; i < find.length; i++) {
        regex = new RegExp(find[i], "g");
        replaceString = replaceString.replace(regex, replace[i]);
    }
    return replaceString;
};


