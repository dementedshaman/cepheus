$(document).ready(function($){
    var cnpj = $('.Cnpj_value');
    $(cnpj).mask('99.999.999/9999-99');
    var zip_code = $('Zip_code');
    $(zip_code).mask('99999-999');
})
