function checkFunction() {
    if($('#masterCheck')[0].checked)
        $('.childrenCheck').attr('checked', true);
    else
        $('.childrenCheck').removeAttr('checked');
}