$(function () {

    function classifyTroll (isTroll, objectId) {

        function updateComment(confirmed, objectId) {
            var selector = 'li.troll-instance[data-object-id="' + objectId + '"]';
            var $comment = $(selector);
            if (confirmed)
                $comment.removeClass('alert-warning').addClass('alert-success');
            else
                $comment.hide();
        }

        function classifyCallback(data) {
            var res = $.parseJSON(data);
            if (res.status === 'success')
                updateComment(res.label, res.objectId);
        }

        var isTroll = isTroll === 'true' ? true : false;
        $.post(
            '/classify',
            {classify: JSON.stringify({label: isTroll, objectId: objectId})},
            classifyCallback
        )

    }

    $('.classify').click(function (e) {
        var $troll = $(this);
        var isTroll = $troll.attr('data-troll');
        var objectId = $troll.attr('data-object-id');
        classifyTroll(isTroll, objectId);
        e.preventDefault();
    });
    var $trollModal = $('#troll-modal');
    $('.troll-them').click(function (e) {
        var objectId = $(this).attr('data-object-id');
        $trollModal.modal('show');
        $('#send-troll-response').attr('data-object-id', objectId);
        e.preventDefault();
    });
    $('#send-troll-response').click(function () {
        var objectId = $(this).attr('data-object-id');
        var content = $('#troll-response-content').val();
        $trollModal.modal('hide');
    });
});